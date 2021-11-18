from os import error
from rest_framework import serializers
from UserApp.models import Patient, User, Person


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'
        #fields=("id","name","cpf","birt_date","civil_state","created")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = '__all__'
        #fields=("id","email","password","tipo")
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
        fields=("person","user","occupation","kinship")
    def create(self, validated_data):
        person_data = validated_data.pop('person')
        user_data = validated_data.pop('user')
        person, p = Person.objects.get_or_create(**person_data)
        user, u = User.objects.get_or_create(**user_data)       
        patient = Patient.objects.update_or_create(person=person, 
                                                    user=user, **validated_data)

        return patient