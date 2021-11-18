from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from UserApp import views

app_name = 'user'
urlpatterns = [
    path('', views.PatientView.as_view()),
    path('<int:pk>', views.PatientView.as_view()),
    path('register/', views.UserView.as_view()),
    path('person/', views.PersonView.as_view()),
    path('person/<int:pk>', views.PersonView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)