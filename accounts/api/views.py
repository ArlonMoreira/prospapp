from rest_framework import generics, status, mixins
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import authenticate, login
from .serializers import LoginSerializer, RegisterSerializer
from accounts.utils import get_token_for_user
from accounts.models import Users

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        
        #Validar formulário de cadastro
        if not serializer.is_valid():
            return Response({'message': 'Falha ao cadastrar usuário', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        #Obter os dados cadastrados
        data = self.serializer_class(serializer.save()).data

        return Response({'message': 'Usuário cadastrado', 'data': data}, status=status.HTTP_201_CREATED)

class RefreshTokenView(TokenRefreshView, mixins.ListModelMixin, mixins.CreateModelMixin):

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        if not(serializer.is_valid()):
            return Response({
                'message': 'Sua sessão foi encerrada.',
                'data': serializer.erros,
                status:status.HTTP_200_OK
            })

        # Decodifica o token refresh usando a chave secreta (secret key)
        decoded_token = RefreshToken(request.data['refresh'], verify=False)
        payload = decoded_token.payload #{'token_type': '', 'exp': , 'iat': , 'jti': '', 'user_id': }
        
        # Obtém o usuário associado ao token
        user = Users.objects.get(id=payload.get('user_id'))
        
        # Cria um novo refresh token
        new_refresh = RefreshToken.for_user(user)
        access_token = new_refresh.access_token

        return Response({
            'message': 'Sessão renovada.',
            'data': {
                'refresh': str(new_refresh),
                'access': str(access_token)
            }
        })

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        #Validar formulário de autenticação
        if not serializer.is_valid():
            return Response({'message': 'Usuário não cadastrado', 'data': serializer.errors}, status=status.HTTP_401_UNAUTHORIZED)
        
        data = serializer.data

        #Autenticação
        user = authenticate(email=data['email'], password=data['password'])
        #Se autenticado
        if user is not None:
            #Realizar login
            login(request, user)
            #Obter token
            data = get_token_for_user(user)

            return Response({'message': 'Autenticação realizada com sucesso', 'data': data}, status=status.HTTP_200_OK)

        return Response({
            'message': 'Usuário ou senha inválidos',
            'data': [
                {
                    'password': 'Senha inválida'
                }
            ]
        }, status=status.HTTP_401_UNAUTHORIZED)
