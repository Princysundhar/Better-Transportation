# Generated by Django 3.2.21 on 2024-02-18 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DriveInnapp', '0004_remove_request_table_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaints_table',
            name='ctype',
            field=models.CharField(max_length=100),
        ),
    ]
