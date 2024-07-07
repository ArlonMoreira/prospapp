from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from accounts.models import Users
from validate_docbr import CPF

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
        if not cpf.validate(value):
            raise serializers.ValidationError('CPF inválido')
        
        return value
    
    def create(self, validated_data):

        user = Users.objects.create(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            doc_number=int(validated_data['doc_number'])
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ('email', 'password')

    def validate_email(self, value):
        
        if not(Users.objects.filter(email=value).exists()):
            raise serializers.ValidationError('Usuário não cadastrado')
        
        return value