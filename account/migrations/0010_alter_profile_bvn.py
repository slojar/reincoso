# Generated by Django 3.2 on 2021-09-22 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_wallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bvn',
            field=models.CharField(max_length=300),
        ),
    ]
