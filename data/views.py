from django.shortcuts import render
from django.http import HttpResponse
import datetime

# Create your views here.
def homepage(request):
    now = datetime.datetime.now()
    now = now.strftime("%d/%m/%Y")
    html = "<html><body>It is now %s.</body></html>" %now
    return HttpResponse(html)
