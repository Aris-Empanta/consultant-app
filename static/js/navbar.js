const navbarAvatar = document.getElementById('navbarAvatar')
const navbarAccountMenu = document.getElementById('navbarAccountMenu')
const messagesPreviewModal = document.getElementById('messagesPreviewModal')
const appointmentsModal = document.getElementById('appointmentsModal')

navbarAvatar.addEventListener('click', () => {

    const messagesModal = document.getElementById('messagesPreviewModal')
    const appointmentsModal= document.getElementById('appointmentsModal')

    if (navbarAccountMenu.style.display !== 'flex') {
        navbarAccountMenu.style.display = 'flex';
        messagesModal.style.display = 'none';
        appointmentsModal.style.display = 'none';
    } else {
        navbarAccountMenu.style.display = 'none'
    }
})