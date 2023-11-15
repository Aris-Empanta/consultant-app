import threading
import time
import django
from ..models import Appointments

class DeleteAppointmentsDaemon:

    def start(self):
        thread = threading.Thread(target=self.background_process)
        thread.daemon = True
        thread.start()

    def background_process(self):
        while True:
            self.delete_past_appointments()
            time.sleep(60*60)

    def delete_past_appointments(self):
        pass
        # With the filter method, and maybe Q, fetch all the appointments 
        # that ending time date is more than 2 hours and delete them.