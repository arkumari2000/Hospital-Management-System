from django.contrib import admin
from .models import User,Doctor,Receptionist,Patient,Appointment
# Register your models here.
admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(Receptionist)
admin.site.register(Patient)
admin.site.register(Appointment)