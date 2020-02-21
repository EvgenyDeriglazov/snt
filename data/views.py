from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from data.models import Snt, LandPlot, ElectricityPayments, Rate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from data.forms import T1NewElectricityPaymentForm, T2NewElectricityPaymentForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import datetime

# Create your views here.
def homepage(request):
    """View function for home page of site"""
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
    current_user = request.user
    land_plot_query_set = current_user.landplot_set.all() 
    if len(land_plot_query_set) == 0:
        error_message = "У вас еще нет ни одного участка."
        context = {
            'error_message': error_message,
            }
        return render(request, 'error_page.html', context=context)
    else:
        snt_name = land_plot_query_set[0].snt
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
        payment_details.plot_number.user == current_user:
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
    elif payment_details.plot_number.user != current_user:
        error_message = "Выбранные показания относятся к другому участку."
        context = {
            'error_message': error_message,
            }
        return render(request, 'error_page.html', context=context)


@login_required
def user_payment_details_view(request, plot_num, pk):
    """View function to display detailed information about
    electricity payment record."""
    current_user = request.user
    # Get ElectricityPayments object from db
    try:
        payment_details = ElectricityPayments.objects.get(id=pk)
    except ElectricityPayments.DoesNotExist:
        error_message = "Запись запрашиваемых показаний отсутствует."
        context = {
            'error_message': error_message,
            }
        return render(request, 'error_page.html', context=context)
    # Get Rate object from db which corresponds to payment_details.date    
    try:
        rate = Rate.objects.filter(
            intro_date__lte=payment_details.record_date,
            ).latest('intro_date')
    except Rate.DoesNotExist:
        error_message = "Запись тарифа для данных показаний отсутствует."
        context = {
            'error_message': error_message,
            }
        return render(request, 'error_page.html', context=context)
    # Get plot instance from db
    try:
        plot = LandPlot.objects.get(id=plot_num)
    except LandPlot.DoesNotExist:
        error_message = "Участка с номером {} нет в базе данных.".format(plot_num)
        context = {
            'error_message': error_message,
            }
        return render(request, 'error_page.html', context=context)
    # Get content from get_qr_code() function
    context, do_render = get_qr_code(current_user, plot_num, payment_details, rate)
    # Check it requested data belongs to current user and land plot
    if payment_details.plot_number.user == current_user and \
        context['payment_details'].plot_number.user == current_user and \
        payment_details.plot_number == plot:
        # If no internal mistake in get_qr_code() - render page
        if do_render == True:
            return render(request, 'payment_details.html', context=context)
        # If there is a mistake in get_qr_code() - render error page
        elif do_render == False:
            return render(request, 'error_page.html', context=context)
    else:
        error_message = "Запрашиваемые показания не относятся к вашему участку."
        context = {
            'error_message': error_message,
            }
        return render(request, 'error_page.html', context=context)

@login_required
def user_new_payment_view(request, plot_num):
    """View function to display form for new electricity payment
    record."""
    current_user = request.user
    # Get requested land plot instance form db or return error page
    try:
        land_plot = LandPlot.objects.get(plot_number=plot_num)
    except LandPlot.DoesNotExist:
        error_message = "Участка с номером {} нет в базе данных.".format(plot_num)
        context = {
            'error_message': error_message,
            }
        return render(request, 'error_page.html', context=context)
    # Get electrical counter model type and model type description
    el_counter_type = land_plot.electrical_counter.model_type
    el_counter_type_disp = land_plot.electrical_counter.get_model_type_display()
    # If user tries to POST data
    if request.method == 'POST' and land_plot.user == current_user:
        # Instantiate form for T1 electric counter type with user data
        if el_counter_type == 'T1':
            form = T1NewElectricityPaymentForm(request.POST)
            # Validate T1 form data and try to save to db 
            if form.is_valid():
                t1_new_cleaned = form.cleaned_data['t1_new']
                try:
                    new_record = ElectricityPayments.objects.create(
                        plot_number=land_plot,
                        t1_new=t1_new_cleaned,
                        )
                    # Calculate payment for new record
                    new_record.calculate_payment()
                except ValidationError as validation_error:
                    # ValidationError from save() method
                    # Prepare error message and context
                    error_message_list = validation_error.message.split("\n")
                    context = {
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
                        plot_number=land_plot,
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
        if el_counter_type == 'T1' and land_plot.user == current_user:
            form = T1NewElectricityPaymentForm()
        elif el_counter_type == 'T2' and land_plot.user == current_user:
            form = T2NewElectricityPaymentForm()
        # If counter type is not correct render error page
        elif el_counter_type != 'T1' and el_counter_type != 'T2':
            error_message = "Неверный тип счетчика."
            context = {
                'error_message': error_message,
                }
            return render(request, 'error_page.html', context=context)
        # If land plot does not belong to current user render error page
        elif land_plot.user != current_user:
            error_message = "У вас нет участка с номером {}.".format(plot_num)
            context = {
                'error_message': error_message,
                }
            return render(request, 'error_page.html', context=context)        

    # Context for empty form
    context = {
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
    user_plot_electricity_paymnents_view."""
    current_user = request.user
    land_plot_query_set = current_user.landplot_set.all() 
    # If user has only 1 land plot,redirect to user_plot_electricity_payments_view
    if len(land_plot_query_set) == 1:
        plot_number = land_plot_query_set[0].plot_number
        return HttpResponseRedirect(
            reverse('plot-electricity-payments', args=[plot_number])
            )
    # If user has more than one land plot
    elif len(land_plot_query_set) > 1:
        context = {
            'snt_name': land_plot_query_set[0].snt,
            'land_plot_query_set': land_plot_query_set,
            }
        return render(request, 'electricity_payments.html', context=context)

@login_required
def user_plot_electricity_payments_view(request, plot_num):
    """View function to display electricity payments for certain
    plot only."""
    # Get current user from request and all his land plots
    current_user = request.user
    land_plot_query_set = current_user.landplot_set.all()
    # Check if current user has any land plots
    if len(land_plot_query_set) == 0:
        error_message = "У вас еще нет ни одного участка."
        context = {
            'error_message': error_message,
            }
        return render(request, 'error_page.html', context=context)
    # Get requested plot instance
    land_plot = land_plot_query_set.filter(plot_number__exact=plot_num).get()
    # Get payments list or raise an error
    try:
        payments_list = ElectricityPayments.objects.filter(
            plot_number__exact=land_plot
            ).order_by('-record_date')
    except ElectricityPayments.DoesNotExist:
        error_message = "У вас еще нет ни одного показания."
        context = {
            'error_message': error_message,
            }
        return render(request, 'error_page.html', context=context)
    # Check if payments_list belongs to current user, otherwise raise error 
    if len(payments_list) > 0:
        if payments_list[0].plot_number.user == current_user:
            snt_name = payments_list[0].plot_number.snt
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
        snt_name = land_plot_query_set.filter(
            plot_number__exact=plot_num).get()
        context = {
            'snt_name': snt_name.snt,
            'plot_number': plot_num,
            'no_records': 'У вас еще нет показаний счетчика.',
            }
        
    return render(request, 'electricity_payments.html', context=context)

def get_qr_code(current_user, plot_num, payment_details, rate):
    """Function to prepare qr code and return result to view
    for rendering web page (context{}, correct(bolean))."""
    qr_text = "ST00012|Name=Садоводческое некоммерческое товаричество{}|\
        PersonalAcc={}|BankName={}|BIC={}|CorrespAcc={}|INN={}|LastName={}|\
        FirstName={}|MiddleName={}|Purpose={}|PayerAddress={}|Sum={}"
    snt_name = payment_details.plot_number.snt
    # Check if requested payment record belonges to current user
    if payment_details.plot_number.user == current_user:
        name = payment_details.plot_number.snt
        p_acc = payment_details.plot_number.snt.personal_acc
        b_name = payment_details.plot_number.snt.bank_name
        bic = payment_details.plot_number.snt.bic
        cor_acc = payment_details.plot_number.snt.corresp_acc
        inn = payment_details.plot_number.snt.inn
        last_name = payment_details.plot_number.owner.last_name
        first_name = payment_details.plot_number.owner.first_name
        middle_name = payment_details.plot_number.owner.middle_name
        e_counter_type = payment_details.plot_number.electrical_counter.model_type
        if e_counter_type == 'T1':
            t1_new = payment_details.t1_new
            t1_prev = payment_details.t1_prev
            t1_cons = payment_details.t1_cons
            t1_rate = rate.t1_rate
            t1_amount = payment_details.t1_amount
            sum_tot = payment_details.sum_tot
            purpose = "Членские взносы за э/энергию, однотарифный/{}-{}/{},\
                {}x{}/{}.Итого/{}." 
            purpose = purpose.format(
                t1_new, t1_prev, t1_cons, t1_cons,
                t1_rate, t1_amount, sum_tot,
                )
        elif e_counter_type == 'T2':
            t1_new = payment_details.t1_new
            t2_new = payment_details.t2_new
            t1_prev = payment_details.t1_prev
            t2_prev = payment_details.t2_prev
            t1_cons = payment_details.t1_cons
            t2_cons = payment_details.t2_cons
            t1_rate = rate.t1_rate
            t2_rate = rate.t2_rate
            t1_amount = payment_details.t1_amount
            t2_amount = payment_details.t2_amount
            sum_tot = payment_details.sum_tot
            purpose = "Членские взносы за э/энергию, T1/{}-{}/{},\
                T2/{}-{}/{}, T1/{}x{}/{}, T2/{}x{}/{}.Итого/{}." 
            purpose = purpose.format(
                t1_new, t1_prev, t1_cons,
                t2_new, t2_prev, t2_cons,
                t1_cons, t1_rate, t1_amount,
                t2_cons, t2_rate, t2_amount,
                sum_tot,
                )
        payer_address = "участок №{}, СНТ{}".format(plot_num, name)   
        sum_tot = payment_details.sum_tot
        qr_text = qr_text.format(
            name, p_acc, b_name, bic, cor_acc,inn, last_name, first_name,
            middle_name, purpose, payer_address, sum_tot,
            )
        context = {
            'snt_name': snt_name,
            'payment_details': payment_details,
            'qr_text': qr_text,
            }
        do_render = True
    else:
        error_message = "Запрашиваемые показания не относятся к вашему участку."
        context = {
            'error_message': error_message,
            }
        do_render = False
    return context, do_render

