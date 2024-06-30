from rest_framework import serializers
from accounts.models import Users

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
            raise serializers.ValidationError('Usuário não cadastrado.')
        
        return value