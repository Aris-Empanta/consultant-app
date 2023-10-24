import math
from datetime import timedelta
from ..models import AvailableHours, Appointments
from django.db import IntegrityError, transaction

class DateUtils:    

    @staticmethod
    def render_day_name(day_number):    
        match day_number:
            case 1:
                return "Monday"
            case 2:
                return "Tuesday"
            case 3:
                return "Wednesday"
            case 4:
                return "Thursday"
            case 5:
                return "Friday"
            case 6:
                return "Saturday"
            case 7:
                return "Sunday"
            
    @staticmethod
    def generate_appointments_per_interval(starting_time, ending_time, duration, breaks):
        interval_length = ending_time - starting_time
        interval_length_in_minutes = interval_length.total_seconds() / 60
        appointments_per_interval = math.floor(interval_length_in_minutes / (duration + breaks))
        #The amount in minutes of the duration and the break time combined.
        duration_and_breaks_combined = duration + breaks
        
        # Now, we will create a list with this format: index: {starting: datetime, ending: datetime} 
        # rendering each appointments starting and ending time.
        appointments = list()

        for x in range(appointments_per_interval):
            starting_ending_times_dict = dict()
            deviation_from_interval_start = duration_and_breaks_combined * (x)
            starting_ending_times_dict["starting"] = starting_time + timedelta(minutes=deviation_from_interval_start)
            starting_ending_times_dict["ending"] = starting_ending_times_dict["starting"] + timedelta(minutes=duration)
            appointments.append(starting_ending_times_dict)

        return appointments
    
    @staticmethod
    def save_intervals_and_appointments(lawyer,starting_time, ending_time ,appointments_per_interval):
        try:
            with transaction.atomic():
                # First we save the interval of available hours
                available_hours_model = AvailableHours(lawyer = lawyer,
                                                       starting_time = starting_time,
                                                       ending_time = ending_time)
                available_hours_model.save()
                # Then we save all the appointments
                for appointment in appointments_per_interval:
                    print(appointment)
                    appointment_model = Appointments(interval=available_hours_model,
                                                     booked=False,
                                                     starting_time=appointment["starting"],
                                                     ending_time=appointment["ending"])
                    appointment_model.save()

        except IntegrityError as e:
            print(f"IntegrityError: {e}")
        except Exception as e:
            print(f"General Exception: {e}")

    # The following method takes the AvailableHours Queryset and 
    # creates a list of dictionaries with the following format: 
    # {day_name: str, date: str, starting_time: str, ending_time: str}
    @staticmethod
    def create_formatted_available_hours_list(available_hours):
        available_hours_list = list(available_hours)

        for i in range(len(available_hours_list)):
            print(available_hours_list[i].starting_time.strftime('%d/%m/%Y'))
        
        # for i in range(len(available_hours_list)):
        #     interval_dictionary = dict()
        #     interval_dictionary['day_name'] = available_hours_list[i].starting_time.strftime('%A')
        #     interval_dictionary['date'] = available_hours_list[i].starting_time.strftime('%d/%m/%Y')
        #     interval_dictionary['intervals'] =  f"{available_hours_list[i].starting_time.strftime('%H:%M')}/{available_hours_list[i].ending_time.strftime('%H:%M')}"
        #     available_hours_list[i] = interval_dictionary
        
        return available_hours_list