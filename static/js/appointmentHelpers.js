import { getCsrfToken } from './csrf.js';

// The function to get the Amount of the unchecked appointments
async function getUncheckedAppointmentsAmount() {

    try {
        // We retrieve the amount of the appointments that the lawyer 
        // hasn't checked yet
        let url = `/unchecked-appointments/`
        let csrftoken = getCsrfToken()

        const request = new Request(url, {
            method: 'GET',
            headers: {
                'X-CSRFToken': csrftoken,
            },
            credentials: "same-origin"
        })

        const response = await fetch(request)

        // Check if the response status is OK (status code 200)
        if (!response.ok) {
            throw new Error('A Network error occured, please try again later.');
        }

        // We parse the JSON response
        let responseData = await response.json();
        let amount = responseData.amount


        return amount
    } catch (error) {
        // Handle any errors that occur during the fetch or response handling (change it in production)
        console.error('An unexpected error occured, please try again later');
    }
}

// The function to fetch all the booked appointments with checked/unchecked 
// flag sorted by date descending.
async function getBookedAppointments() {

    try {
        // We all the booked appointments of the lawyer
        let url = `/booked-appointments/`
        let csrftoken = getCsrfToken()

        const request = new Request(url, {
            method: 'GET',
            headers: {
                'X-CSRFToken': csrftoken,
            },
            credentials: "same-origin"
        })

        const response = await fetch(request)

        // Check if the response status is OK (status code 200)
        if (!response.ok) {
            throw new Error('A Network error occured, please try again later.');
        }

        // We parse the JSON response
        let responseData = await response.json();
        let appointments = responseData.booked_appointments

        return appointments
    } catch (error) {
        // Handle any errors that occur during the fetch or response handling (change it in production)
        console.error('An unexpected error occured, please try again later');
    }
}

// The function to show the appointments modal.
function showBookedAppointments(appointments, appointmentsModal, loadingAppointments) {

    loadingAppointments.style.display = 'none'
        
    // We empty the modal's content to refresh it for the case the modal was open.
    appointmentsModal.innerHTML = ''

    for(let i = 0; i < appointments.length; i++) {
        let appointmentDetails
        let currentAppointment = appointments[i]

        // We render diferent HTML for the checked and unchecked appointments.
        if(currentAppointment.checked) {
            appointmentDetails = `<div class="checkedAppointmentWrapper">
                                    <p>
                                        ${currentAppointment.client_first_name} 
                                        ${currentAppointment.client_last_name} 
                                        booked an appointment
                                    </p>  
                                    <p>${currentAppointment.time_since} ago</p>
                                    </div>`
        } else {
            appointmentDetails = `<div class="uncheckedAppointmentWrapper">
                                    <p>
                                        ${currentAppointment.client_first_name} 
                                        ${currentAppointment.client_last_name} 
                                        booked an appointment
                                    </p> 
                                    <p>${currentAppointment.time_since} ago</p>
                                    </div>`
        }
        
        appointmentsModal.insertAdjacentHTML('beforeend', appointmentDetails)
    }       
}

// The function to collapse the booked appointments modal
function hideBookedAppointments(appointmentsModal) {

    appointmentsModal.style.display = 'none'
}

// The function to send an HTTP request to the backend in order to mark all the 
// appointments of the lawyer as checked.
async function markAppointmentAsChecked() {
    
    try {
        const csrftoken = getCsrfToken();
        const url = '/mark-appointment-as-checked/';

        //We define the request attributes:
        const request = new Request(url, {
            method: 'PATCH', // Specify the HTTP method (e.g., GET, POST)
            headers: {
              'X-CSRFToken': csrftoken,
              'Content-Type': 'application/json', 
            },
            credentials: "same-origin"
          });

        // Use the Fetch API with async/await to make the GET request
        const response = await fetch(request);

        // Check if the response status is OK (status code 200)
        if (!response.ok) {
            throw new Error('A Network error occured, please try again later.');
        }
        } catch (error) {
            // Handle any errors that occur during the fetch or response handling (change it in production)
            console.error('An unexpected error occured, please try again later');
        }
}

export { getBookedAppointments, 
         getUncheckedAppointmentsAmount, 
         showBookedAppointments, 
         hideBookedAppointments,
         markAppointmentAsChecked }