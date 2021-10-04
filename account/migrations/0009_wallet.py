# Generated by Django 3.2 on 2021-09-15 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_usercard_gateway'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('pending', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('bonus', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('updated_on', models.DateField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='account.profile')),
            ],
        ),
    ]