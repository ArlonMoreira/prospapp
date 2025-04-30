from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import LocalSerialier
from company.models import CompanyPeople

class LocalViews(generics.GenericAPIView):
    serializer_class = LocalSerialier
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
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