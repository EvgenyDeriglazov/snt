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
