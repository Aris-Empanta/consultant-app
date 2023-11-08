let authenticatedLawyerInfo = document.getElementById('authenticatedLawyerInfo')
let editLawyerInfoForm = document.getElementById('editLawyerInfoForm')
let editLawyerInfoButton = document.getElementById('editLawyerInfoButton')
let cancelUpdatingLawyerInfo = document.getElementById('cancelUpdatingLawyerInfo')
let lawyerInfoLink = document.getElementById('lawyerInfoLink')
let lawyerAvailableHoursLink = document.getElementById('lawyerAvailableHoursLink')
let lawyerAppointmentsLink = document.getElementById('lawyerAppointmentsLink')
let lawyerInfoWrapper = document.getElementById('lawyerEditableInfoWrapper')
let availableHoursWrapper = document.getElementById('editableLawyerAvailableHoursWrapper')
let appointmentsWrapper = document.getElementById('lawyerAppointmentsWrapper')
let editLawyerProfileInfoModal = document.getElementById('editLawyerProfileInfoModal')
let editLawyerProfileInfoButton = document.getElementById('editLawyerProfileInfoButton')

editLawyerInfoButton.addEventListener('click', () => {
    authenticatedLawyerInfo.style.display = 'none'
    editLawyerInfoForm.style.display = 'flex'
    lawyerAvailableHoursLink.disabled = true
    lawyerAppointmentsLink.disabled = true
})

editLawyerProfileInfoButton.addEventListener('click', () => {
    editLawyerProfileInfoModal.style.display='flex'
    console.log('pressed')
})

cancelUpdatingLawyerInfo.addEventListener('click', (e) => {
    e.preventDefault()
    editLawyerInfoForm.style.display = 'none'
    authenticatedLawyerInfo.style.display = 'initial'
    lawyerAvailableHoursLink.disabled = false
    lawyerAppointmentsLink.disabled = false
})

lawyerInfoLink.addEventListener('click', () => {
    lawyerInfoWrapper.style.display = 'initial'
    availableHoursWrapper.style.display = 'none'
    appointmentsWrapper.style.display = 'none'
})

lawyerAvailableHoursLink.addEventListener('click', () => {
    lawyerInfoWrapper.style.display = 'none'
    availableHoursWrapper.style.display = 'initial'
    appointmentsWrapper.style.display = 'none'
})

lawyerAppointmentsLink.addEventListener('click', () => {
    lawyerInfoWrapper.style.display = 'none'
    availableHoursWrapper.style.display = 'none'
    appointmentsWrapper.style.display = 'initial'
})