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
    path('password-reset/', views.PasswordResetView.as_view(), name="password_reset"),
    path('password-reset/done/', views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password-reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password-reset/complete', views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('<slug:username>/', views.Profile.as_view(), name="lawyer_profile"),
    path('lawyer-info/', views.LawyerInfo.as_view(), name='lawyer_info'),
    path('lawyer-available-hours/', views.LawyerAvailableHours.as_view(), name='lawyer_available_hours'),
]