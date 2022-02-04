from django.utils.functional import empty
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from UserApp.patientdto import PatientDTO
from UserApp.models import *
from UserApp.serializers import *
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
        medic = Medic.objects.filter(user__email=payload['email']).first()
        if check_user_jwt(request, medic.user.email):
            medic.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise AuthenticationFailed('Not authenticated')
class PrenatalView(APIView):
    def get(self, request,pk):
        token = request.COOKIES.get('jwt')
        payload = check_jwt_token(token)  
        medic = Medic.objects.filter(user__email=payload['email']).first()
        if check_user_jwt(request, medic.user.email):
            id = int(pk)
            if pk==0:
                prenatais = Prenatal.objects.filter(medic=medic)
                serializer = PrenatalSerializer(prenatais,many=True)
                return Response(serializer.data)
            else:
                prenatal = Prenatal.objects.filter(patient__id=id).first()
                serializer = PrenatalSerializer(prenatal)
                return Response(serializer.data)
        raise AuthenticationFailed('Not authenticated')         
    def put(self, request, pk):
        token = request.COOKIES.get('jwt')
        payload = check_jwt_token(token)  
        medic = Medic.objects.filter(user__email=payload['email']).first()
        if check_user_jwt(request, medic.user.email):
            prenatal_data = request.data
            prenatal = Prenatal.objects.get(id=int(pk))
            # prenatal_serializer = PrenatalSerializer(prenatal, prenatal_data)
            # prenatal_serializer.is_valid(raise_exception=True)
            # prenatal_serializer.save()
            if('start_date' in prenatal_data):
                prenatal.start_date = prenatal_data['start_date']
            if('ultrasound_gestational_start' in prenatal_data 
               and prenatal_data['ultrasound_gestational_start'] != ''):
                prenatal.ultrasound_gestational_start = prenatal_data['ultrasound_gestational_start']
            if('last_menstrual_period' in prenatal_data 
               and prenatal_data['last_menstrual_period'] != ''):
                prenatal.last_menstrual_period = prenatal_data['last_menstrual_period']
            if('don' in prenatal_data):
                prenatal.don = prenatal_data['don']
                prenatal.dopp = prenatal_data['dopp']
                prenatal.dopa = prenatal_data['dopa']
                prenatal.dg = prenatal_data['dg']
                prenatal.dcc = prenatal_data['dcc']
            prenatal.save()
            response = Response()
            response.data = {
                'patient':'prenatal update success'
            }
            return response
        raise AuthenticationFailed('Not authenticated')
class PatientView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        payload = check_jwt_token(token)  
        medic = Medic.objects.filter(user__email=payload['email']).first()
        if check_user_jwt(request, medic.user.email):
            patient_serializer = PatientSerializer(data=request.data['patient'])
            patient_serializer.is_valid(raise_exception=True)
            pat = patient_serializer.save()
            
            serializer_address = AddressSerializer(data=request.data['address'])
            serializer_address.is_valid(raise_exception=True)
            address = serializer_address.save()
            
            pat.person.address_set.add(address, bulk=False)
            
            prenatal_data = request.data['prenatal']
            prenatal = Prenatal()
            prenatal.patient = pat
            prenatal.medic = medic
            if('start_date' in prenatal_data):
                prenatal.start_date = prenatal_data['start_date']
            else:
                prenatal.start_date = datetime.datetime.utcnow()
            # prenatal.last_menstrual_period = prenatal_data['last_menstrual_period']
            # prenatal.ultrasound_gestational_start = prenatal_data['ultrasound_gestational_start']
            # prenatal.don = prenatal_data['don']
            # prenatal.dopp = prenatal_data['dopp']
            # prenatal.dopa = prenatal_data['dopa']
            # prenatal.dg = prenatal_data['dg']
            # prenatal.dcc = prenatal_data['dcc']
            prenatal.save()
            
            response = Response()
            response.data = {
                'patient':'patient creation success',
                'id':pat.user.id,
                'prenatalId': prenatal.id
            }
            return response
        raise AuthenticationFailed('Not authenticated')
    def get(self, request,pk):
        token = request.COOKIES.get('jwt')
        payload = check_jwt_token(token)  
        medic = Medic.objects.filter(user__email=payload['email']).first()
        if check_user_jwt(request, medic.user.email):
            id = int(pk)
            if pk==0:
                patients = []
                prenatais = Prenatal.objects.filter(medic=medic)
                for prenatal in prenatais:
                    patients.append(PatientDTO(prenatal.patient.id,
                                               prenatal.patient.person.name, 
                                               prenatal.patient.person.cpf,
                                               prenatal.patient.person.birt_date,
                                               prenatal.patient.user.email))
                serializer = PatientDTOSerializer(patients,many=True)
                return Response(serializer.data)

            else:
                patient = Patient.objects.filter(id=id).first()
                serializer = PatientSerializer(patient)
                return Response(serializer.data)
        raise AuthenticationFailed('Not authenticated')

    def put(self, request, pk):
        patient = Patient.objects.filter(id=int(pk)).first()
        if isAuthenticated(request):
            data = request.data
            PatientSerializer.updateCuston(instance=patient,data=data)
            response = Response()
            response.data = {
                'patient':'patient update success'
            }
            return response
        raise AuthenticationFailed('Not authenticated')
           
    def delete(self, request, pk):
        if isAuthenticated(request):
            id = int(pk)
            Patient.objects.filter(id=id).delete()
            Prenatal.objects.filter(patient__id=id).delete()
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
    def get(self, request,pk):
        if isAuthenticated(request):
            id = int(pk)
            patient = Patient.objects.filter(id=id).first()
            address = Address.objects.filter(person=patient.person)
            serializer = AddressSerializer(address, many=True)
            return Response(serializer.data)
        raise AuthenticationFailed('Not authenticated')
    
class AppointmentView(APIView):
    def post(self, request):
        if isAuthenticated(request):
            id = int(request.data['patient_id'])
            pre = Prenatal.objects.filter(patient__id=id).first()
            data = request.data['appointment']
            serializer = AppointmentSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            appointmentInstance = serializer.save()
            pre.appointment_set.add(appointmentInstance, bulk=False)
            response = Response()
            response.data = {
                'appointment':'appointment creation success',
                'patientId':id,
                'prenatalId': pre.id,
                'appointmentId' : appointmentInstance.id
            }
            return response
        raise AuthenticationFailed('Not authenticated')
    def get(self, request,pk):
        if isAuthenticated(request):
            id = int(pk)
            appointment = Appointment.objects.filter(id=id).first()
            serializer = AppointmentSerializer(appointment)
            return Response(serializer.data)
        raise AuthenticationFailed('Not authenticated')
    def put(self, request,pk):
        if isAuthenticated(request):
            id = int(pk)
            appointment = Appointment.objects.get(id=id)
            serializer = AppointmentSerializer(appointment,data=request.data)
            serializer.is_valid(raise_exception=True)    
            serializer.save()
            response = Response()
            response.data = {
                'appointment':'appointment update success'
            }
            return response
        raise AuthenticationFailed('Not authenticated')
    def delete(self, request, pk):
        if isAuthenticated(request):
            id = int(pk)
            Appointment.objects.filter(id=id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise AuthenticationFailed('Not authenticated')

class AppointmentsView(APIView):
     def get(self, request,pk):
        if isAuthenticated(request):
            id = int(pk)
            appointment = Appointment.objects.filter(prenatal__patient__id=id)
            serializer = AppointmentSerializer(appointment, many=True)
            return Response(serializer.data)
        raise AuthenticationFailed('Not authenticated')

class NumericExamView(APIView):
    def get(self, request,pk):
        if isAuthenticated(request):
            id = int(pk)
            exams = NumericMedicalExam.objects.filter(exam__prenatal__patient__id=id)
            serializer = NumericMedicalExamSerializer(exams, many=True)
            return Response(serializer.data)
        raise AuthenticationFailed('Not authenticated')
    def post(self, request):
        if isAuthenticated(request):
            id = int(request.data['patient_id'])
            pre = Prenatal.objects.filter(patient__id=id).first()
            serializer = NumericMedicalExamSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            exam_instance = serializer.save()
            pre.medicalexam_set.add(exam_instance.exam, bulk=False)
            return Response(serializer.data)
        raise AuthenticationFailed('Not authenticated')
    def put(self, request,pk):
        if isAuthenticated(request):
            id = int(pk)
            numeric_exam = NumericMedicalExam.objects.get(id=id)
            serializer = NumericMedicalExamSerializer(numeric_exam,data=request.data)
            serializer.is_valid(raise_exception=True)    
            serializer.save()
            response = Response()
            response.data = {
                'exam':'exam update success'
            }
            return response
        raise AuthenticationFailed('Not authenticated')
    def delete(self, request, pk):
        if isAuthenticated(request):
            id = int(pk)
            NumericMedicalExam.objects.filter(id=id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise AuthenticationFailed('Not authenticated')
class OtherExamView(APIView):
    def get(self, request,pk):
        if isAuthenticated(request):
            id = int(pk)
            exams = OtherExam.objects.filter(exam__prenatal__patient__id=id)
            serializer = OtherExamSerializer(exams, many=True)
            return Response(serializer.data)
        raise AuthenticationFailed('Not authenticated')
    def post(self, request):
        if isAuthenticated(request):
            id = int(request.data['patient_id'])
            pre = Prenatal.objects.filter(patient__id=id).first()
            serializer = OtherExamSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            exam_instance = serializer.save()
            pre.medicalexam_set.add(exam_instance.exam, bulk=False)
            return Response(serializer.data)
        raise AuthenticationFailed('Not authenticated')
    def put(self, request,pk):
        if isAuthenticated(request):
            id = int(pk)
            reagent_exam = OtherExam.objects.get(id=id)
            serializer = OtherExamSerializer(reagent_exam,data=request.data)
            serializer.is_valid(raise_exception=True)    
            serializer.save()
            response = Response()
            response.data = {
                'exam':'exam update success'
            }
            return response
        raise AuthenticationFailed('Not authenticated')
    def delete(self, request, pk):
        if isAuthenticated(request):
            id = int(pk)
            OtherExam.objects.filter(id=id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise AuthenticationFailed('Not authenticated')
       
class ReagentExamView(APIView):
    def get(self, request,pk):
        if isAuthenticated(request):
            id = int(pk)
            exams = ReagentExam.objects.filter(exam__prenatal__patient__id=id)
            serializer = ReagentExamSerializer(exams, many=True)
            return Response(serializer.data)
        raise AuthenticationFailed('Not authenticated')
    def post(self, request):
        if isAuthenticated(request):
            id = int(request.data['patient_id'])
            pre = Prenatal.objects.filter(patient__id=id).first()
            serializer = ReagentExamSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            exam_instance = serializer.save()
            pre.medicalexam_set.add(exam_instance.exam, bulk=False)
            return Response(serializer.data)
        raise AuthenticationFailed('Not authenticated')
    def put(self, request,pk):
        if isAuthenticated(request):
            id = int(pk)
            reagent_exam = ReagentExam.objects.get(id=id)
            serializer = ReagentExamSerializer(reagent_exam,data=request.data)
            serializer.is_valid(raise_exception=True)    
            serializer.save()
            response = Response()
            response.data = {
                'exam':'exam update success'
            }
            return response
        raise AuthenticationFailed('Not authenticated')
    def delete(self, request, pk):
        if isAuthenticated(request):
            id = int(pk)
            ReagentExam.objects.filter(id=id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        raise AuthenticationFailed('Not authenticated')
    
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
            'jwt':token,
            'userName': get_person(payload).name,
            'email': email,
            'tipo': user.tipo
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
def isAuthenticated(request):
    token = request.COOKIES.get('jwt')
    payload = check_jwt_token(token)
    medic = Medic.objects.filter(user__email=payload['email']).first()
    return check_user_jwt(request, medic.user.email)

class LogoutView(APIView):   
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message':'logout success'
        }
        return response