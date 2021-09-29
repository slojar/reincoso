# Generated by Django 3.2 on 2021-09-28 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('savings', '0005_auto_20210928_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saving',
            name='payment_gateway',
            field=models.CharField(choices=[('paystack', 'Paystack'), ('flutterwave', 'Flutterwave')], default='paystack', max_length=50),
        ),
    ]
