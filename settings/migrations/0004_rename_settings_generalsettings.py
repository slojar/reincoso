# Generated by Django 3.2 on 2021-05-24 10:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('settings', '0003_paymentgateway_site'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Settings',
            new_name='GeneralSettings',
        ),
    ]
