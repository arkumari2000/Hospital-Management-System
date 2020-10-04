from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', views.user_logout, name='logout'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('appointments', views.appointments, name='appointments'),
    path('prescription', views.prescription, name='prescription'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('account', views.account, name='account'),
    path('invoice', views.invoice, name='invoice'),
    path('profile', views.profile, name='profile'),
    path('profile/<int:id>', views.profile, name='profile_update'),
    path('delete/<int:id>', views.delete, name='profile_delete'),
    path('delete/<int:id>/confirm', views.delete_confirm, name='delete_confirm'),
    path('create_prescription', views.create_prescription, name='create_prescription'),
    path('create_appointment', views.create_appointment, name='create_appointment'),
    path('create', views.create, name='create'),
    path('create_invoice', views.create_invoice, name='create_invoice'),
]
