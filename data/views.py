from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from data.models import Snt, LandPlot, ElectricityPayments, Rate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from data.forms import T1NewElectricityPaymentForm, T2NewElectricityPaymentForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError, PermissionDenied
import datetime

# Create your views here.
def homepage(request):
    """View function to display site home page"""
    num_snt = Snt.objects.all().count
    num_land_plots = LandPlot.objects.all().count
    num_users = User.objects.filter(groups__name__exact='Users').count()
    
    context = {
        'num_snt': num_snt,
        'num_land_plots': num_land_plots,
        'num_users': num_users,
    }
    
    return render(request, 'index.html', context=context)

@login_required
def user_payments_view(request):
    """View function to display links for each payment type."""
    snt = Snt.objects.get(id=1)
    snt_name = snt.name
    context = {
        'snt_name': snt_name,
        }
    return render(request, 'user_payments.html', context=context)

@login_required
def user_payment_edit_view(request, pk):
    """View function to display specific payment details. Payments
    with record_status='n' (new) can be edited by the authenticated
    user. Other paymnets with record_status='p', 'c', 'i' are not
    allowed to be edited (only view mode)."""
    current_user = request.user
    #payment_edit = get_object_or_404(ElectricityPayments, pk=pk)
    try:
        payment_edit = ElectricityPayments.objects.get(id=pk)
    except ElectricityPayments.DoesNotExist:
        error_message = "Запись запрашиваемых показаний отсутствует."
        context = {
            'error_message': error_message,
            }
        return render(request, 'error_page.html', context=context)
    if payment_edit.record_status == 'n' and \
        payment_details.land_plot.user == current_user:
        context = {
            'payment_edit': payment_edit,
            }
        return render(request, 'payment_edit.html', context=context)
    elif payment_edit.record_status != 'n':
        payment_status = payment_edit.get_record_status_display
        error_message = "Отредактировать можно только новые показания. \
            Текущая запись имеет статус {}.".format(payment_status)
        context = {
            'error_message': error_message,
            }
        return render(request, 'error_page.html', context=context)
    elif payment_details.land_plot.user != current_user:
        error_message = "Выбранные показания относятся к другому участку."
        context = {
            'error_message': error_message,
            }
        return render(request, 'error_page.html', context=context)


@login_required
def user_payment_details_view(request, plot_num, pk):
    """View function to display detailed information about
    electricity payment record."""
    el_payment_obj = get_electricity_payment_object_or_404(pk, plot_num)
    check_user_or_404(request, el_payment_obj)
    rate_obj = get_rate_object_or_404_by_sub_func(el_payment_obj)
    if el_payment_obj.record_status == 'n':
        el_payment_obj.calculate_payment()
    context = electricity_payment_qr_code(plot_num, el_payment_obj, rate_obj)
    return render(request, 'payment_details.html', context=context)

@login_required
def user_new_payment_view(request, plot_num):
    """View function to display form for new electricity payment
    record."""
    # Get requested land plot instance form db or return error page
    try:
        land_plot = LandPlot.objects.get(plot_number=plot_num)
    except LandPlot.DoesNotExist:
        error_message = "Участка с номером {} нет в базе данных.".format(plot_num)
        context = {
            'error_message': error_message,
            }
        return render(request, 'error_page.html', context=context)
    snt_name = land_plot.snt.name
    # Get electrical counter model type and model type description
    el_counter_type = land_plot.electrical_counter.model_type
    el_counter_type_disp = land_plot.electrical_counter.get_model_type_display()
    # If user tries to POST data
    if request.method == 'POST' and land_plot.user == request.user:
        # Instantiate form for T1 electric counter type with user data
        if el_counter_type == 'T1':
            form = T1NewElectricityPaymentForm(request.POST)
            # Validate T1 form data and try to save to db 
            if form.is_valid():
                t1_new_cleaned = form.cleaned_data['t1_new']
                try:
                    new_record = ElectricityPayments.objects.create(
                        land_plot=land_plot,
                        t1_new=t1_new_cleaned,
                        )
                    # Calculate payment for new record
                    new_record.calculate_payment()
                except ValidationError as validation_error:
                    # ValidationError from save() method
                    # Prepare error message and context
                    error_message_list = validation_error.message.split("\n")
                    context = {
                        'snt_name': snt_name,
                        'plot_number': plot_num,
                        'form': form,
                        'error_message_list': error_message_list,
                        'el_counter_type_disp': el_counter_type_disp,
                        }
                    # Render form with error message
                    return render(request, 'new_payment.html', context=context)
                # Redirect to plot electricity payments list page
                return HttpResponseRedirect(
                    reverse('plot-electricity-payments', args=[plot_num])
                    ) 

        # Instantiate form for T2 electric counter type with user data
        else: 
            form = T2NewElectricityPaymentForm(request.POST) 
            # Validate T2 form data and try to save to db
            if form.is_valid():
                t1_new_cleaned = form.cleaned_data['t1_new']
                t2_new_cleaned = form.cleaned_data['t2_new']
                try:
                    new_record = ElectricityPayments.objects.create(
                        land_plot=land_plot,
                        t1_new=t1_new_cleaned,
                        t2_new=t2_new_cleaned,
                        )
                    # Calculate payment for new record
                    new_record.calculate_payment()
                except ValidationError as validation_error:
                    # ValidationError from save() method
                    # Prepare error message and context
                    error_message_list = validation_error.message.split("\n")
                    context = {
                        'snt_name': snt_name,
                        'plot_number': plot_num,
                        'form': form,
                        'error_message_list': error_message_list,
                        'el_counter_type_disp': el_counter_type_disp,
                        }
                    # Render form with error message
                    return render(request, 'new_payment.html', context=context)
                # Redirect to plot electricity payments list page
                return HttpResponseRedirect(
                    reverse('plot-electricity-payments', args=[plot_num])
                    )
    else:
        # Instantiate empty form for certain electric counter type
        if el_counter_type == 'T1' and land_plot.user == request.user:
            form = T1NewElectricityPaymentForm()
        elif el_counter_type == 'T2' and land_plot.user == request.user:
            form = T2NewElectricityPaymentForm()
        # If counter type is not correct render error page
        elif el_counter_type != 'T1' and el_counter_type != 'T2':
            error_message = "Неверный тип счетчика."
            context = {
                'error_message': error_message,
                }
            return render(request, 'error_page.html', context=context)
        # If land plot does not belong to current user render error page
        elif land_plot.user != request.user:
            error_message = "У вас нет участка с номером {}.".format(plot_num)
            context = {
                'error_message': error_message,
                }
            return render(request, 'error_page.html', context=context)        

    # Context for empty form
    context = {
        'snt_name': snt_name,
        'plot_number': plot_num,
        'form': form,
        'el_counter_type_disp': el_counter_type_disp,
        }
    # Render empty form
    return render(request, 'new_payment.html', context=context)

@login_required
def user_electricity_payments_view(request):
    """View function to display list of links 
    to certain land plot electricity payment page or
    if a user has only one land plot it will redicrect to
    user_plot_electricity_payments_view."""
    user_land_plots = LandPlot.objects.filter(user__exact=request.user)
    # If user has only 1 land plot,redirect to user_plot_electricity_payments_view
    if len(user_land_plots) == 1:
        plot_number = user_land_plots[0].plot_number
        return HttpResponseRedirect(
            reverse('plot-electricity-payments', args=[plot_number])
            )
    # If user has more than one land plot
    elif len(user_land_plots) > 1:
        context = {
            'snt_name': user_land_plots[0].snt,
            'user_land_plots': user_land_plots,
            }
        return render(request, 'electricity_payments.html', context=context)
    else:
        error_message = "У вас еще нет ни одного участка."
        context = {
            'error_message': error_message,
            }
        return render(request, 'error_page.html', context=context)

@login_required
def user_plot_electricity_payments_view(request, plot_num):
    """View function to display electricity payments for certain
    plot only."""
    # Get current user from request and all his land plots
    user_land_plots = LandPlot.objects.filter(user__exact=request.user)
    # Check if current user has any land plots
    if len(user_land_plots) == 0:
        error_message = "У вас еще нет ни одного участка."
        context = {
            'error_message': error_message,
            }
        return render(request, 'error_page.html', context=context)
    # Get requested plot instance
    try:
        land_plot = user_land_plots.get(plot_number=plot_num)
    except LandPlot.DoesNotExist:
        error_message = "У вас нет участка с таким номером."
        context = {
            'error_message': error_message,
            }
        return render(request, 'error_page.html', context=context)
    # Get payments list or raise an error
    try:
        payments_list = ElectricityPayments.objects.filter(
            land_plot__exact=land_plot
            ).order_by('-record_date')
    except ElectricityPayments.DoesNotExist:
        error_message = "У вас еще нет ни одного показания."
        context = {
            'error_message': error_message,
            }
        return render(request, 'error_page.html', context=context)
    # Check if payments_list belongs to current user, otherwise raise error 
    if len(payments_list) > 0:
        if payments_list[0].land_plot.user == request.user:
            snt_name = payments_list[0].land_plot.snt
            context = {
                'snt_name': snt_name,
                'plot_number': plot_num,
                'payments_list': payments_list,
                }
        else:
            error_message = "Запрашиваемые показания не относятся к вашему участку."
            context = {
                'error_message': error_message,
                }
            return render(context, 'error_page.html', context=context)
    else:
        snt_name = land_plot.snt
        context = {
            'snt_name': snt_name,
            'plot_number': plot_num,
            'no_records': 'У вас еще нет показаний счетчика.',
            }
        
    return render(request, 'electricity_payments.html', context=context)

# Reusable functions
def electricity_payment_qr_code(plot_num, el_payment_obj, rate_obj):
    """Function to prepare qr code and return result to view
    for rendering web page (context{}, correct(bolean))."""
    qr_text = "ST00012|Name=Садоводческое некоммерческое товаричество{}|\
        PersonalAcc={}|BankName={}|BIC={}|CorrespAcc={}|INN={}|LastName={}|\
        FirstName={}|MiddleName={}|Purpose={}|PayerAddress={}|Sum={}"
    snt_name = el_payment_obj.land_plot.snt
    name = el_payment_obj.land_plot.snt
    p_acc = el_payment_obj.land_plot.snt.personal_acc
    b_name = el_payment_obj.land_plot.snt.bank_name
    bic = el_payment_obj.land_plot.snt.bic
    cor_acc = el_payment_obj.land_plot.snt.corresp_acc
    inn = el_payment_obj.land_plot.snt.inn
    last_name = el_payment_obj.land_plot.owner.last_name
    first_name = el_payment_obj.land_plot.owner.first_name
    middle_name = el_payment_obj.land_plot.owner.middle_name
    e_counter_type = el_payment_obj.land_plot.electrical_counter.model_type
    if e_counter_type == 'T1':
        t1_new = el_payment_obj.t1_new
        t1_prev = el_payment_obj.t1_prev
        t1_cons = el_payment_obj.t1_cons
        t1_rate = rate_obj.t1_rate
        t1_amount = el_payment_obj.t1_amount
        sum_tot = el_payment_obj.sum_tot
        purpose = "Членские взносы за э/энергию, однотарифный/{}-{}/{},\
            {}x{}/{}. Итого/{}." 
        purpose = purpose.format(
            t1_new, t1_prev, t1_cons, t1_cons,
            t1_rate, t1_amount, sum_tot,
            )
    elif e_counter_type == 'T2':
        t1_new = el_payment_obj.t1_new
        t2_new = el_payment_obj.t2_new
        t1_prev = el_payment_obj.t1_prev
        t2_prev = el_payment_obj.t2_prev
        t1_cons = el_payment_obj.t1_cons
        t2_cons = el_payment_obj.t2_cons
        t1_rate = rate_obj.t1_rate
        t2_rate = rate_obj.t2_rate
        t1_amount = el_payment_obj.t1_amount
        t2_amount = el_payment_obj.t2_amount
        sum_tot = el_payment_obj.sum_tot
        purpose = "Членские взносы за э/энергию, T1/{}-{}/{},\
            T2/{}-{}/{}, T1/{}x{}/{}, T2/{}x{}/{}. Итого/{}." 
        purpose = purpose.format(
            t1_new, t1_prev, t1_cons, t2_new, t2_prev, t2_cons, t1_cons,
            t1_rate, t1_amount, t2_cons, t2_rate, t2_amount, sum_tot,
            )
        payer_address = "участок №{}, СНТ {}".format(plot_num, name)   
        sum_tot = el_payment_obj.sum_tot * 100
        qr_text = qr_text.format(
            name, p_acc, b_name, bic, cor_acc,inn, last_name, first_name,
            middle_name, purpose, payer_address, sum_tot,
            )
        context = {
            'snt_name': snt_name,
            'el_payment_obj': el_payment_obj,
            'qr_text': qr_text,
            'payer_address': payer_address,
            'purpose': purpose,
            'last_name': last_name,
            'first_name': first_name,
            'middle_name': middle_name,
            }
    return context

def get_electricity_payment_object_or_404(pk, plot_num):
    """Function takes ElectricityPayments primary key and plot number as
    positional arguments and makes db query to get ElectricityPayments
    object by primary key filtered by plot number. It returns
    ElectricityPayment object or if object DoesNotExist raises Http404."""  
    try:
        el_payment_obj = ElectricityPayments.objects.filter(
            land_plot__plot_number__exact=plot_num
            ).get(id=pk)
    except ElectricityPayments.DoesNotExist:
        raise Http404("get_electricity_payment_object_or_404():\
        exception ElectricityPayments.DoesNotExist")
    return el_payment_obj

def get_rate_object_or_404_by_sub_func(el_payment_obj):
    """Function takes ElectricityPayments object as positional argument.
    If ElectricityPayments.record_status == 'n' it calls
    get_rate_object_by_record_date_or_404(), in all other cases
    it calls get_rate_object_by_pay_date_or_404(). Function returns
    Rate object or Http404 is raised by above mentioned functions
    when object DoesNotExist."""
    if el_payment_obj.record_status == 'n':
        rate_obj = get_rate_object_by_record_date_or_404(el_payment_obj)
    else:
        rate_obj = get_rate_object_by_pay_date_or_404(el_payment_obj)
    return rate_obj

def get_rate_object_by_record_date_or_404(el_payment_obj):
    """Function takes ElectricityPayment object as positional argument
    and makes db query to get latest Rate object by intro_date where
    intro_date is later or equal to ElectricityPayments.record_date."""
    try:
        rate_obj = Rate.objects.filter(
            intro_date__lte=el_payment_obj.record_date,
            rate_status__exact='c',
            ).latest('intro_date')
    except Rate.DoesNotExist:
        raise Http404("get_rate_object_by_record_date_or_404():\
        exception Rate.DoesNotExist")
    return rate_obj

def get_rate_object_by_pay_date_or_404(el_payment_obj):
    """Function takes ElectricityPayment object as positional argument
    and makes db query to get latest Rate object by intro_date where
    intro_date is later or equal to ElectricityPayments.pay_date."""
    try:
        rate_obj = Rate.objects.filter(
            intro_date__lte=el_payment_obj.pay_date,
            ).latest('intro_date')
    except Rate.DoesNotExist:
        raise Http404("get_rate_object_by_pay_date_or_404():\
        exception Rate.DoesNotExist")
    return rate_obj
 
def check_user_or_404(request, el_payment_obj):
    """Function checks if ElectricityPayments object belongs
    to request.user and returns Http404 when request.user tries
    to access other user data. """
    if el_payment_obj.land_plot.user != request.user:
        raise Http404("check_user_or_404():\
        el_payment_obj does not belong to request.user") 
