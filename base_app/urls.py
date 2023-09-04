from django.urls import path
from . import viewsFiles


urlpatterns = [
    path('', viewsFiles.Home.as_view(), name="home"),
    path('login/', viewsFiles.Login.as_view(), name="login"),
    path('question-specialty/', viewsFiles.QuestionSpecialty.as_view(), name="question-specialty"),  
    path('register-client/', viewsFiles.RegisterClient.as_view(), name="register-client"),
    path('register-lawyer/', viewsFiles.RegisterLawyer.as_view(), name="register-lawyer"),
]