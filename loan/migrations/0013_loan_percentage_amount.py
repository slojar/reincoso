# Generated by Django 3.2 on 2021-05-05 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0012_auto_20210505_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='percentage_amount',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=20),
        ),
    ]
