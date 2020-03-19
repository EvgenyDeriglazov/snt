from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
#from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
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
        "Название СНТ",
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
    snt (fk), electrical counter (one-to-one), user."""
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
    electrical_counter = models.OneToOneField(
        'ElectricalCounter',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Счетчик',
        help_text="Данные прибора учета электроэнергии",
        )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Логин",
        help_text="Аккаунт пользователя на сайте",
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
    last_name = models.CharField(
        "Фамилия",
        max_length=50,
        help_text="Введите фамилию",
        validators = [validate_human_names],
    )
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

class ElectricalCounter(models.Model):
    """Model representing an electric counter with basic information
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
    intro_date = models.DateField(
        verbose_name="дата установки/приемки",
    )
    t1 = models.PositiveIntegerField(
        "Показание при установке/приемке (день)",
        help_text="Тариф Т1 (6:00-23:00)",
        null=True,
        blank=True,
        default=None,
    )
    t2 = models.PositiveIntegerField(
        "Показание при установке/приемке (ночь)",
        help_text="Тариф Т2 (23:00-6:00)",
        null=True,
        blank=True,
        default=None,
    )
    t_single = models.PositiveIntegerField(
        "Показание при установке/приемке",
        help_text="Однотарифный",
        null=True,
        blank=True,
        default=None,
    )

    # Model functions
    def check_t1_model_type(self):
        """
        Function checks t_single field is not empty.
        Returns "pass" or error_message.
        """
        if self.t_single == None:
            error_message = "Необходимо указать данные для поля - \
                {}".format(self._meta.get_field('t_single').help_text)
            return error_message
        else:
            return "pass"
        
    def check_t2_model_type(self):
        """
        Function checks t1 and t2 fields are not empty.
        Returns "pass" or error_message.
        """
        if self.t1 == None or self.t2 == None:
            error_message = "Необходимо указать данные для полей: \
               \n {} \n {}".format(
                    self._meta.get_field('t1').help_text,
                    self._meta.get_field('t2').help_text
                    )
            return error_message
        else:
            return "pass"

    def save(self, *args, **kwargs):
        """
        Custom save function which checks model data before saving it
        to data base. It checks t1, t2, t_single fields conformity with
        model_type field choice. If model_type is 'T1', t_single should
        be provided with data, t1 and t2 should be empty. If model_type
        is 'T2', t1 and t2 should be provided with data, t_single 
        should be empty. If unconformity found raises ValidationError.
        """
        if self.model_type == 'T1':
            result = self.check_t1_model_type()
            self.t1 = None
            self.t2 = None
        elif self.model_type == 'T2':
            result = self.check_t2_model_type()
            self.t_single = None

        if result == "pass":
            super().save(*args, **kwargs)
        else:
            raise ValidationError(_(result))
 
    class Meta:
        verbose_name = "прибор учета электроэнергии"
        verbose_name_plural = "приборы учета электроэнергии"

    def __str__(self):
        """String for representing the Model object."""
        return self.model

    def get_absolute_url(self):
        """Returns the url to access a detail record for this chairman."""
        return reverse('electric-counter-detail', args=[str(self.id)])

class ElectricityPayments(models.Model):
    """Model represents electricity payment details."""
    land_plot = models.ForeignKey(
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
    counter_number = models.CharField(
        "Номер счетчика",
        max_length=50,
        help_text="Серийный номер прибора учета электроэнергии",
        null=True,
        blank=True,
        default=None,
    )
    t1_new = models.PositiveIntegerField(
        "Текущее показание (день)",
        help_text="Тариф Т1 (6:00-23:00)",
        null=True,
        blank=True,
        default=None,
    )
    t2_new = models.PositiveIntegerField(
        "Текущее показание (ночь)",
        help_text="Тариф Т2 (23:00-6:00)",
        null=True,
        blank=True,
        default=None,
    )
    t_single_new = models.PositiveIntegerField(
        "Текущее показание",
        help_text="Однотарифный",
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
    t_single_prev = models.PositiveIntegerField(
        "Предыдущее показание",
        help_text="Однотарифный",
        null=True,
        blank=True,
        default=None,
    )
    t1_cons = models.PositiveIntegerField(
        "Потрачено квт/ч (день)",
        help_text="Тариф Т1 (6:00-23:00)",
        null=True,
        blank=True,
        default=None,
    )
    t2_cons = models.PositiveIntegerField(
        "Потрачено квт/ч (ночь)",
        help_text="Тариф Т2 (23:00-6:00)",
        null=True,
        blank=True,
        default=None,
    )
    t_single_cons = models.PositiveIntegerField(
        "Потрачено квт/ч",
        help_text="Однотарифный",
        null=True,
        blank=True,
        default=None,
    )
    RECORD_STATUS = [
        ('n', 'Новые показания'),
        ('p', 'Оплачено'),
        ('c', 'Оплата подтверждена'),
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
    t_single_amount = models.DecimalField(
        "Сумма",
        help_text="Сумма (однотарифный)",
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
        verbose_name = "электроэнергия"
        verbose_name_plural = "электроэнергия"
        #unique_together = ['record_date', 'land_plot']

    def __str__(self):
        """String for representing the Model object."""
        return self.land_plot.plot_number + ' ' + str(self.record_date)

    def get_absolute_url(self):
        """Returns the url to access a detail record for this model data."""
        return reverse('payment-details', kwargs={
            'plot_num': self.land_plot,
            'pk': self.id,
            })

    # Model business logic functions
    def count_n_records(self, all_obj):
        """
        Takes ElectricalPayments query set as positional argument and
        returns number of n-records in it.
        """
        result = 0
        i = 0
        for i in range(len(all_obj)):
            if all_obj[i].record_status == 'n':
                result += 1
        return result

    def count_p_records(self, all_obj):
        """
        Takes ElectricalPayments query set as positional argument and
        returns number of p-records in it.
        """
        result = 0
        i = 0
        for i in range(len(all_obj)):
            if all_obj[i].record_status == 'p':
                result += 1
        return result

    def count_c_records(self, all_obj):
        """
        Takes ElectricalPayments query set as positional argument and
        returns number of c-records in it.
        """
        result = 0
        i = 0
        for i in range(len(all_obj)):
            if all_obj[i].record_status == 'c':
                result += 1
        return result

    def table_state(self):
        """
        Checks table state of specific land plot and returns result.
        'n' - one n record. 'p' - one p record.
        'c' - one or many c records. 'nc' - one n record and one or
        many c records. 'pc' - one p record and one or many c records.
        """ 
        all_obj = ElectricityPayments.objects.filter(land_plot__exact=self.land_plot)
        n_rec = self.count_n_records(all_obj)
        p_rec = self.count_p_records(all_obj)
        c_rec = self.count_c_records(all_obj)
        if n_rec == 1 and len(all_obj) == 1:
            return "n"
        elif p_rec == 1 and len(all_obj) == 1:
            return "p"
        elif c_rec >= 1 and len(all_obj) == c_rec:
            return "c"
        elif n_rec == 1 and c_rec >= 1 and len(all_obj) == (n_rec + c_rec):
            return "nc"
        elif p_rec == 1 and c_rec >= 1 and len(all_obj) == (p_rec + c_rec):
            return "pc"

    def get_p_record(self):
        """
        Returns latest record from db with record_status='p'
         for self.land_plot.
        """
        try:
            p_record_obj = ElectricityPayments.objects.get(
                Q(land_plot__exact=self.land_plot),
                Q(record_date__lte=date.today()),
                Q(record_status__exact='p'),
                )
        except:
            return False
            #error_message = "Невозможно найти ни одной оплаченной записи."
            #raise ValidationError(_(error_message))
        return p_record_obj

    def get_c_record(self):
        """
        Returns latest record from database with record_status='c'
        for self.land_plot.
        """
        try:
            c_record_obj = ElectricityPayments.objects.filter(
                land_plot__exact=self.land_plot,
                record_status__exact='c',
                ).latest('record_date')
        except:
            return False
            #error_message = "Невозможно найти ни одной записи с подтвержденной оплатой."
            #raise ValidationError(_(error_message))
        return c_record_obj

    def get_electrical_counter(self):
        """Returns actual electrical counter record from database."""
        try:
            land_plot_obj = LandPlot.objects.get(
                plot_number__exact=self.land_plot
                )
        except:
            return False
            #error_message = "Невозможно найти участок."
            #raise ValidationError(_(error_message))
        electrical_counter_obj = land_plot_obj.electrical_counter
        return electrical_counter_obj

    def get_current_rate(self):
        """Returns record from database with Rate.rate_status='c'."""
        try:
            current_rate_obj = Rate.objects.get(rate_status__exact='c')
        except:
            return False
        return current_rate_obj

    def state_c_t1_new_fill_calc(self, c_record, el_counter, rate):
        """
        Fills t1 type record and calculates payment. 
        Takes 3 positional arguments: previous electrical
        payment object, electrical counter object and rate object.
        """
        if self.t_single_new > c_record.t_single_new:
            self.t_single_prev = c_record.t_single_new 
            self.t_single_cons = self.t_single_new - self.t_single_prev
            self.t_single_amount = self.t_single_cons * rate.t_single_rate
            self.sum_tot = self.t_single_amount
            self.counter_number = el_counter.serial_number
            self.t1_prev = None
            self.t2_prev = None
            self.t1_cons = None
            self.t2_cons = None
            return True
        elif self.t_single_new <= self.c_record.t_single_new: 
            return False
    
    def empty_t1_new_fill_calc(self, el_counter, rate):
        """
        Fills t1 type record and calculates payment. 
        Takes 2 positional arguments: electrical counter
        object and rate object.
        """
        if self.t_single_new > el_counter.t_single:
            self.t_single_prev = el_counter.t_single 
            self.t_single_cons = self.t_single_new - self.t_single_prev
            self.t_single_amount = self.t_single_cons * rate.t_single_rate
            self.sum_tot = self.t_single_amount
            self.counter_number = el_counter.serial_number
            self.t1_prev = None
            self.t2_prev = None
            self.t1_cons = None
            self.t2_cons = None
            return True
        elif self.t_single_new <= el_counter.t_single: 
            return False
    
    def state_c_t2_new_fill_calc(self, c_record, el_counter, rate):
        """
        Fills t2 type record and calculates payment. 
        Takes 3 positional arguments: previous electrical
        payment object, electrical counter object and rate object.
        """
        if self.t1_new > c_record.t1_new and self.t2_new > self.c_record.t2_new:
            self.t1_prev = c_record.t1_new 
            self.t1_cons = self.t1_new - self.t1_prev
            self.t1_amount = self.t1_cons * rate.t1_rate
            self.t2_prev = c_record.t2_new 
            self.t2_cons = self.t2_new - self.t2_prev
            self.t2_amount = self.t2_cons * rate.t2_rate           
            self.sum_tot = self.t1_amount + self.t2_amount
            self.counter_number = el_counter.serial_number
            self.t_single_prev = None
            self.t_single_cons = None
            return True
        elif self.t1_new <= self.c_record.t1_new or \
            self.t2_new <= self.c_record.t2_new: 
            return False
            
    def empty_t2_new_fill_calc(self, el_counter, rate):
        """
        Fills t1 type record and calculates payment. 
        Takes 2 positional arguments: electrical counter
        object and rate object.
        """
        if self.t1_new > el_counter.t1 and self.t2_new > el_counter.t1:
            self.t1_prev = el_counter.t1 
            self.t1_cons = self.t1_new - self.t1_prev
            self.t1_amount = self.t1_cons * rate.t1_rate
            self.t2_prev = el_counter.t2 
            self.t2_cons = self.t2_new - self.t2_prev
            self.t2_amount = self.t2_cons * rate.t2_rate
            self.sum_tot = self.t1_amount + self.t2_amount
            self.counter_number = el_counter.serial_number
            self.t_single_prev = None
            self.t_single_cons = None
            return True
        elif self.t1_new <= el_counter.t1 or self.t2_new <= el_counter.t2: 
            return False
 
    def calc_new_record(self):
        """Fills record with relevant data from previous payment
        details (previous electrical counter readings)."""
        state = self.table_state()
        el_counter = self.get_electrical_counter()
        if state == "c" and el_counter.model_type == 'T1':
            c_record = self.get_c_record()
            result = self.state_c_t1_new_fill_calc(c_record, el_counter, rate)
            
        elif state == "empty" and el_counter.model_type == 'T1':
            result = self.empty_t1_new_fill_calc(el_counter, rate)

        elif state == "c" and el_counter.model_type == 'T2':
            c_record = self.get_c_record()
            result = self.state_c_t2_new_fill_calc(c_record, el_counter, rate)

        elif state == "empty" and el_counter.model_type == 'T2':
            result = self.empty_t2_new_fill_calc(el_counter, rate)

        return result

    def fill_n_record(self):
        """Fills record_type='n' (new record) row (columns t1_prev, t2_prev)
        with data from record_type='c' (prev record) row or
        record_type='i' (columns t1_new, t2_new)."""
        # Validate that record's status is 'n'
        if self.record_status != 'n':
            return False # Raise Error Here
        # Query all 'n' and 'p' records
        n_records = ElectricityPayments.objects.filter(
            land_plot__exact=self.land_plot,
            record_status__exact='n'
            )
        p_records = ElectricityPayments.objects.filter(
            land_plot__exact=self.land_plot,
            record_status__exact='p'
            )
        # Check if 'n' and 'p' records exist
        if len(n_records) > 1:
            return False # Raise Error Here
        elif len(p_records) > 0:
            return False # Raise Error Here
        # Query data objects
        em_model_type = self.land_plot.electrical_counter.model_type
        c_record = self.get_c_record()
        i_record = self.get_i_record()
        # Conditional for T1 and T2 types filling
        # T1 c_record
        if c_record and em_model_type == 'T1':
            # New record data have to be bigger than previous
            if self.t1_new > c_record.t1_new:
                self.t1_prev = c_record.t1_new
                self.t2_prev = None
                self.t2_new = None # Remove data in case of user input mistake
                return True
            else:
                return False
        # T2 c_record
        elif c_record and em_model_type == 'T2':
            # New record data have to be bigger than previous
            if self.t1_new > c_record.t1_new and self.t2_new > c_record.t2_new:
                self.t1_prev = c_record.t1_new
                self.t2_prev = c_record.t2_new
                return True
            else:
                return False
        # T1 i_record
        elif i_record and em_model_type == 'T1':
            # New record data have to be bigger than previous
            if self.t1_new > i_record.t1_new:
                self.t1_prev = i_record.t1_new
                self.t2_prev = None
                self.t2_new = None # Remove data in case of user input mistake
                return True
            else:
                return False
        # T2 i_record
        elif i_record and em_model_type == 'T2':
            # New record data have to be bigger than previous
            if self.t1_new > i_record.t1_new and self.t2_new > i_record.t2_new:
                self.t1_prev = i_record.t1_new
                self.t2_prev = i_record.t2_new
                return True
            else:
                return False

    # Basic operation functions for model instances (database entities)
    def calculate_payment(self):
        """Calculates consumption of electricity and sum for payment.
        Fills relevant data in record_type='n' t1_cons, t2_cons, t1_amount
        t2_amount and sum_tot. electrical_counter.model_type is taken into
        account during all calculations and db row pupulating."""
        fill_n_record = self.fill_n_record()
        current_rate_obj = self.get_current_rate()
        em_model_type = self.land_plot.electrical_counter.model_type
        if em_model_type == 'T1' and fill_n_record and current_rate_obj:
            # Calculate consumption, amount (T1 rate) and 'sum_tot'
            self.t1_cons = self.t1_new - self.t1_prev
            self.t2_cons = None
            self.t1_amount = self.t1_cons * current_rate_obj.t1_rate
            self.t2_amount = None
            self.sum_tot = self.t1_amount
            self.save(modify=True)
        elif em_model_type == 'T2' and fill_n_record and current_rate_obj:
            # Calculate consumption, amount (T1 & T2 rates) and 'sum_tot'
            self.t1_cons = self.t1_new - self.t1_prev
            self.t2_cons = self.t2_new - self.t2_prev
            self.t1_amount = self.t1_cons * current_rate_obj.t1_rate
            self.t2_amount = self.t2_cons * current_rate_obj.t2_rate
            self.sum_tot = self.t1_amount + self.t2_amount
            self.save(modify=True)
        elif not fill_n_record:
            self.set_initial()
        else:
            return False # raise an error

    def set_paid(self):
        """Change the status of the row (db entity) from new to paid via bank
        (record_status = 'n' change to record_status = 'p')"""
        if self.record_status != 'n':
            return False
        elif self.sum_tot != None:
            if self.sum_tot > 0:
                self.record_status = 'p'
                self.pay_date = date.today()
                self.save()
            else:
                return False
        else:
            return False

    def set_payment_confirmed(self):
        """Change the status of the row (db entity) from 'paid via bank' to
        'payment confirmed' (record_status = 'p' to record_status = 'c')."""
        if self.record_status != 'p':
            return False
        elif self.sum_tot != None:
            if self.sum_tot > 0:
                self.record_status = 'c'
                self.save()
            else:
                return False
        else:
            return False

    def check_t1_t2_or_validation_error(self, all_obj):
        """Function takes query set of all ElectricityPayments
        objects which belong to specific land plot as positional
        argument. t1_new and t2_new fields of new record should be
        bigger than t1_new and t2_new fields of latest record with
        record_status = 'c' in db."""
        latest_c_record = all_obj.filter(
            record_status__exact='c'
            ).latest('record_date')
        el_counter_type = self.land_plot.electrical_counter.model_type
        if el_counter_type == 'T1':
            if self.t1_new <= latest_c_record.t1_new:
                error = "Новые показания не должны быть равны\
                    или меньше предыдущих."
                error += "\nПоследние данные: Т1 {}.".format(
                    latest_c_record.t1_new
                    )
                raise ValidationError(_(error))
        elif el_counter_type == 'T2':
            if self.t1_new <= latest_c_record.t1_new or \
                self.t2_new <= latest_c_record.t2_new:
                error = "Новые показания не должны быть равны\
                    или меньше предыдущих."
                error += "\nПоследние данные: Т1 {}, Т2 {}.".format(
                    latest_c_record.t1_new,
                    latest_c_record.t2_new,
                    )
                raise ValidationError(_(error)) 


    def save(self, *args, **kwargs):
        all_obj = ElectricityPayments.objects.filter(
            land_plot__exact=self.land_plot,
            )
        n_records = all_obj.filter(record_status__exact='n')
        p_records = all_obj.filter(record_status__exact='p')
        modify = kwargs.pop('modify', False)
        #self.check_t1_t2_or_validation_error(all_obj)
        # Check if user try to add n-record while n or p records exist in db
        if self.record_status == 'n' and not modify and\
            (len(n_records) > 0 or len(p_records) > 0):
            # Create error message
            error = "Невозможно сохранить новые показания."
            # Error 1
            if len(n_records) > 0:
                error += "\nУ вас уже есть запись с новыми показаниями."
            # Error 2
            if len(p_records) > 0:
                error += "\nУ вас уже есть оплаченный взнос ожидающий \
                            подтверждения оплаты."
            # Raise validation error
            raise ValidationError(_(error))
        else:
            super().save(*args, **kwargs)
        

class Rate(models.Model):
    """Model representing snt rates to calculate 
    payments."""
    intro_date = models.DateField(
        verbose_name="Дата",
        help_text="Дата введения/изменения тарифа",
        auto_now_add=True,
    )
    t1_rate = models.DecimalField(
        verbose_name="Тариф день",
        help_text="Тариф Т1 (6:00-23:00)",
        max_digits=4,
        decimal_places=2,
    )
    t2_rate = models.DecimalField(
        verbose_name="Тариф ночь",
        help_text="Тариф Т2 (23:00-6:00)",
        max_digits=4,
        decimal_places=2,
    )
    t_single_rate = models.DecimalField(
        verbose_name="Однотарифный",
        help_text="Однотарифный",
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
