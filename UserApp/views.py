from django.utils.functional import empty
from rest_framework import generics, serializers
from rest_framework import response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from UserApp.models import Patient, User, Person
from UserApp.serializers import PatientSerializer, UserSerializer, PersonSerializer
import jwt, datetime
from rest_framework import status

# Create your views here.
class PatientView(APIView):
    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = Response()
        response.data = {
            'patient':'patient creation success'
        }
        return response
    
    def get(self, request, pk):
        patient = Patient.objects.filter(person__cpf=pk).first()
        serializer = PatientSerializer(patient)
        return Response(serializer.data)
    
    def put(self, request, pk):
        patient = Patient.objects.filter(person__cpf=pk).first()
        data = request.data
        patient.occupation = data["occupation"] 
        patient.kinship = data['kinship']
        data['person'] = patient.person.id
        data['user'] = patient.user.id
        serializer = PatientSerializer(patient,data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
        
class PersonView(APIView):
    def post(self, request):
        serializer = PersonSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def get(self, request, pk):
        #token = request.COOKIES.get('jwt')
        #payload = check_jwt_token(token)
        person = Person.objects.filter(cpf=pk).first()    
        serializer = PersonSerializer(person)
        return Response(serializer.data)
    def put(self, request,pk):
        #token = request.COOKIES.get('jwt')
        #payload = check_jwt_token(token)
        person = Person.objects.filter(cpf=pk).first()
        serializer = PersonSerializer(person,data=request.data)
        serializer.is_valid(raise_exception=True)    
        serializer.save()
        return Response(serializer.data)
    def delete(self, request, pk):
        #token = request.COOKIES.get('jwt')
        #payload = check_jwt_token(token)
        person = Person.objects.filter(cpf=pk)
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
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
            'id':serializer.data['id'],
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
        user = User.objects.filter(id=payload['id']).first()    
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
def check_authentication(password, user):
    if user is None:
        raise AuthenticationFailed("User not found!")
    if not user.check_password(password):
        raise AuthenticationFailed("incorrect password!")
    
def check_jwt_token(token):
    if not token:
        raise AuthenticationFailed('Not authenticated')
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Not authenticated')
    return payload

class LogoutView(APIView):   
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message':'logout success'
        }
        return response