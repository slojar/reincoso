# Generated by Django 3.2 on 2021-05-26 20:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0004_loan_amount_left_to_pay'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loan',
            old_name='amount_left_to_pay',
            new_name='amount_left_to_repay',
        ),
    ]
