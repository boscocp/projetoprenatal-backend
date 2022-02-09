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
    path('appointments/<int:pk>', views.AppointmentsView.as_view()),
    path('appointment/<int:pk>', views.AppointmentView.as_view()),
    path('singup/', views.MedicRegisterView.as_view()),
    path('numericexam/', views.NumericExamView.as_view()),
    path('numericexam/<int:pk>', views.NumericExamView.as_view()),
    path('reagentexam/', views.ReagentExamView.as_view()),
    path('reagentexam/<int:pk>', views.ReagentExamView.as_view()),
    path('otherexam/', views.OtherExamView.as_view()),
    path('otherexam/<int:pk>', views.OtherExamView.as_view()),
    path('prenatal/', views.PrenatalView.as_view()),
    path('prenatal/<int:pk>', views.PrenatalView.as_view()),
    path('addendum/', views.AddendumView.as_view()),
    path('addendum/<int:pk>', views.AddendumView.as_view()),
    path('ultrassound/', views.UltrassoundExamView.as_view()),
    path('ultrassound/<int:pk>', views.UltrassoundExamView.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)