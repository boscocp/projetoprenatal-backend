import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

USER_TIPE_CHOICES = [
    ('MED', 'medic'),
    ('ADM', 'administrator'),
    ('PAT', 'patient'),
    ('AUD', 'auditor'),
]

MARITAL_STATUS_CHOICES = [
    ('S', 'Sigle'),
    ('M', 'Married'),
    ('D', 'Divorced'),
]

REAGENT_EXAM_CHOICES = [
    ('NR', 'Not reagent'),
    ('R', 'Reagent'),
]

CPF = RegexValidator(
    regex=r'^([0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})|([0-9]{3}[\.]?[0-9]{3}[\.]?[0-9]{3}[-]?[0-9]{2})$',
    message='CPF must be valid',
    code='invalid_CPF'
)

# Create your models here.

class Person(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular person')
    name = models.CharField(max_length=200)
    cpf = models.CharField(unique=True, max_length=14, blank=False, validators=[CPF])
    birt_date = models.DateField(blank=False)
    civil_state = models.CharField(choices=MARITAL_STATUS_CHOICES,max_length=1,default='S')
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['name']
        
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id}, {self.name}'

class Address(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    number = models.IntegerField()
    zipcode =  models.IntegerField()
    def __str__(self):
        return self.address
    
class ContactInfo(models.Model):
    person = models.OneToOneField(Person,on_delete=models.CASCADE,primary_key=True)
    phoneNumber = models.IntegerField()
    
class Father(models.Model):
    person = models.OneToOneField(Person,on_delete=models.CASCADE,primary_key=True)
    occupation = models.CharField(max_length=100)
    
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular user')
    email = models.EmailField(blank=False,unique=True)
    password = models.CharField(max_length=100,blank=False)
    tipo = models.CharField(max_length=15,blank=False,choices=USER_TIPE_CHOICES,default='PAT')
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Patient(models.Model):
    person = models.OneToOneField(Person,on_delete=models.CASCADE)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    occupation = models.CharField(max_length=100)
    kinship = models.BooleanField(default=False)

class Medic(models.Model):
    person = models.OneToOneField(Person,on_delete=models.CASCADE)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    crm = models.IntegerField()
    
class Prenatal(models.Model):
    patient = models.OneToOneField(Patient,on_delete=models.DO_NOTHING)
    medic = models.OneToOneField(Medic,on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(blank=False)
    
class Appointment(models.Model):
    prenatal = models.ForeignKey(Prenatal,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    weight = models.FloatField()
    date = models.DateField(blank=False)
    ig = models.CharField(max_length=80)
    pa = models.CharField(max_length=80)
    edema = models.CharField(max_length=80)
    av = models.CharField(max_length=80)
    bcf = models.CharField(max_length=80)
    complication = models.CharField(max_length=200)
    cd = models.CharField(max_length=80)
    substance_use = models.CharField(max_length=200)

class MedicalExam(models.Model):
    patient = models.ForeignKey(Person,on_delete=models.DO_NOTHING)
    medic = models.ForeignKey(Medic,on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    date = models.DateField(blank=False)
    name = models.CharField(max_length=80)

class NumericMedicalExam(models.Model):
    exam = models.OneToOneField(MedicalExam,on_delete=models.CASCADE)
    value = models.FloatField()

class ReagentExam(models.Model):
    exam = models.OneToOneField(MedicalExam,on_delete=models.CASCADE)
    value = models.CharField(choices=REAGENT_EXAM_CHOICES, blank=False,max_length=2)
    
class OtherExam(models.Model):
    exam = models.OneToOneField(MedicalExam,on_delete=models.CASCADE)
    value = models.CharField(max_length=200, blank=False)