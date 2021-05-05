# Generated by Django 3.2 on 2021-04-28 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0014_delete_saving'),
        ('savings', '0004_saving_auto_save'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavingTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(choices=[('paystack', 'Paystack'), ('flutterwave', 'Flutterwave')], default='paystack', max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('reference', models.CharField(max_length=100, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('success', 'Success'), ('failed', 'Failed')], max_length=50)),
                ('response', models.TextField(blank=True, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('saving', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='savings.saving')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.profile')),
            ],
        ),
    ]
