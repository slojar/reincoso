# Generated by Django 3.2 on 2021-09-21 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('settings', '0008_remove_loansetting_site'),
    ]

    operations = [
        migrations.AddField(
            model_name='loansetting',
            name='site',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sites.site'),
        ),
    ]
