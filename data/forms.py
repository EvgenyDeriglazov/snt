from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class UpdateElectricityPaymentForm(forms.Form):
    """Form to update electricity payment details used for records with
    record_status='n'."""
    pass

class NewElectricityPaymentForm(forms.Form):
    """Form to create new ElectricityPayment record in db."""
    t1_new = forms.IntegerField(
    	label="Текущее покзание (день)",
    	help_text="Тариф Т1 (6:00-23:00)",
    	)
    def clean_t1_new(self):
    	data = self.cleaned_data['t1_new']
    	return data
