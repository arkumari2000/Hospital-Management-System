from django.shortcuts import render,redirect
from .forms import UserRegisterForm , PatientForm , DoctorForm , UpdateForm, ReceptionistForm
from django.views.generic import View
from django.contrib import messages

# Create your views here.
def index(request):
	return render(request,'index.html')

def test(request):
	return render(request,'index.html')

def register(request):
    if request.method == 'POST':
        u_form = UserRegisterForm(request.POST)
        p_form = PatientForm(request.POST)

        if u_form.is_valid():
            username = u_form.cleaned_data.get('username')
            u_form.save()
            messages.success(request, f'Account created for {username}!')
            return redirect('index')
    else:
        u_form = UserRegisterForm()
    return render(request, 'register.html', {'u_form': u_form,})