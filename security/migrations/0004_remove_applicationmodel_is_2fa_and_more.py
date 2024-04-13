# Generated by Django 4.2.11 on 2024-04-13 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0003_alter_twofactorsettingsmodel_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicationmodel',
            name='is_2fa',
        ),
        migrations.RemoveField(
            model_name='historicalapplicationmodel',
            name='is_2fa',
        ),
        migrations.AddField(
            model_name='applicationmodel',
            name='two_factor_enabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalapplicationmodel',
            name='two_factor_enabled',
            field=models.BooleanField(default=False),
        ),
    ]