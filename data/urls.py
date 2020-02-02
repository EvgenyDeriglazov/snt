from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('1', views.homepage2, name='homepage2'),

]
