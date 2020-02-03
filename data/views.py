from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from data.models import Snt, LandPlot, ElectricityPayments
from django.views import generic
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
