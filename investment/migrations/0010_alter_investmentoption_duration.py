# Generated by Django 3.2 on 2021-09-17 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0009_auto_20210813_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investmentoption',
            name='duration',
            field=models.ManyToManyField(blank=True, to='investment.InvestmentDuration'),
        ),
    ]
