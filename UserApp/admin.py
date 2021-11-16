from django.contrib import admin
from .models import Patient

# Register your models here.
#admin.site.register(Patient)
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id','last_name', 'first_name', 'created')