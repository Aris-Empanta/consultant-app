from django.apps import AppConfig
import os

class BaseAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base_app'

    # def ready(self):
    #     # We avoid creating 2 processes by default.
    #     run_once = os.environ.get('CMDLINERUNNER_RUN_ONCE') 

    #     if run_once is not None:
    #         return
        
    #     os.environ['CMDLINERUNNER_RUN_ONCE'] = 'True'

    #     # We start the daemon that handles the appointments in a new process
    #     from .background_services.appointments_daemon import AppointmentsDaemon
    #     import time

    #     appointments_daemon = AppointmentsDaemon()
    #     appointments_daemon.start()