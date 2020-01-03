from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Data validators
def validate_account_number(value):
    """Makes account number validation."""
    char_set = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    wrong_char_list = []
    for char in value:
        if char not in char_set and char not in wrong_char_list:
            wrong_char_list.append(char)
    if len(value) < 20:
        raise ValidationError(
            _('Неверный номер счета (меньше 20-и знаков).')
        )
    elif wrong_char_list:
        wrong_string = ", ".join(wrong_char_list) 
        raise ValidationError(
            _('Некорректный символ в номере счета - (' + wrong_string + ')'),
            params={'value': value},
        )

# Create your models here.
class Snt(models.Model):
    """Model representing a SNT with basic information such as
    SNT name, chairman, payment details, address."""
    name = models.CharField(
        "Наименование СНТ",
        max_length=200,
        help_text="Введите полное название вашего СНТ",
    )
    personal_acc = models.CharField(
        "Номер расчетного счета",
        max_length=20,
        help_text="Введите номер расчетного счета (20-и значное число)",
        validators=[validate_account_number],
    )
    bank_name = models.CharField(
        "Наименование банка получателя",
        max_length=45,
        help_text="Введите наименование банка получателя",
    )
    bic = models.CharField(
        "БИК",
        max_length=9,
        help_text="Введите БИК",
    )
    corresp_acc = models.CharField(
        "Номер кор./счета",
        max_length=20,
        help_text="Введите номер кор./счета",
    )
    inn = models.CharField(
        "ИНН",
        max_length=10,
        help_text="Введите номер ИНН",
    )
    kpp = models.CharField(
        "КПП",
        max_length=9,
        help_text="Введите номер КПП",
    )

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
