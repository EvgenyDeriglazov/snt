from django.urls import path
from . import views

urlpatterns = [
    path('user-payments/', views.user_payments_view, name='user-payments'),
    path(
    	'user-payments/<int:pk>',
    	views.user_payment_details_view,
    	name='payment-details',
    	),
]
