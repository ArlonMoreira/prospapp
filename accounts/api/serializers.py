from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from accounts.models import Users
from company.models import CompanyPeople, Company
from validate_docbr import CPF

class EditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ('email', 'full_name', 'doc_number')

    def save(self):
        Me = self.instance

        Me.email = self.validated_data.get('email', Me.email)
        Me.full_name = self.validated_data.get('full_name', Me.full_name)
        Me.doc_number = self.validated_data.get('foc_number', Me.doc_number)

        Me.save()

        return Me

class RegisterSerializer(serializers.ModelSerializer):   
    password = serializers.CharField(
        write_only=True, #Não irá retornar na resposta da requisição, apenas leitura
        required=True,
        validators=[validate_password]
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': 'As senhas não coincidem'
            })

        return attrs
    
    class Meta:
        model = Users
        fields = ('email', 'full_name', 'doc_number', 'password', 'confirm_password')

    def validate_doc_number(self, value):
        cpf = CPF()
        if value and not cpf.validate(value):
            raise serializers.ValidationError('CPF inválido')
        
        return value
    
    def create(self, validated_data):

        user = Users.objects.create(
            email=validated_data['email'].lower().strip(),
            full_name=validated_data['full_name'],
            doc_number=validated_data['doc_number']
        )
        
        user.set_password(validated_data['password'])
        user.save()

        #Criar uma instância, colocando por padrão associando a Prospere com o usuário recém cadastrado
        if(user):
            companyPeople = CompanyPeople(
                user=user,
                company=Company.objects.filter(id=1)[0],
                is_joined=True
            )

            companyPeople.save()

        return user
    
class ResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]        
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]        
    )

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': 'As senhas não coincidem'
            })
        return super().validate(attrs)

    class Meta:
        model = Users
        fields = ('password', 'confirm_password')

    def save(self, **kwargs):
        User = self.instance
        User.set_password(self.validated_data['password'])
        User.save()

        return User

class LoginSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        error_messages={
            'invalid': 'E-mail inválido',
            'required': 'O campo e-mail é obrigatório',
            'unique': 'E-mail já cadastrado'
        }
    )

    class Meta:
        model = Users
        fields = ('email', 'password')

    def validate_email(self, value):
        
        if not(Users.objects.filter(email=value).exists()):
            raise serializers.ValidationError('Usuário não cadastrado')
        
        return value