from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from data.models import Snt, LandPlot, ElectricityPayments
from django.views import generic
from django.contrib.auth.decorators import login_required
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

class ElectricityPaymentsListView(generic.ListView):
    model = ElectricityPayments
    context_object_name = 'payments'
    template_name = 'data/payments.html'

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
def user_payment_details_view(request, pk):
    """View function to display specific payment details. Payments
    with record_status='n' (new) can be edited by the authenticated
    user. Other paymnets with record_status='p', 'c', 'i' are not
    allowed to be edited (only view mode)."""
    current_user = request.user
    payment_details = ElectricityPayments.objects.get(id=pk)
    context = {
        'payment_details': payment_details
        }

    return render(request, 'payment_details.html', context=context)

@login_required
def user_new_record_view(request):
    pass


