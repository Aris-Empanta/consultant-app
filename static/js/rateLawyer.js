import { getCsrfToken } from './csrf.js';

const rateLawyerButton = document.getElementById('rateLawyerButton')

if(rateLawyerButton) {
    const rateLawyerModal = document.getElementById('ratingLawyerModalWrapper')
    const closeRateLawyerModalButton = document.getElementById('closeRateLawyerModalButton')
    const submitLawyerRatingButton = document.getElementById('submitLawyerRatingButton')

    // The functionality to show/hide the lawyer's rating modal
    rateLawyerButton.addEventListener('click', () => {
        rateLawyerModal.style.display = 'flex'
    })

    closeRateLawyerModalButton.addEventListener('click', () => {
        rateLawyerModal.style.display = 'none'
    })

    submitLawyerRatingButton.addEventListener('click', async () => {

        try {
            const csrftoken = getCsrfToken();
            const url = '/lawyer-ratings/';
            
            //Start the loader
            waitingForRating()

            // We extract the lawyer's username from the url
            let lawyerUsernameWithSlashes = window.location.href.split('profile')[1]
            // We remove the remaining slashes forward and after
            let lawyerUsername = lawyerUsernameWithSlashes.substring(1, lawyerUsernameWithSlashes.length - 1)
            
            let rating = document.getElementById('lawyerRatingNumber').value
            let comments = document.getElementById('lawyerRatingComments').value

            //We define the request attributes:
            const request = new Request(url, {
                method: 'POST', 
                headers: {
                  'X-CSRFToken': csrftoken,
                  'Content-Type': 'application/json', 
                },
                // Include the request body, if applicable
                body: JSON.stringify({ 
                                       'lawyer': lawyerUsername, 
                                       'rating': rating,
                                       'comments': comments
                                      }),
                credentials: "same-origin"
              });

            // Use the Fetch API with async/await to make the GET request
            const response = await fetch(request);

            // Check if the response status is OK (status code 200)
            if (!response.ok) {
                restoreRatingSubmitButton()
                return alert('A Network error occured, please try again later.');
            }

            ratingSubmitted()
        } catch (error) {
            // Handle any errors that occur during the fetch or response handling (change it in production)
            restoreRatingSubmitButton()
           alert('An unexpected error occured, please try again later');
        }
    })

    function waitingForRating() {
        submitLawyerRatingButton.innerHTML = 'Please Wait'
        submitLawyerRatingButton.style.backgroundColor = 'green'
    }

    function ratingSubmitted() {
        submitLawyerRatingButton.innerHTML = 'Rating submited!'
        submitLawyerRatingButton.style.backgroundColor = 'blue'
        setTimeout(() => window.location.reload(), 2000)
    }

    function restoreRatingSubmitButton() {
        submitLawyerRatingButton.innerHTML = 'Submit'
        submitLawyerRatingButton.style.backgroundColor = 'silver'
    }
}