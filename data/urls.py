from django.urls import path
from . import views

urlpatterns = [
    path('payments/', views.user_payments_view, name='payments'),
    path(
    	'payments/electricity-payments/',
    	views.user_electricity_payments_view,
    	name='electricity-payments',
    	),
    path(
    	'payments/electricity-payments/plot-<plot_num>',
    	views.user_plot_electricity_payments_view,
    	name='plot-electricity-payments',
    	),
    path(
    	'payments/electricity-payments/plot-<plot_num>/new_payment',
    	views.user_new_payment_view,
    	name='new-payment',
    	),
    path(
    	'payments/electricity-payments/plot-<plot_num>/payment-<int:pk>',
    	views.user_payment_details_view,
    	name='payment-details',
    	),
 
]
