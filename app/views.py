from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from .forms import UserRegisterForm , PatientForm , DoctorForm , UpdateForm, ReceptionistForm,PrescriptionForm
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,logout,login
from django.http import Http404

# Create your views here.
def index(request):
	return render(request,'index.html')

def test(request):
	return render(request,'index.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        p_form = PatientForm(request.POST)

        if form.is_valid():
            username = u_form.cleaned_data.get('username')
            form.save()
            messages.success(request, f'Account created for {username}!')
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form,})

@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

@login_required(login_url='login')
def appointments(request):
    if request.user.user_type is 1:
        return render(request,'appointment.html')
    elif request.user.user_type is 2:
        return render(request,'appointment.html')
    else:
        raise Http404

@login_required(login_url='login')
def prescription(request):
    if request.user.user_type is 1:
        return render(request,'prescription.html')
    elif request.user.user_type is 2:
        return render(request,'prescription.html')
    else:
        raise Http404

# def create_prescription(request):
