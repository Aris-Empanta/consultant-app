from .template_views.login_logout import Login, Logout, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .template_views.register import QuestionSpecialty, RegisterUser
from .template_views.home import Home
from .template_views.oauth_handler import OauthHandler
from .template_views.register_lawyer import LawyerInfo, LawyerAvailableHours
from .template_views.profile import Profile
from .api_views.bookAppointment import BookAppointment
from .api_views.checkAppointment import CheckAppointment
from .api_views.allBookedAppointments import AllBookedAppointments