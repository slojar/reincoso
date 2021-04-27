# Generated by Django 3.2 on 2021-04-27 10:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bot', '0013_auto_20210427_1029'),
    ]

    operations = [
        migrations.CreateModel(
            name='Duration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('interval', models.IntegerField(default=30, help_text='No. of days')),
            ],
        ),
        migrations.CreateModel(
            name='Saving',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fixed_payment', models.FloatField(blank=True, default=0.0, null=True)),
                ('last_payment', models.FloatField(blank=True, default=0.0, null=True)),
                ('last_payment_date', models.DateTimeField(blank=True, null=True)),
                ('next_payment_date', models.DateTimeField(blank=True, null=True)),
                ('balance', models.FloatField(blank=True, default=0.0, null=True)),
                ('repayment_day', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30'), ('31', '31')], default='25', max_length=20)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('duration', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='savings.duration')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='bot.profile')),
            ],
        ),
    ]
