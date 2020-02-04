from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from data.models import Snt, LandPlot, ElectricityPayments
from django.views import generic
from django.contrib.auth.decorators import login_required
import datetime

# Create your views here.
def homepage(request):
    now = datetime.datetime.now()
    now = now.strftime("%d/%m/%Y")
    html = "<html><body>It is now %s.</body></html>" %now
    return HttpResponse(html)

def homepage2(request):
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
    """View function for user payments page."""
    context = {}
    current_user = request.user
    land_plot_query_set = current_user.landplot_set.all() 
    if len(land_plot_query_set) == 1:
        plot = land_plot_query_set[0]
        context['plot'] = plot
        payments = ElectricityPayments.objects.filter(
            plot_number__exact=plot
            ).order_by('-record_date')
        context['payments'] = payments
    elif len(land_plot_query_set) > 1:
        context['plot_list'] = land_plot_query_set
    
    return render(request, 'user_payments.html', context=context)
