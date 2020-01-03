from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Data validators
def validate_account(value):
    valid_symbols = list(range(0, 11))
    if value not in valid_symbols:
        raise ValidationError(
            _('%(value)s is not a number'),
        )

# Create your models here.
class Snt(models.Model):
    """Model representing a SNT with basic information such as
    SNT name, chairman, payment details, address."""
    name = models.CharField(
        "Название СНТ",
        max_length=200,
        help_text="Введите полное название вашего СНТ",
    )
    personal_acc = models.CharField(
        max_length=20,
        validators=[validate_account],
        help_text="Введите номер расчетного счета",
    )
    bank_name = models.CharField(max_length=45)
    bic = models.CharField(max_length=9)
    corresp_acc = models.CharField(max_length=20)
    payee_inn = models.CharField(max_length=10)
    kpp = models.CharField(max_length=9)

    class Meta:
        verbose_name_plural = "СНТ"

    def __str__(self):
        """String for representing the Model object."""
        return self.name
    def get_absolute_url(self):
        """Returns the url to access a detail record for this snt."""
        return reverse('snt-detail', args=[str(self.id)])
 

class LandPlot(models.Model):
    """Model representing a land plot with basic information
    such as plot number (pk), area, owners (many-to-many), 
    snt (fk), electric meter (one-to-one)."""
    pass

class ChairMan(models.Model):
    """Model representing a chairman of snt with basic information
    such as first name, last name, status (current or former)
    hire date, retire date, snt (one-to-one)."""
    pass

class Owner(models.Model):
    """Model representing an owner of land plot with basic infromation
    such as first name, last name, status (current or former), 
    land plot (many-to-many), start owner date, end owner date."""
    pass

class ElectricMeter(models.Model):
    """Model representing an electric meter with basic information
    such as serial number, type (1T/2T), land plot (one-to-one)."""
    pass

class ElectricMeterReadings(models.Model):
    """Model representing electic meter readings to keep records and
    calculate payment for each land plot."""
    pass

class Tarrifs(models.Model):
    """Model representing different snt tarrifs to calculate 
    payments."""
    pass
