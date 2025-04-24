from django.db import models

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
        null=False   
    )    
    workload_minutes = models.IntegerField(
        verbose_name='Carga Horária/Minutos',
        blank=False,
        null=False       
    )
    is_active = models.IntegerField(
        verbose_name='Ativa',
        blank=False,
        null=False,
        default=True
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Local de registro'
        verbose_name_plural = 'Locais de registro'