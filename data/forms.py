from django import forms
from data.models import LandPlot
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class UpdateElectricityPaymentForm(forms.Form):
    """Form to update electricity payment details used for records with
    record_status='n'."""
    pass

class NewElectricityPaymentForm(forms.Form):
    """Form to create new ElectricityPayment record in db."""
    t1_new = forms.IntegerField(
    	label="Текущее показание (день)",
    	help_text="Тариф Т1 (6:00-23:00)",
        min_value=0,
    	)
    t2_new = forms.IntegerField(
    	label="Текущее показание (ночь)",
    	help_text="Тариф Т2 (23:00-6:00)",
        min_value=0
    	)
    def clean_t1_new(self):
    	data = self.cleaned_data['t1_new']
    	return data

    def clean_t2_new(self):
    	data = self.cleaned_data['t2_new']
    	return data

