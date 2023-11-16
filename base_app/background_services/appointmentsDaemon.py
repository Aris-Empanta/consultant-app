from multiprocessing import Process
import time
from datetime import datetime
import requests
from requests import RequestException
import os
from dotenv import load_dotenv

load_dotenv()

class AppointmentsDaemon:
    
    def start(self):
        process = Process(target=self.task,daemon=True)
        process.start()
        
    def task(self):
        while True:
            try:
                remind_appointment_headers = {'Api-Key': os.getenv('REMIND_APPOINTMENTS_API_KEY')}
                remind_appointments = requests.post(os.getenv('REMIND_APPOINTMENTS_URL'),
                                                    headers=remind_appointment_headers)
                response = remind_appointments.json()
                print(response['message'])

                # We will delete the past appointments every midnight.
                hour_now = int(datetime.now().strftime('%H'))

                if hour_now == 0:
                    delete_appointments_headers = {'Api-Key': os.getenv('DELETE_APPOINTMENTS_API_KEY')}
                    delete_appointments = requests.delete(os.getenv('DELETE_APPOINTMENTS_URL'), 
                                                        headers=delete_appointments_headers)
                    response = delete_appointments.json()
                    print(response['message'])
            except RequestException as e:
                print(f"An error occurred during the request: {e}")

            # The daemon will run every 10 minutes for the appointments reminder.
            time.sleep(10*60)