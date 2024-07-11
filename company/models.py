from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from accounts.models import Users

class Company(models.Model):

    identification_number = models.BigIntegerField(
        verbose_name='CNPJ',
        blank=False,
        null=False
    )
    legal_name = models.CharField(
        max_length=225,
        verbose_name='Razão social',
        blank=False,
        null=False
    )
    trade_name = models.CharField(
        max_length=255,
        verbose_name='Nome fantasia',
        blank=False,
        null=False
    )
    logo = models.ImageField(
        upload_to='companys/',
        null=True,
        blank=True,
        default='companys/logo.png'
    )
    primary_color = models.CharField(
        verbose_name='Cor primária',
        null=False,
        blank=False,
        default='#0C6661'
    )
    secundary_color = models.CharField(
        verbose_name='Cor secundária',
        null=False,
        blank=False,
        default='#008C81'
    )

    def __str__(self):
        return self.trade_name

    class Meta:
        verbose_name='Companhia'
        verbose_name_plural='Companhias'

class CompanyPeople(models.Model):

    ROLE_CHOICES = (
        ('Gestor','Gestor'),
        ('Colaborador', 'Colaborador')
    )

    user = models.ForeignKey(
        Users,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Usuário')
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Empresa')
    role = models.CharField(
        verbose_name="Perfil",
        max_length=65,
        blank=True,
        null=True,
        choices=ROLE_CHOICES,
        default='Colaborador'
    )
    is_joined = models.BooleanField(
        verbose_name="Ingressou",
        default=False
    )
    is_pending = models.BooleanField(
        verbose_name="Aguardando",
        default=False
    )
    date_joined = models.DateTimeField(
        verbose_name="Data/Ingresso",
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.user} - {self.company} - {self.role}"
    
    def clean(self):
        if self.is_joined and self.is_pending: #Impossibilitar que seja possível ingressar e aguardar o ingresso ao mesmo tempo
            raise ValidationError('This action could not be performed. The fields is_joined and is_pending can not True togheter.')
    
    def save(self, *args, **kwargs):
        instance = CompanyPeople.objects.filter(id=self.id) #Obtenho a relação já cadastrada

        if instance.exists(): #Caso essa relação já existir
            if instance[0].is_joined != self.is_joined:
                if self.is_joined:
                    self.date_joined = timezone.now()
                    self.is_pending = False
                else:
                    self.date_joined = None

        else:
            if self.is_joined: #Caso ainda não existir no banco e is_joined for True, será passado a data atual como padrão para date_joined
                self.date_joined = timezone.now()
                self.is_pending = False
            else:
                self.date_joined = None

        if self.is_pending: #Não é possível estar pendente e associado ao mesmo tempo, se marcou como pendente automaticamnete o associado será marcado como False
            self.is_joined = False

        super().save(*args, **kwargs)
    
    class Meta:
        unique_together = ('user', 'company')
        verbose_name = 'Relação empresa-colaborador'

