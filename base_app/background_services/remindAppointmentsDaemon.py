import threading
import time
import django
from ..models import Appointments

class RemindAppointmentsDaemon:

    def start(self):
        thread = threading.Thread(target=self.background_process)
        thread.daemon = True
        thread.start()

    def background_process(self):
        while True:
            self.remind_appointments()
            time.sleep(60*60)

    def remind_appointments(self):
        pass
        # Fetch all appointments that start in less than 3 hours and send 
        # asynchronous email to the client and lawyer.
