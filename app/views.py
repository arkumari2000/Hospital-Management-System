from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .forms import UserRegisterForm, PatientForm, DoctorForm, UpdateForm, ReceptionistForm, PrescriptionForm,UserUpdationForm
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from django.http import Http404
from .models import User,Doctor,Receptionist,Patient,Appointment,Invoice,Prescription

# Create your views here.


def index(request):
    return render(request, 'index.html')


def test(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            user=form.save()
            user_type=form.cleaned_data.get('user_type')
            if user_type==2:
                Patient.objects.create(person=user)
            if user_type==1:
                Doctot.objects.create(person=user)
            messages.success(request, f'Account created for {username}!')
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form, })


@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def hrdashboard(request):
    return render(request, 'HRdashboard.html')


def recdashboard(request):
    return render(request, 'Rdashboard.html')


def account(request):
    return render(request, 'accounting.html')


@login_required(login_url='login')
def appointments(request):
    if request.user.user_type==1:
        return render(request, 'appointment.html')
    elif request.user.user_type==2:
        return render(request, 'appointment.html')
    else:
        return HttpResponse(f'user_type is {request.user.user_type} {type(request.user.user_type)}')


@login_required(login_url='login')
def prescription(request):
    if request.user.user_type==1:
        prescriptions=request.user.doctor.prescription_set.all()
        return render(request, 'prescription.html',{'prescriptions':prescriptions,})
    elif request.user.user_type==2:
        prescriptions=request.user.patient.prescription_set.all()
        return render(request, 'prescription.html',{'prescriptions':prescriptions,})
    else:
        return HttpResponse('user_type is ',user_type)

def invoice(request):
    invoices=request.user.patient.invoice_set.all()
    if not invoices:
        invoices=("-","-","-","-")
    return render(request, 'invoice.html',{'invoices':invoices,})
# def create_prescription(request):
def profile(request):
    if request.user.user_type==1:
        doctor=request.user.doctor
        u_form=UserUpdationForm(instance=request.user)
        p_form=DoctorForm(instance=doctor)
        if request.method=='POST':
            u_form=UserUpdationForm(request.POST)
            p_form=PatientForm(request.POST)
            if u_form.is_valid():
                u_form=UserUpdationForm(request.POST,instance=request.user)
                p_form=PatientForm(request.POST,instance=doctor)
                u_form.save()
                p_form.save()
                return redirect('profile')
        return render(request,'profile.html',{'u_form':u_form,'p_form':p_form})
    elif request.user.user_type==2:
        patient=request.user.patient
        u_form=UserUpdationForm(instance=request.user)
        p_form=PatientForm(instance=patient)
        if request.method=='POST':
            u_form=UserUpdationForm(request.POST)
            p_form=PatientForm(request.POST)
            if u_form.is_valid():
                u_form=UserUpdationForm(request.POST,instance=request.user)
                p_form=PatientForm(request.POST,instance=patient)
                u_form.save()
                p_form.save()
                return redirect('profile')
        return render(request,'profile.html',{'u_form':u_form,'p_form':p_form})
    else:
        return redirect('index')

def create_prescription(request):
    if request.user.user_type==1:
        form=PrescriptionForm()
        if request.method=='POST':
            form=PrescriptionForm(request.POST)
            prescription=form.save(commit=False)
            prescription.doctor=request.user.doctor
            prescription.save()
            return redirect('prescription')
        return render(request,'presform.html',{'form':form,})