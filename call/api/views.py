from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from call.api.serializers import ClassOfStudentSerializer, ClassOfStudent, StudentSerializer

class StudentView(generics.GenericAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if(not serializer.is_valid()):
            return Response({'message': 'Falha ao cadastrar aluno', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        data = self.serializer_class(serializer.save()).data

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