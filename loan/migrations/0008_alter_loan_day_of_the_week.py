# Generated by Django 3.2 on 2022-05-14 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0007_auto_20220514_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='day_of_the_week',
            field=models.CharField(choices=[('1', 'Monday'), ('2', 'Tuesday'), ('3', 'Wednesday'), ('4', 'Thursday'), ('5', 'Friday'), ('6', 'Saturday'), ('7', 'Sunday')], default='1', max_length=20),
        ),
    ]
