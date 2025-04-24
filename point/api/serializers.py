from rest_framework import serializers
from ..models import Local

class LocalSerialier(serializers.ModelSerializer):

    class Meta:
        model = Local
        fields = ('name', 'identification_number', 'workload_hour', 'workload_minutes')


    def save(self, **kwargs):

        local = Local(
            name=self.validated_data.get('name'),
            identification_number=self.validated_data.get('identification_number'),
            workload_hour=self.validated_data.get('workload_hour'),
            workload_minutes=self.validated_data.get('workload_minutes'),
        )

        local.save()

        return local