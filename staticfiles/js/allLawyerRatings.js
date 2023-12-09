const openALLRatingsModal = document.getElementById('openALLRatingsModal')
const allRatingsModalWrapper = document.getElementById('allRatingsModalWrapper')
const closeAllRatingsModal = document.getElementById('closeAllRatingsModal')
const loadingAllRatings = document.getElementById('loadingAllRatings')
const allRatingsModal = document.getElementById('allRatingsModal')
const allFetchedRatingsWrapper = document.getElementById('allFetchedRatingsWrapper')

// Rating lawyer modal should close with esc button
document.addEventListener('keydown', (event) => {

    if (event.key === 'Escape') {
        allRatingsModalWrapper.style.display = 'none'
    }
});

openALLRatingsModal.addEventListener('click', () => {

    openRatingsModal() 
    getAllLawyerRatings()   
})

closeAllRatingsModal.addEventListener('click', () => {
    
    allRatingsModalWrapper.style.display = 'none'
    loadingAllRatings.style.display = 'initial'
    allFetchedRatingsWrapper.innerHTML = ''
})

function openRatingsModal() {

    allRatingsModalWrapper.style.display = 'flex'
}

async function getAllLawyerRatings() {
    try {
        let urlFirstWord = '/profile/'
        let lawyerUsernameWithSlash = window.location.pathname.slice(urlFirstWord.length,)
        lawyerUsername = lawyerUsernameWithSlash.slice(0,lawyerUsernameWithSlash.length-1)

        // We retrieve the amount of the appointments that the lawyer 
        // hasn't checked yet
        let url = `/get-all-ratings/${lawyerUsername}`

        const request = new Request(url, {
            method: 'GET',
            credentials: "same-origin"
        })

        const response = await fetch(request)

        // Check if the response status is OK (status code 200)
        if (!response.ok) {
            throw new Error('A Network error occured, please try again later.');
        }

        // We parse the JSON response
        let responseData = await response.json();
        
        // We render all the fetched ratings to the UI
        renderAllRatings(responseData.all_ratings)

    } catch (error) {
        // Handle any errors that occur during the fetch or response handling (change it in production)
        alert('An unexpected error occured, please try again later');
    }
}

function renderAllRatings(ratings) {
    loadingAllRatings.style.display = 'none'
    allFetchedRatingsWrapper.style.display = 'flex'

    for(let i=0; i<ratings.length; i++ ) {

        let ratingHtml = `<div class="fetchedRatingInfoWrapper">
                            <div class="ratingClientImageAndName">
                                <img src="${ratings[i].avatar}" class="ratingClientAvatar">
                                <p class="ratingClientName">${ratings[i].first_name}</p>
                                <p class="ratingClientName">${ratings[i].last_name}</p>
                                <p class="clientRatingValue">${ratings[i].value}/5</p>
                            </div>                            
                            <p class="ratingClientComment">${ratings[i].comment}</p>
                          </div>`
        allFetchedRatingsWrapper.insertAdjacentHTML('beforeend', ratingHtml)
    }
}