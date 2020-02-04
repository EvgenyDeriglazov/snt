from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('1', views.homepage2, name='homepage2'),
    path(
        'payments/',
        views.ElectricityPaymentsListView.as_view(),
        name='payments'
        ),
    path('user-payments/', views.user_payments_view, name='user-payments'),

]
