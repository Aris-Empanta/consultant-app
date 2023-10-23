authenticatedLawyerInfo = document.getElementById('authenticatedLawyerInfo')
editLawyerInfoForm = document.getElementById('editLawyerInfoForm')
editLawyerInfoButton = document.getElementById('editLawyerInfoButton')
cancelUpdatingLawyerInfo = document.getElementById('cancelUpdatingLawyerInfo')
lawyerInfoLink = document.getElementById('lawyerInfoLink')
lawyerAvailableHoursLink = document.getElementById('lawyerAvailableHoursLink')
lawyerAppointmentsLink = document.getElementById('lawyerAppointmentsLink')
lawyerInfoWrapper = document.getElementById('lawyerEditableInfoWrapper')
availableHoursWrapper = document.getElementById('editableLawyerAvailableHoursWrapper')
appointmentsWrapper = document.getElementById('lawyerAppointmentsWrapper')

editLawyerInfoButton.addEventListener('click', () => {
    authenticatedLawyerInfo.style.display = 'none'
    editLawyerInfoForm.style.display = 'flex'
    lawyerAvailableHoursLink.disabled = true
    lawyerAppointmentsLink.disabled = true
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