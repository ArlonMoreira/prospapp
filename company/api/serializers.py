from rest_framework import serializers
from ..models import Company

class StatusSerializer(serializers.ModelSerializer):

    is_joined = serializers.BooleanField()
    is_pending = serializers.BooleanField()

    class Meta:
        model = Company
        fields = ('id', 'identification_number', 'trade_name', 'logo', 'is_joined', 'is_pending')