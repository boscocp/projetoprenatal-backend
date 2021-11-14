from os import name
from django.urls import path
from UserApp import views

app_name = 'user'
urlpatterns = [
    path('', views.userApi, name='user'),
    path('<int:pk>/', views.userApi, name='post')
]