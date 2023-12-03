# The views that render or redirect to a template.
from .template_views.login_logout import Login, Logout, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .template_views.register import QuestionSpecialty, RegisterUser
from .template_views.home import Home
from .template_views.oauth_handler import OauthHandler
from .template_views.register_lawyer import LawyerInfo, LawyerAvailableHours
from .template_views.profile import Profile
from .template_views.booked_appointments_page import BookedAppointmentsPage
from .template_views.update_profile_pic import UpdateProfilePic
from .template_views.update_user_fullname import UpdateUserFullname
from .template_views.messages_page import MessagesPage
from .template_views.delete_account import DeleteAccount
from .template_views.lawyers_search_results import LawyersSearchResults

# The views that work as an api. 
from .api_views.book_appointment import BookAppointment
from .api_views.get_unchecked_appointments import GetUncheckedAppointments
from .api_views.all_booked_appointments import AllBookedAppointments
from .api_views.mark_appointment_as_checked import MarkAppointmentAsChecked
from .api_views.get_unchecked_messages import GetUncheckedMessages
from .api_views.mark_messages_as_checked import MarkMessagesAsChecked
from .api_views.get_all_conversations import GetAllConversations
from .api_views.mark_messages_as_read import MarkMessagesAsRead
from .api_views.delete_past_appointments import DeletePastAppointments
from .api_views.remind_appointments import RemindAppointments
from .api_views.lawyer_ratings import LawyerRatings
from .api_views.cancel_appointment import CancelAppointment
from .api_views.areas_of_expertise import AreasOfExpertiseView
from .api_views.get_all_ratings import GetAllRatings