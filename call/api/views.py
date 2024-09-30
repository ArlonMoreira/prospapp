from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from call.api.serializers import ClassOfStudentSerializer, ClassOfStudent, StudentSerializer, Student, CallSerializer, Call
from django.utils import timezone

class CallView(generics.GenericAPIView):
    serializer_class = CallSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if(not serializer.is_valid()):
            return Response({'message': 'Falha ao registrar chamada', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        data = self.serializer_class(serializer.save()).data

        return Response({'message': 'Chamada registrada com sucesso.', 'data': data}, status=status.HTTP_201_CREATED)

class StudentView(generics.GenericAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, classId=None):
        # Obtendo a data atual
        today = timezone.now().date()

        # Carregando todas as chamadas da data atual em uma única query
        calls = Call.objects.filter(date__date=today).select_related('student')

        # Criando um dicionário {student_id: call_object} para acesso rápido
        call_dict = {call.student.id: call for call in calls}

        # Filtrando os estudantes da turma específica e que estão ativos
        students = Student.objects.filter(classOfStudent=classId, is_active=True)

        # Serializando os estudantes
        serializer = self.serializer_class(students, many=True).data

        # Populando os dados de presença e data de maneira eficiente
        for row in serializer:
            student_call = call_dict.get(row['id'])  # Verifica se existe uma chamada para o estudante
            if student_call:
                row['present'] = student_call.present
                row['date'] = student_call.date.strftime('%Y-%m-%d')
            else:
                row['present'] = None
                row['date'] = None             

        return Response({'message': 'Dados recuperados com sucesso', 'data': serializer}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if(not serializer.is_valid()):
            return Response({'message': 'Falha ao cadastrar aluno', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        data = self.serializer_class(serializer.save()).data

        data['present'] = None
        data['date'] = None 

        return Response({'message': 'Aluno registrado com sucesso.', 'data': data}, status=status.HTTP_201_CREATED)
    
class ClassOfStudentView(generics.GenericAPIView):
    serializer_class = ClassOfStudentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, company=None):
        classOfStudent = ClassOfStudent.objects.filter(company=company)   
        serializer = self.serializer_class(classOfStudent, many=True).data

        return Response({'message': 'Dados recuperados com sucesso', 'data': serializer}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        
        if(not serializer.is_valid()):
            return Response({'message': 'Falha ao cadastrar turma', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        data = self.serializer_class(serializer.save()).data

        return Response({'message': 'Turma registrada com sucesso.', 'data': data}, status=status.HTTP_201_CREATED)