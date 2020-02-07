from django.urls import path
from . import views

urlpatterns = [
    path('user-payments/', views.user_payments_view, name='user-payments'),
    path(
    	'user-payments/<int:pk>',
    	views.user_payment_details_view,
    	name='payment-details',
    	),
    path(
    	'user-payments/new',
    	views.user_new_record_view,
    	name='payment-new',
    	)
]
