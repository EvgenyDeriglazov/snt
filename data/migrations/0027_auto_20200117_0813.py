# Generated by Django 3.0.2 on 2020-01-17 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0026_auto_20200117_0807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='electricmeterreadings',
            name='sum_tot',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, help_text='Общая сумма к оплате', max_digits=7, null=True, verbose_name='Итог'),
        ),
        migrations.AlterField(
            model_name='electricmeterreadings',
            name='t1_amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, help_text='Сумма по тарифу Т1', max_digits=7, null=True, verbose_name='Сумма (день)'),
        ),
        migrations.AlterField(
            model_name='electricmeterreadings',
            name='t1_cons',
            field=models.PositiveIntegerField(blank=True, default=None, null=True, verbose_name='Потрачено квт/ч (день)'),
        ),
        migrations.AlterField(
            model_name='electricmeterreadings',
            name='t1_prev',
            field=models.PositiveIntegerField(blank=True, default=None, help_text='Тариф Т1 (6:00-23:00)', null=True, verbose_name='Предыдущее показание (день)'),
        ),
        migrations.AlterField(
            model_name='electricmeterreadings',
            name='t2_amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=None, help_text='Сумма по тарифу Т2', max_digits=7, null=True, verbose_name='Сумма (ночь)'),
        ),
        migrations.AlterField(
            model_name='electricmeterreadings',
            name='t2_cons',
            field=models.PositiveIntegerField(blank=True, default=None, null=True, verbose_name='Потрачено квт/ч (ночь)'),
        ),
        migrations.AlterField(
            model_name='electricmeterreadings',
            name='t2_new',
            field=models.PositiveIntegerField(blank=True, default=None, help_text='Тариф Т2 (23:00-6:00)', null=True, verbose_name='Текущее показание (ночь)'),
        ),
        migrations.AlterField(
            model_name='electricmeterreadings',
            name='t2_prev',
            field=models.PositiveIntegerField(blank=True, default=None, help_text='Тариф Т2 (23:00-6:00)', null=True, verbose_name='Предыдущее показание (ночь)'),
        ),
    ]
