from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from data.models import Snt, LandPlot, ElectricityPayments
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from data.forms import NewElectricityPaymentForm
from django.utils.translation import gettext_lazy as _
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
    """View function for user payments page. It will display
    either payments table for one plot or consolidated payments
    table for many plots owned by authenticated user."""
    context = {}
    current_user = request.user
    land_plot_query_set = current_user.landplot_set.all() 
    if len(land_plot_query_set) == 1:
        plot = land_plot_query_set[0]
        context['snt_name'] = plot.snt
        context['plot'] = plot
        payments_list = ElectricityPayments.objects.filter(
            plot_number__exact=plot
            ).order_by('-record_date')
        context['payments_list'] = payments_list
    elif len(land_plot_query_set) > 1:
        payments_consolidated_list = []
        context['snt_name'] = land_plot_query_set[0].snt
        for plot in land_plot_query_set:
            payments_list = ElectricityPayments.objects.filter(
                plot_number__exact=plot
                ).order_by('-record_date')
            for item in payments_list:
                    payments_consolidated_list.append(item)
        context['payments_consolidated_list'] = payments_consolidated_list
                
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
def user_payment_details_view(request, pk):
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
def user_new_record_view(request):
    """View function to display form for new electricity payment
    record."""
    current_user = request.user
    if request.method == 'POST':
        form = NewElectricityPaymentForm(request.POST, user=current_user)
        if form.is_valid():
            plot_number_cleaned = form.cleaned_data['plot_number']
            t1_new_cleaned = form.cleaned_data['t1_new']
            t2_new_cleaned = form.cleaned_data['t2_new']
            new_record = ElectricityPayments.objects.create(
                plot_number=plot_number_cleaned,
                record_date="",
                t1_new=t1_new_cleaned,
                t2_new=t2_new_cleaned,
                )
            new_record.calculate_payment()
            return HttpResponseRedirect(reverse('user-payments'))
    else:
        form = NewElectricityPaymentForm(user=current_user)

    context = {
        'form': form,
        }

    return render(request, 'payment_new.html', context=context)


