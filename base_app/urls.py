from django.urls import path
from . import views


urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('login/', views.Login.as_view(), name="login"),
    path('question-specialty/', views.QuestionSpecialty.as_view(), name="question-specialty"),  
    path('register-client/', views.RegisterClient.as_view(), name="register-client"),
    path('register-lawyer/', views.RegisterLawyer.as_view(), name="register-lawyer"),
]