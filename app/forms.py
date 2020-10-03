from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import Appointment, Doctor, Invoice, Patient, Prescription, User


class UserRegisterForm(UserCreationForm):
    CHOICES = (
        (1, 'doctor'),
        (2, 'patient'),
    )
    email = forms.EmailField()
    user_type = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
            'user_type',
        ]


class UserUpdationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = (
            'Address',
            'Phone',
            'gender',
            'case_paper',
            'records',
            'blood_group',
            'age',
        )


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ('Address', 'Phone', 'gender', 'Department')


class UpdateDoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = (
            'Address',
            'Phone',
            'gender',
            'Department',
            'status',
            'attendance',
            'salary',
        )


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'patient', 'status']


class PrescriptionForm(forms.ModelForm):
    Description = forms.CharField(label=_("Prescription"),)
    Symptoms = forms.CharField(label=_("Disease"),)

    class Meta:
        model = Prescription
        fields = ['Description', 'Symptoms', 'patient']


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'
