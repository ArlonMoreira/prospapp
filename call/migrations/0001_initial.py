# Generated by Django 5.0.6 on 2024-09-08 20:56

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0003_alter_companypeople_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassOfStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45, verbose_name='Nome')),
                ('is_active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.company', verbose_name='Organização')),
            ],
            options={
                'verbose_name': 'Turma',
                'verbose_name_plural': 'Turmas',
                'unique_together': {('name', 'company')},
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=145, verbose_name='Nome')),
                ('identification_number', models.BigIntegerField(verbose_name='CPF')),
                ('is_active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('classOfStudent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='call.classofstudent', verbose_name='Organização')),
            ],
            options={
                'verbose_name': 'Estudante',
                'verbose_name_plural': 'Estudantes',
            },
        ),
        migrations.CreateModel(
            name='Call',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('present', models.BooleanField(default=False, verbose_name='Presente')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data/Cadastro')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='call.student', verbose_name='Aluno')),
            ],
            options={
                'verbose_name': 'Chamada',
                'verbose_name_plural': 'Chamadas',
            },
        ),
    ]