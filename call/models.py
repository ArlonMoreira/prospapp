from django.db import models
from company.models import Company
from django.utils import timezone

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
    identification_number = models.BigIntegerField(
        verbose_name='CPF',
        null=False,
        blank=False
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
    date = models.DateTimeField(
        verbose_name="Data/Cadastro",
        default=timezone.now
    )
    
    def __str__(self):
        return self.student  

    class Meta:
        verbose_name='Chamada'
        verbose_name_plural='Chamadas'       