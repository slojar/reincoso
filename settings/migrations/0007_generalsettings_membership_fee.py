# Generated by Django 3.2.2 on 2021-05-28 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0006_loansetting_number_of_guarantor'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalsettings',
            name='membership_fee',
            field=models.DecimalField(decimal_places=2, default=1000, max_digits=20),
        ),
    ]