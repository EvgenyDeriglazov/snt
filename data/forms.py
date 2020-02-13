from django import forms
from data.models import LandPlot
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class UpdateElectricityPaymentForm(forms.Form):
    """Form to update electricity payment details used for records with
    record_status='n'."""
    pass

class T1NewElectricityPaymentForm(forms.Form):
    """Form to create new ElectricityPayment record in db
    for T2 type of electricity meter (day and night rates)."""
    t1_new = forms.IntegerField(
    	label="Новое показание",
    	help_text="",
        min_value=0,
    	)
    def clean_t1_new(self):
    	data = self.cleaned_data['t1_new']
    	return data

class T2NewElectricityPaymentForm(forms.Form):
    """Form to create new ElectricityPayment record in db
    for T2 type of electricity meter (day and night rates)."""
    t1_new = forms.IntegerField(
    	label="Новое показание (день)",
    	help_text="Тариф Т1 (6:00-23:00)",
        min_value=0,
    	)
    t2_new = forms.IntegerField(
    	label="Новое показание (ночь)",
    	help_text="Тариф Т2 (23:00-6:00)",
        min_value=0
    	)
    def clean_t1_new(self):
    	data = self.cleaned_data['t1_new']
    	return data

    def clean_t2_new(self):
    	data = self.cleaned_data['t2_new']
    	return data

