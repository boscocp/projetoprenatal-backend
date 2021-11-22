from django.contrib import admin
from .models import Patient, User

# Register your models here.
#admin.site.register(Patient)
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("id","occupation")
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = fields=("id","email","password","tipo")