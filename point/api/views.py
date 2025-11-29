from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import PointsJustifySerializer, LocalSerialier, Local, PointsSerializer, Points, LocalDisableSerializer
from company.models import CompanyPeople
from datetime import datetime
from django.utils import timezone
from geopy.distance import geodesic

class GetLocalViews(generics.GenericAPIView):
    serializer_class = LocalSerialier
    permission_classes = [IsAuthenticated]

    def get(self, request, companyId=None):
        companyPeople = CompanyPeople.objects.filter(user=request.user)

        if not companyPeople.exists():
            return Response({'message': 'Esse usuário não está vinculado a nenhum companhia.', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
        
        locals = Local.objects.filter(company_id=companyId, is_active=True)

        locals = self.serializer_class(locals, many=True).data

        return Response({'message': 'Locais de ponto recuperado', 'data': locals}, status=status.HTTP_200_OK)

def ResponseUpdateLocal(self, **kwargs):
    local = Local.objects.filter(id=kwargs['localId'])
    if local.exists():
        serializer = self.serializer_class(local, data=kwargs['request'].data)

        if(not serializer.is_valid()):
            return Response({'message': 'Falha ao atualizar o local de registro de ponto.', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        data = self.serializer_class(serializer.save()).data

        return Response({'message': 'Local de registro de ponto atualizado com sucesso.', 'data': data}, status=status.HTTP_200_OK)  

    return Response({'message': 'Local de registro de ponto não encontrado.'}, status=status.HTTP_404_NOT_FOUND)      

class LocalUpdateView(generics.GenericAPIView):
    serializer_class = LocalSerialier
    permission_classes = [IsAuthenticated]

    def put(self, request, localId=None):
        return ResponseUpdateLocal(self, request=request, localId=localId)
    
class LocalDisableView(generics.GenericAPIView):
    serializer_class = LocalDisableSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, localId=None):
        return ResponseUpdateLocal(self, request=request, localId=localId)    

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
        
        now = timezone.now() #timezone.localtime(timezone.now())
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

class RemovePointTodayView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PointsSerializer

    def delete(self, request, pointId=None):
        now = timezone.now() #timezone.localtime(timezone.now())
        today = now.date()  

        point = Points.objects.filter(id=pointId, date=today).first()

        if not point:
            return Response({'message': 'Ponto não encontrado.', 'data': []}, status=status.HTTP_400_BAD_REQUEST)
         
        serializer = self.serializer_class(point)
        data = serializer.data  # salva os dados antes da deleção

        point.delete()

        return Response({'message': 'Ponto eletrônico removido.', 'data': data}, status=status.HTTP_200_OK)
    
class ReportPointView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.data.get("user_id")
        year = request.data.get("year")
        month = request.data.get("month")

        if not user_id:
            return Response({"message": "Parâmetro 'user_id' é obrigatório.", 'data': []}, status=status.HTTP_400_BAD_REQUEST)      

        if not year:
            return Response({"message": "Parâmetro 'year' é obrigatório.", 'data': []}, status=status.HTTP_400_BAD_REQUEST)                

        if not month:
            return Response({"message": "Parâmetro 'month' é obrigatório.", 'data': []}, status=status.HTTP_400_BAD_REQUEST)

        points = Points.objects.filter(user=user_id, date__year=year, date__month=month)
        locals = Local.objects.all().values()

        weekdays_pt = {
            "Monday": "segunda-feira",
            "Tuesday": "terça-feira",
            "Wednesday": "quarta-feira",
            "Thursday": "quinta-feira",
            "Friday": "sexta-feira",
            "Saturday": "sábado",
            "Sunday": "domingo"
        }        
        
        result = {
            local['name']: [
                {
                    "date": point.date.isoformat(),
                    "dayOfWeek": weekdays_pt[point.date.strftime("%A")],  # traduz o nome do dia
                    "entry_datetime": point.entry_datetime.time().strftime("%H:%M:%S"),
                    "exit_datetime": point.exit_datetime.time().strftime("%H:%M:%S") if point.exit_datetime is not None else None,
                    "hours_worked": round(
                        (point.exit_datetime - point.entry_datetime).total_seconds() / 3600, 2
                    ) if point.exit_datetime else None,
                    "hours_worked_hours": (
                        f"{(point.exit_datetime - point.entry_datetime).seconds // 3600:02d}:"
                        f"{((point.exit_datetime - point.entry_datetime).seconds % 3600) // 60:02d}"
                    ) if point.exit_datetime else None,
                    "is_justify": point.is_justify,
                    "justify_description": point.justify_description           
                }
                for point in points.filter(local=local['id'])                    
            ]
            for local in locals 
        }

        result = {
            key: value for key, value in result.items() if len(value) > 0
        }
        
        return Response({"message": "Dados do relatório obtido com sucesso.", 'data': result}, status=status.HTTP_200_OK)

class RegisterPointJustifyView(generics.GenericAPIView):
    serializer_class = PointsJustifySerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Transformar dados em um dicionário mutável
        data = request.data.copy()

        # Local
        try:        
            data['local'] = Local.objects.get(id=data['local'])
        except Local.DoesNotExist:
            return Response({"message": "Local não informado ou inválido.", 'data': []}, status=status.HTTP_400_BAD_REQUEST)
        
        # Obter data atual
        now = timezone.now() #timezone.localtime(timezone.now())
        today = now.date()

        data['date'] = today

        # Obter data de entrada
        try: 
            naive_entry_dt = timezone.make_aware(datetime.strptime(f"{today} {data['entry_datetime']}", "%Y-%m-%d %H:%M:%S"))
            data['entry_datetime'] = naive_entry_dt #timezone.localtime(naive_entry_dt)
        except:
            return Response({"message": "Horário de entrada não informado ou inválido.", 'data': []}, status=status.HTTP_400_BAD_REQUEST)        

        # Obter data de saída
        try:
            naive_exit_dt = timezone.make_aware(datetime.strptime(f"{today} {data['exit_datetime']}", "%Y-%m-%d %H:%M:%S"))
            data['exit_datetime'] = naive_exit_dt #timezone.localtime(naive_exit_dt)  
        except:
            return Response({"message": "Horário de saída não informado ou inválido.", 'data': []}, status=status.HTTP_400_BAD_REQUEST)              

        # Confirmar justificativa
        data['is_justify'] = True

        # Local deve ser o id também (e não objeto)
        data['local'] = data['local'].id

        serializer = self.serializer_class(data=data, context={'user': request.user})
        
        # Validar formulário
        if not serializer.is_valid():
            return Response({'message': 'Falha ao justificar ponto.', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        # Salvar e retornar dados
        data = self.serializer_class(serializer.save()).data

        return Response({'message': 'Ponto justificado com sucesso.', 'data': data}, status=status.HTTP_201_CREATED)


class RegisterPointView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        local_id = request.data.get("local_id")
        latitude_register = request.data.get("latitude")
        longitude_register = request.data.get("longitude")

        if not latitude_register:
            return Response({"message": "Parâmetro 'latitude' é obrigatório.", 'data': []}, status=status.HTTP_400_BAD_REQUEST)      

        if not longitude_register:
            return Response({"message": "Parâmetro 'longitude' é obrigatório.", 'data': []}, status=status.HTTP_400_BAD_REQUEST)                

        if not local_id:
            return Response({"message": "Parâmetro 'local_id' é obrigatório.", 'data': []}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            local = Local.objects.get(id=local_id)
        except Local.DoesNotExist:
            return Response({"message": "Local não encontrado.", 'data': []}, status=status.HTTP_400_BAD_REQUEST)
        
        # Calcula a distância em metros entre o local e a posição atual
        distancia = geodesic(
            (local.latitude, local.longitude),
            (float(latitude_register), float(longitude_register))
        ).meters

        if distancia > local.limit_radius:
            return Response({
                "message": f"Você está fora do raio permitido de {local.limit_radius:.2f} metros.",
                "data": []
            }, status=status.HTTP_400_BAD_REQUEST)
        
        now = timezone.now()#timezone.localtime(timezone.now())

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

        