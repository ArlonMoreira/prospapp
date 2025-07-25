# Generated by Django 5.0.6 on 2025-07-10 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('point', '0007_alter_local_is_active_alter_local_limit_radius'),
    ]

    operations = [
        migrations.AddField(
            model_name='points',
            name='is_justify',
            field=models.BooleanField(default=False, verbose_name='Ponto justificado'),
        ),
        migrations.AddField(
            model_name='points',
            name='justify_description',
            field=models.CharField(blank=True, max_length=125, null=True, verbose_name='Justificativa'),
        ),
    ]
