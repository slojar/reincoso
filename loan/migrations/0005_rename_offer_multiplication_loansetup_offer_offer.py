# Generated by Django 3.2 on 2021-05-04 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0004_loansetup_offer_multiplication'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loansetup',
            old_name='offer_multiplication',
            new_name='offer_offer',
        ),
    ]
