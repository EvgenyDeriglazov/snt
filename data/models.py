from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from datetime import date
from django.db.models import Q
from django.urls import reverse

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
            _('Некорректный символ - (' + wrong_string + ')')
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
    plot_area = models.PositiveIntegerField(
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

class ElectricityPayments(models.Model):
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
        null=True,
        blank=True,
        default=None,
    )
    t1_prev = models.PositiveIntegerField(
        "Предыдущее показание (день)",
        help_text="Тариф Т1 (6:00-23:00)",
        null=True,
        blank=True,
        default=None,
    )
    t2_prev = models.PositiveIntegerField(
        "Предыдущее показание (ночь)",
        help_text="Тариф Т2 (23:00-6:00)",
        null=True,
        blank=True,
        default=None,
    )
    t1_cons = models.PositiveIntegerField(
        "Потрачено квт/ч (день)",
        null=True,
        blank=True,
        default=None,
    )
    t2_cons = models.PositiveIntegerField(
        "Потрачено квт/ч (ночь)",
        null=True,
        blank=True,
        default=None,
    )

    RECORD_STATUS = [
        ('n', 'Новые показания'),
        ('p', 'Оплачено'),
        ('c', 'Оплата подтверждена'),
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
        blank=True,
        null=True,
    )
    t1_amount = models.DecimalField(
        "Сумма (день)",
        help_text="Сумма по тарифу Т1",
        null=True,
        blank=True,
        default=None,
        max_digits=7,
        decimal_places=2,
    )
    t2_amount = models.DecimalField(
        "Сумма (ночь)",
        help_text="Сумма по тарифу Т2",
        null=True,
        blank=True,
        default=None,
        max_digits=7,
        decimal_places=2,
    )
    sum_tot = models.DecimalField(
        "Итог",
        help_text="Общая сумма к оплате",
        null=True,
        blank=True,
        default=None,
        max_digits=7,
        decimal_places=2,
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
        return reverse('electricity-payments-detail', args=[str(self.id)])

    # Re-use functions for model instance basic operation functions
    def get_n_record(self):
        """Returns row from database with record_status='n',
        new record for particular (self.plot_number)."""
        try:
            n_record_obj = ElectricityPayments.objects.get(
                Q(plot_number__exact=self.plot_number),
                Q(record_date__lte=date.today()),
                Q(record_status__exact='n'),
            )
        except:
            return False
        return n_record_obj

    def get_p_record(self):
        """Returns row from database with record_status='p'
        (payed via bank) for self.plot_number."""
        try:
            p_record_obj = ElectricityPayments.objects.get(
                Q(plot_number__exact=self.plot_number),
                Q(record_date__lt=date.today()),
                Q(record_status__exact='p'),
            )
        except:
            return False
        return p_record_obj

    def get_c_record(self):
        """Returns row from database with record_status='c'
        (last confirmed payment) for self.plot_number."""
        try:
            c_record_obj = ElectricityPayments.objects.get(
                Q(plot_number__exact=self.plot_number),
                Q(record_date__lt=date.today()),
                Q(record_status__exact='c'),
            )
        except:
            return False
        return c_record_obj

    def get_current_rate(self):
        """Returns row from database (Rate model) with Rate.rate_status='c'
        (current rate for electricity T1 and T2 payment calculation)."""
        try:
            current_rate_obj = Rate.objects.filter(rate_status__exact='c').latest('intro_date')
        except:
            return False
        return current_rate_obj

    def fill_n_record(self):
        """Fills record_type='n' (new record) row (columns t1_prev, t2_prev)
        with data from record_type='c' (prev record) row
        (columns t1_new, t2_new)."""
        em_model_type = self.plot_number.electric_meter.model_type
        c_record = self.get_c_record()
        if c_record:
            if em_model_type == 'T1':
                self.t1_prev = c_record.t1_new
                self.t2_prev = None
                self.t2_new = None # Remove data in case of user input mistake
                return True
            else:
                self.t1_prev = c_record.t1_new
                self.t2_prev = c_record.t2_new
                return True
        else:
            return False

    # Basic operation functions for model instances (database entities)
    def calculate_payment(self):
        """Calculates consumption of electricity and sum for payment.
        Fills relevant data in record_type='n' t1_cons, t2_cons, t1_amount
        t2_amount and sum_tot. electric_meter.model_type is taken into
        account during all calculations and db row pupulating."""
        fill_n_record = self.fill_n_record()
        current_rate_obj = self.get_current_rate()
        em_model_type = self.plot_number.electric_meter.model_type
        if em_model_type == 'T1' and fill_n_record and current_rate_obj:
            # Calculate consumption, amount (T1 rate) and 'sum_tot'
            self.t1_cons = self.t1_new - self.t1_prev
            self.t2_cons = None
            self.t1_amount = self.t1_cons * current_rate_obj.t1_rate
            self.t2_amount = None
            self.sum_tot = self.t1_amount
            self.save()
        elif em_model_type == 'T2' and fill_n_record and current_rate_obj:
            # Calculate consumption, amount (T1 & T2 rates) and 'sum_tot'
            self.t1_cons = self.t1_new - self.t1_prev
            self.t2_cons = self.t2_new - self.t2_prev
            self.t1_amount = self.t1_cons * current_rate_obj.t1_rate
            self.t2_amount = self.t2_cons * current_rate_obj.t2_rate
            self.sum_tot = self.t1_amount + self.t2_amount
            self.save()

    def set_paid(self):
        """Change the status of the row (db entity) from new to paid via bank
        (record_status = 'n' change to record_status = 'p')"""
        new_p_record = self.get_n_record()
        if new_p_record and new_p_record.sum_tot != None:
            new_p_record.record_status = 'p'
            new_p_record.pay_date = date.today()
            new_p_record.save()

    def set_payment_confirmed(self):
        """Change the status of the row (db entity) from 'paid via bank' to
        'payment confirmed' (record_status = 'p' to record_status = 'c'),
        and previous 'payment confirmed' to 'old payment' (record_status = 'c'
        to record_status = 'o')."""
        current_c_record = self.get_c_record()
        new_c_record = self.get_p_record()
        if current_c_record and new_c_record:
            current_c_record.record_status = 'o'
            new_c_record.record_status = 'c'
            current_c_record.save()
            new_c_record.save()
        elif not current_c_record and new_c_record:
            new_c_record.record_status = 'c'
            new_c_record.save()

class Rate(models.Model):
    """Model representing snt rates to calculate 
    payments."""
    intro_date = models.DateField(
        verbose_name="Дата",
        help_text="Дата введения/изменения тарифа",
        auto_now_add=True,
    )
    t1_rate = models.DecimalField(
        verbose_name="Электроэнергия день",
        help_text="Тариф Т1 (6:00-23:00)",
        max_digits=4,
        decimal_places=2,
    )
    t2_rate = models.DecimalField(
        verbose_name="Электроэнергия ночь",
        help_text="Тариф Т2 (23:00-6:00)",
        max_digits=4,
        decimal_places=2,
    )

    RATE_STATUS = [
        ('c', 'Действующий'),

    ]

    rate_status = models.CharField(
        "Вид тарифа",
        max_length=1,
        choices=RATE_STATUS,
        default='c',
        help_text="",
        unique=True,
        null=True,
        blank=True,
        unique_for_date="intro_date",
    )

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"
        unique_together = ['intro_date', 'rate_status']

    def __str__(self):
        """String for representing the Model object."""
        return str(self.intro_date)

    def get_absolute_url(self):
        """Returns the url to access a detail record for this chairman."""
        return reverse('rates-detail', args=[str(self.id)])
