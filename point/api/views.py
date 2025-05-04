from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import LocalSerialier, Local, PointsSerializer, Points
from company.models import CompanyPeople
from datetime import datetime
from django.utils import timezone

class GetLocalViews(generics.GenericAPIView):
    serializer_class = LocalSerialier
    permission_classes = [IsAuthenticated]

    def get(self, request, companyId=None):
        companyPeople = CompanyPeople.objects.filter(user=request.user)

        if not companyPeople.exists():
            return Response({'message': 'Esse usuário não está vinculado a nenhum companhia.', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
        
        locals = Local.objects.filter(company_id=companyId)

        locals = self.serializer_class(locals, many=True).data

        return Response({'message': 'Locais de ponto recuperado', 'data': locals}, status=status.HTTP_200_OK)     


class LocalViews(generics.GenericAPIView):
    serializer_class = LocalSerialier
    permission_classes = [IsAuthenticated]

    def post(self, request):
        companyPeople = CompanyPeople.objects.filter(user=request.user)

        if not companyPeople.exists():
            return Response({'message': 'Esse usuário não está vinculado a nenhum companhia.', 'data': []}, status=status.HTTP_400_BAD_REQUEST)

        if companyPeople.first().role != 'Gestor':
            return Response({'message': 'Esse usuário não tem permissão para essa ação.', 'data': []}, status=status.HTTP_401_UNAUTHORIZED)

        #Serilizando dados
        serializer = self.serializer_class(data=request.data, context={'user': request.user})
        
        #Validando o cadastro do local de ponto
        if not serializer.is_valid():
            return Response({'message': 'Falha ao cadastrar empresa.', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        data = self.serializer_class(serializer.save()).data

        return Response({'message': 'Empresa cadastrada com sucesso.', 'data': data}, status=status.HTTP_201_CREATED)  
    
class RegisterPointActualView(generics.GenericAPIView):
    serializer_class = PointsSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, localId=None):

        try:
            local = Local.objects.get(id=localId)
        except Local.DoesNotExist:
            return Response({"message": "Local não encontrado.", 'data': []}, status=status.HTTP_400_BAD_REQUEST)
        
        now = timezone.localtime(timezone.now())
        today = now.date()        
        
        open_point = Points.objects.filter(
            user=request.user,
            local=local,
            date=today,
            exit_datetime__isnull=True
        ).first()
        open_point_serializer = self.serializer_class(open_point)

        all_points_today = Points.objects.filter(
            user=request.user,
            local=local,
            date=today
        )  
        all_points_today_serializer = self.serializer_class(all_points_today, many=True)

        all_points = Points.objects.filter(
            user=request.user,
            local=local
        )  
        all_points_serializer = self.serializer_class(all_points, many=True)        

        data = {
            'open_point': open_point_serializer.data,
            'all_points_today': all_points_today_serializer.data,
            'all_points': all_points_serializer.data
        }

        return Response({'message': 'Consulta realizada com sucesso.', 'data': data}, status=status.HTTP_200_OK)

class RegisterPointView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        local_id = request.data.get("local_id")

        if not local_id:
            return Response({"message": "Parâmetro 'local_id' é obrigatório.", 'data': []}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            local = Local.objects.get(id=local_id)
        except Local.DoesNotExist:
            return Response({"message": "Local não encontrado.", 'data': []}, status=status.HTTP_400_BAD_REQUEST)
        
        now = timezone.localtime(timezone.now())
        today = now.date()

        # Verifica se já existe um ponto aberto (sem saída) hoje para esse local
        open_point = Points.objects.filter(
            user=request.user,
            local=local,
            date=today,
            exit_datetime__isnull=True
        ).first()

        if open_point:
            # Fecha o ponto com a hora de saída
            open_point.exit_datetime = now
            open_point.save()
            serializer = PointsSerializer(open_point)

            return Response({"message": "Saída registrada com sucesso.", 'data': serializer.data}, status=status.HTTP_201_CREATED)
        
        else:
            # Cria um novo ponto com a hora de entrada
            new_point = Points.objects.create(
                user=request.user,
                local=local,
                date=today,
                entry_datetime=now
            )
            serializer = PointsSerializer(new_point)

            return Response({"message": "Entrada registrada com sucesso.", 'data': serializer.data}, status=status.HTTP_201_CREATED)

        