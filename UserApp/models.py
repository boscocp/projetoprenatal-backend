from django.db import models
from pygments.lexers import get_all_lexers
from django.urls import reverse
import uuid
from django.contrib.auth.models import AbstractUser

LEXERS = [item for item in get_all_lexers() if item[1]]
USER_TIPE_CHOICES = [
    ('MED', 'medic'),
    ('ADM', 'administrator'),
    ('PAT', 'patient'),
    ('AUD', 'auditor'),
]

# Create your models here.
class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular patient')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['first_name']
        
    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id}, {self.last_name}, {self.first_name}'
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular user')
    email = models.CharField(max_length=100, unique=True,blank=False)
    password = models.CharField(max_length=100,blank=False)
    tipo = models.CharField(max_length=15,blank=False,choices=USER_TIPE_CHOICES,default='PAT')
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []