import { getCsrfToken } from './csrf.js';

 const cancelAppointmentButtons = document.querySelectorAll('.cancelAppointmentButton')
 const appointmentDates = document.querySelectorAll('.appointmentDates')
 const startingTimes = document.querySelectorAll('.startingTimes')

 // We add the functionality to cancel appointment to all the buttons.
 for(let i=0; i<cancelAppointmentButtons.length; i++) {

    cancelAppointmentButtons[i].addEventListener('click', async() => {

        cancelAppointmentButtons[i].style.backgroundColor = 'rgb(105, 53, 156)'
        cancelAppointmentButtons[i].innerHTML = 'Please Wait'

        try {
            const csrftoken = getCsrfToken();
            const url = '/cancel-appointment/';
            
            // We send the starting time which will be unique for both lawyer and 
            // client to find the appointment.
            let starting_time = appointmentDates[i].innerText + ' ' + startingTimes[i].innerText
    
            const request = new Request(url, {
                    method: 'PATCH', 
                    headers: {
                      'X-CSRFToken': csrftoken,
                      'Content-Type': 'application/json', 
                    },
                    // Include the request body, if applicable
                    body: JSON.stringify({ 
                                           'starting_time': starting_time
                                          }),
                    credentials: "same-origin"
                  })

            const response = await fetch(request);

            // Check if the response status is OK (status code 200)
            if (!response.ok) {
                cancelAppointmentButtons[i].style.backgroundColor = '#D2122E'
                cancelAppointmentButtons[i].innerHTML = 'Cancel Appointment'
                return alert('A Network error occured, please try again later.');
            }    
            cancelAppointmentButtons[i].style.backgroundColor = '#4286A8'
            cancelAppointmentButtons[i].innerHTML = 'Appointment Cancelled'

            setTimeout(() => window.location.reload(), 2000)
        } catch (error) {
                cancelAppointmentButtons[i].style.backgroundColor = '#D2122E'
                cancelAppointmentButtons[i].innerHTML = 'Cancel Appointment'
               alert('An unexpected error occured, please try again later');
            }
     })
 }