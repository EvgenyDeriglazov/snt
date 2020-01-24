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
        cls.obj =  ElectricityPayments.objects.create(
            plot_number=LandPlot.objects.get(id=1),
            record_date=date(2020, 1, 1),
            t1_new=0,
            t2_new=0,
        )
        ElectricityPayments.objects.filter(id=1).update(
            record_date=date(2020, 1, 1))
        
    # Test fields
    def test_plot_number_field(self):
        #obj = ElectricityPayments.objects.get(id=1)
        ref_obj = LandPlot.objects.get(id=1)
        is_null = self.obj._meta.get_field('plot_number').null
        field_label = self.obj._meta.get_field('plot_number').verbose_name
        help_text = self.obj._meta.get_field('plot_number').help_text
        is_unique = self.obj._meta.get_field('plot_number').unique_for_date
        self.assertEqual(is_null, True)
        self.assertEqual(field_label, "Номер участка")
        self.assertEqual(help_text, "Номер участка")
        self.assertEqual(is_unique, "record_date")
        self.assertEqual(self.obj.plot_number, ref_obj)

    def test_record_date_field(self):
        obj = ElectricityPayments.objects.get(id=1)
        auto_now_add = obj._meta.get_field('record_date').auto_now_add
        field_label = obj._meta.get_field('record_date').verbose_name
        help_text = obj._meta.get_field('record_date').help_text
        self.assertEqual(auto_now_add, True)
        self.assertEqual(field_label, "Дата")
        self.assertEqual(help_text, "Дата снятия показаний счетчика")
        self.assertEqual(obj.record_date, date(2020, 1, 1))

    def test_t1_new_field(self):
        obj = ElectricityPayments.objects.get(id=1)
        field_label = obj._meta.get_field('t1_new').verbose_name
        help_text = obj._meta.get_field('t1_new').help_text
        self.assertEqual(field_label, "Текущее показание (день)")
        self.assertEqual(help_text, "Тариф Т1 (6:00-23:00)")
        self.assertEqual(obj.t1_new, Decimal('0'))

    def test_t2_new_field(self):
        obj = ElectricityPayments.objects.get(id=1)
        field_label = obj._meta.get_field('t2_new').verbose_name
        help_text = obj._meta.get_field('t2_new').help_text
        is_null = obj._meta.get_field('t2_new').null
        is_blank = obj._meta.get_field('t2_new').blank
        is_default = obj._meta.get_field('t2_new').default
        self.assertEqual(field_label, "Текущее показание (ночь)")
        self.assertEqual(help_text, "Тариф Т2 (23:00-6:00)")
        self.assertEqual(is_null, True)
        self.assertEqual(is_blank, True)
        self.assertEqual(is_default, None)
        self.assertEqual(obj.t2_new, Decimal('0'))

    def test_t1_prev_field(self):
        obj = ElectricityPayments.objects.get(id=1)
        field_label = obj._meta.get_field('t1_prev').verbose_name
        help_text = obj._meta.get_field('t1_prev').help_text
        is_null = obj._meta.get_field('t1_prev').null
        is_blank = obj._meta.get_field('t1_prev').blank
        is_default = obj._meta.get_field('t1_prev').default
        self.assertEqual(field_label, "Предыдущее показание (день)")
        self.assertEqual(help_text, "Тариф Т1 (6:00-23:00)")
        self.assertEqual(is_null, True)
        self.assertEqual(is_blank, True)
        self.assertEqual(is_default, None)
        self.assertEqual(obj.t1_prev, None)

    def test_t2_prev_field(self):
        obj = ElectricityPayments.objects.get(id=1)
        field_label = obj._meta.get_field('t2_prev').verbose_name
        help_text = obj._meta.get_field('t2_prev').help_text
        is_null = obj._meta.get_field('t2_prev').null
        is_blank = obj._meta.get_field('t2_prev').blank
        is_default = obj._meta.get_field('t2_prev').default
        self.assertEqual(field_label, "Предыдущее показание (ночь)")
        self.assertEqual(help_text, "Тариф Т2 (23:00-6:00)")
        self.assertEqual(is_null, True)
        self.assertEqual(is_blank, True)
        self.assertEqual(is_default, None)
        self.assertEqual(obj.t2_prev, None)

    def test_t1_cons_field(self):
        obj = ElectricityPayments.objects.get(id=1)
        field_label = obj._meta.get_field('t1_cons').verbose_name
        is_null = obj._meta.get_field('t1_cons').null
        is_blank = obj._meta.get_field('t1_cons').blank
        is_default = obj._meta.get_field('t1_cons').default
        self.assertEqual(field_label, "Потрачено квт/ч (день)")
        self.assertEqual(is_null, True)
        self.assertEqual(is_blank, True)
        self.assertEqual(is_default, None)
        self.assertEqual(obj.t1_cons, None)

    def test_t2_cons_field(self):
        obj = ElectricityPayments.objects.get(id=1)
        field_label = obj._meta.get_field('t2_cons').verbose_name
        is_null = obj._meta.get_field('t2_cons').null
        is_blank = obj._meta.get_field('t2_cons').blank
        is_default = obj._meta.get_field('t2_cons').default
        self.assertEqual(field_label, "Потрачено квт/ч (ночь)")
        self.assertEqual(is_null, True)
        self.assertEqual(is_blank, True)
        self.assertEqual(is_default, None)
        self.assertEqual(obj.t2_cons, None)
   
    def test_record_status_field(self):
        obj = ElectricityPayments.objects.get(id=1)
        RECORD_STATUS = [
            ('n', 'Новые показания'),
            ('p', 'Оплачено'),
            ('c', 'Оплата подтверждена'),
            ('i', 'Первые показания'),
        ]
        field_label = obj._meta.get_field('record_status').verbose_name
        max_length = obj._meta.get_field('record_status').max_length
        choice = obj._meta.get_field('record_status').choices
        is_default = obj._meta.get_field('record_status').default
        help_text = obj._meta.get_field('record_status').help_text
        self.assertEquals(field_label, 'Статус')
        self.assertEquals(max_length, 1)
        self.assertEquals(choice, RECORD_STATUS)
        self.assertEquals(is_default, 'n')
        self.assertEquals(help_text, 'Статус показаний')
        self.assertEquals(obj.record_status, 'n')

    def test_pay_date_field(self):
        obj = ElectricityPayments.objects.get(id=1)
        field_label = obj._meta.get_field('pay_date').verbose_name
        is_blank = obj._meta.get_field('pay_date').blank
        is_null = obj._meta.get_field('pay_date').null
        self.assertEqual(field_label, "Дата оплаты")
        self.assertEqual(is_blank, True)
        self.assertEqual(is_null, True)
        self.assertEqual(obj.pay_date, None)

    def test_t1_amount_field(self):
        obj = ElectricityPayments.objects.get(id=1)
        field_label = obj._meta.get_field('t1_amount').verbose_name
        help_text = obj._meta.get_field('t1_amount').help_text
        is_null = obj._meta.get_field('t1_amount').null
        is_blank = obj._meta.get_field('t1_amount').blank
        is_default = obj._meta.get_field('t1_amount').default
        is_max_digits = obj._meta.get_field('t1_amount').max_digits
        is_dec_places = obj._meta.get_field('t1_amount').decimal_places
        self.assertEqual(field_label, "Сумма (день)")
        self.assertEqual(help_text, "Сумма по тарифу Т1")
        self.assertEqual(is_null, True)
        self.assertEqual(is_blank, True)
        self.assertEqual(is_default, None)
        self.assertEqual(is_max_digits, 7)
        self.assertEqual(is_dec_places, 2)
        self.assertEqual(obj.t1_amount, None)

    def test_t2_amount_field(self):
        obj = ElectricityPayments.objects.get(id=1)
        field_label = obj._meta.get_field('t2_amount').verbose_name
        help_text = obj._meta.get_field('t2_amount').help_text
        is_null = obj._meta.get_field('t2_amount').null
        is_blank = obj._meta.get_field('t2_amount').blank
        is_default = obj._meta.get_field('t2_amount').default
        is_max_digits = obj._meta.get_field('t2_amount').max_digits
        is_dec_places = obj._meta.get_field('t2_amount').decimal_places
        self.assertEqual(field_label, "Сумма (ночь)")
        self.assertEqual(help_text, "Сумма по тарифу Т2")
        self.assertEqual(is_null, True)
        self.assertEqual(is_blank, True)
        self.assertEqual(is_default, None)
        self.assertEqual(is_max_digits, 7)
        self.assertEqual(is_dec_places, 2)
        self.assertEqual(obj.t2_amount, None)

    def test_sum_tot_field(self):
        obj = ElectricityPayments.objects.get(id=1)
        field_label = obj._meta.get_field('sum_tot').verbose_name
        help_text = obj._meta.get_field('sum_tot').help_text
        is_null = obj._meta.get_field('sum_tot').null
        is_blank = obj._meta.get_field('sum_tot').blank
        is_default = obj._meta.get_field('sum_tot').default
        is_max_digits = obj._meta.get_field('sum_tot').max_digits
        is_dec_places = obj._meta.get_field('sum_tot').decimal_places
        self.assertEqual(field_label, "Итог")
        self.assertEqual(help_text, "Общая сумма к оплате")
        self.assertEqual(is_null, True)
        self.assertEqual(is_blank, True)
        self.assertEqual(is_default, None)
        self.assertEqual(is_max_digits, 7)
        self.assertEqual(is_dec_places, 2)
        self.assertEqual(obj.sum_tot, None)

    def test_object_name(self):
        obj = ElectricityPayments.objects.get(id=1)
        obj_name = f'{obj.plot_number.plot_number} {str(obj.record_date)}' 
        self.assertEquals(obj_name, obj.__str__())
        # or self.assertEquals(object_name, str(lp_obj))
    
    def test_get_absolute_url(self):
        obj = Rate.objects.get(id=1)
        self.assertEquals(obj.get_absolute_url(), '/data/electricity-payments-detail/1')

    def test_verbose_names(self):
        self.assertEquals(
            ElectricityPayments._meta.verbose_name,
            'электроэнергия'
        )
        self.assertEquals(
            ElectricityPayments._meta.verbose_name_plural,
            'электроэнергия'
        )
        self.assertEquals(
            ElectricityPayments._meta.unique_together,
            (('record_date', 'plot_number'),)
        )
    # Test model class methods
    def test_set_initial_function(self):
        """Test set_initial() for following states:
        (n) record in db - change record_status to 'i'
        (i) record in db - return error (False)
        (i,n) records in db - return error (False)"""
        # Check initial state
        self.assertEquals(self.obj.record_status, 'n')
        # State 1 check
        check = self.obj.set_initial()
        self.assertEquals(self.obj.record_status, 'i')
        self.assertEquals(check, self.obj)
        # State 2 check
        check = self.obj.set_initial()
        self.assertEquals(check, False)
        # State 3 check
        obj_1 =  ElectricityPayments.objects.create(
            plot_number=LandPlot.objects.get(id=1),
            t1_new=0,
            t2_new=0,
        )
        check = obj_1.set_initial()
        self.assertEquals(obj_1.record_status, 'n')
        self.assertEquals(check, self.obj_1)
        # Remove new entity and keep record (i)
        obj_1.delete()

    def test_get_i_record_function(self):
        """Test get_i_record() for following states:
        (i) record in db - return i_record object
        (n) record in db - return error (False)"""
        pass

    def test_get_n_record_function(self):
        """Test get_n_record() for following states:
        (i) record in db - return error (False)
        (i,n) records in db - return n_record object"""
        pass

    def test_get_p_record_function(self):
        """Test get_p_record() for following states:
        (i) record in db - return error (False) 
        (i,p) records in db - return p_record object"""
        pass

    def test_get_c_record_function(self):
        """Test get_c_record() for following states:
        (i) record in db - return error (False)
        (i,c) records in db - return c_record
        (i,c,c..) records in db - return latest c_record object"""
        pass

    def test_get_current_rate_function(self):
        """Test descr."""
        pass

    def test_fill_n_record_function(self):
        """Test fill_n_record() for following states:
        (i,n) records in db - use data from i_record object
        (i,c) records in db - use data from c_record object
        (i,c,p,n) records in db - return error (False)
        (i,p,n) records in db - return error (False)"""
        pass
        
    def test_calculate_payment_function(self):
        """Test descr."""
        pass

    def test_set_paid_function(self):
        """Test descr."""
        pass

    def test_set_payment_confirmed_function(self):
        """Test descr."""
        pass

