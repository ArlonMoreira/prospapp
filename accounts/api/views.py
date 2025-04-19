from rest_framework import generics, status, mixins
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from django.db.models import F
from .serializers import LoginSerializer, RegisterSerializer, EditSerializer, ResetPasswordSerializer, RegisterVerificationSerializer
from accounts.utils import get_token_for_user
from accounts.models import Users, VerificationCode
from company.models import CompanyPeople
from django.conf import settings
from accounts.utils import generated_random_code, send_code_mail
import logging

logger = logging.getLogger(__name__)

class LogoutView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)

            token.blacklist()

            return Response({'message': 'Usuário deslogado com sucesso.'}, status=status.HTTP_200_OK)
        
        except TokenError as e:
            return Response({'error': 'Token inválido ou expirado'}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            logger.error(f"Erro no logout: {e}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class MeView(generics.GenericAPIView):
    permission_classes=[IsAuthenticated]

    def get(self, request, *args, **kwargs):
        companys = CompanyPeople.objects.filter(user=request.user, is_joined=True).annotate(
            company_id_annotated=F('company_id'),
            slug_name=F('company__slug_name'),
            logo=F('company__logo'),
            primary_color=F('company__primary_color'),
            secundary_color=F('company__secundary_color')
        ).values(
            'company_id_annotated', 'slug_name', 'logo', 'role', 'primary_color', 'secundary_color', 'is_joined', 'is_pending'
        )

        companys_joined = list(companys)

        data = {
            'full_name': request.user.full_name,
            'doc_number': request.user.doc_number,
            'email': request.user.email,
            'profileImage': request.user.profileImage.url if request.user.profileImage else settings.MEDIA_URL+'profiles/default_profile.png',
            'companys_joined': companys_joined,
            'is_staff': request.user.is_staff
        }

        return Response({'message': 'Dados obtidos com sucesso', 'data': data}, status=status.HTTP_200_OK)

class ResetPasswordView(generics.UpdateAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        User = Users.objects.get(id=request.user.id)
        serializer = self.serializer_class(User, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response({'message': 'Falha ao alterar a senha do usuário', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response({'message': 'Senha alterada com sucesso'}, status=status.HTTP_200_OK)

class EditView(generics.GenericAPIView):
    serializer_class = EditSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            Me = Users.objects.get(id=request.user.id)
        except Users.DoesNotExist:
            return Response({'message': 'Falha ao encontrar o usuário'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(Me, data=request.data, partial=True)  # 'partial=True' permite atualização parcial

        if not serializer.is_valid():
            return Response({'message': 'Falha ao alterar dados do usuário', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response({'message': 'Dados do usuário atualizado', 'data': serializer.data}, status=status.HTTP_200_OK)
    
class CheckVerificationView(APIView):
    permission_classes = []
    authentication_classes = []    

    def post(self, request):
        try:
            code = request.data['code']
        except:
            return Response({'message': 'Código de verificação não informado.'}, status=status.HTTP_400_BAD_REQUEST)
                        
        try:
            email = request.data['email']
        except:
            return Response({'message': 'E-mail de verificação não informado.'}, status=status.HTTP_400_BAD_REQUEST)

        User = Users.objects.filter(email=email).first()
        if not User:
            return Response({'message': 'Usuário não cadastrado.'}, status=status.HTTP_400_BAD_REQUEST)
        
        instance_code = VerificationCode.objects.filter(user=User, code=code)

        if not instance_code.exists():
            return Response({'message': 'Código de verificação inválido.'}, status=status.HTTP_400_BAD_REQUEST)
        
        User.is_active = True
        User.save()
        instance_code.delete()

        login(request, User)
        #Obter token

        data = get_token_for_user(User)

        return Response({'message': 'Autenticação realizada com sucesso', 'data': data}, status=status.HTTP_200_OK)
    
class GenerateCodeAgainView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        try:
            user = Users.objects.filter(email=request.data['email']).first()
            VerificationCode = generated_random_code(user)

            send_code_mail(user, VerificationCode.code)

            return Response({'message': 'Código de verificação reenviado.', 'data': []}, status=status.HTTP_201_CREATED)
    
        except:
            return Response({'message': 'Falha ao gerar código de verificação.', 'data': []}, status=status.HTTP_400_BAD_REQUEST)

class RegisterVerificationView(generics.GenericAPIView):
    serializer_class = RegisterVerificationSerializer
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        #Obter uma instância inativa do usuário
        instance_user = Users.objects.filter(email=request.data['email'].lower().strip(), is_active=False)

        #Caso tiver algum usuário que esteja aguardando por verificação vou deletar a instância existente e permitir a criação de uma nova instância.
        if instance_user.exists() and VerificationCode.objects.filter(user=instance_user.first()).exists():
            instance_user.delete()        

        serializer = self.serializer_class(data=request.data)
     
        #Validar formulário de cadastro
        if not serializer.is_valid():
            return Response({'message': 'Falha ao cadastrar usuário', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        #Obter os dados cadastrados
        data = self.serializer_class(serializer.save()).data

        user = Users.objects.filter(email=data['email']).first()
        verificationCode = generated_random_code(user)

        send_code_mail(user, verificationCode.code)

        return Response({'message': 'Usuário cadastrado', 'data': data}, status=status.HTTP_201_CREATED)
    
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = []
    authentication_classes = []

    def post(self, request):

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
        user_data = Users.objects.filter(email=data['email'])
        
        if user_data.exists() and not user_data.first().is_active:
            return Response({'message': 'O usuário não está ativo', 'data': []}, status=status.HTTP_401_UNAUTHORIZED) 

        #Autenticação
        user = authenticate(email=data['email'].lower().strip(), password=data['password'])
        
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
