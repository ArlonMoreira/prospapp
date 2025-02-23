from django.db import models
from django.core.validators import MinLengthValidator
from company.models import Company
from django.utils import timezone
import pytz

class ClassOfStudent(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Organização'
    )
    name = models.CharField(
        max_length=45,
        verbose_name='Nome',
        null=False,
        blank=False
    )
    is_active = models.BooleanField(
        verbose_name="Ativo",
        default=True
    )

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'company')
        verbose_name='Turma'
        verbose_name_plural='Turmas'

class Student(models.Model):
    name = models.CharField(
        max_length=145,
        verbose_name='Nome',
        null=False,
        blank=False
    )    
    identification_number = models.CharField(
        verbose_name="CPF",
        max_length=11,
        validators=[MinLengthValidator(11)],
        blank=True,
        null=True,
        error_messages={
            'invalid': 'CPF inválido',
            'required': 'O campo CPF é obrigatório',
            'unique': 'CPF já cadastrado'      
        }  
    )
    classOfStudent = models.ForeignKey(
        ClassOfStudent,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Classe'
    )    
    is_active = models.BooleanField(
        verbose_name="Ativo",
        default=True
    )    

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='Estudante'
        verbose_name_plural='Estudantes'

def get_brasilia_time():
    return timezone.now().astimezone(pytz.timezone('America/Sao_Paulo')).date()       

class Call(models.Model):  
    student = models.ForeignKey(
        Student,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Aluno'                
    )
    present = models.BooleanField(
        default=False,
        verbose_name='Presente'
    )
    date = models.DateField(
        verbose_name="Data/Cadastro",
        default=get_brasilia_time
    )
    
    def __str__(self):
        return self.student.name 

    class Meta:
        verbose_name='Chamada'
        verbose_name_plural='Chamadas'       