let editLawyerInfoButton = document.getElementById('editLawyerInfoButton')
let closeUpdateLawyerInfoModalButton = document.getElementById('closeUpdateLawyerInfoModalButton')
let updateLawyerInfoWrapper = document.getElementById('updateLawyerInfoWrapper')
let lawyerInfoLink = document.getElementById('lawyerInfoLink')
let lawyerAvailableHoursLink = document.getElementById('lawyerAvailableHoursLink')
let lawyerAppointmentsLink = document.getElementById('lawyerAppointmentsLink')
let editLawyerProfileInfoButton = document.getElementById('editLawyerProfileInfoButton')
let editLawyerProfileInfoModal = document.getElementById('editLawyerProfileInfoModal')
let lawyerInfoWrapper = document.getElementById('lawyerEditableInfoWrapper')
let availableHoursWrapper = document.getElementById('editableLawyerAvailableHoursWrapper')
let appointmentsWrapper = document.getElementById('lawyerAppointmentsWrapper')

//The function to open the lawyer info edit modal
editLawyerInfoButton.addEventListener('click', () => {
    updateLawyerInfoWrapper.style.display = 'flex'
})

//The function to close the lawyer info update modal in lawyer's profile
closeUpdateLawyerInfoModalButton.addEventListener('click', (e) => {
    e.preventDefault();
    updateLawyerInfoWrapper.style.display = 'none'
})

//The function to edit the lawyer's full name.
editLawyerProfileInfoButton.addEventListener('click', () => {
    editLawyerProfileInfoModal.style.display='flex'
})

//The function to show only the lawyer's info in lawyer's profile
lawyerInfoLink.addEventListener('click', () => {
    lawyerInfoWrapper.style.display = 'initial'
    availableHoursWrapper.style.display = 'none'
    appointmentsWrapper.style.display = 'none'
})

//The function to show only the lawyer's available hours in lawyer's profile
lawyerAvailableHoursLink.addEventListener('click', () => {
    lawyerInfoWrapper.style.display = 'none'
    availableHoursWrapper.style.display = 'initial'
    appointmentsWrapper.style.display = 'none'
})

//The function to show only the lawyer's booked appointments in lawyer's profile
lawyerAppointmentsLink.addEventListener('click', () => {
    lawyerInfoWrapper.style.display = 'none'
    availableHoursWrapper.style.display = 'none'
    appointmentsWrapper.style.display = 'initial'
})