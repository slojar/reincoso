# Generated by Django 3.2 on 2021-04-21 11:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_auto_20210421_1013'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=20),
        ),
        migrations.AddField(
            model_name='profile',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
