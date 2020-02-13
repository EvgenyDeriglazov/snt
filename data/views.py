from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from data.models import Snt, LandPlot, ElectricityPayments
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
        raise Http404(_("Такой записи не существует."))
    if payment_edit.record_status == 'n' and \
        payment_details.plot_number.user == current_user:
        context = {
            'payment_edit': payment_edit,
            }
    else:
        context = {
            'payment_details': 'Данные отсутствуют.',
            }

    return render(request, 'payment_edit.html', context=context)

@login_required
def user_payment_details_view(request, plot_num, pk):
    """View function to display detailed information about
    electricity payment record."""
    current_user = request.user
    #payment_details = get_object_or_404(ElectricityPayments, pk=pk)
    try:
        payment_details = ElectricityPayments.objects.get(id=pk)
    except ElectricityPayments.DoesNotExist:
        raise Http404(_("Такой записи не существует."))

    # Check if requested payment record belonges to current user
    if payment_details.plot_number.user == current_user:
        context = {
            'payment_details': payment_details,
            }
    else:
        context = {
            'payment_details': 'Данные отсутствуют.',
            }

    return render(request, 'payment_details.html', context=context)
    pass

@login_required
def user_new_payment_view(request, plot_num):
    """View function to display form for new electricity payment
    record."""
    current_user = request.user
    land_plot = LandPlot.objects.get(id=plot_num)
    electric_meter_type = land_plot.electric_meter.model_type
    electric_meter_type_disp = land_plot.electric_meter.get_model_type_display()
    if request.method == 'POST' and land_plot.user == current_user:
        # Instantiate form for T1 electric meter type with user data
        if electric_meter_type == 'T1':
            form = T1NewElectricityPaymentForm(request.POST)
            # Validate T1 form data 
            if form.is_valid():
                t1_new_cleaned = form.cleaned_data['t1_new']
                try:
                    new_record = ElectricityPayments.objects.create(
                        plot_number=land_plot,
                        t1_new=t1_new_cleaned,
                        )
                    new_record.calculate_payment()
                except ValidationError as validation_error:
                    error_message_list = validation_error.message.split("\n")
                    context = {
                        'plot_number': plot_num,
                        'form': form,
                        'error_message_list': error_message_list,
                        'electric_meter_type': electic_meter_type_disp,
                        }
                    return render(request, 'new_payment.html', context=context)
                return HttpResponseRedirect(
                    reverse('plot-electricity-payments', args=plot_num)
                    ) 

        # Instantiate form for T2 electric meter type with user data
        else: 
            form = T2NewElectricityPaymentForm(request.POST) 
            # Validate T2 form data
            if form.is_valid():
                t1_new_cleaned = form.cleaned_data['t1_new']
                t2_new_cleaned = form.cleaned_data['t2_new']
                try:
                    new_record = ElectricityPayments.objects.create(
                        plot_number=land_plot,
                        t1_new=t1_new_cleaned,
                        t2_new=t2_new_cleaned,
                        )
                    new_record.calculate_payment()
                except ValidationError as validation_error:
                    error_message_list = validation_error.message.split("\n")
                    context = {
                        'plot_number': plot_num,
                        'form': form,
                        'error_message_list': error_message_list,
                        'electric_meter_type': electic_meter_type_disp,
                        }
                    return render(request, 'new_payment.html', context=context)
                return HttpResponseRedirect(
                    reverse('plot-electricity-payments', args=plot_num)
                    )
    else:
        # Instantiate empty form for certain electric meter type
        if electric_meter_type == 'T1':
            form = T1NewElectricityPaymentForm()
        else:
            form = T2NewElectricityPaymentForm()

    context = {
        'plot_number': plot_num,
        'form': form,
        'electric_meter_type': land_plot.electric_meter.get_model_type_display(),
        }

    return render(request, 'new_payment.html', context=context)

@login_required
def user_electricity_payments_view(request):
    """View function to display electricity payments for certain land
    plot or if user has many land plots it will display list of url
    links to certain land plot electricity payment page."""
    current_user = request.user
    land_plot_query_set = current_user.landplot_set.all() 
    # If user has only one land plot
    if len(land_plot_query_set) == 1:
        plot_number = land_plot_query_set[0].plot_number
        return HttpResponseRedirect(reverse('plot-electricity-payments', args=plot_number))
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
    current_user = request.user
    land_plot_query_set = current_user.landplot_set.all()
    payments_list = ElectricityPayments.objects.filter(
        plot_number__exact=plot_num
        ).order_by('-record_date')
    # Check if requested payments belong to current user
    if payments_list[0].plot_number.user == current_user:
        snt_name = land_plot_query_set[0].snt
        context = {
            'snt_name': snt_name,
            'plot_number': plot_num,
            'payments_list': payments_list,
            }
    return render(request, 'electricity_payments.html', context=context)
