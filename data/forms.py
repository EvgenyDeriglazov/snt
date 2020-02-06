from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class UpdateElectricityPaymentForm(forms.Form):
    """Form to update electricity payment details used for records with
    record_status='n'."""
    pass

class NewElectricityPaymentForm(forms.Form):
    """Form to populate new record for electricity payment."""
    pass
