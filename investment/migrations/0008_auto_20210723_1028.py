# Generated by Django 3.2 on 2021-07-23 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0007_investmenttransaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='investment',
            name='end_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='investment',
            name='start_date',
            field=models.DateTimeField(null=True),
        ),
    ]
