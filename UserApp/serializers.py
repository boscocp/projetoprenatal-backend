from os import error
from UserApp.patientdto import PatientDTO
from django.core.serializers.json import Serializer
from rest_framework import serializers
from UserApp.models import *

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    person = PersonSerializer(source="persons", many=True, read_only=True)
    class Meta:
        model = Address
        fields = '__all__'
        extra_kwargs = {'persons': {'required': False}}

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only':True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
class PatientSerializer(serializers.ModelSerializer):
    person = PersonSerializer(required=True)
    user = UserSerializer(required=True)
    class Meta:
        model = Patient
        fields = '__all__'
        related_fields = ['person','user']

    def create(self, validated_data):
        person_data = validated_data.pop('person')
        user_data = validated_data.pop('user')
        person, p = Person.objects.get_or_create(**person_data)
        user, u = User.objects.get_or_create(**user_data)       
        patient = Patient.objects.create(person=person, user=user, **validated_data)
        return patient 
    
    @staticmethod
    def updateCuston(instance, data):
        dataPatient = data['patient']
        person = Person.objects.get(id=instance.person.id)
        serializerPerson = PersonSerializer(person,data=dataPatient['person'])
        serializerPerson.is_valid(raise_exception=True)
        serializerPerson.save()
        user = User.objects.get(id=instance.user.id)
        dataUser = dataPatient['user']
        if 'password' not in dataUser or dataUser['password']=='':
            dataUser['password']=user.password
            
        serializerUser = UserSerializer(user,data=dataPatient['user'])
        serializerUser.is_valid(raise_exception=True)
        serializerUser.save()
        address = Address.objects.filter(person__id=instance.person.id).first()
        serializerAddress=AddressSerializer(address,data=data['address'])
        serializerAddress.is_valid(raise_exception=True)
        serializerAddress.save()
        instance.occupation = dataPatient['occupation'] 
        instance.kinship = dataPatient['kinship']
        instance.save()
        return instance
    
class PatientDTOSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=10)
    name = serializers.CharField(max_length=200)
    cpf = serializers.CharField(max_length=200)
    birt_date = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    
class MedicSerializer(serializers.ModelSerializer):
    person = PersonSerializer(required=True)
    user = UserSerializer(required=True)
    class Meta:
        model = Medic
        fields = '__all__'
        related_fields = ['person','user']

    def create(self, validated_data):
        person_data = validated_data.pop('person')
        user_data = validated_data.pop('user')
        person, p = Person.objects.create(**person_data)
        user, u = User.objects.get_or_create(**user_data)       
        patient = Medic.objects.create(person=person, user=user, **validated_data)
        return patient 
    def update(self, instance, validated_data):
        for related_object_name in self.Meta.related_fields:
            related_instance = getattr(instance, related_object_name)
            related_instance.save()    
        return super().update(instance, validated_data)
    
class PrenatalSerializer(serializers.ModelSerializer):
    medic = MedicSerializer(source="medics",many=True, read_only=True)
    patient = PatientSerializer(required=True)
    class Meta:
        model = Prenatal
        fields = '__all__'
        related_fields = ['medic','patient']
        extra_kwargs = {'medics': {'required': False}}
        
    def create(self, validated_data):
        medic_data = validated_data.pop('medic')
        patient_data = validated_data.pop('patient')
        medic = Medic.objects.get(**medic_data)
        patient, p = Patient.objects.get_or_create(**patient_data)     
        prenatal = Prenatal.objects.create(medic=medic, patient=patient, **validated_data)
        return prenatal 
    def update(self, instance, validated_data):
        for related_object_name in self.Meta.related_fields:
            related_instance = getattr(instance, related_object_name)
            related_instance.save()    
        return super().update(instance, validated_data)
    
class AppointmentSerializer(serializers.ModelSerializer):
    prenatal = PrenatalSerializer(source="prenatals",many=True, read_only=True)
    class Meta:
        model = Appointment
        fields = '__all__'
        extra_kwargs = {'prenatals': {'required': False}}
        
class AddendumSerializer(serializers.ModelSerializer):
    appointment = AppointmentSerializer(source="appointments",many=True, read_only=True)
    class Meta:
        model = Addendum
        fields = '__all__'
        extra_kwargs = {'appointments': {'required': False}}      
          
class MedicalExamSerializer(serializers.ModelSerializer):
    prenatal = PrenatalSerializer(source="prenatals",many=True, read_only=True)
    class Meta:
        model = MedicalExam
        fields = '__all__'
        related_fields = ['prenatal']
        extra_kwargs = {'prenatals': {'required': False}}        
        
    def create(self, validated_data): 
        prenatal_data = validated_data.pop('prenatal') 
        prenatal = Prenatal.objects.get(**prenatal_data)  
        exam = MedicalExam.objects.get_or_create(prenatal=prenatal, **validated_data)
        return exam 
    def update(self, instance, validated_data):
        for related_object_name in self.Meta.related_fields:
            related_instance = getattr(instance, related_object_name)
            related_instance.save()    
        return super().update(instance, validated_data)

class NumericMedicalExamSerializer(serializers.ModelSerializer):
    exam = MedicalExamSerializer(required=True)
    class Meta:
        model = NumericMedicalExam
        fields = '__all__'
        related_fields = ['exam']
        
    def create(self, validated_data):
        exam_data = validated_data.pop('exam')  
        exam = MedicalExam.objects.create(**exam_data)
        numeric_exam = NumericMedicalExam.objects.create(exam=exam, **validated_data)
        return numeric_exam
    def update(self, instance, validated_data):     
        related_instance = getattr(instance, 'exam')
        serializer = MedicalExamSerializer(related_instance,validated_data['exam'])
        serializer.is_valid(raise_exception=True) 
        serializer.save()
        instance.value = validated_data['value']
        instance.save()
        return instance
        
class ReagentExamSerializer(serializers.ModelSerializer):
    exam = MedicalExamSerializer(required=True)
    class Meta:
        model = ReagentExam
        fields = '__all__'
    def create(self, validated_data):
        exam_data = validated_data.pop('exam')  
        exam = MedicalExam.objects.create(**exam_data)
        reagent_exam = ReagentExam.objects.create(exam=exam, **validated_data)
        return reagent_exam
    def update(self, instance, validated_data):
        related_instance = getattr(instance, 'exam')
        serializer = MedicalExamSerializer(related_instance,validated_data['exam'])
        serializer.is_valid(raise_exception=True) 
        serializer.save()
        instance.value = validated_data['value']
        instance.save()
        return instance

class UltrasoundExamSerializer(serializers.ModelSerializer):
    exam = MedicalExamSerializer(required=True)
    class Meta:
        model = UltrasoundExam
        fields = '__all__'
    def create(self, validated_data):
        exam_data = validated_data.pop('exam')  
        exam = MedicalExam.objects.create(**exam_data)
        exam.name = "ultrassound"
        ultrassound_exam = UltrasoundExam.objects.create(exam=exam, **validated_data)
        return ultrassound_exam
    def update(self, instance, validated_data):
        related_instance = getattr(instance, 'exam')
        serializer = MedicalExamSerializer(related_instance,validated_data['exam'])
        serializer.is_valid(raise_exception=True) 
        serializer.save()
        instance.value = validated_data['value']
        instance.save()
        return instance
    
class OtherExamSerializer(serializers.ModelSerializer):
    exam = MedicalExamSerializer(required=True)
    class Meta:
        model = OtherExam
        fields = '__all__'
    def create(self, validated_data):
        exam_data = validated_data.pop('exam')  
        exam = MedicalExam.objects.create(**exam_data)
        numeric_exam = OtherExam.objects.create(exam=exam, **validated_data)
        return numeric_exam
    def update(self, instance, validated_data):
        related_instance = getattr(instance, 'exam')
        serializer = MedicalExamSerializer(related_instance,validated_data['exam'])
        serializer.is_valid(raise_exception=True) 
        serializer.save()
        instance.value = validated_data['value']
        instance.save()
        return instance