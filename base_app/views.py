# The views that render or redirect to a template.
from .template_views.login_logout import Login, Logout, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .template_views.register import QuestionSpecialty, RegisterUser
from .template_views.home import Home
from .template_views.oauth_handler import OauthHandler
from .template_views.register_lawyer import LawyerInfo, LawyerAvailableHours
from .template_views.profile import Profile
from .template_views.bookedAppointmentsPage import BookedAppointmentsPage
from .template_views.updateProfilePic import UpdateProfilePic
from .template_views.updateUserFullname import UpdateUserFullname
from .template_views.messagesPage import MessagesPage

# The views that work as an api. 
from .api_views.bookAppointment import BookAppointment
from .api_views.getUncheckedAppointments import GetUncheckedAppointments
from .api_views.allBookedAppointments import AllBookedAppointments
from .api_views.markAppointmentAsChecked import MarkAppointmentAsChecked
from .api_views.getUncheckedMessages import GetUncheckedMessages
from .api_views.markMessagesAsChecked import MarkMessagesAsChecked
from .api_views.getAllConversations import GetAllConversations
from .api_views.markMessagesAsRead import MarkMessagesAsRead
from .api_views.deletePastAppointments import DeletePastAppointments
from .api_views.remindAppointments import RemindAppointments
from .api_views.lawyerRatings import LawyerRatings