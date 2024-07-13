from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import PendingSerializer
from ..models import Company, CompanyPeople
from functools import wraps

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
