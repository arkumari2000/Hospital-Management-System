from .models import User

from django import forms
from .models import  Appointment , Patient , Doctor, Receptionist,Prescription
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _



class UserRegisterForm(UserCreationForm):
    CHOICES = (
      (1, 'doctor'),
      (2, 'patient'),
  )
    email = forms.EmailField()
    user_type = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password1', 'password2','user_type']


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('Address', 'Email', 'Phone', 'gender', 'location', 'bio')

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ('Address', 'Email', 'Phone', 'gender', 'Speciality',)


class ReceptionistForm(forms.ModelForm):
    class Meta:
        model = Receptionist
        fields = ('Address', 'Email', 'Phone', 'gender',)


class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = ['Doctor', 'Date']

class PrescriptionForm(forms.ModelForm):
    Description=forms.CharField(label=_("Prescription"),)
    Symptoms=forms.CharField(label=_("Disease"),)

    class Meta:
        model=Prescription
        fields= ['Description','Symptoms','Patient']

class Login(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class UpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username',)


