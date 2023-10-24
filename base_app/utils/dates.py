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
        # We onvert starting_time and ending_time to aware datetime objects
        starting_time = starting_time
        ending_time = ending_time

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
                    appointment_model = Appointments(interval=available_hours_model,
                                                     booked=False,
                                                     starting_time=appointment["starting"],
                                                     ending_time=appointment["ending"])
                    appointment_model.save()

        except IntegrityError as e:
            print(f"IntegrityError: {e}")
        except Exception as e:
            print(f"General Exception: {e}")
    
    def update_ending_time(lawyer, ending_time_1, ending_time_2):
        try:
            with transaction.atomic():
                interval = AvailableHours.objects.filter(lawyer=lawyer, ending_time=ending_time_1)
                ending_time_1 = ending_time_2
                interval.update(ending_time=ending_time_1)
        except IntegrityError as e:
            print(f"IntegrityError: {e}")
        except Exception as e:
            print(f"General Exception: {e}")

    # The following method takes the AvailableHours Queryset and 
    # creates a list of dictionaries with the following format: 
    # { dayname: str, date: str, intervals: [{starting_time: str, ending_time: str}, .... ]}
    @staticmethod
    def format_available_hours_list(available_hours):
        available_hours_list = list(available_hours)

        # if 2 intervals have the same date, we concatonate them to a list.
        for i in range(len(available_hours_list)):
            
            if available_hours_list[i-1] is not None and i-1 >= 0:
                previous_interval_date = available_hours_list[i-1].starting_time.strftime('%d/%m/%Y')
            else:
                continue
            current_interval_date = available_hours_list[i].starting_time.strftime('%d/%m/%Y')

            if previous_interval_date == current_interval_date:
                available_hours_list[i-1] = [available_hours_list[i-1], available_hours_list[i]]
                available_hours_list[i] = None

        while None in available_hours_list:
            available_hours_list.remove(None)
        # print(available_hours_list)

        
        available_hours = list()

        # We fillup the available hours list to be used with the following format:
        # { dayname: str, date: str, intervals: [{starting_time: str, ending_time: str}, .... ]}
        for i in range(len(available_hours_list)):
            available_hours_in_day_dict = dict()

            if type(available_hours_list[i]) == list:
                available_hours_in_day_dict['dayname'] = available_hours_list[i][0].starting_time.strftime("%A")
                available_hours_in_day_dict['date'] = available_hours_list[i][0].starting_time.strftime("%d/%m/%Y")
                available_hours_in_day_dict['intervals'] = [{'starting_time': available_hours_list[i][0].starting_time.strftime("%H:%M"),
                                                             'ending_time': available_hours_list[i][0].ending_time.strftime("%H:%M")}, 
                                                             {'starting_time': available_hours_list[i][1].starting_time.strftime("%H:%M"),
                                                             'ending_time': available_hours_list[i][1].ending_time.strftime("%H:%M")}]
                
            else:
                available_hours_in_day_dict['dayname'] = available_hours_list[i].starting_time.strftime("%A")
                available_hours_in_day_dict['date'] = available_hours_list[i].starting_time.strftime("%d/%m/%Y")
                available_hours_in_day_dict['intervals'] = [{'starting_time': available_hours_list[i].starting_time.strftime("%H:%M"),
                                                             'ending_time': available_hours_list[i].ending_time.strftime("%H:%M")}]
                
            available_hours.append(available_hours_in_day_dict)
       
        return available_hours