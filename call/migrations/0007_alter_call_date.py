# Generated by Django 5.0.6 on 2024-11-11 01:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('call', '0006_alter_call_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='call',
            name='date',
            field=models.DateTimeField(default=datetime.date(2024, 11, 10), verbose_name='Data/Cadastro'),
        ),
    ]