# Generated by Django 5.0.6 on 2024-06-30 10:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name': 'Companhia', 'verbose_name_plural': 'Companhias'},
        ),
        migrations.AddField(
            model_name='company',
            name='logo',
            field=models.ImageField(blank=True, default='companys/logo.png', null=True, upload_to='companys/'),
        ),
        migrations.AddField(
            model_name='company',
            name='primary_color',
            field=models.CharField(default='#0C6661', verbose_name='Cor primária'),
        ),
        migrations.AddField(
            model_name='company',
            name='secundary_color',
            field=models.CharField(default='#008C81', verbose_name='Cor secundária'),
        ),
        migrations.CreateModel(
            name='CompanyPeople',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(blank=True, choices=[('Gestor', 'Gestor'), ('Colaborador', 'Colaborador')], max_length=65, null=True, verbose_name='Perfil')),
                ('is_joined', models.BooleanField(default=False, verbose_name='Ingressou')),
                ('is_pending', models.BooleanField(default=True, verbose_name='Aguardando')),
                ('date_joined', models.DateTimeField(null=True, verbose_name='Data/Ingresso')),
                ('company', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.company')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'company')},
            },
        ),
    ]