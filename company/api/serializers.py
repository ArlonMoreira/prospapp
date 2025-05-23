from rest_framework import serializers
from ..models import CompanyPeople

class PendingSerializer(serializers.ModelSerializer):

    identification_number = serializers.CharField(required=False)
    trade_name = serializers.CharField(required=False)
    slug_name = serializers.CharField(required=False)
    logo = serializers.CharField(required=False)

    class Meta:
        model = CompanyPeople
        fields = ('company', 'identification_number', 'trade_name', 'slug_name', 'logo', 'is_joined', 'is_pending')
    
    def save(self, **kwargs):
        companyPeople = self.instance

        #Caso a instância exista só irei atualizar o status
        if(companyPeople):
            companyPeople = companyPeople.first()
            companyPeople.is_pending = self.validated_data.get('is_pending')
            companyPeople.save()
        #Se a instância não existir eu irei criar uma nova com o status de pendente.
        else:
            companyPeople = CompanyPeople(
                user=self.context['user'],
                company=self.validated_data.get('company'),
                is_pending=True
            )
            companyPeople.save()
        
        return companyPeople
    
class UsersPendingSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=False)
    doc_number = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    
    class Meta:
        model = CompanyPeople
        fields = ('user_id', 'company_id', 'full_name', 'doc_number', 'email', 'role', 'is_joined', 'is_pending')
    
class UsersPendingUpdateSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=False)
    doc_number = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    
    class Meta:
        model = CompanyPeople
        fields = ('user_id', 'company_id', 'full_name', 'doc_number', 'email', 'role', 'is_joined', 'is_pending')

    def save(self, **kwargs):
        companyPeople = self.instance

        if(companyPeople):
            companyPeople = companyPeople.first()
            companyPeople.role = self.validated_data.get('role', companyPeople.role)
            companyPeople.is_joined = self.validated_data.get('is_joined', companyPeople.is_joined)
            companyPeople.is_pending = self.validated_data.get('is_pending', companyPeople.is_pending)
            companyPeople.save()

        return companyPeople


