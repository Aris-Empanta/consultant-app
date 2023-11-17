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
    path('profile/<slug:username>/', views.Profile.as_view(), name="profile"),
    path('lawyer-info/', views.LawyerInfo.as_view(), name='lawyer_info'),
    path('lawyer-available-hours/', views.LawyerAvailableHours.as_view(), name='lawyer_available_hours'),
    path('book-appointment/', views.BookAppointment.as_view(), name='book_appointment'),
    path('unchecked-appointments/', views.GetUncheckedAppointments.as_view(), name='unchecked-appointments'),
    path('booked-appointments/', views.AllBookedAppointments.as_view(), name='booked_appointments'),
    path('mark-appointment-as-checked/', views.MarkAppointmentAsChecked.as_view(), name='mark_appointment_as_checked'),
    path('booked-appointments-page/', views.BookedAppointmentsPage.as_view(), name='booked_appointments_page' ),
    path('update-profile-pic/', views.UpdateProfilePic.as_view() , name='update_profile_pic'),
    path('update-user-fullname/', views.UpdateUserFullname.as_view(), name='update_user_fullname'),
    path('messages/<slug:username>/', views.MessagesPage.as_view() ,name='messages'),
    path('unchecked-messages/', views.GetUncheckedMessages.as_view(), name='unchecked-messages'),
    path('mark-messages-as-checked/', views.MarkMessagesAsChecked.as_view(), name='mark_messages_as_checked'),
    path('get-all-conversations/', views.GetAllConversations.as_view(), name="get_all_conversations"),
    path('mark-messages-as-read/', views.MarkMessagesAsRead.as_view(), name='mark_messages_as_read'),
    path('lawyer-ratings/', views.LawyerRatings.as_view(), name='lawyer_ratings'),
]

daemon_urls = [
    path('delete-past-appointments/', views.DeletePastAppointments.as_view(), name='delete_past_appointments'),
    path('remind-appointments/', views.RemindAppointments.as_view(), name='remind_appointments'),
]

urlpatterns += daemon_urls