from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('test', views.test, name="test"),
    path('login', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', views.user_logout, name='logout'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('appointments', views.appointments, name='appointments'),
    path('prescription', views.prescription, name='prescription'),
    path('hrdashboard', views.hrdashboard, name='hrdashboard'),
    path('recdashboard', views.recdashboard, name='recdashboard'),
    path('account', views.account, name='account'),
    path('invoice', views.invoice, name='invoice'),
    path('profile', views.profile, name='profile'),
    path('create_prescription', views.create_prescription, name='create_prescription'),
]
