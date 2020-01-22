# Generated by Django 3.0.2 on 2020-01-22 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_auto_20200121_2137'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='electricitypayments',
            options={'verbose_name': 'электроэнергия', 'verbose_name_plural': 'электроэнергия'},
        ),
        migrations.AlterField(
            model_name='electricitypayments',
            name='t1_new',
            field=models.PositiveIntegerField(help_text='Тариф Т1 (6:00-23:00)', verbose_name='Текущее показание (день)'),
        ),
    ]
