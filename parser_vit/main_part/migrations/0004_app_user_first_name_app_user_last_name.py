# Generated by Django 4.1.1 on 2022-11-16 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_part', '0003_app_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='app_user',
            name='first_name',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='app_user',
            name='last_name',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
