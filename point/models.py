from django.db import models
from company.models import Company
from accounts.models import Users

# Create your models here.
class Local(models.Model):
    name = models.CharField(
        max_length=145,
        verbose_name='Nome do local',
        null=False,
        blank=False
    )
    identification_number = models.BigIntegerField(
        verbose_name='CNPJ',
        blank=True,
        null=True
    )
    workload_hour = models.IntegerField(
        verbose_name='Carga Horária/Hora',
        blank=False,
        null=False,
        default=0
    )    
    workload_minutes = models.IntegerField(
        verbose_name='Carga Horária/Minutos',
        blank=False,
        null=False,
        default=0  
    )
    is_active = models.BooleanField(
        verbose_name='Ativa',
        blank=False,
        null=False,
        default=True,
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        verbose_name='Empresa'
    )
    latitude = models.FloatField(
        verbose_name='Latitude',
        null=True,
        blank=True
    )
    longitude = models.FloatField(
        verbose_name='Longitude',
        null=True,
        blank=True
    )
    limit_radius = models.FloatField(
        verbose_name='Rio limite',
        null=True,
        blank=True,
        default=100
    )      

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Local de registro'
        verbose_name_plural = 'Locais de registro'

class Points(models.Model):
    user = models.ForeignKey(
        Users,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Usuário'
    )
    local = models.ForeignKey(
        Local,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Local/Empresa'
    )
    date = models.DateField(
        verbose_name='Data de registro',
        null=False,
        blank=False       
    )
    entry_datetime = models.DateTimeField(
        verbose_name='Data e hora de entrada',
        null=False,
        blank=False
    )
    exit_datetime = models.DateTimeField(
        verbose_name='Data e hora de saída',
        null=True,  # permite que o ponto seja aberto sem saída ainda
        blank=True
    )

    def __str__(self):
        return f"{self.user} - Entrada: {self.entry_datetime} / Saída: {self.exit_datetime or '---'}"

    class Meta:
        verbose_name = 'Registro de ponto'
        verbose_name_plural = 'Registros de ponto'
