# Generated by Django 4.2.2 on 2023-08-24 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0002_forsystem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forsystem',
            name='check_time',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]