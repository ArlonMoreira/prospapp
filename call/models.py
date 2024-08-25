from django.db import models
from django.core.exceptions import ValidationError
from company.models import Company

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
    is_active = models.BooleanField(
        verbose_name="Ativo",
        default=True
    )    

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='Estudante'
        verbose_name_plural='Estudantes'

class Registration(models.Model):
    classOfStudent = models.ForeignKey(
        ClassOfStudent,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Organização'
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Estudante'
    )
    date_joined = models.DateTimeField(
        verbose_name="Data/Ingresso",
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.classOfStudent} - {self.student}"

    class Meta:
        verbose_name='Matrícula'
        verbose_name_plural='Matrículados'    