# Generated by Django 4.2.11 on 2024-04-13 06:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('security', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TwoFactorSettingsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_enabled', models.BooleanField(default=False)),
                ('recovery_token', models.CharField(blank=True, max_length=100, null=True)),
                ('token', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('token_expiry', models.DateTimeField(blank=True, null=True)),
                ('otp', models.CharField(blank=True, max_length=6)),
                ('otp_expiry', models.DateTimeField(blank=True, null=True)),
                ('failed_attempts', models.PositiveIntegerField(default=0)),
                ('blocked_until', models.DateTimeField(blank=True, null=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalTwoFactorSettingsModel',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('is_enabled', models.BooleanField(default=False)),
                ('recovery_token', models.CharField(blank=True, max_length=100, null=True)),
                ('token', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('token_expiry', models.DateTimeField(blank=True, null=True)),
                ('otp', models.CharField(blank=True, max_length=6)),
                ('otp_expiry', models.DateTimeField(blank=True, null=True)),
                ('failed_attempts', models.PositiveIntegerField(default=0)),
                ('blocked_until', models.DateTimeField(blank=True, null=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical two factor settings model',
                'verbose_name_plural': 'historical two factor settings models',
                'db_table': 'tsec_hist_two_factor_settings',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]