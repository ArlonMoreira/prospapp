# Generated by Django 5.0.6 on 2024-11-11 02:49

import call.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('call', '0010_alter_call_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='call',
            name='date',
            field=models.DateField(default=call.models.get_brasilia_time, verbose_name='Data/Cadastro'),
        ),
    ]