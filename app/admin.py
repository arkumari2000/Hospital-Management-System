from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Doctor,Receptionist,Patient,Appointment,Invoice,Prescription
from django.utils.translation import gettext, gettext_lazy as _

@admin.register(User)
class CustomAdmin(UserAdmin):
	fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Custom Fields'), {'fields': ('user_type',)}),
    )

# Register your models here.
admin.site.register(Doctor)
admin.site.register(Receptionist)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Prescription)
admin.site.register(Invoice)