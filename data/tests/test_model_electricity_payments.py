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

        ElectricalCounter.objects.create(
            model="НЕВА",
            serial_number="123456789",
            model_type="T1",
            intro_date=date.today(),
            t_single=1,
        )

        ElectricalCounter.objects.create(
            model="НЕВА-2",
            serial_number="000000000",
            model_type="T2",
            intro_date=date.today(),
            t1=1,
            t2=1,
        )

        LandPlot.objects.create(
            plot_number="1",
            plot_area=6000,
            snt=Snt.objects.get(id=1),
            owner=Owner.objects.get(id=1),
            electrical_counter=ElectricalCounter.objects.get(id=1),
        )

        LandPlot.objects.create(
            plot_number="2",
            plot_area=8000,
            snt=Snt.objects.get(id=1),
            owner=Owner.objects.get(id=1),
            electrical_counter=ElectricalCounter.objects.get(id=2),
        )

        ElectricityPayments.objects.create(
            land_plot=LandPlot.objects.get(id=1),
            record_date=date(2020, 1, 1),
            t_single_new=0,
        )

        ElectricityPayments.objects.filter(id=1).update(
            record_date=date(2020, 1, 1))
        
        ElectricityPayments.objects.create(
            land_plot=LandPlot.objects.get(id=2),
            record_date=date(2020, 1, 1),
            t1_new=0,
            t2_new=0,
        )

        ElectricityPayments.objects.filter(id=2).update(
            record_date=date(2020, 1, 1))

        Rate.objects.create(
            t1_rate=5.5,
            t2_rate=2.5,
            t_single_rate=5.5,
        )
        
    # Test fields
    def test_plot_number_field(self):
        obj = ElectricityPayments.objects.get(id=1)
        ref_obj = LandPlot.objects.get(id=1)
        is_null = obj._meta.get_field('land_plot').null
        field_label = obj._meta.get_field('land_plot').verbose_name
        help_text = obj._meta.get_field('land_plot').help_text
        is_unique = obj._meta.get_field('land_plot').unique_for_date
        self.assertEqual(is_null, True)
        self.assertEqual(field_label, "Номер участка")
        self.assertEqual(help_text, "Номер участка")
        self.assertEqual(is_unique, "record_date")
        self.assertEqual(obj.land_plot, ref_obj)

    def test_record_date_field(self):
        obj = ElectricityPayments.objects.get(id=1)
        auto_now_add = obj._meta.get_field('record_date').auto_now_add
        field_label = obj._meta.get_field('record_date').verbose_name
        help_text = obj._meta.get_field('record_date').help_text
        self.assertEqual(auto_now_add, True)
        self.assertEqual(field_label, "Дата")
        self.assertEqual(help_text, "Дата снятия показаний счетчика")
        self.assertEqual(obj.record_date, date(2020, 1, 1))

    def test_counter_number_field(self):
        obj = ElectricityPayments.objects.get(id=1)
        field_label = obj._meta.get_field('counter_number').verbose_name
        max_length = obj._meta.get_field('counter_number').max_length
        help_text = obj._meta.get_field('counter_number').help_text
        is_null = obj._meta.get_field('counter_number').null
        is_blank = obj._meta.get_field('counter_number').blank
        is_default = obj._meta.get_field('counter_number').default
        self.assertEqual(field_label, "Номер счетчика")
        self.assertEqual(max_length, 50)
        self.assertEqual(help_text, "Серийный номер прибора учета электроэнергии")
        self.assertEqual(is_null, True)
        self.assertEqual(is_blank, True)
        self.assertEqual(is_default, None)

       
    def test_t1_new_field(self):
        obj = ElectricityPayments.objects.get(id=1)
        field_label = obj._meta.get_field('t1_new').verbose_name
        help_text = obj._meta.get_field('t1_new').help_text
        is_null = obj._meta.get_field('t1_new').null
        is_blank = obj._meta.get_field('t1_new').blank
        is_default = obj._meta.get_field('t1_new').default
        self.assertEqual(field_label, "Текущее показание (день)")
        self.assertEqual(help_text, "Тариф Т1 (6:00-23:00)")
        self.assertEqual(is_null, True)
        self.assertEqual(is_blank, True)
        self.assertEqual(is_default, None)
        self.assertEqual(obj.t1_new, None)

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
        self.assertEqual(obj.t2_new, None)

    def test_t_single_new_field(self):
        obj = ElectricityPayments.objects.get(id=1)
        field_label = obj._meta.get_field('t_single_new').verbose_name
        help_text = obj._meta.get_field('t_single_new').help_text
        is_null = obj._meta.get_field('t_single_new').null
        is_blank = obj._meta.get_field('t_single_new').blank
        is_default = obj._meta.get_field('t_single_new').default
        self.assertEqual(field_label, "Текущее показание")
        self.assertEqual(help_text, "Однотарифный")
        self.assertEqual(is_null, True)
        self.assertEqual(is_blank, True)
        self.assertEqual(is_default, None)
        self.assertEqual(obj.t_single_new, 0)

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

    def test_t_single_prev_field(self):
        obj = ElectricityPayments.objects.get(id=1)
        field_label = obj._meta.get_field('t_single_prev').verbose_name
        help_text = obj._meta.get_field('t_single_prev').help_text
        is_null = obj._meta.get_field('t_single_prev').null
        is_blank = obj._meta.get_field('t_single_prev').blank
        is_default = obj._meta.get_field('t_single_prev').default
        self.assertEqual(field_label, "Предыдущее показание")
        self.assertEqual(help_text, "Однотарифный")
        self.assertEqual(is_null, True)
        self.assertEqual(is_blank, True)
        self.assertEqual(is_default, None)
        self.assertEqual(obj.t_single_prev, None)


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
 
    def test_t_single_cons_field(self):
        obj = ElectricityPayments.objects.get(id=1)
        field_label = obj._meta.get_field('t_single_cons').verbose_name
        is_null = obj._meta.get_field('t_single_cons').null
        is_blank = obj._meta.get_field('t_single_cons').blank
        is_default = obj._meta.get_field('t_single_cons').default
        self.assertEqual(field_label, "Потрачено квт/ч")
        self.assertEqual(is_null, True)
        self.assertEqual(is_blank, True)
        self.assertEqual(is_default, None)
        self.assertEqual(obj.t_single_cons, None)
   
    def test_record_status_field(self):
        obj = ElectricityPayments.objects.get(id=1)
        RECORD_STATUS = [
            ('n', 'Новые показания'),
            ('p', 'Оплачено'),
            ('c', 'Оплата подтверждена'),
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

    def test_t_single_amount_field(self):
        obj = ElectricityPayments.objects.get(id=1)
        field_label = obj._meta.get_field('t_single_amount').verbose_name
        help_text = obj._meta.get_field('t_single_amount').help_text
        is_null = obj._meta.get_field('t_single_amount').null
        is_blank = obj._meta.get_field('t_single_amount').blank
        is_default = obj._meta.get_field('t_single_amount').default
        is_max_digits = obj._meta.get_field('t_single_amount').max_digits
        is_dec_places = obj._meta.get_field('t_single_amount').decimal_places
        self.assertEqual(field_label, "Сумма")
        self.assertEqual(help_text, "Сумма (однотарифный)")
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
        obj_name = f'{obj.land_plot.plot_number} {str(obj.record_date)}' 
        self.assertEqual(obj_name, obj.__str__())
        # or self.assertEquals(object_name, str(lp_obj))
    
    def test_get_absolute_url(self):
        obj = ElectricityPayments.objects.get(id=1)
        self.assertEquals(
            obj.get_absolute_url(),
            '/payments/electricity-payments/plot-1/payment-1')

    def test_verbose_names(self):
        self.assertEquals(
            ElectricityPayments._meta.verbose_name,
            'электроэнергия'
        )
        self.assertEquals(
            ElectricityPayments._meta.verbose_name_plural,
            'электроэнергия'
        )

    # Test model class methods
    def test_count_n_records(self):
        """Check count_n_record() method."""
        all_obj = ElectricityPayments.objects.filter(id=1)
        count = all_obj[0].count_n_records(all_obj)
        self.assertEquals(count, 1)

    def test_count_p_records(self):
        """Check count_p_record() method."""
        ElectricityPayments.objects.filter(id=1).update(record_status='p')
        all_obj = ElectricityPayments.objects.filter(id=1)
        count = all_obj[0].count_p_records(all_obj)
        self.assertEquals(count, 1)

    def test_count_c_records(self):
        """Check count_c_record() method."""
        ElectricityPayments.objects.filter(id=1).update(record_status='c')
        all_obj = ElectricityPayments.objects.filter(id=1)
        count = all_obj[0].count_c_records(all_obj)
        self.assertEquals(count, 1)

    def test_table_state(self):
        """Check table_state() method."""
        # Check 'n' state
        payment = ElectricityPayments.objects.get(id=1)
        result = payment.table_state()
        self.assertEquals(result, "n")
        # Check 'p' state
        ElectricityPayments.objects.filter(id=1).update(record_status='p')
        payment = ElectricityPayments.objects.get(id=1)
        result = payment.table_state()
        self.assertEquals(result, "p")
        # Check 'c' state (one 'c' record)
        ElectricityPayments.objects.filter(id=1).update(record_status='c')
        payment = ElectricityPayments.objects.get(id=1)
        result = payment.table_state()
        self.assertEquals(result, "c")
        # Check 'nc' state (one 'n' and one 'c' record)
        ElectricityPayments.objects.create(
            land_plot=LandPlot.objects.get(id=1),
            t_single_new=0,
            )
        payment = ElectricityPayments.objects.get(id=1)
        result = payment.table_state()
        self.assertEquals(result, "nc")
        # Check 'pc' state (one 'p' and one 'c' record)
        ElectricityPayments.objects.filter(id=3).update(record_status='p')
        payment = ElectricityPayments.objects.get(id=1)
        result = payment.table_state()
        self.assertEquals(result, "pc")
        # Check 'c'+ state (two 'c' records)
        ElectricityPayments.objects.filter(id=3).update(record_status='c')
        payment = ElectricityPayments.objects.get(id=1)
        result = payment.table_state()
        self.assertEquals(result, "c")
        # Check 'nc+' state (two 'c' and one 'n' record)
        ElectricityPayments.objects.create(
            land_plot=LandPlot.objects.get(id=1),
            t_single_new=5,
            )
        result = payment.table_state()
        self.assertEquals(result, "nc")
        # Check 'pc+' state (two 'c' and one 'p' record)
        ElectricityPayments.objects.filter(id=4).update(record_status='p')
        result = payment.table_state()
        self.assertEquals(result, "pc")

    def test_get_p_record(self):
        """Check get_p_record() method."""
        # p-record does not exist
        payment = ElectricityPayments.objects.get(id=1)
        result = payment.get_p_record()
        self.assertEquals(result, False)
        # p-record exists
        ElectricityPayments.objects.filter(id=1).update(record_status='p')
        payment = ElectricityPayments.objects.get(id=1)
        result = payment.get_p_record()
        self.assertEquals(result, payment)
        
    def test_get_c_record(self):
        """Check get_p_record() method."""
        # c-record does not exist
        payment = ElectricityPayments.objects.get(id=1)
        result = payment.get_c_record()
        self.assertEquals(result, False)
        # c-record exists
        ElectricityPayments.objects.filter(id=1).update(record_status='c')
        payment = ElectricityPayments.objects.get(id=1)
        result = payment.get_c_record()
        self.assertEquals(result, payment)
        # 2 c-records exist
        ElectricityPayments.objects.create(
            land_plot=LandPlot.objects.get(id=1),
            t_single_new=5,
            )
        ElectricityPayments.objects.filter(id=3).update(record_status='c')
        payment = ElectricityPayments.objects.get(id=3)
        result = payment.get_c_record()
        self.assertEquals(result, payment)
 
    def test_get_current_rate(self):
        """Check get_current_rate() method."""
        # 2 records in db. One has 'c' rate status
        Rate.objects.create(
            t1_rate = 10,
            t2_rate = 15,
            t_single_rate = 12,
            rate_status = None,
            )
        payment = ElectricityPayments.objects.get(id=1)
        rate = Rate.objects.get(id=1)
        result = payment.get_current_rate()
        self.assertEquals(result, rate)
        # 2 records in db. No one has 'c' rate status
        Rate.objects.filter(id=1).update(rate_status=None)
        result = payment.get_current_rate()
        self.assertEquals(result, False)

    def test_get_electrical_counter(self):
        """Check get_electrical_counter() method."""
        # Electrical counter exists
        payment = ElectricityPayments.objects.get(id=1)
        el_counter = ElectricalCounter.objects.get(id=1)
        result = payment.get_electrical_counter()
        self.assertEquals(result, el_counter)
        # Electrical counter does not exist
        ElectricalCounter.objects.filter(id=1).delete()
        payment = ElectricityPayments.objects.get(id=1)
        result = payment.get_electrical_counter()
        self.assertEquals(result, None)
