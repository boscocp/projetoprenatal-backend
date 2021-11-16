from rest_framework import generics

from UserApp.models import Patient
from UserApp.serializers import PatientSerializer
# Create your views here.

class PatientList(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class PatientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class =PatientSerializer