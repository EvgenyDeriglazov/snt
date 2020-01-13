from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

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
        help_text="Полное название СНТ",
    )
    personal_acc = models.CharField(
        "Номер расчетного счета",
        max_length=20,
        help_text="Номер расчетного счета (20-и значное число)",
        validators=[validate_number, validate_20_length],
    )
    bank_name = models.CharField(
        "Наименование банка получателя",
        max_length=45,
        help_text="Наименование банка получателя",
    )
    bic = models.CharField(
        "БИК",
        max_length=9,
        help_text="БИК (9-и значное число)",
        validators=[validate_number, validate_9_length],
    )
    corresp_acc = models.CharField(
        "Номер кор./счета",
        max_length=20,
        help_text="Номер кор./счета (20-и значное число)",
        validators=[validate_number, validate_20_length],
    )
    inn = models.CharField(
        "ИНН",
        max_length=10,
        help_text="ИНН (10-и значное число)",
        validators=[validate_number, validate_10_length],
    )
    kpp = models.CharField(
        "КПП",
        max_length=9,
        help_text="КПП (9-и значное число)",
        validators=[validate_number, validate_9_length],
    )
    chair_man = models.OneToOneField(
        'ChairMan',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='председатель',
        help_text="Председатель садоводства",
    )


    class Meta:
        verbose_name = "СНТ"
        verbose_name_plural = "СНТ"

    def __str__(self):
        """String for representing the Model object."""
        return self.name 
    
    def get_absolute_url(self): 
        """Returns the url to access a detail record for this snt.""" 
        return reverse('snt-detail', args=[str(self.id)])
 

class LandPlot(models.Model):
    """Model representing a land plot with basic information
    such as plot number (unique), area, owners (many-to-many), 
    snt (fk), electric meter (one-to-one)."""
    plot_number = models.CharField(
        "Номер участка",
        max_length=10,
        help_text="Номер участка",
        unique=True,
    )
    plot_area = models.FloatField(
        "Размер участка",
        help_text="Единица измерения кв.м",
    )
    snt = models.ForeignKey(
       Snt,
       on_delete=models.SET_NULL,
       null=True,
       verbose_name="СНТ",
       help_text="Расположен в СНТ",
    ) 
    owner = models.ForeignKey(
        'Owner',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="владелец участка",
        help_text="Владелец участка",
    )   
    electric_meter = models.OneToOneField(
        'ElectricMeter',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Счетчик',
        help_text="Данные прибора учета электроэнергии",
    )

    class Meta:
        verbose_name = "участок"
        verbose_name_plural = "участки"


    def __str__(self):
        """String for representing the Model object."""
        return self.plot_number

    def get_absolute_url(self):
        """Returns the url to access a detail record for land plot."""
        return reverse('land-plot-detail', args=[str(self.id)])

class ChairMan(models.Model):
    """Model representing a chairman of snt with basic information
    such as first name, last name, status (current or former)
    hire date, retire date, snt (one-to-one)."""
    first_name = models.CharField(
        "Имя",
        max_length=50,
        help_text="Введите имя",
        validators = [validate_human_names],
    )
    middle_name = models.CharField(
        "Отчество",
        max_length=50,
        help_text="Введите отчество",
        validators = [validate_human_names],
    )
    last_name = models.CharField(
        "Фамилия",
        max_length=50,
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
    first_name = models.CharField(
        "Имя",
        max_length=50,
        help_text="Введите имя",
        validators = [validate_human_names],
    )
    middle_name = models.CharField(
        "Отчество",
        max_length=50,
        help_text="Введите отчество",
        validators = [validate_human_names],
    )
    last_name = models.CharField(
        "Фамилия",
        max_length=50,
        help_text="Введите фамилию",
        validators = [validate_human_names],
    )

    OWNER_STATUS = [
        ('c', 'Настоящий'),
        ('p', 'Прежний'),
    ]

    status = models.CharField(
        "Статус владельца",
        max_length=1,
        choices=OWNER_STATUS,
        default='c',
        help_text="Статус владельца",
    )
    
    start_owner_date = models.DateField(
        verbose_name="дата начала владения",
    )
    end_owner_date = models.DateField(
        verbose_name="дата окончания владения",
        blank=True,
        null=True,
    )
    
    class Meta:
        verbose_name = "владелец"
        verbose_name_plural = "владельцы"

    def __str__(self):
        """String for representing the Model object."""
        return self.last_name + ' ' + self.first_name + ' ' + self.middle_name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this chairman."""
        return reverse('owner-detail', args=[str(self.id)])


class ElectricMeter(models.Model):
    """Model representing an electric meter with basic information
    such as serial number, type (1T/2T), land plot (one-to-one)."""
    model = models.CharField(
        "Модель",
        max_length=50,
        help_text="Модель прибора учета электроэнергии",
    )
    serial_number = models.CharField(
        "Серийный номер",
        max_length=50,
        help_text="Серийный номер прибора учета электроэнергии",
    )

    MODEL_TYPE = [
        ('T1', 'Однотарифный'),
        ('T2', 'Двухтарифный'),
    ]

    model_type = models.CharField(
        "Тип",
        max_length=2,
        choices=MODEL_TYPE,
        default='T1',
        help_text="Тип прибора учета",
    )
    acceptance_date = models.DateField(
        verbose_name="дата установки",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "прибор учета электроэнергии"
        verbose_name_plural = "приборы учета электроэнергии"

    def __str__(self):
        """String for representing the Model object."""
        return self.model

    def get_absolute_url(self):
        """Returns the url to access a detail record for this chairman."""
        return reverse('electric-meter-detail', args=[str(self.id)])
class ElectricMeterReadings(models.Model):
    """Model representing electic meter readings to keep records and
    calculate payment for each land plot."""
    plot_number = models.ForeignKey(
        LandPlot,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Номер участка",
        help_text="Номер участка",
        unique_for_date="record_date",
    )
    record_date = models.DateField(
        auto_now_add=True,
        verbose_name="Дата",
        help_text="Дата снятия показаний счетчика",
    )
    t1_new = models.PositiveIntegerField(
        "Текущее показание (день)",
        help_text="Тариф T1 (6:00-23:00)",
    )
    t2_new = models.PositiveIntegerField(
        "Текущее показание (ночь)",
        help_text="Тариф Т2 (23:00-6:00)",
    )
    t1_prev = models.PositiveIntegerField(
        "Предыдущее показание (день)",
        help_text="Тариф Т1 (6:00-23:00)",
    )
    t2_prev = models.PositiveIntegerField(
        "Предыдущее показание (ночь)",
        help_text="Тариф Т2 (23:00-6:00)",
    )
    t1_cons = models.PositiveIntegerField(
        "Потрачено квт/ч (день)",
    )
    t2_cons = models.PositiveIntegerField(
        "Потрачено квт/ч (ночь)",
    )

    
    RECORD_STATUS = [
        ('n', 'Новые показания'),
        ('p', 'Оплачено через банк'),
        ('c', 'Последняя оплата'),
        ('o', 'Оплачено ранее'),
    ] 

    record_status = models.CharField(
        "Статус",
        max_length=1,
        choices=RECORD_STATUS,
        default='n',
        help_text="Статус показаний",
    )
    pay_date = models.DateField(
        verbose_name = "Дата оплаты",
    )
    t1_amount = models.FloatField(
        "Сумма (день)",
        help_text="Сумма по тарифу Т1",
    )
    t2_amount = models.FloatField(
        "Сумма (ночь)",
        help_text="Сумма по тарифу Т2",
    )
    sum_tot = models.FloatField(
        "Итог",
        help_text="Общая сумма к оплате",
    )


    class Meta:
        verbose_name = "данные показаний счетчика"
        verbose_name_plural = "показания счетчика"
        unique_together = ['record_date', 'plot_number']

    def __str__(self):
        """String for representing the Model object."""
        return self.plot_number.plot_number + ' ' + str(self.record_date)


    def get_absolute_url(self):
        """Returns the url to access a detail record for this chairman."""
        return reverse('electric-meter-reading-detail', args=[str(self.id)])




class Rate(models.Model):
    """Model representing snt rates to calculate 
    payments."""
    intro_date = models.DateField(
        verbose_name="Дата",
        help_text="Дата введения/изменения тарифа",
    )
    t1_rate = models.FloatField(
        verbose_name="Электроэнергия день",
        help_text="Тариф Т1 (6:00-23:00)",
    )
    t2_rate = models.FloatField(
        verbose_name="Электроэнергия ночь",
        help_text="Тариф Т2 (23:00-6:00)",
    )

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"
        unique_together = ['intro_date', 't1_rate', 't2_rate']

    def __str__(self):
        """String for representing the Model object."""
        return self.intro_date

    def get_absolute_url(self):
        """Returns the url to access a detail record for this chairman."""
        return reverse('rates-detail', args=[str(self.id)])
