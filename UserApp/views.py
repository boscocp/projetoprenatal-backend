from django.utils.functional import empty
from rest_framework import generics, serializers
from rest_framework import response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from UserApp.models import Patient, User, Person, Medic, Address
from UserApp.serializers import PatientSerializer, UserSerializer, PersonSerializer, MedicSerializer, AddressSerializer
import jwt, datetime
from rest_framework import status

# Create your views here.
class MedicRegisterView(APIView):
    def post(self, request):
        request_medic = request.data['medic']
        request_address = request.data['address']
        request_medic['tipo'] = 'MED'
        
        serializer_medic = MedicSerializer(data=request_medic)
        serializer_medic.is_valid(raise_exception=True)
        medic = serializer_medic.save()
        
        serializer_address = AddressSerializer(data=request_address)
        serializer_address.is_valid(raise_exception=True)
        address = serializer_address.save()    
        
        medic.person.address_set.add(address, bulk=False)
        response = Response()
        response.data = {
            'medic':'medic register success',
            'id':medic.user.id
        }
        return response
class MedicView(APIView):
    def post(self, request):
        request.data['tipo'] = 'MED'
        serializer = MedicSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pat = serializer.save()
        response = Response()
        response.data = {
            'medic':'medic creation success',
            'id':pat.user.id
        }
        return response
    
    def get(self, request):
        token = request.COOKIES.get('jwt')
        payload = check_jwt_token(token)  
        medic = Medic.objects.filter(user__email=payload['email']).first()
        serializer = MedicSerializer(medic)
        return Response(serializer.data)
    def put(self, request):
        token = request.COOKIES.get('jwt')
        payload = check_jwt_token(token)  
        medic = Medic.objects.filter(user__email=payload['email']).first()
        if check_user_jwt(request, medic.user.email):
            data = request.data
            medic.crm = data["crm"] 
            data['person'] = medic.person.id
            data['user'] = medic.user.id
            serializer = MedicSerializer(medic,data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = Response()
            response.data = {
                'medic':'medic update success'
            }
            return response
        raise AuthenticationFailed('Not authenticated')
           
    def delete(self, request):
        token = request.COOKIES.get('jwt')
        payload = check_jwt_token(token)  
        medic = Medic.objects.filter(user__email=payload['email'])
        if check_user_jwt(request, medic.user.email):
            medic.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise AuthenticationFailed('Not authenticated')
class PatientView(APIView):
    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pat = serializer.save()
        response = Response()
        response.data = {
            'patient':'patient creation success',
            'id':pat.user.id
        }
        return response
    
    def get(self, request, pk):
        patient = Patient.objects.filter(id=int(pk)).first()
        serializer = PatientSerializer(patient)
        if check_user_jwt(request, patient.user.email):
            return Response(serializer.data)
        raise AuthenticationFailed('Not authenticated')
    def put(self, request, pk):
        patient = Patient.objects.filter(id=int(pk)).first()
        if check_user_jwt(request, patient.user.email):
            data = request.data
            patient.occupation = data["occupation"] 
            patient.kinship = data['kinship']
            data['person'] = patient.person.id
            data['user'] = patient.user.id
            serializer = PatientSerializer(patient,data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = Response()
            response.data = {
                'patient':'patient update success'
            }
            return response
        raise AuthenticationFailed('Not authenticated')
           
    def delete(self, request, pk):
        patient = Patient.objects.filter(id=int(pk))
        if check_user_jwt(request, patient.user.email):
            patient.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise AuthenticationFailed('Not authenticated')
    
class PersonView(APIView):
    def post(self, request):
        serializer = PersonSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def get(self, request):
        token = request.COOKIES.get('jwt')
        payload = check_jwt_token(token)
        person = get_person(payload)    
        serializer = PersonSerializer(person)
        return Response(serializer.data)
    def put(self, request,pk):
        token = request.COOKIES.get('jwt')
        payload = check_jwt_token(token)       
        person = get_person(payload)
        serializer = PersonSerializer(person,data=request.data)
        serializer.is_valid(raise_exception=True)    
        serializer.save()
        return Response(serializer.data)
    def delete(self, request, pk):
        token = request.COOKIES.get('jwt')
        payload = check_jwt_token(token)
        person = get_person(payload)
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AddressView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        payload = check_jwt_token(token)       
        person = get_person(payload)
        data = request.data
        serializer_address = AddressSerializer(data=data)
        serializer_address.is_valid(raise_exception=True)
        address = serializer_address.save()    
        person.address_set.add(address, bulk=False)
        response = Response()
        response.data = {
            'address':'address creation success'
        }
        return response

    
class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        serializer = UserSerializer(user)
        check_authentication(password, user)
        payload = {
            'email':serializer.data['email'],
            'tipo':user.tipo,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }
        
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt',value=token,httponly=True)
        response.data = {
            'jwt':token
        }
        return response   
         
    def get(self, request):
        token = request.COOKIES.get('jwt')
        payload = check_jwt_token(token)
        user = User.objects.filter(id=payload['email']).first()    
        serializer = UserSerializer(user)
        return Response(serializer.data)

def get_person(payload):
    if payload['tipo'] == 'PAT':
        patient = Patient.objects.filter(user__email=payload['email']).first()
        person = patient.person
    elif payload['tipo'] == 'MED':
        medic = Medic.objects.filter(user__email=payload['email']).first()
        person = medic.person
    return person

def check_authentication(password, user):
    if user is None:
        raise AuthenticationFailed("User not found!")
    if user.password == password:
        return True
    raise AuthenticationFailed("incorrect password!")
    
def check_jwt_token(token):
    if not token:
        raise AuthenticationFailed('Not authenticated')
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Not authenticated')
    return payload

def check_user_jwt(request, email):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Not authenticated')
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        if payload['email'] == email:
            return True
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Not authenticated')
    return False

class LogoutView(APIView):   
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message':'logout success'
        }
        return response