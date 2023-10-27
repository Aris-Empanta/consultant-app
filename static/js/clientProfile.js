const openClientEditModal = document.getElementById('openClientEditModal')
const editClientProfileModal = document.getElementById('editClientProfileModal')
const closeClientEditModal = document.getElementById('closeClientEditModal')

openClientEditModal.addEventListener('click', () => {
    editClientProfileModal.style.display = 'flex'
})

closeClientEditModal.addEventListener('click', () => {
    editClientProfileModal.style.display = 'none'  
})