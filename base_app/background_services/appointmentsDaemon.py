from multiprocessing import Process
from time import sleep
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class AppointmentsDaemon:
    
    def start(self):
        process = Process(target=self.task,daemon=True)
        process.start()
        
    def task(self):
        while True:
            appointments = requests.get(os.getenv('DELETE_APPOINTMENTS_URL'))
            print(appointments)
            sleep(2)