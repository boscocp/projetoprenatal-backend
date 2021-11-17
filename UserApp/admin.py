from django.contrib import admin
from .models import Patient, User

# Register your models here.
#admin.site.register(Patient)
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id','last_name', 'first_name', 'created')
@admin.register(User)
class PatientAdmin(admin.ModelAdmin):
    list_display = fields=("id","first_name",'last_name',"email","password","tipo")