# Generated by Django 3.2.21 on 2024-02-19 03:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DriveInnapp', '0006_request_table_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment_table',
            name='USER_TABLE',
        ),
        migrations.RemoveField(
            model_name='payment_table',
            name='WORKER_TABLE',
        ),
        migrations.AddField(
            model_name='payment_table',
            name='REQUEST_TABLE',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='DriveInnapp.request_table'),
        ),
    ]
