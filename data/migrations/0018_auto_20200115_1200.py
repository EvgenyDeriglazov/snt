# Generated by Django 3.0.2 on 2020-01-15 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0017_auto_20200115_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='electricmeterreadings',
            name='t2_new',
            field=models.PositiveIntegerField(default=0, help_text='Тариф Т2 (23:00-6:00)', verbose_name='Текущее показание (ночь)'),
        ),
    ]
