from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import PendingSerializer, UsersPendingSerializer, UsersPendingUpdateSerializer
from ..models import Company, CompanyPeople
from functools import wraps
from django.db.models import F 

def get_status_company(function): #Seria como eu estivesse interceptandoa função send_response
    @wraps(function)
    def wrap(self, request, *args, **kwargs): #Seria como eu estivesse instancia send_response aqui, passando os mesmos parâmetros
        companys = Company.objects.all()
    
        result = []
        for company in companys:
            joined = CompanyPeople.objects.filter(company=company.id, user=request.user)
            result.append({
                'company': company,
                'identification_number': company.identification_number,
                'trade_name': company.trade_name,
                'slug_name': company.slug_name,
                'logo': company.logo,
                'is_joined': joined.first().is_joined if joined.exists() else False,
                'is_pending': joined.first().is_pending if joined.exists() else False
            })
        
        kwargs['serializer'] = self.serializer_class(result, many=True).data    
         
        return function(self, request, *args, **kwargs) #Seria como eu estivesse instancia send_response aqui, passando os mesmos parâmetros
    
    return wrap

class PendingViews(generics.GenericAPIView):
    serializer_class = PendingSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        companyPeople = CompanyPeople.objects.filter(user=request.user, company=request.data['company'])
        serializer = None

        if(companyPeople.exists()):
            is_pending = False if companyPeople.first().is_pending else True #Aqui cancela e descancela o status de pendente, permitindo que o usuário possa alternar.
            serializer = self.serializer_class(companyPeople, data={'is_pending': is_pending})
            
        else:
            serializer = self.serializer_class(companyPeople, data=request.data, context={'user': request.user})

        if(not serializer.is_valid()):
            return Response({'message': 'Falhou', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return self.send_response(request)
    
    @get_status_company
    def send_response(self, request, *args, **kwargs):
        return Response({'message': 'Dados retornados com sucesso', 'data': kwargs['serializer']}, status=status.HTTP_200_OK)
    
    @get_status_company
    def get(self, request, *args, **kwargs):
        return Response({'message': 'Dados retornados com sucesso', 'data': kwargs['serializer']}, status=status.HTTP_200_OK)

class UsersPendingUpdateViews(generics.GenericAPIView):
    serializer_class = UsersPendingUpdateSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, companyId=None, userId=None):
        companyPeople = CompanyPeople.objects.filter(user=userId, company=companyId)
        if companyPeople.exists():
            serializer = self.serializer_class(companyPeople, data=request.data)

            if(not serializer.is_valid()):
                return Response({'message': 'Falha ao atualizar a situação do usuário na empresa', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            
            companysPeople = CompanyPeople.objects.filter(company=companyId).exclude(user=request.user)
            companysPeople = companysPeople \
                .values('role', 'is_joined', 'is_pending') \
                .annotate(user_id=F('user__id')) \
                .annotate(company_id=F('company__id')) \
                .annotate(full_name=F('user__full_name')) \
                .annotate(doc_number=F('user__doc_number')) \
                .annotate(email=F('user__email'))

            data = self.serializer_class(companysPeople, many=True).data

            return Response({'message': 'Dados do usuário atualizado com sucesso.', 'data': data}, status=status.HTTP_201_CREATED)

        return Response({'message': 'O usuário não está relacionado a empresa.'}, status=status.HTTP_404_NOT_FOUND)

class UsersPendingViews(generics.GenericAPIView):
    serializer_class = UsersPendingSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, companyId=None, excludeMe=False):
        company = Company.objects.filter(id=companyId)
        if company.exists():
            if excludeMe:
                companyPeople = CompanyPeople.objects.filter(company=company.first().id).exclude(user=request.user)
            else:
                companyPeople = CompanyPeople.objects.filter(company=company.first().id)
            
            userRole = CompanyPeople.objects.filter(user=request.user, company=company.first().id).first()
            
            if userRole.role == 'Gestor' or request.user.is_staff:
                companyPeople = companyPeople \
                    .values('role', 'is_joined', 'is_pending') \
                    .annotate(user_id=F('user__id')) \
                    .annotate(company_id=F('company__id')) \
                    .annotate(full_name=F('user__full_name')) \
                    .annotate(doc_number=F('user__doc_number')) \
                    .annotate(email=F('user__email'))

                companyPeople = self.serializer_class(companyPeople, many=True).data

                return Response({'message': 'Usuários retornados com sucesso', 'data': companyPeople}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'O usuário não tem autorização para acessar essa área'}, status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response({'message': 'Empresa não localizada'}, status=status.HTTP_404_NOT_FOUND)