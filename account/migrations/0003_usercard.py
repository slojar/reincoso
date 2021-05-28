# Generated by Django 3.2.2 on 2021-05-24 20:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_loanguarantor'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('bank', models.CharField(max_length=50, null=True)),
                ('card_type', models.CharField(max_length=50, null=True)),
                ('bin', models.CharField(max_length=50, null=True)),
                ('last4', models.CharField(max_length=50, null=True)),
                ('exp_month', models.CharField(max_length=2, null=True)),
                ('exp_year', models.CharField(max_length=4, null=True)),
                ('signature', models.CharField(max_length=200, null=True)),
                ('authorization_code', models.CharField(max_length=200, null=True)),
                ('payload', models.TextField(null=True)),
                ('default', models.BooleanField(default=False, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.profile')),
            ],
        ),
    ]