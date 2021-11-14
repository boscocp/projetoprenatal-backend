from django.shortcuts import render
from django.views.decorators import csrf
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse, HttpResponse

from UserApp.models import User
from UserApp.serializers import UserSerializer
# Create your views here.

@csrf_exempt
def userApi(request,pk=1):
    if request.method=='GET':
        users = User.objects.all()
        users_serializer=UserSerializer(users,many=True)
        return JsonResponse(users_serializer.data,safe=False)
    elif request.method=='POST':
        user_data=JSONParser().parse(request)
        users_serializer=UserSerializer(data=user_data)
        if users_serializer.is_valid():
            users_serializer.save()
            return JsonResponse("User added Successfully",safe=False)
    elif request.method=='PUT':
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return HttpResponse(status=404)
        user_data=JSONParser().parse(request)
        users_serializer=UserSerializer(user,data=user_data)
        if users_serializer.is_valid():
            users_serializer.save()
            return JsonResponse("User update successfully",safe=False)
        return HttpResponse(status=400)
    elif request.method=='DELETE':
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return HttpResponse(status=404)
        user.delete()
        return JsonResponse("User deleted",safe=False)