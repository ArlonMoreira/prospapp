from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from call.api.serializers import StudentDisableSerializer, StudentUpdateSerializer, ClassOfStudentDisableSerializer, ClassOfStudentUpdateSerializer, ClassOfStudentSerializer, ClassOfStudent, StudentSerializer, Student, CallSerializer, Call
from django.utils import timezone
from django.db.models import F
from datetime import date, timedelta
import calendar
import pytz

class CallView(generics.GenericAPIView):
    serializer_class = CallSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not isinstance(request.data, list):
            return Response({'message': 'Falha ao registrar chamada, é esperado uma lista de alunos'}, status=status.HTTP_400_BAD_REQUEST)
        
        responses = []        
        
        #Percorre a lista de chamada passada no formato {student: 29, present: true}, percorre essa lista, armazena as respostas em responses.
        for item in request.data:
            serializer = self.serializer_class(data=item)

            if(not serializer.is_valid()):
                return Response({'message': 'Falha ao registrar chamada', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            responses.append(self.serializer_class(serializer.save()).data)

        return Response({'message': 'Chamada registrada com sucesso.', 'data': responses}, status=status.HTTP_201_CREATED)
    
class ReportCallView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, classId=None, year=None, month=None):

        # obtém chamadas
        calls = Call.objects.filter(student__classOfStudent=classId, date__year=year, date__month=month)

        # Obtém o último dia do mês
        last_day = calendar.monthrange(int(year), int(month))[1]
        # Cria a data de início e fim do mês
        start_date = date(int(year), int(month), 1)
        end_date = date(int(year), int(month), last_day)
        # Gera todas as datas do mês
        dates = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range((end_date - start_date).days + 1)]

        # Obter estudantes
        students = Student.objects.filter(classOfStudent=classId)

        if students.exists():
            students = list(students.values())

            privot_data = {}
            for entry in students:
                student = entry['name']
                if student not in privot_data: #Serve para não deixar incluir repetidos, caso contrário, um mesmo estudante vai aparecer mais de uma vez
                    privot_data[student] = { day: None for day in dates }

            if calls.exists():
                calls = list(calls.values('student__name', 'date', 'present'))

                # Tratar campos
                calls = [{'student': call['student__name'], 'date': call['date'].strftime('%Y-%m-%d'), 'present': call['present']} for call in calls]
                
                # Preenhcer privot_data com os status de cada estudante por dia
                for entry in calls:
                    privot_data[entry['student']][entry['date']] = entry['present']

            return Response({'message': 'Relatório gerado com sucesso', 'data': privot_data}, status=status.HTTP_200_OK)

        return Response({'message': 'Falha ao gerar o relatório'}, status=status.HTTP_400_BAD_REQUEST)

class StudentView(generics.GenericAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, classId=None, date=timezone.now().astimezone(pytz.timezone('America/Sao_Paulo')).date()):
        # Obtendo a data atual
        # today = timezone.now().astimezone(pytz.timezone('America/Sao_Paulo')).date()

        # Carregando todas as chamadas da data atual em uma única query
        calls = Call.objects.filter(date=date).select_related('student')

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
    
def ResponseUpdateStudent(self, **kwargs):

    student = Student.objects.filter(id=kwargs['student'])

    if student.exists():
        serializer = self.serializer_class(student, data=kwargs['request'].data)

        if (not serializer.is_valid()):
            return Response({'message': 'Falha ao cadastrar aluno', 'data':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        data = self.serializer_class(serializer.save()).data

        return Response({'message': 'Aluno registrado com sucesso', 'data': data}, status=status.HTTP_200_OK)        

    return Response({'message': 'Aluno não localizado'}, status=status.HTTP_404_NOT_FOUND)
    
class StudentUpdateView(generics.GenericAPIView):
    serializer_class = StudentUpdateSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, student=None):
        return ResponseUpdateStudent(self, request=request, student=student)
    
class StudentDisableView(generics.GenericAPIView):
    serializer_class = StudentDisableSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, student=None):
        return ResponseUpdateStudent(self, request=request, student=student)

class ClassOfStudentView(generics.GenericAPIView):
    serializer_class = ClassOfStudentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, company=None):
        classOfStudent = ClassOfStudent.objects.filter(company=company, is_active=True)   
        serializer = self.serializer_class(classOfStudent, many=True).data

        return Response({'message': 'Dados recuperados com sucesso', 'data': serializer}, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        
        if(not serializer.is_valid()):
            return Response({'message': 'Falha ao cadastrar turma', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        data = self.serializer_class(serializer.save()).data

        return Response({'message': 'Turma registrada com sucesso.', 'data': data}, status=status.HTTP_201_CREATED)

def ResponseUpdateClass(self, **kwargs):

    Class = ClassOfStudent.objects.filter(id=kwargs['Class'])

    if Class.exists():
        serializer = self.serializer_class(Class, data=kwargs['request'].data)

        if(not serializer.is_valid()):
            return Response({'message': 'Falha ao atualizar dados da turma', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        data = self.serializer_class(serializer.save()).data

        return Response({'message': 'Dados da turma atualizado com sucesso.', 'data': data}, status=status.HTTP_200_OK)

    else:
        return Response({'message': 'Turma não localizada.'}, status=status.HTTP_404_NOT_FOUND)


class ClassOfStudentUpdateView(generics.GenericAPIView):
    serializer_class = ClassOfStudentUpdateSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, Class=None):
        
        return ResponseUpdateClass(self, request=request, Class=Class)

class ClassOfStudentDisableView(generics.GenericAPIView):
    serializer_class = ClassOfStudentDisableSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, Class=None):

        return ResponseUpdateClass(self, request=request, Class=Class)

