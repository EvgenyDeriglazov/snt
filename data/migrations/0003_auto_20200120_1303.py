# Generated by Django 3.0.2 on 2020-01-20 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_auto_20200118_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landplot',
            name='plot_area',
            field=models.PositiveIntegerField(help_text='Единица измерения кв.м', verbose_name='Размер участка'),
        ),
    ]
