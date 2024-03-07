# Generated by Django 3.2.21 on 2024-02-16 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DriveInnapp', '0002_chat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='credit_point_table',
            name='PAYMENT_TABLE',
        ),
        migrations.RemoveField(
            model_name='credit_point_table',
            name='date',
        ),
        migrations.AddField(
            model_name='credit_point_table',
            name='LOGIN_TABLE',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='DriveInnapp.login_table'),
        ),
    ]