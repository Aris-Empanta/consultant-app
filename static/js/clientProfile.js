const editClientFullName = document.getElementById('editClientFullName');
const clientFullname = document.getElementById('clientFullname');
const editClientFullNameForm = document.getElementById('editClientFullNameForm');
const cancelUpdateClientFullname = document.getElementById('cancelUpdateClientFullname');

// The listener to show the input fields to update client's fullname
editClientFullName.addEventListener('click', () => {

    clientFullname.style.display = 'none';
    editClientFullName.style.display = 'none';
    editClientFullNameForm.style.display = 'flex';
})

// The listener to cancel the update of the client's fullname
cancelUpdateClientFullname.addEventListener('click', (e) => {
    e.preventDefault();
    editClientFullNameForm.style.display = 'none';
    clientFullname.style.display = 'flex';
    editClientFullName.style.display = 'flex';
})