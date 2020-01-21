# Generated by Django 3.0.2 on 2020-01-21 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='rate_status',
            field=models.CharField(blank=True, choices=[('c', 'Действующий')], default='c', max_length=1, null=True, unique=True, unique_for_date='intro_date', verbose_name='Вид тарифа'),
        ),
    ]
