# Generated by Django 3.2 on 2021-10-21 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0012_auto_20211021_0902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investmenttype',
            name='slug',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
