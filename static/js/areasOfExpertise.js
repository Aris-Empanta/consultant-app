const areasOfExpertiseDropdownList = document.getElementById('areasOfExpertiseDropdownList')
const showAreasOfExpertiseButton = document.getElementById('showAreasOfExpertiseButton')
const areasOfExpertiseSearchInput = document.getElementById('areasOfExpertiseSearchInput')
const areasOfExpertiseloader = document.getElementById('areasOfExpertiseloader')
const searchAreasOfExpertiseArrow = document.getElementById('searchAreasOfExpertiseArrow')

// Once we click the arrow down button we show all the areas of expertise
showAreasOfExpertiseButton.addEventListener('click', async () => {

    let areasOfExpertise = await fetchAreasOfExpertise('all')
})

// Once we write in the areas of expertise input it makes api call to 
// fetch areas of expertise that contain the word we wrote - case insensitive.
areasOfExpertiseSearchInput.addEventListener('input', async () => {

    let input = areasOfExpertiseSearchInput.value
    let areasOfExpertise = await fetchAreasOfExpertise(input)
})

//When we click out of the input box it stops any data fetching
window.addEventListener('click', () => {
    exitFetchingData()
})

async function fetchAreasOfExpertise(areaOfExpertise) {

    waitingForData()

    areaOfExpertise = areaOfExpertise.trim()

    if(areaOfExpertise === '') {
        areaOfExpertise = 'none'
    }

    try {
        const url = `/areas-of-expertise/${areaOfExpertise}/`;

        //We define the request attributes:
        const request = new Request(url, {
            method: 'GET', // Specify the HTTP method (e.g., GET, POST)
            headers: {
              'Content-Type': 'application/json', 
            },
            credentials: "same-origin"
          });

        // Use the Fetch API with async/await to make the GET request
        const response = await fetch(request);

        // Check if the response status is OK (status code 200)
        if (!response.ok) {

            exitFetchingData()
            showNoResults()
            return
        }
        let responseData = await response.json();

        dataSuccessfullyFetched(responseData)

        return responseData.areas
    } catch (error) {
        exitFetchingData()
        console.log(error)
        showNoResults()
    }
}

function waitingForData() {

    areasOfExpertiseloader.style.display = 'initial'
    searchAreasOfExpertiseArrow.style.display = 'none'
    areasOfExpertiseDropdownList.style.display = 'none'
}

function exitFetchingData() {

    areasOfExpertiseDropdownList.style.display = 'none'
    areasOfExpertiseloader.style.display = 'none'
    searchAreasOfExpertiseArrow.style.display = 'initial'
}

function dataSuccessfullyFetched(data) {

    areasOfExpertiseloader.style.display = 'none'
    searchAreasOfExpertiseArrow.style.display = 'initial'
    areasOfExpertiseDropdownList.style.display = 'flex'
    let areas = data.areas

    areasOfExpertiseDropdownList.innerHTML = ''

    if(areas === 'none') {
        exitFetchingData()
        return
    }

    if(areas.length > 0) {
        // logic to show areas
        areasOfExpertiseDropdownList.innerHTML = '<p>All areas</p>'
        return
    } 

    showNoResults()

    // logic to inform that no areas with that name exist

    //areasOfExpertiseDropdownList.insertAdjacentHTML('beforeend', conversationPreview)
}

function showNoResults() {
    areasOfExpertiseloader.style.display = 'none'
    searchAreasOfExpertiseArrow.style.display = 'initial'
    areasOfExpertiseDropdownList.style.display = 'flex'

    // First we clear the areas of expertise box
    areasOfExpertiseDropdownList.innerHTML = ''

    // Then we append the message
    areasOfExpertiseDropdownList.innerHTML = '<p>No results</p>'
}