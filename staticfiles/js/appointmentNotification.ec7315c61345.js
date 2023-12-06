import { getBookedAppointments, 
         getUncheckedAppointmentsAmount, 
         showBookedAppointments,
         hideBookedAppointments,
         markAppointmentAsChecked } from './appointmentHelpers.js';

//We fetch all the unchecked appointments and show it in the navbar.
let uncheckedAppointments = document.getElementById('uncheckedAppointments')
let uncheckedAppointmentsWrapper = document.getElementById('uncheckedAppointmentsWrapper')
let amount = await getUncheckedAppointmentsAmount()
let appointmentsNotificationBellButton = document.getElementById('appointmentsNotificationBellButton')
let loadingAppointments = document.getElementById('loadingAppointments')
let appointmentsModal = document.getElementById('appointmentsModal')


appointmentsNotificationBellButton.addEventListener('click', async () => {

    messagesPreviewModal.style.display = 'none'
    navbarAccountMenu.style.display = 'none'

    // If the modal is open we close it.
    if(appointmentsModal.style.display === 'flex') {

        hideBookedAppointments(appointmentsModal)
        appointmentsModal.innerHTML = `<p id="appointmentsModalTitle">Appointments</p>
                                        <div id="loadingAppointments"></div>`
        await markAppointmentAsChecked()
        return
    }
    
    // Intitially we just hide the indicator, so that we still know 
    // which messages are unchecked to highlight them, and we show 
    // the appointments modal.
    appointmentsModal.style.display = 'flex'
    uncheckedAppointmentsWrapper.style.display = 'none'
    uncheckedAppointments.innerText = 0

    // We fetch all the lawyer's future appointments and we highlight the unchecked
    // All the appointments are links to the appointments page. 
    let appointments = await getBookedAppointments()
    
    showBookedAppointments(appointments, appointmentsModal, loadingAppointments)

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

socket.onmessage = async (event) => {

    // When the appointments modal is closed:
    if(appointmentsModal.style.display !== 'flex') {

        let uncheckedAppointmentsAmount = await getUncheckedAppointmentsAmount()
        uncheckedAppointmentsWrapper.style.display = 'initial'
        uncheckedAppointments.innerText = uncheckedAppointmentsAmount
        return
    }
   // When the appointments modal is open:
   let appointments = await getBookedAppointments()
    
   showBookedAppointments(appointments, appointmentsModal, loadingAppointments)
};         