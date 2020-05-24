from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
import datetime

BLOOD_CHOICES = (
    (1, 'A+'),
    (2, 'A-'),
    (3, 'B+'),
    (4, 'B-'),
    (5, 'AB+'),
    (6, 'AB-'),
    (7, 'O+'),
    (8, 'O-'),
    )

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'doctor'),
        (2, 'patient'),
        (3, 'HR'),
        (4, 'Receptionist'),
        )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES,default=2)

class Doctor(models.Model):
    person = models.OneToOneField(User, on_delete=models.CASCADE)
    Speciality = models.CharField(max_length=100 , default=None,blank=True)
    Address = models.CharField(max_length=100 , default=None,blank=True)
    Email = models.CharField(max_length=100 , default=None,blank=True)
    Phone = models.CharField(max_length=100 , default=None,blank=True)
    gender = models.CharField(max_length=100 , default=None,blank=True)

    def __str__(self):
        return self.person.username

class Receptionist(models.Model):
    person = models.OneToOneField(User, on_delete=models.CASCADE)
    Address = models.CharField(max_length=100 , default=None)
    Email = models.CharField(max_length=100 , default=None)
    Phone = models.CharField(max_length=100 , default=None)
    gender = models.CharField(max_length=100 , default=None)

    def __str__(self):
        return self.person.user.username


class Patient(models.Model):
    person = models.OneToOneField(User, on_delete=models.CASCADE)
    Address = models.CharField(max_length=100 , blank=True,null=True)
    Phone = models.CharField(max_length=100 , blank=True,null=True)
    gender = models.CharField(max_length=100 , blank=True,null=True)
    age=models.IntegerField(blank=True,default=None,null=True)
    case_paper=models.IntegerField(blank=True,null=True)
    records=models.FileField(upload_to='records',blank=True)
    blood_group=models.PositiveSmallIntegerField(choices=BLOOD_CHOICES,default=7)

    def __str__(self):
        return self.person.username

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, null=True,on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, default=None,on_delete=models.CASCADE)
    date = models.DateField(("Date"), default=datetime.date.today)
    time = models.TimeField(auto_now_add=True)
    Pending= 'PD'
    Approved= 'AP'
    Rejected = 'RJ'
    STATUS = (
        (Pending, 'Pending'),
        (Approved, 'Approved'),
        (Rejected, 'rejected'),
    )
    status = models.CharField(
        max_length=2,
        choices=STATUS,
        default=Pending,
    )

    message = models.CharField(max_length=1000 , default="Pending Approval")

    def __str__(self):
        return str(self.patient)

    def get_absolute_url(self):
        return reverse('index')

class Prescription(models.Model):
    patient = models.ForeignKey(Patient, null=True,on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, default=None,on_delete=models.CASCADE)
    date = models.DateField(("Date"), default=datetime.date.today)
    Symptoms = models.CharField(max_length=100)
    Description = models.TextField()

# class Invoice

class Invoice(models.Model):
    patient = models.ForeignKey(Patient, null=True,on_delete=models.CASCADE)
    date = models.DateField(("Date"), default=datetime.date.today)
    remain=models.IntegerField()
    paid=models.IntegerField()
    link=models.FileField(upload_to='invoices',blank=True)

    def __str__(self):
        return str(self.patient)