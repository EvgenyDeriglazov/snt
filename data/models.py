from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Data validators
def validate_number(value):
    """Makes number validation (use only numbers)."""
    wrong_char_list = []
    for char in value:
        if ord(char) > 57 or ord(char) < 48:
            wrong_char_list.append(char)
    if wrong_char_list:
        wrong_string = ", ".join(wrong_char_list)
        raise ValidationError(
            _('Некорректный символ в номере счета - (' + wrong_string + ')')
        )

def validate_20_length(value):
    """Makes 20 length number validation."""
    if len(value) < 20:
        raise ValidationError(
            _('Неверный номер (меньше 20-и знаков)')
        )

def validate_10_length(value):
    """Makes 10 length number validation."""
    if len(value) < 10:
        raise ValidationError(
            _('Неверный номер (меньше 10-и знаков)')
        )

def validate_9_length(value):
    """Makes 9 length numbers validation."""
    if len(value) < 9:
        raise ValidationError(
            _('Неверный номер (меньше 9-и знаков)')
        )

def validate_human_names(value):
    """Makes name validation (use only Russian letters)."""
    for char in value:
        if ord(char) < 1040 or ord(char) > 1103:
            raise ValidationError(
                _('Можно использовать только русские символы')
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
        validators=[validate_number, validate_20_length],
    )
    bank_name = models.CharField(
        "Наименование банка получателя",
        max_length=45,
        help_text="Введите наименование банка получателя",
    )
    bic = models.CharField(
        "БИК",
        max_length=9,
        help_text="Введите БИК (9-и значное число)",
        validators=[validate_number, validate_9_length],
    )
    corresp_acc = models.CharField(
        "Номер кор./счета",
        max_length=20,
        help_text="Введите номер кор./счета (20-и значное число)",
        validators=[validate_number, validate_20_length],
    )
    inn = models.CharField(
        "ИНН",
        max_length=10,
        help_text="Введите ИНН (10-и значное число)",
        validators=[validate_number, validate_10_length],
    )
    kpp = models.CharField(
        "КПП",
        max_length=9,
        help_text="Введите КПП (9-и значное число)",
        validators=[validate_number, validate_9_length],
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
    first_name = models.CharField(
        "Имя",
        max_length=200,
        help_text="Введите имя",
        validators = [validate_human_names],
    )
    middle_name = models.CharField(
        "Отчество",
        max_length=200,
        help_text="Введите отчество",
        validators = [validate_human_names],
    )
    last_name = models.CharField(
        "Фамилия",
        max_length=200,
        help_text="Введите фамилию",
        validators = [validate_human_names],
    )

    class Meta:
        verbose_name = "председатель"
        verbose_name_plural = "председатели"

    def __str__(self):
        """String for representing the Model object."""
        return self.last_name + ' ' + self.first_name + ' ' + self.middle_name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this chairman."""
        return reverse('chairman-detail', args=[str(self.id)])

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
