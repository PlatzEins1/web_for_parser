# Generated by Django 4.1.1 on 2022-11-16 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_part', '0004_app_user_first_name_app_user_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='data_file',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main_part.app_user'),
        ),
    ]
