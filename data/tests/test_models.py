# --- Collectstatic (ValueError: Missing staticfiles manifest entry...) ---
# python3 manage.py collectstatic
# --- Verbosity ---
# python3 manage.py test --verbosity (1-default, 0, 1, 2, 3)
# --- Run specific test modules ---
# python3 manage.py test data.tests
# python3 manage.py test data.tests.test_models
# python3 manage.py test data.tests.test_models.TestClass
# --- Coverage.py --- 
# coverage run --source='.' manage.py test <appname>
# coverage report

from django.test import TestCase
from data.models import *
from datetime import date
from decimal import *

class SntModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        ChairMan.objects.create(
            first_name='Иван',
            middle_name='Иванович',
            last_name='Иванов',
        )
        Snt.objects.create(
            name='СНТ Бобровка',
            personal_acc='01234567898765432101',
            bank_name='Банк',
            bic='123456789',
            corresp_acc='01234567898765432101',
            inn='0123456789',
            kpp='123456789',
            chair_man=ChairMan.objects.get(id=1),
        )
    # Test functions
    def test_name_field(self):
        snt = Snt.objects.get(id=1)
        field_label = snt._meta.get_field('name').verbose_name
        help_text = snt._meta.get_field('name').help_text
        max_length = snt._meta.get_field('name').max_length
        self.assertEquals(field_label, 'Наименование СНТ')   
        self.assertEqual(max_length, 200)
        self.assertEqual(help_text, 'Полное название СНТ')

    def test_personal_acc_field(self):
        snt = Snt.objects.get(id=1)
        field_label = snt._meta.get_field('personal_acc').verbose_name
        max_length = snt._meta.get_field('personal_acc').max_length
        help_text = snt._meta.get_field('personal_acc').help_text
        self.assertEqual(field_label, 'Номер расчетного счета')
        self.assertEqual(max_length, 20)
        self.assertEqual(help_text, 'Номер расчетного счета (20-и значное число)')

    def test_bank_name_field(self):
        snt = Snt.objects.get(id=1)
        field_label = snt._meta.get_field('bank_name').verbose_name
        max_length = snt._meta.get_field('bank_name').max_length
        help_text = snt._meta.get_field('bank_name').help_text
        self.assertEqual(field_label, 'Наименование банка получателя')
        self.assertEqual(max_length, 45)
        self.assertEqual(help_text, 'Наименование банка получателя')

    def test_bic_field(self):
        snt = Snt.objects.get(id=1)
        field_label = snt._meta.get_field('bic').verbose_name
        max_length = snt._meta.get_field('bic').max_length
        help_text = snt._meta.get_field('bic').help_text
        self.assertEqual(field_label, 'БИК')
        self.assertEqual(max_length, 9)
        self.assertEqual(help_text, 'БИК (9-и значное число)')

    def test_corresp_acc_field(self):
        snt = Snt.objects.get(id=1)
        field_label = snt._meta.get_field('corresp_acc').verbose_name
        max_length = snt._meta.get_field('corresp_acc').max_length
        help_text = snt._meta.get_field('corresp_acc').help_text
        self.assertEqual(field_label, 'Номер кор./счета')
        self.assertEqual(max_length, 20)
        self.assertEqual(help_text, 'Номер кор./счета (20-и значное число)')

    def test_inn_field(self):
        snt = Snt.objects.get(id=1)
        field_label = snt._meta.get_field('inn').verbose_name
        max_length = snt._meta.get_field('inn').max_length
        help_text = snt._meta.get_field('inn').help_text
        self.assertEqual(field_label, 'ИНН')
        self.assertEqual(max_length, 10)
        self.assertEqual(help_text, 'ИНН (10-и значное число)')

    def test_kpp_field(self):
        snt = Snt.objects.get(id=1)
        field_label = snt._meta.get_field('kpp').verbose_name
        max_length = snt._meta.get_field('kpp').max_length
        help_text = snt._meta.get_field('kpp').help_text
        self.assertEqual(field_label, 'КПП')
        self.assertEqual(max_length, 9)
        self.assertEqual(help_text, 'КПП (9-и значное число)')

    def test_chair_man_field(self):
        snt = Snt.objects.get(id=1)
        ch_m_obj = ChairMan.objects.get(id=1)
        field_label = snt._meta.get_field('chair_man').verbose_name
        help_text = snt._meta.get_field('chair_man').help_text
        self.assertEqual(snt.chair_man, ch_m_obj)
        self.assertEqual(field_label, 'председатель')
        self.assertEqual(help_text, 'Председатель садоводства')
    
    def test_object_name(self):
        snt = Snt.objects.get(id=1)
        object_name = f'{snt.name}'
        self.assertEquals(object_name, str(snt))

    def test_get_absolute_url(self):
        snt = Snt.objects.get(id=1)
        self.assertEquals(snt.get_absolute_url(), '/data/snt-detail/1')

    def test_verbose_names(self):
        self.assertEquals(Snt._meta.verbose_name, 'СНТ')
        self.assertEquals(Snt._meta.verbose_name_plural, 'СНТ')

class ChairManModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ChairMan.objects.create(
            first_name='Иван',
            middle_name='Иванович',
            last_name='Иванов',
        )
    # Test functions
    def test_first_name_field(self):
        ch_m = ChairMan.objects.get(id=1)
        field_label = ch_m._meta.get_field('first_name').verbose_name
        max_length = ch_m._meta.get_field('first_name').max_length
        help_text = ch_m._meta.get_field('first_name').help_text
        self.assertEquals(field_label, "Имя")
        self.assertEquals(max_length, 50)
        self.assertEquals(help_text, "Введите имя")

    def test_middle_name_field(self):
        ch_m = ChairMan.objects.get(id=1)
        field_label = ch_m._meta.get_field('middle_name').verbose_name
        max_length = ch_m._meta.get_field('middle_name').max_length
        help_text = ch_m._meta.get_field('middle_name').help_text
        self.assertEquals(field_label, "Отчество")
        self.assertEquals(max_length, 50)
        self.assertEquals(help_text, "Введите отчество")
    
    def test_last_name_field(self):
        ch_m = ChairMan.objects.get(id=1)
        field_label = ch_m._meta.get_field('last_name').verbose_name
        max_length = ch_m._meta.get_field('last_name').max_length
        help_text = ch_m._meta.get_field('last_name').help_text
        self.assertEquals(field_label, "Фамилия")
        self.assertEquals(max_length, 50)
        self.assertEquals(help_text, "Введите фамилию")
        
    def test_object_name(self):
        ch_m = ChairMan.objects.get(id=1)
        object_name = f'{ch_m.last_name} {ch_m.first_name} {ch_m.middle_name}'
        self.assertEquals(object_name, str(ch_m))

    def test_get_absolute_url(self):
        ch_m = ChairMan.objects.get(id=1)
        self.assertEquals(ch_m.get_absolute_url(), '/data/chairman-detail/1')

    def test_verbose_names(self):
        self.assertEquals(ChairMan._meta.verbose_name, 'председатель')
        self.assertEquals(ChairMan._meta.verbose_name_plural, 'председатели')
        
class LandPlotModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ChairMan.objects.create(
            first_name='Иван',
            middle_name='Иванович',
            last_name='Иванов',
        )
        Snt.objects.create(
            name='СНТ Бобровка',
            personal_acc='01234567898765432101',
            bank_name='Банк',
            bic='123456789',
            corresp_acc='01234567898765432101',
            inn='0123456789',
            kpp='123456789',
            chair_man=ChairMan.objects.get(id=1),
        )
        Owner.objects.create(
            first_name="Сергей",
            middle_name="Сергеевич",
            last_name="Сергеев",
            status='c',
            start_owner_date=date(2020, 1, 1),
            end_owner_date=None,
        )
        ElectricMeter.objects.create(
            model="НЕВА",
            serial_number="123456789",
            model_type="T1",
            acceptance_date=None,
        )
        LandPlot.objects.create(
            plot_number="10",
            plot_area=6000,
            snt=Snt.objects.get(id=1),
            owner=Owner.objects.get(id=1),
            electric_meter=ElectricMeter.objects.get(id=1),
        )
    # Test functions
    def test_plot_number_field(self):
        l_p = LandPlot.objects.get(id=1)
        field_label = l_p._meta.get_field('plot_number').verbose_name
        max_length = l_p._meta.get_field('plot_number').max_length
        help_text = l_p._meta.get_field('plot_number').help_text 
        unique_prop = l_p._meta.get_field('plot_number').unique
        self.assertEqual(field_label, "Номер участка")
        self.assertEqual(max_length, 10)
        self.assertEqual(help_text, "Номер участка")
        self.assertEqual(unique_prop, True)
        self.assertEqual(l_p.plot_number, "10")

    def test_plot_area_field(self):
        l_p = LandPlot.objects.get(id=1)
        field_label = l_p._meta.get_field('plot_area').verbose_name
        help_text = l_p._meta.get_field('plot_area').help_text 
        self.assertEqual(field_label, "Размер участка")
        self.assertEqual(help_text, "Единица измерения кв.м")
        self.assertEqual(l_p.plot_area, 6000)

    def test_snt_field(self):
        lp_obj = LandPlot.objects.get(id=1)
        snt_obj = Snt.objects.get(id=1)
        field_label = lp_obj._meta.get_field('snt').verbose_name
        help_text = lp_obj._meta.get_field('snt').help_text 
        self.assertEqual(field_label, "СНТ")
        self.assertEqual(help_text, "Расположен в СНТ")
        self.assertEqual(lp_obj.snt, snt_obj)

    def test_owner_field(self):
        lp_obj = LandPlot.objects.get(id=1)
        owner_obj = Owner.objects.get(id=1)
        field_label = lp_obj._meta.get_field('owner').verbose_name
        help_text = lp_obj._meta.get_field('owner').help_text
        is_null = lp_obj._meta.get_field('owner').null
        #on_delete = lp_obj._meta.get_field('owner').on_delete
        self.assertEqual(field_label, "владелец участка")
        self.assertEqual(help_text, "Владелец участка")
        self.assertEqual(is_null, True)
        #self.assertEqual(on_delete, models.SET_NULL)
        self.assertEqual(lp_obj.owner, owner_obj)

    def test_electric_meter_field(self):
        lp_obj = LandPlot.objects.get(id=1)
        em_obj = ElectricMeter.objects.get(id=1)
        field_label = lp_obj._meta.get_field('electric_meter').verbose_name
        help_text = lp_obj._meta.get_field('electric_meter').help_text
        is_null = lp_obj._meta.get_field('electric_meter').null
        self.assertEqual(field_label, "Счетчик")
        self.assertEqual(help_text, "Данные прибора учета электроэнергии")
        self.assertEqual(is_null, True)
        self.assertEqual(lp_obj.electric_meter, em_obj)
        
    def test_object_name(self):
        lp_obj = LandPlot.objects.get(id=1)
        object_name = f'{lp_obj.plot_number}'
        self.assertEquals(object_name, lp_obj.__str__())
        # or self.assertEquals(object_name, str(lp_obj))
    
    def test_get_absolute_url(self):
        lp_obj = LandPlot.objects.get(id=1)
        self.assertEquals(lp_obj.get_absolute_url(), '/data/land-plot-detail/1')

    def test_verbose_names(self):
        self.assertEquals(LandPlot._meta.verbose_name, 'участок')
        self.assertEquals(LandPlot._meta.verbose_name_plural, 'участки')

class OwnerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Owner.objects.create(
            first_name="Сергей",
            middle_name="Сергеевич",
            last_name="Сергеев",
            status='p',
            start_owner_date=date(2020, 1, 1),
            end_owner_date=None,
        )
    # Test functions
    def test_first_name_field(self):
        owner_obj = Owner.objects.get(id=1)
        field_label = owner_obj._meta.get_field('first_name').verbose_name
        max_length = owner_obj._meta.get_field('first_name').max_length
        help_text = owner_obj._meta.get_field('first_name').help_text
        validators = owner_obj._meta.get_field('first_name').validators
        self.assertEquals(field_label, 'Имя')
        self.assertEquals(max_length, 50)
        self.assertEquals(help_text, 'Введите имя')
        self.assertEquals(validators[0:1], [validate_human_names])
        self.assertEquals(owner_obj.first_name, "Сергей")
       
    def test_middle_name_field(self):
        owner_obj = Owner.objects.get(id=1)
        field_label = owner_obj._meta.get_field('middle_name').verbose_name
        max_length = owner_obj._meta.get_field('middle_name').max_length
        help_text = owner_obj._meta.get_field('middle_name').help_text
        validators = owner_obj._meta.get_field('middle_name').validators
        self.assertEquals(field_label, 'Отчество')
        self.assertEquals(max_length, 50)
        self.assertEquals(help_text, 'Введите отчество')
        self.assertEquals(validators[0:1], [validate_human_names])
        self.assertEquals(owner_obj.middle_name, "Сергеевич")
    
    def test_last_name_field(self):
        owner_obj = Owner.objects.get(id=1)
        field_label = owner_obj._meta.get_field('last_name').verbose_name
        max_length = owner_obj._meta.get_field('last_name').max_length
        help_text = owner_obj._meta.get_field('last_name').help_text
        validators = owner_obj._meta.get_field('last_name').validators
        self.assertEquals(field_label, 'Фамилия')
        self.assertEquals(max_length, 50)
        self.assertEquals(help_text, 'Введите фамилию')
        self.assertEquals(validators[0:1], [validate_human_names])
        self.assertEquals(owner_obj.last_name, "Сергеев")
    
    def test_status_field(self):
        owner_obj = Owner.objects.get(id=1)
        OWNER_STATUS = [
            ('c', 'Настоящий'),
            ('p', 'Прежний'),
        ]
        field_label = owner_obj._meta.get_field('status').verbose_name
        max_length = owner_obj._meta.get_field('status').max_length
        owner_status = owner_obj._meta.get_field('status').choices
        defaults = owner_obj._meta.get_field('status').default
        help_text = owner_obj._meta.get_field('status').help_text
        self.assertEquals(field_label, 'Статус владельца')
        self.assertEquals(max_length, 1)
        self.assertEquals(owner_status, OWNER_STATUS)
        self.assertEquals(defaults, 'c')
        self.assertEquals(help_text, 'Статус владельца')
        self.assertEquals(owner_obj.status, 'p')
    
    def test_start_owner_date_field(self):
        owner_obj = Owner.objects.get(id=1)
        field_label = owner_obj._meta.get_field('start_owner_date').verbose_name
        self.assertEquals(field_label, 'дата начала владения')
        self.assertEquals(owner_obj.start_owner_date, date(2020, 1, 1))
    
    def test_end_owner_date_field(self):
        owner_obj = Owner.objects.get(id=1)
        field_label = owner_obj._meta.get_field('end_owner_date').verbose_name
        blank = owner_obj._meta.get_field('end_owner_date').blank
        null = owner_obj._meta.get_field('end_owner_date').null
        self.assertEquals(field_label, 'дата окончания владения')
        self.assertEquals(blank, True)
        self.assertEquals(null, True)
        self.assertEquals(owner_obj.end_owner_date, None)
    
    def test_object_name(self):
        obj = Owner.objects.get(id=1)
        obj_name = f'{obj.last_name} {obj.first_name} {obj.middle_name}'
        self.assertEquals(obj_name, obj.__str__())
        # or self.assertEquals(object_name, str(lp_obj))
    
    def test_get_absolute_url(self):
        obj = Owner.objects.get(id=1)
        self.assertEquals(obj.get_absolute_url(), '/data/owner-detail/1')

    def test_verbose_names(self):
        self.assertEquals(Owner._meta.verbose_name, 'владелец')
        self.assertEquals(Owner._meta.verbose_name_plural, 'владельцы')
       
class ElectricMeterModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ElectricMeter.objects.create(
            model="НЕВА",
            serial_number="123456789",
            model_type="T2",
            acceptance_date=None,
        )

    # Test functions
    def test_model_field(self):
        obj = ElectricMeter.objects.get(id=1)
        field_label = obj._meta.get_field('model').verbose_name
        max_length = obj._meta.get_field('model').max_length
        help_text = obj._meta.get_field('model').help_text
        self.assertEquals(field_label, 'Модель')
        self.assertEquals(max_length, 50)
        self.assertEquals(help_text, 'Модель прибора учета электроэнергии')
        self.assertEquals(obj.model, 'НЕВА')
    
    def test_serial_number_field(self):
        obj = ElectricMeter.objects.get(id=1)
        field_label = obj._meta.get_field('serial_number').verbose_name
        max_length = obj._meta.get_field('serial_number').max_length
        help_text = obj._meta.get_field('serial_number').help_text
        self.assertEquals(field_label, 'Серийный номер')
        self.assertEquals(max_length, 50)
        self.assertEquals(help_text, 'Серийный номер прибора учета электроэнергии')
        self.assertEquals(obj.serial_number, '123456789')
    
    def test_model_type_field(self):
        obj = ElectricMeter.objects.get(id=1)
        MODEL_TYPE = [
            ('T1', 'Однотарифный'),
            ('T2', 'Двухтарифный'),
        ]
        field_label = obj._meta.get_field('model_type').verbose_name
        max_length = obj._meta.get_field('model_type').max_length
        choice = obj._meta.get_field('model_type').choices
        defaults = obj._meta.get_field('model_type').default
        help_text = obj._meta.get_field('model_type').help_text
        self.assertEquals(field_label, 'Тип')
        self.assertEquals(max_length, 2)
        self.assertEquals(choice, MODEL_TYPE)
        self.assertEquals(defaults, 'T1')
        self.assertEquals(help_text, 'Тип прибора учета')
        self.assertEquals(obj.model_type, 'T2')

    def test_acceptance_date_field(self):
        obj = ElectricMeter.objects.get(id=1)
        field_label = obj._meta.get_field('acceptance_date').verbose_name
        is_blank = obj._meta.get_field('acceptance_date').blank
        is_null = obj._meta.get_field('acceptance_date').null
        self.assertEquals(field_label, 'дата установки')
        self.assertEquals(is_blank, True)
        self.assertEquals(is_null, True)
        self.assertEquals(obj.acceptance_date, None)

    def test_object_name(self):
        obj = ElectricMeter.objects.get(id=1)
        obj_name = f'{obj.model}' 
        self.assertEquals(obj_name, obj.__str__())
        # or self.assertEquals(object_name, str(lp_obj))
    
    def test_get_absolute_url(self):
        obj = ElectricMeter.objects.get(id=1)
        self.assertEquals(obj.get_absolute_url(), '/data/electric-meter-detail/1')

    def test_verbose_names(self):
        self.assertEquals(ElectricMeter._meta.verbose_name, 'прибор учета электроэнергии')
        self.assertEquals(ElectricMeter._meta.verbose_name_plural, 'приборы учета электроэнергии')

class RateModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Rate.objects.create(
            intro_date=date(2020, 1, 1),
            t1_rate=0.01,
            t2_rate=99.99,
            rate_status=None,
        )
    # Test functions
    def test_intro_rate_field(self):
        obj = Rate.objects.get(id=1)
        field_label = obj._meta.get_field('intro_date').verbose_name
        help_text = obj._meta.get_field('intro_date').help_text
        auto_now_add = obj._meta.get_field('intro_date').auto_now_add
        self.assertEquals(field_label, 'Дата')
        self.assertEquals(help_text, 'Дата введения/изменения тарифа')
        self.assertEquals(auto_now_add, True)
        self.assertEquals(obj.intro_date, date.today())

    def test_t1_rate_field(self):
        obj = Rate.objects.get(id=1)
        field_label = obj._meta.get_field('t1_rate').verbose_name
        help_text = obj._meta.get_field('t1_rate').help_text
        max_dig = obj._meta.get_field('t1_rate').max_digits
        dec_plc = obj._meta.get_field('t1_rate').decimal_places
        self.assertEquals(field_label, 'Электроэнергия день')
        self.assertEquals(help_text, 'Тариф Т1 (6:00-23:00)')
        self.assertEquals(max_dig, 4)
        self.assertEquals(dec_plc, 2)
        self.assertEquals(obj.t1_rate, Decimal('0.01'))

    def test_t2_rate_field(self):
        obj = Rate.objects.get(id=1)
        field_label = obj._meta.get_field('t2_rate').verbose_name
        help_text = obj._meta.get_field('t2_rate').help_text
        max_dig = obj._meta.get_field('t2_rate').max_digits
        dec_plc = obj._meta.get_field('t2_rate').decimal_places
        self.assertEquals(field_label, 'Электроэнергия ночь')
        self.assertEquals(help_text, 'Тариф Т2 (23:00-6:00)')
        self.assertEquals(max_dig, 4)
        self.assertEquals(dec_plc, 2)
        self.assertEquals(obj.t2_rate, Decimal('99.99'))

    def test_rate_status_field(self):
        obj = Rate.objects.get(id=1)
        RATE_STATUS = [
            ('c', 'Действующий'),
        ]
        field_label = obj._meta.get_field('rate_status').verbose_name
        max_length = obj._meta.get_field('rate_status').max_length
        choice = obj._meta.get_field('rate_status').choices
        defaults = obj._meta.get_field('rate_status').default
        help_text = obj._meta.get_field('rate_status').help_text
        is_unique = obj._meta.get_field('rate_status').unique
        is_null = obj._meta.get_field('rate_status').null
        is_blank = obj._meta.get_field('rate_status').blank
        is_unique_for_date = obj._meta.get_field('rate_status').unique_for_date
        self.assertEquals(field_label, 'Вид тарифа')
        self.assertEquals(max_length, 1)
        self.assertEquals(choice, RATE_STATUS)
        self.assertEquals(defaults, 'c')
        self.assertEquals(help_text, '')
        self.assertEquals(is_unique, True)
        self.assertEquals(is_null, True)
        self.assertEquals(is_blank, True)
        self.assertEquals(is_unique_for_date, "intro_date")
        self.assertEquals(obj.rate_status, None)

    def test_object_name(self):
        obj = Rate.objects.get(id=1)
        obj_name = f'{obj.intro_date}' 
        self.assertEquals(obj_name, obj.__str__())
        # or self.assertEquals(object_name, str(lp_obj))
    
    def test_get_absolute_url(self):
        obj = Rate.objects.get(id=1)
        self.assertEquals(obj.get_absolute_url(), '/data/rates-detail/1')

    def test_verbose_names(self):
        self.assertEquals(Rate._meta.verbose_name, 'Тариф')
        self.assertEquals(Rate._meta.verbose_name_plural, 'Тарифы')
        self.assertEquals(Rate._meta.unique_together, (('intro_date', 'rate_status'),))

class ElectricityPaymentsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ChairMan.objects.create(
            first_name='Иван',
            middle_name='Иванович',
            last_name='Иванов',
        )
        Snt.objects.create(
            name='СНТ Бобровка',
            personal_acc='01234567898765432101',
            bank_name='Банк',
            bic='123456789',
            corresp_acc='01234567898765432101',
            inn='0123456789',
            kpp='123456789',
            chair_man=ChairMan.objects.get(id=1),
        )
        Owner.objects.create(
            first_name="Сергей",
            middle_name="Сергеевич",
            last_name="Сергеев",
            status='c',
            start_owner_date=date(2020, 1, 1),
            end_owner_date=None,
        )
        ElectricMeter.objects.create(
            model="НЕВА",
            serial_number="123456789",
            model_type="T1",
            acceptance_date=None,
        )
        LandPlot.objects.create(
            plot_number="1",
            plot_area=6000,
            snt=Snt.objects.get(id=1),
            owner=Owner.objects.get(id=1),
            electric_meter=ElectricMeter.objects.get(id=1),
        )
        ElectricityPayments.objects.create(
            plot_number=LandPlot.objects.get(id=1),
            record_date=date(2020, 1, 1),
            t1_new=0,
            t2_new=0,
        )
    # Test functions
