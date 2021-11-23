# Generated by Django 3.2 on 2021-10-26 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0016_auto_20211022_1054'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='investmentoption',
            managers=[
            ],
        ),
        migrations.RenameField(
            model_name='investmentspecification',
            old_name='investment_option',
            new_name='option',
        ),
        migrations.AlterField(
            model_name='investmentspecification',
            name='key',
            field=models.CharField(choices=[('key metric', 'Key metric'), ('minimum return', 'Minimum return'), ('target for return per annum', 'Target for return per annum'), ('investible asset claim', 'Investible asset claim'), ('30 days average return', '30 days average return'), ('return on investment', 'Return on investment'), ('minimum investment', 'Minimum investment'), ('maximum investment', 'Maximum investment')], max_length=100),
        ),
    ]