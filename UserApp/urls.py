from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from UserApp import views

app_name = 'user'
urlpatterns = [
    path('', views.PatientList.as_view()),
    path('<int:pk>/', views.PatientDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)