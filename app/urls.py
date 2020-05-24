from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
	path('',views.index,name='index'),
	path('register', views.register , name='register'),
	path('test',views.test,name="test"),
]