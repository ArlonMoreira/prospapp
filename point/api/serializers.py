from rest_framework import serializers
from ..models import Local, Points
from company.models import Company

class LocalDisableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Local
        fields = ('id', 'is_active')

    def save(self, **kwargs):

        Local = self.instance.first()

        if Local.is_active:
            Local.is_active = False
            Local.save()

            return Local
        
        Local.is_active = True
        Local.save()

        return Local        


class LocalSerialier(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), required=False)

    class Meta:
        model = Local
        fields = (
            'id', 'name', 'identification_number', 'workload_hour', 
            'workload_minutes', 'company', 'latitude', 'longitude', 'limit_radius',
            'is_active'
        )

    def save(self, **kwargs):
        local = self.instance

        if local:
            local = local.first()  # Isso ainda é estranho, você está usando .first() com um objeto, veja mais abaixo
            local.name = self.validated_data.get('name', local.name)
            local.identification_number = self.validated_data.get('identification_number', local.identification_number)
            local.workload_hour = self.validated_data.get('workload_hour', local.workload_hour)
            local.workload_minutes = self.validated_data.get('workload_minutes', local.workload_minutes)
            local.latitude = self.validated_data.get('latitude', local.latitude)
            local.longitude = self.validated_data.get('longitude', local.longitude)
            local.limit_radius = self.validated_data.get('limit_radius', local.limit_radius)
            local.company = self.validated_data.get('company', local.company)
            local.save()
        else:
            local = Local.objects.create(
                name=self.validated_data.get('name'),
                identification_number=self.validated_data.get('identification_number'),
                workload_hour=self.validated_data.get('workload_hour', 0),
                workload_minutes=self.validated_data.get('workload_minutes', 0),
                latitude=self.validated_data.get('latitude', -16.69057),
                longitude=self.validated_data.get('longitude', -49.25223),
                limit_radius=self.validated_data.get('limit_radius', 100),
                company=self.validated_data.get('company')
            )

        return local
    
class PointsJustifySerializer(serializers.ModelSerializer):

    class Meta:
        model = Points
        fields = ('id', 'user', 'local', 'date', 'entry_datetime', 'exit_datetime', 'is_justify', 'justify_description')

    def validate_justify_description(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("A justificativa é obrigatório e não pode estar vazio.")
        return value
    
    def validate_exit_datetime(self, value):
        entry_datetime = self.initial_data.get('entry_datetime')

        if isinstance(entry_datetime, str):
            from django.utils.dateparse import parse_datetime
            entry_datetime = parse_datetime(entry_datetime)

        if entry_datetime and value and value < entry_datetime:
            raise serializers.ValidationError("A saída não pode ser anterior à entrada.")

        return value    

    def save(self, **kwargs):
        point = Points(
            user=self.context['user'],
            local=self.validated_data.get('local'),
            date=self.validated_data.get('date'),
            entry_datetime=self.validated_data.get('entry_datetime'),
            exit_datetime=self.validated_data.get('exit_datetime'),
            is_justify=self.validated_data.get('is_justify'),
            justify_description=self.validated_data.get('justify_description'),
        )

        point.save()
        return point     
    
class PointsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Points
        fields = ('id', 'user', 'local', 'date', 'entry_datetime', 'exit_datetime', 'is_justify', 'justify_description')
        read_only_fields = ('user', 'local', 'date', 'entry_datetime', 'exit_datetime', 'is_justify', 'justify_description')

    def get_date(self, obj):
        return obj.entry_datetime.date() if obj.entry_datetime else None        