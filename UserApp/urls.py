from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from UserApp import views

app_name = 'user'
urlpatterns = [
    path('patient/', views.PatientView.as_view()),
    path('patient/<int:pk>', views.PatientView.as_view()),
    path('register/', views.UserView.as_view()),
    path('person/', views.PersonView.as_view()),
    path('person/<int:pk>', views.PersonView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('medic/', views.MedicView.as_view()),
    path('address/', views.AddressView.as_view()),
    path('address/<int:pk>', views.AddressView.as_view()),
    path('appointment/', views.AppointmentView.as_view()),
    path('appointment/<int:pk>', views.AppointmentView.as_view()),
    path('singup/', views.MedicRegisterView.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)