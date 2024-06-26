# Generated by Django 4.2.11 on 2024-04-17 06:46

from django.db import migrations, models
import security.models.application_model


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0006_sessionhistorymodel_sessionmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationmodel',
            name='logo',
            field=models.FileField(blank=True, default=None, null=True, upload_to=security.models.application_model.path_file),
        ),
        migrations.AddField(
            model_name='historicalapplicationmodel',
            name='logo',
            field=models.TextField(blank=True, default=None, max_length=100, null=True),
        ),
    ]
