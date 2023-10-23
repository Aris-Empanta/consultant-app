authenticatedLawyerInfo = document.getElementById('authenticatedLawyerInfo')
editLawyerInfoForm = document.getElementById('editLawyerInfoForm')
editLawyerInfoButton = document.getElementById('editLawyerInfoButton')
cancelUpdatingLawyerInfo = document.getElementById('cancelUpdatingLawyerInfo')

editLawyerInfoButton.addEventListener('click', () => {
    authenticatedLawyerInfo.style.display = 'none'
    editLawyerInfoForm.style.display = 'flex'
})

cancelUpdatingLawyerInfo.addEventListener('click', (e) => {
    e.preventDefault()
    editLawyerInfoForm.style.display = 'none'
    authenticatedLawyerInfo.style.display = 'initial'
})