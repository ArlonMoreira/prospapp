# Generated by Django 5.0.6 on 2025-05-23 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('point', '0006_local_latitude_local_limit_radius_local_longitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='local',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Ativa'),
        ),
        migrations.AlterField(
            model_name='local',
            name='limit_radius',
            field=models.FloatField(blank=True, default=100, null=True, verbose_name='Rio limite'),
        ),
    ]
