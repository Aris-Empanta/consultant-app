from django.apps import AppConfig

class BaseAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base_app'

    def ready(self):
        from .background_services.appointmentsDaemon import AppointmentsDaemon

        appointments_daemon = AppointmentsDaemon()
        appointments_daemon.start()
        # from .background_services.deleteAppointmentsDaemon import DeleteAppointmentsDaemon
        # from .background_services.remindAppointmentsDaemon import RemindAppointmentsDaemon

        # delete_appointments_daemon = DeleteAppointmentsDaemon()
        # remind_appointments_daemon = RemindAppointmentsDaemon()

        # delete_appointments_daemon.start()
        # remind_appointments_daemon.start()