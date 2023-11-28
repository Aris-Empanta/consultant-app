import { getCsrfToken } from './csrf.js';

const deleteAccountButton  = document.getElementById('deleteAccountButton')

deleteAccountButton.addEventListener('click', async () => {

    deleteAccountButton.style.backgroundColor = 'green'
    deleteAccountButton.innerHTML = 'Please Wait'

    try {
        const csrftoken = getCsrfToken();
        const url = `${window.location.origin}/delete-account/`;
                
        //We define the request attributes:
        const request = new Request(url, {
            method: 'DELETE',
            headers: {
              'X-CSRFToken': csrftoken,
              'Content-Type': 'application/json', 
            },
            credentials: "same-origin"
          });

        const response = await fetch(request);

        // Check if the response status is OK (status code 200)
        if (!response.ok) {
            deleteAccountButton.style.backgroundColor = 'red'
            deleteAccountButton.innerHTML = 'Delete Account'
            return alert('A Network error occured, please try again later.');
        }
        const data = await response.json()

        if(data.deleted) {
            deleteAccountButton.style.backgroundColor = 'blue'
            deleteAccountButton.innerHTML = 'Account Deleted!'

            setTimeout(() => {
                return window.location.href = '/';
            }, 2000)
            return 
        }

        deleteAccountButton.style.backgroundColor = 'red'
        deleteAccountButton.innerHTML = 'Delete Account'

        alert('A Network error occured, please try again later.');
    } catch (error) {
        console.log(error)
        // Handle any errors that occur during the fetch or response handling (change it in production)
        alert('An unexpected error occured, please try again later');
    }
})