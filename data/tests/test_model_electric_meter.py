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
