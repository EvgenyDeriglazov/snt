# Generated by Django 3.0.2 on 2020-03-08 18:56

import data.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChairMan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text='Введите имя', max_length=50, validators=[data.models.validate_human_names], verbose_name='Имя')),
                ('middle_name', models.CharField(help_text='Введите отчество', max_length=50, validators=[data.models.validate_human_names], verbose_name='Отчество')),
                ('last_name', models.CharField(help_text='Введите фамилию', max_length=50, validators=[data.models.validate_human_names], verbose_name='Фамилия')),
            ],
            options={
                'verbose_name': 'председатель',
                'verbose_name_plural': 'председатели',
            },
        ),
        migrations.CreateModel(
            name='ElectricalCounter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(help_text='Модель прибора учета электроэнергии', max_length=50, verbose_name='Модель')),
                ('serial_number', models.CharField(help_text='Серийный номер прибора учета электроэнергии', max_length=50, verbose_name='Серийный номер')),
                ('model_type', models.CharField(choices=[('T1', 'Однотарифный'), ('T2', 'Двухтарифный')], default='T1', help_text='Тип прибора учета', max_length=2, verbose_name='Тип')),
                ('intro_date', models.DateField(verbose_name='дата установки/приемки')),
                ('t1', models.PositiveIntegerField(blank=True, default=None, help_text='Тариф Т1 (6:00-23:00)', null=True, verbose_name='Показание при установке/приемке (день)')),
                ('t2', models.PositiveIntegerField(blank=True, default=None, help_text='Тариф Т2 (23:00-6:00)', null=True, verbose_name='Показание при установке/приемке (ночь)')),
                ('t_single', models.PositiveIntegerField(blank=True, default=None, help_text='Однотарифный', null=True, verbose_name='Показание при установке/приемке')),
            ],
            options={
                'verbose_name': 'прибор учета электроэнергии',
                'verbose_name_plural': 'приборы учета электроэнергии',
            },
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(help_text='Введите фамилию', max_length=50, validators=[data.models.validate_human_names], verbose_name='Фамилия')),
                ('first_name', models.CharField(help_text='Введите имя', max_length=50, validators=[data.models.validate_human_names], verbose_name='Имя')),
                ('middle_name', models.CharField(help_text='Введите отчество', max_length=50, validators=[data.models.validate_human_names], verbose_name='Отчество')),
                ('status', models.CharField(choices=[('c', 'Настоящий'), ('p', 'Прежний')], default='c', help_text='Статус владельца', max_length=1, verbose_name='Статус владельца')),
                ('start_owner_date', models.DateField(verbose_name='дата начала владения')),
                ('end_owner_date', models.DateField(blank=True, null=True, verbose_name='дата окончания владения')),
            ],
            options={
                'verbose_name': 'владелец',
                'verbose_name_plural': 'владельцы',
            },
        ),
        migrations.CreateModel(
            name='Snt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Полное название СНТ', max_length=200, verbose_name='Название СНТ')),
                ('personal_acc', models.CharField(help_text='Номер расчетного счета (20-и значное число)', max_length=20, validators=[data.models.validate_number, data.models.validate_20_length], verbose_name='Номер расчетного счета')),
                ('bank_name', models.CharField(help_text='Наименование банка получателя', max_length=45, verbose_name='Наименование банка получателя')),
                ('bic', models.CharField(help_text='БИК (9-и значное число)', max_length=9, validators=[data.models.validate_number, data.models.validate_9_length], verbose_name='БИК')),
                ('corresp_acc', models.CharField(help_text='Номер кор./счета (20-и значное число)', max_length=20, validators=[data.models.validate_number, data.models.validate_20_length], verbose_name='Номер кор./счета')),
                ('inn', models.CharField(help_text='ИНН (10-и значное число)', max_length=10, validators=[data.models.validate_number, data.models.validate_10_length], verbose_name='ИНН')),
                ('kpp', models.CharField(help_text='КПП (9-и значное число)', max_length=9, validators=[data.models.validate_number, data.models.validate_9_length], verbose_name='КПП')),
                ('chair_man', models.OneToOneField(help_text='Председатель садоводства', null=True, on_delete=django.db.models.deletion.SET_NULL, to='data.ChairMan', verbose_name='председатель')),
            ],
            options={
                'verbose_name': 'СНТ',
                'verbose_name_plural': 'СНТ',
            },
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intro_date', models.DateField(auto_now_add=True, help_text='Дата введения/изменения тарифа', verbose_name='Дата')),
                ('t1_rate', models.DecimalField(decimal_places=2, help_text='Тариф Т1 (6:00-23:00)', max_digits=4, verbose_name='Электроэнергия день')),
                ('t2_rate', models.DecimalField(decimal_places=2, help_text='Тариф Т2 (23:00-6:00)', max_digits=4, verbose_name='Электроэнергия ночь')),
                ('rate_status', models.CharField(blank=True, choices=[('c', 'Действующий')], default='c', max_length=1, null=True, unique=True, unique_for_date='intro_date', verbose_name='Вид тарифа')),
            ],
            options={
                'verbose_name': 'Тариф',
                'verbose_name_plural': 'Тарифы',
                'unique_together': {('intro_date', 'rate_status')},
            },
        ),
        migrations.CreateModel(
            name='LandPlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plot_number', models.CharField(help_text='Номер участка', max_length=10, unique=True, verbose_name='Номер участка')),
                ('plot_area', models.PositiveIntegerField(help_text='Единица измерения кв.м', verbose_name='Размер участка')),
                ('electrical_counter', models.OneToOneField(help_text='Данные прибора учета электроэнергии', null=True, on_delete=django.db.models.deletion.SET_NULL, to='data.ElectricalCounter', verbose_name='Счетчик')),
                ('owner', models.ForeignKey(help_text='Владелец участка', null=True, on_delete=django.db.models.deletion.SET_NULL, to='data.Owner', verbose_name='владелец участка')),
                ('snt', models.ForeignKey(help_text='Расположен в СНТ', null=True, on_delete=django.db.models.deletion.SET_NULL, to='data.Snt', verbose_name='СНТ')),
                ('user', models.ForeignKey(blank=True, help_text='Аккаунт пользователя на сайте', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Логин')),
            ],
            options={
                'verbose_name': 'участок',
                'verbose_name_plural': 'участки',
            },
        ),
        migrations.CreateModel(
            name='ElectricityPayments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_date', models.DateField(auto_now_add=True, help_text='Дата снятия показаний счетчика', verbose_name='Дата')),
                ('counter_number', models.CharField(blank=True, default=None, help_text='Серийный номер прибора учета электроэнергии', max_length=50, null=True, verbose_name='Номер счетчика')),
                ('t1_new', models.PositiveIntegerField(blank=True, default=None, help_text='Тариф Т1 (6:00-23:00)', null=True, verbose_name='Текущее показание (день)')),
                ('t2_new', models.PositiveIntegerField(blank=True, default=None, help_text='Тариф Т2 (23:00-6:00)', null=True, verbose_name='Текущее показание (ночь)')),
                ('t_single_new', models.PositiveIntegerField(blank=True, default=None, help_text='Однотарифный', null=True, verbose_name='Текущее показание')),
                ('t1_prev', models.PositiveIntegerField(blank=True, default=None, help_text='Тариф Т1 (6:00-23:00)', null=True, verbose_name='Предыдущее показание (день)')),
                ('t2_prev', models.PositiveIntegerField(blank=True, default=None, help_text='Тариф Т2 (23:00-6:00)', null=True, verbose_name='Предыдущее показание (ночь)')),
                ('t_single_prev', models.PositiveIntegerField(blank=True, default=None, help_text='Однотарифный', null=True, verbose_name='Предыдущее показание')),
                ('t1_cons', models.PositiveIntegerField(blank=True, default=None, help_text='Тариф Т1 (6:00-23:00)', null=True, verbose_name='Потрачено квт/ч (день)')),
                ('t2_cons', models.PositiveIntegerField(blank=True, default=None, help_text='Тариф Т2 (23:00-6:00)', null=True, verbose_name='Потрачено квт/ч (ночь)')),
                ('t_single_cons', models.PositiveIntegerField(blank=True, default=None, help_text='Однотарифный', null=True, verbose_name='Потрачено квт/ч')),
                ('record_status', models.CharField(choices=[('n', 'Новые показания'), ('p', 'Оплачено'), ('c', 'Оплата подтверждена')], default='n', help_text='Статус квитанции', max_length=1, verbose_name='Статус')),
                ('pay_date', models.DateField(blank=True, null=True, verbose_name='Дата оплаты')),
                ('t1_amount', models.DecimalField(blank=True, decimal_places=2, default=None, help_text='Сумма по тарифу Т1', max_digits=7, null=True, verbose_name='Сумма (день)')),
                ('t2_amount', models.DecimalField(blank=True, decimal_places=2, default=None, help_text='Сумма по тарифу Т2', max_digits=7, null=True, verbose_name='Сумма (ночь)')),
                ('t_single_amount', models.DecimalField(blank=True, decimal_places=2, default=None, help_text='Сумма (однотарифный)', max_digits=7, null=True, verbose_name='Сумма')),
                ('sum_tot', models.DecimalField(blank=True, decimal_places=2, default=None, help_text='Общая сумма к оплате', max_digits=7, null=True, verbose_name='Итог')),
                ('land_plot', models.ForeignKey(help_text='Номер участка', null=True, on_delete=django.db.models.deletion.SET_NULL, to='data.LandPlot', unique_for_date='record_date', verbose_name='Номер участка')),
            ],
            options={
                'verbose_name': 'электроэнергия',
                'verbose_name_plural': 'электроэнергия',
            },
        ),
    ]
