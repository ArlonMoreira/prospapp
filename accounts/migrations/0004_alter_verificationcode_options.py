# Generated by Django 5.0.6 on 2025-04-16 03:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_verificationcode'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='verificationcode',
            options={'verbose_name': 'Código de verificação', 'verbose_name_plural': 'Códigos de verificação'},
        ),
    ]
