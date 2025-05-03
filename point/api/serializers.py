from rest_framework import serializers
from ..models import Local
from company.models import Company

class LocalSerialier(serializers.ModelSerializer):

    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), required=True)

    class Meta:
        model = Local
        fields = ('id', 'name', 'identification_number', 'workload_hour', 'workload_minutes', 'company')

    def save(self, **kwargs):
        local = Local(
            name=self.validated_data.get('name'),
            identification_number=self.validated_data.get('identification_number'),
            workload_hour=self.validated_data.get('workload_hour', 0),
            workload_minutes=self.validated_data.get('workload_minutes', 0),
            company=self.validated_data.get('company')
        )

        local.save()

        return local