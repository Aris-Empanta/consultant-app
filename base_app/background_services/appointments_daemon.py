from multiprocessing import Process
import socket
import time
from datetime import datetime
import requests
from requests import RequestException
import os
from dotenv import load_dotenv
from django.conf import settings

load_dotenv()

class AppointmentsDaemon:

    def __init__(self):
        self.running = True
    
    def start(self):
        if not self.running:
            self.running = True
            
        process = Process(target=self.task,daemon=True)
        process.start()

    def stop(self):
        self.running = False
        
    def task(self):
        while self.running:
            try:
                remind_appointment_headers = {'Api-Key': os.getenv('API_KEY')}
                remind_appointments = requests.post(os.getenv('REMIND_APPOINTMENTS_URL'),
                                                    headers=remind_appointment_headers)
                response = remind_appointments.json()
                print(response['message'])

                # We will delete the past appointments every midnight.
                hour_now = int(datetime.now().strftime('%H'))

                if hour_now == 15:
                    delete_appointments_headers = {'Api-Key': os.getenv('API_KEY')}
                    delete_appointments = requests.delete(os.getenv('DELETE_APPOINTMENTS_URL'), 
                                                          headers=delete_appointments_headers)
                    response = delete_appointments.json()
                    print(response['message'])
            except socket.error as e:
                # We retry to start the process after 2 seconds if the 
                # "Port is occupied error" appears
                print(f"Port is already in use. Retrying in 2 seconds.")
                time.sleep(2) 
                continue
            except RequestException as e:
                print(f"An error occurred during the request: {e}")
            except Exception as e:
                print(f"General Exception in Daemon: {e}")


            # The daemon will run every 10 minutes for the appointments reminder.
            time.sleep(10 * 60)