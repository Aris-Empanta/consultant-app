openClientEditModal = document.getElementById('openClientEditModal')
editClientProfileModal = document.getElementById('editClientProfileModal')
closeClientEditModal = document.getElementById('closeClientEditModal')

openClientEditModal.addEventListener('click', () => {
    editClientProfileModal.style.display = 'flex'
})

closeClientEditModal.addEventListener('click', () => {
    editClientProfileModal.style.display = 'none'  
})