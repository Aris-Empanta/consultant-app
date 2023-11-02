import { getCsrfToken } from './csrf.js';

//We fetch all the unchecked appointments and show it in the navbar.
let uncheckedAppointments = document.getElementById('uncheckedAppointments')
let uncheckedAppointmentsWrapper = document.getElementById('uncheckedAppointmentsWrapper')
let amount = await getUncheckedAppointments()
let appointmentsNotificationBellButton = document.getElementById('appointmentsNotificationBellButton')

appointmentsNotificationBellButton.addEventListener('click', () => {
    // We hide the uncheckedAppointmentsWrapper and we set the inner 
    // text of uncheckedAppointmentsWrapper to 0.

    // We fetch all the lawyer's future appointments and we highlight the unchecked
    // All the appointments are links to the appointments page. 

    // We send http request to the backend to make all the lawyer's appointments 
    // checked field to True.
})

// The unchecked appointments amount circle will be shown only if there is at least 
// one unchecked appointment. 
if(amount > 0) {
    uncheckedAppointmentsWrapper.style.display = 'initial'
    uncheckedAppointments.innerText = amount
}

// We configure and handle the websocket client, which sends request 
// to our backend's consumer (websocket server).
const webHost = window.location.host;
const socket = new WebSocket(`ws://${webHost}/ws/book-appointment/`);

socket.onopen = () => {
    console.log('connection established')
}

socket.onmessage = async function(event) {

    let uncheckedAppointmentsAmount = await getUncheckedAppointments()
    uncheckedAppointmentsWrapper.style.display = 'initial'
    uncheckedAppointments.innerText = uncheckedAppointmentsAmount

    // We should handle the case of the modal being open and receiving notifications, 
    // when we might need to refetch the appointments.
};         

// The helper function to get the unchecked appointments
async function getUncheckedAppointments() {

    // We retrieve all the amount of the appointments that the lawyer 
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
}