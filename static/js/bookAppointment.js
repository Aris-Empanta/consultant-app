import { getCsrfToken } from './csrf.js';

const openBookAppointmentModalButton = document.getElementById('bookAppointment')

openBookAppointmentModalButton.addEventListener('click', () => {

    let modal = document.getElementById('appointmentsModalWrapper')

    modal.style.display = 'flex'
})

const closeAppointmentsModal = document.getElementById('closeAppointmentsModal')

closeAppointmentsModal.addEventListener('click', () => {

    let modal = document.getElementById('appointmentsModalWrapper')

    modal.style.display = 'none'
})

const bookAppointmentButton = document.querySelectorAll('.bookAppointmentButton')

for(let i=0; i < bookAppointmentButton.length; i++) {

    bookAppointmentButton[i].addEventListener('click', async () => {  

        try {
            const csrftoken = getCsrfToken();
            const url = '/book-appointment/';
            
            // We extract the lawyer's username from the url
            let lawyerUsernameWithSlashes = window.location.href.split('profile')[1]
            // We remove the remaining slashes forward and after
            let lawyerUsername = lawyerUsernameWithSlashes.substring(1, lawyerUsernameWithSlashes.length - 1)
            
            // We start the loading spinner
            startLoading(bookAppointmentButton[i])
            
            //The date and time of the appointment to be sent to the backend.
            let appointmentDateAndTime = document.querySelectorAll('.appointmentDateAndTime')[i].value

            //We define the request attributes:
            const request = new Request(url, {
                method: 'PATCH', // Specify the HTTP method (e.g., GET, POST)
                headers: {
                  'X-CSRFToken': csrftoken,
                  'Content-Type': 'application/json', 
                },
                // Include the request body, if applicable
                body: JSON.stringify({ 'lawyer': lawyerUsername, 
                                       'appointment_date_and_time': appointmentDateAndTime }),
                credentials: "same-origin"
              });

            // Use the Fetch API with async/await to make the GET request
            const response = await fetch(request);

            // Check if the response status is OK (status code 200)
            if (!response.ok) {
                throw new Error('A Network error occured, please try again later.');
            }

            // We parse the JSON response
            const responseData = await response.json();

            //handle data 
            if(responseData.data === 'Booked!') {

                appointmentSuccessfullyBooked(bookAppointmentButton[i], responseData.data)
            } else {
                //Create Modal later
                alert(responseData.data)
            }

            setTimeout(() => location.reload(), 2000);
        } catch (error) {
            // Handle any errors that occur during the fetch or response handling (change it in production)
            console.error('An unexpected error occured, please try again later');
        }
    })
}

function startLoading(button) {
    
    button.innerText = `Please Wait`
    button.style.backgroundColor = 'red'
}

function appointmentSuccessfullyBooked(button, response) {

    button.innerText = response
    button.style.backgroundColor = 'green'
}