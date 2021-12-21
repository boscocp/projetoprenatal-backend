from os import error
from rest_framework import serializers
from UserApp.models import Patient, User, Person, Medic, Address, Prenatal

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    person = PersonSerializer(many=True, read_only=True)
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
    def update(self, instance, validated_data):
        for related_object_name in self.Meta.related_fields:
            related_instance = getattr(instance, related_object_name)
            related_instance.save()    
        return super().update(instance, validated_data)

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
        person, p = Person.objects.get_or_create(**person_data)
        user, u = User.objects.get_or_create(**user_data)       
        patient = Medic.objects.create(person=person, user=user, **validated_data)
        return patient 
    def update(self, instance, validated_data):
        for related_object_name in self.Meta.related_fields:
            related_instance = getattr(instance, related_object_name)
            related_instance.save()    
        return super().update(instance, validated_data)
    
class PrenatalSerializer(serializers.ModelSerializer):
    medic = MedicSerializer(many=True, read_only=True)
    patient = PatientSerializer(required=True)
    class Meta:
        model = Prenatal
        fields = '__all__'
        related_fields = ['medic','patient']
        extra_kwargs = {'medics': {'required': False}}
        
    def create(self, validated_data):
        medic_data = validated_data.pop('medic')
        patient_data = validated_data.pop('patient')
        medic, m = Medic.objects.get_or_create(**medic_data)
        patient, p = Patient.objects.get_or_create(**patient_data)     
        prenatal = Prenatal.objects.create(medic=medic, patient=patient, **validated_data)
        return prenatal 
    def update(self, instance, validated_data):
        for related_object_name in self.Meta.related_fields:
            related_instance = getattr(instance, related_object_name)
            related_instance.save()    
        return super().update(instance, validated_data)