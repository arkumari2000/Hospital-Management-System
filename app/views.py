from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .forms import UserRegisterForm, PatientForm, DoctorForm, UpdateForm, ReceptionistForm, PrescriptionForm, UserUpdationForm, UpdateDoctorForm, AppointmentForm
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from django.http import Http404
from .models import User, Doctor, Receptionist, Patient, Appointment, Invoice, Prescription

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
            user = form.save()
            user_type = form.cleaned_data.get('user_type')
            if user_type == 2:
                Patient.objects.create(person=user)
            if user_type == 1:
                Doctot.objects.create(person=user)
            messages.success(request, f'Account created for {username}!')
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form, })


@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('index')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def hrdashboard(request):
    doctors = Doctor.objects.all()
    active = Doctor.objects.filter(status=1).count()
    patients = Patient.objects.all().count()
    context = {
        'doctors': doctors,
        'active': active,
        'patients': patients,
    }
    return render(request, 'HRdashboard.html', context)


def recdashboard(request):
    appointments = Appointment.objects.all()
    patients = Patient.objects.all()
    approved = Appointment.objects.filter(status='AP').count()
    context = {
        'appointments': appointments,
        'patients': patients,
        'approved': approved,

    }
    return render(request, 'Rdashboard.html', context)


def account(request):
    return render(request, 'accounting.html')


@login_required(login_url='login')
def appointments(request):
    appointments = Appointment.objects.all()
    context = {
        'appointments': appointments,
    }
    if request.user.user_type == 1:
        return render(request, 'appointment.html', context)
    elif request.user.user_type == 2:
        return render(request, 'appointment.html', context)
    else:
        return HttpResponse(f'user_type is {request.user.user_type} {type(request.user.user_type)}')


@login_required(login_url='login')
def prescription(request):
    if request.user.user_type == 1:
        prescriptions = request.user.doctor.prescription_set.all()
        return render(request, 'prescription.html', {'prescriptions': prescriptions, })
    elif request.user.user_type == 2:
        prescriptions = request.user.patient.prescription_set.all()
        return render(request, 'prescription.html', {'prescriptions': prescriptions, })
    else:
        return HttpResponse('user_type is ', user_type)


def invoice(request):
    invoices = request.user.patient.invoice_set.all()
    if not invoices:
        invoices = ("-", "-", "-", "-")
    return render(request, 'invoice.html', {'invoices': invoices, })
# def create_prescription(request):


def profile(request, id=None):
    if request.user.user_type == 1:
        doctor = request.user.doctor
        u_form = UserUpdationForm(instance=request.user)
        p_form = DoctorForm(instance=doctor)
        if request.method == 'POST':
            u_form = UserUpdationForm(request.POST)
            p_form = PatientForm(request.POST)
            if u_form.is_valid():
                u_form = UserUpdationForm(request.POST, instance=request.user)
                p_form = DoctorForm(request.POST, instance=doctor)
                u_form.save()
                p_form.save()
                return redirect('profile')
        return render(request, 'profile.html', {'u_form': u_form, 'p_form': p_form})
    elif request.user.user_type == 2:
        patient = request.user.patient
        u_form = UserUpdationForm(instance=request.user)
        p_form = PatientForm(instance=patient)
        if request.method == 'POST':
            u_form = UserUpdationForm(request.POST)
            p_form = PatientForm(request.POST)
            if u_form.is_valid():
                u_form = UserUpdationForm(request.POST, instance=request.user)
                p_form = PatientForm(request.POST, instance=patient)
                u_form.save()
                p_form.save()
                return redirect('profile')
        return render(request, 'profile.html', {'u_form': u_form, 'p_form': p_form})
    elif request.user.user_type == 3:
        doctor = Doctor.objects.filter(id=id).first()
        user = doctor.person
        u_form = UserUpdationForm(instance=doctor.person)
        p_form = UpdateDoctorForm(instance=doctor)
        if request.method == 'POST':
            u_form = UserUpdationForm(request.POST)
            p_form = PatientForm(request.POST)
            if u_form.is_valid():
                u_form = UserUpdationForm(request.POST, instance=doctor.person)
                p_form = DoctorForm(request.POST, instance=doctor)
                u_form.save()
                p_form.save()
                return redirect('hrdashboard')
        return render(request, 'profile.html', {'u_form': u_form, 'p_form': p_form})
    elif request.user.user_type == 4:
        patient = Patient.objects.filter(id=id).first()
        u_form = UserUpdationForm(instance=patient.person)
        p_form = PatientForm(instance=patient)
        if request.method == 'POST':
            u_form = UserUpdationForm(request.POST)
            p_form = PatientForm(request.POST)
            if u_form.is_valid():
                u_form = UserUpdationForm(
                    request.POST, instance=patient.person)
                p_form = PatientForm(request.POST, instance=patient)
                u_form.save()
                p_form.save()
                return redirect('recdashboard')
        return render(request, 'profile.html', {'u_form': u_form, 'p_form': p_form})


def delete(request, id):
    if request.user.user_type == 3:
        doctor = Doctor.objects.filter(id=id).first()
        doctor.person.delete()
        return redirect('hrdashboard')
    if request.user.user_type == 4:
        doctor = Patient.objects.filter(id=id).first()
        doctor.person.delete()
        return redirect('recdashboard')


def create_prescription(request):
    if request.user.user_type == 1:
        form = PrescriptionForm()
        if request.method == 'POST':
            form = PrescriptionForm(request.POST)
            prescription = form.save(commit=False)
            prescription.doctor = request.user.doctor
            prescription.save()
            return redirect('prescription')
        return render(request, 'presform.html', {'form': form, })


def create_appointment(request):
    if request.user.user_type == 4:
        form = AppointmentForm()
        if request.method == 'POST':
            form = AppointmentForm(request.POST)
            if form.is_valid():
                form.save()
            return redirect('recdashboard')
        return render(request, 'appointment_form.html', {'form': form, })
    else:
        raise Http404


def create_patient(request):
    if request.user.user_type == 4:
        u_form = UserUpdationForm()
        p_form = PatientForm()
        if request.method == 'POST':
            u_form = UserUpdationForm(request.POST)
            p_form = PatientForm(request.POST)
            if u_form.is_valid():
                user = u_form.save(commit=False)
                instance = p_form.save(commit=False)
                instance.user = user
                user.save()
                instance.save()
                return redirect('recdashboard')
        return render(request, 'profile.html', {'u_form': u_form, 'p_form': p_form})
