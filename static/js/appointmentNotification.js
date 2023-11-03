import { getBookedAppointments, 
         getUncheckedAppointmentsAmount, 
         markAppointmentAsChecked } from './appointmentHelpers.js';

//We fetch all the unchecked appointments and show it in the navbar.
let uncheckedAppointments = document.getElementById('uncheckedAppointments')
let uncheckedAppointmentsWrapper = document.getElementById('uncheckedAppointmentsWrapper')
let amount = await getUncheckedAppointmentsAmount()
let appointmentsNotificationBellButton = document.getElementById('appointmentsNotificationBellButton')

appointmentsNotificationBellButton.addEventListener('click', async () => {
    
    // Intitially we just hide the indicator, so that we still know 
    // which messages are unchecked to highlight them.
    uncheckedAppointmentsWrapper.style.display = 'none'
    uncheckedAppointments.innerText = 0

    // We fetch all the lawyer's future appointments and we highlight the unchecked
    // All the appointments are links to the appointments page. 
    await getBookedAppointments()

    // We send http request to the backend to make all the lawyer's appointments 
    // checked field to True.
    await markAppointmentAsChecked()
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

    // If the appointments modal is open we refetch the notifications without 
    // a loader. If it is now, we show the unchecked appointments amount.
    let uncheckedAppointmentsAmount = await getUncheckedAppointmentsAmount()
    uncheckedAppointmentsWrapper.style.display = 'initial'
    uncheckedAppointments.innerText = uncheckedAppointmentsAmount
};         