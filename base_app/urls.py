from django.urls import path
from . import views 


urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('login/', views.Login.as_view(), name="login"),
    path('logout/', views.Logout.as_view(), name="logout"),
    path('examine-oauth/', views.OauthHandler.as_view(), name="examine-oauth"),
    path('question-specialty/', views.QuestionSpecialty.as_view(), name="question-specialty"),  
    path('register-client/', views.RegisterUser.as_view(lawyerRegister = False), name="register-client"),
    path('register-lawyer/', views.RegisterUser.as_view(lawyerRegister = True), name="register-lawyer"),
]