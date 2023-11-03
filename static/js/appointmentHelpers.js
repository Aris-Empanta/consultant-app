import { getCsrfToken } from './csrf.js';

// The helper function to get the Amount of the unchecked appointments
async function getUncheckedAppointmentsAmount() {

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

// The helper function to fetch all the booked appointments with checked/unchecked 
// flag sorted by date descending.
async function getBookedAppointments() {

}

// The helper function to send an HTTP request to the backend in order to mark all the 
// appointments of the lawyer as checked.
async function markAppointmentAsChecked() {

}

export { getBookedAppointments, getUncheckedAppointmentsAmount, markAppointmentAsChecked }