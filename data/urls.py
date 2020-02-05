from django.urls import path
from . import views

urlpatterns = [
    path('user-payments/', views.user_payments_view, name='user-payments'),

]
