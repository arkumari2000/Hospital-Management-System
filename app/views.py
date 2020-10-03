from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .forms import UserRegisterForm, PatientForm, DoctorForm, PrescriptionForm, UserUpdationForm, UpdateDoctorForm, AppointmentForm, InvoiceForm
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from django.http import Http404
from .models import User, Doctor, Patient, Appointment, Invoice, Prescription

# Create your views here.


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = form.save()
            user_type = form.cleaned_data.get('user_type')
            if user_type == '2':
                Patient.objects.create(person=user)
            if user_type == '1':
                Doctor.objects.create(person=user)
            messages.success(request, f'Account created for {username}!')
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form, })


@login_required(login_url='login')
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
                p_form = UpdateDoctorForm(request.POST, instance=doctor)
                u_form.save()
                p_form.save()
                return redirect('dashboard')
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
                return redirect('dashboard')
        return render(request, 'profile.html', {'u_form': u_form, 'p_form': p_form})
    else:
        raise Http404


@login_required(login_url='login')
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
    else:
        raise Http404


@login_required(login_url='login')
def create_invoice(request):
    if request.user.user_type == 3:
        form = InvoiceForm()
        if request.method == 'POST':
            form = InvoiceForm(request.POST)
            invoice = form.save(commit=False)
            invoice.save()
            return redirect('account')
        return render(request, 'presform.html', {'form': form, })
    else:
        raise Http404


@login_required(login_url='login')
def appointments(request):
    if request.user.user_type == 1:
        appointments = request.user.doctor.appointment_set.all()
        return render(request, 'appointment.html', {'appointments': appointments, })
    elif request.user.user_type == 2:
        appointments = request.user.patient.appointment_set.all()
        return render(request, 'appointment.html', {'appointments': appointments, })
    else:
        raise Http404


@login_required(login_url='login')
def prescription(request):
    if request.user.user_type == 1:
        prescriptions = request.user.doctor.prescription_set.all()
        return render(request, 'prescription.html', {'prescriptions': prescriptions, })
    elif request.user.user_type == 2:
        prescriptions = request.user.patient.prescription_set.all()
        return render(request, 'prescription.html', {'prescriptions': prescriptions, })
    else:
        raise Http404


@login_required(login_url='login')
def invoice(request):
    invoices = request.user.patient.invoice_set.all()
    if not invoices:
        invoices = ("-", "-", "-", "-")
    return render(request, 'invoice.html', {'invoices': invoices, })


@login_required(login_url='login')
def account(request):
    invoices = Invoice.objects.all()
    return render(request, 'accounting.html', {'invoices': invoices, })


@login_required(login_url='login')
def delete(request, id):
    if request.user.user_type == 3:
        doctor = Doctor.objects.filter(id=id).first()
        doctor.person.delete()
        return redirect('dashboard')
    elif request.user.user_type == 4:
        doctor = Patient.objects.filter(id=id).first()
        doctor.person.delete()
        return redirect('dashboard')
    else:
        raise Http404


def delete_confirm(request, id):
    return render(request, "delete.html", {
        'id': id,
    })


def dashboard(request):
    if request.user.user_type == 3:
        doctors = Doctor.objects.all()
        active = Doctor.objects.filter(status=1).count()
        patients = Patient.objects.all().count()
        context = {
            'doctors': doctors,
            'active': active,
            'patients': patients,
        }
    elif request.user.user_type == 4:
        appointments = Appointment.objects.all()
        patients = Patient.objects.all()
        approved = Appointment.objects.filter(status='AP').count()
        context = {
            'appointments': appointments,
            'patients': patients,
            'approved': approved,
        }
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
def create(request):
    if request.user.user_type == 3:
        u_form = UserUpdationForm()
        p_form = UpdateDoctorForm()
        if request.method == 'POST':
            u_form = UserUpdationForm(request.POST)
            p_form = UpdateDoctorForm(request.POST)
            if u_form.is_valid():
                user = u_form.save(commit=False)
                instance = p_form.save(commit=False)
                user.username = user.first_name.lower()+"_"+user.last_name.lower()
                user.user_type = 2
                user.set_password("Samidha123")
                instance.person = user
                user.save()
                instance.save()
                return redirect('dashboard')
        return render(request, 'profile.html', {'u_form': u_form, 'p_form': p_form})

    elif request.user.user_type == 4:
        u_form = UserUpdationForm()
        p_form = PatientForm()
        if request.method == 'POST':
            u_form = UserUpdationForm(request.POST)
            p_form = PatientForm(request.POST)
            if u_form.is_valid():
                user = u_form.save(commit=False)
                instance = p_form.save(commit=False)
                user.username = user.first_name.lower()+"_"+user.last_name.lower()
                user.user_type = 2
                user.set_password("Samidha123")
                instance.person = user
                user.save()
                instance.save()
                return redirect('dashboard')
        return render(request, 'profile.html', {'u_form': u_form, 'p_form': p_form})
    else:
        raise Http404


@login_required(login_url='login')
def create_appointment(request):
    if request.user.user_type == 4:
        form = AppointmentForm()
        if request.method == 'POST':
            form = AppointmentForm(request.POST)
            if form.is_valid():
                form.save()
            return redirect('dashboard')
        return render(request, 'appointment_form.html', {'form': form, })
    else:
        raise Http404


@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('index')