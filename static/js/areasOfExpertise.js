import { getCsrfToken } from './csrf.js';

const areasOfExpertiseDropdownList = document.getElementById('areasOfExpertiseDropdownList')
const showAreasOfExpertiseButton = document.getElementById('showAreasOfExpertiseButton')
const areasOfExpertiseSearchInput = document.getElementById('areasOfExpertiseSearchInput')
const areasOfExpertiseloader = document.getElementById('areasOfExpertiseloader')
const searchAreasOfExpertiseArrow = document.getElementById('searchAreasOfExpertiseArrow')

// Once we click the arrow down button we show all the areas of expertise
showAreasOfExpertiseButton.addEventListener('click', async () => {
    
    let areasOfExpertise = await fetchAreasOfExpertise('all')
    addChangeFocusHanders()
})

// Once we write in the areas of expertise input it makes api call to 
// fetch areas of expertise that contain the word we wrote - case insensitive.
areasOfExpertiseSearchInput.addEventListener('input', async () => {

    let input = areasOfExpertiseSearchInput.value
    let areasOfExpertise = await fetchAreasOfExpertise(input)
    addChangeFocusHanders()
})

// If in the input we press the arrow down button the focus will go to 
// the first area of expertise in the list (if exists)
areasOfExpertiseSearchInput.addEventListener('keydown', (event) => {

    if (event.key === 'ArrowDown') {
        let areas = document.querySelectorAll('.eachAreaOfExpertise')

        if(areas.length > 0) {
            areas[0].focus()
        }
    }
  }
)

//When we click out of the input box it stops any data fetching
window.addEventListener('click', () => {
    exitFetchingData()
})

// The function to fetch the areas of expertsise that match the user's input
async function fetchAreasOfExpertise(areaOfExpertise) {

    waitingForData()

    areaOfExpertise = areaOfExpertise.trim()

    if(areaOfExpertise === '') {
        areaOfExpertise = 'none'
    }

    try {
        const url = `/areas-of-expertise/`;
        const csrftoken = getCsrfToken()

        //We define the request attributes:
        const request = new Request(url, {
            method: 'POST', // Specify the HTTP method (e.g., GET, POST)
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/json', 
            },
            body: JSON.stringify({ 'areaOfExpertise': areaOfExpertise}),
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
        areasOfExpertiseDropdownList.innerHTML = '<p class="areasPreviewTitle">All areas</p>'

        for(let i=0; i<areas.length; i++) {
            let area = `<div class="eachAreaOfExpertise" tabindex="-1">
                        <p>${areas[i]}</p>
                        </div>`
            areasOfExpertiseDropdownList.innerHTML += area
        }

        //We make each area of expertise to populate the search input onclick
        const eachAreaOfExpertise = document.querySelectorAll('.eachAreaOfExpertise')

        for(let i=0; i < eachAreaOfExpertise.length; i++) {
            eachAreaOfExpertise[i].addEventListener('click', () => {

                let areaValue = eachAreaOfExpertise[i].innerText
                areasOfExpertiseSearchInput.value = areaValue
            })
        }
        return
    } 
 
    showNoResults()
}

function showNoResults() {
    areasOfExpertiseloader.style.display = 'none'
    searchAreasOfExpertiseArrow.style.display = 'initial'
    areasOfExpertiseDropdownList.style.display = 'flex'

    // First we clear the areas of expertise box
    areasOfExpertiseDropdownList.innerHTML = ''

    // Then we append the message
    areasOfExpertiseDropdownList.innerHTML = '<p class="areasPreviewTitle">No results found</p>'
}

let areasOfExpertiseInput = document.getElementById('areasOfExpertiseSearchInput')

//The listener to choose areas of expertise with the keydown and keyup
areasOfExpertiseInput.addEventListener('keydown', async () => {

    if (areasOfExpertiseDropdownList.style.display !== 'flex') {

        let areasOfExpertise = await fetchAreasOfExpertise('all');

        if(document.activeElement===document.getElementById('areasOfExpertiseSearchInput')) {
            addChangeFocusHanders()       
        }
    } 
})

function addChangeFocusHanders() {

    // If the focus is in the areas of expertise input element we change it to the first area 
    // of expertise. Then we put listeners to all the areas of expertise div elements so that 
    // the focus changes with keydown and key up.
    let areas = document.querySelectorAll('.eachAreaOfExpertise')
    
    // We add the listeners we need to all areas of expertise divs
    for (let i = 0; i < areas.length; i++) {           
        
        // The listeners to change focus on arrow down and arrow up
        areas[i].addEventListener('keydown', (event) => {

            if (event.key === 'ArrowDown') {

                if(document.activeElement===areas[areas.length-1] ) {

                    areas[0].focus()
                    return
                }
        
                if(document.activeElement === areas[i]) {
                    areas[i + 1].focus()
                }
            } else if (event.key === 'ArrowUp') {

                if(document.activeElement===areas[0]) {
                    areas[areas.length-1].focus()
                    return
                }

                if(document.activeElement!==areas[0]) {
                    areas[i-1].focus()
                }
            } else if (event.key ==='Enter') {
                
                let focusedArea = document.activeElement.querySelector('p').innerText

                areasOfExpertiseDropdownList.style.display = 'none'
                areasOfExpertiseSearchInput.value = focusedArea
            }                
        })   
        
        //it changes focus on hover
        areas[i].addEventListener('mouseover', () => {
            areas[i].focus()
        })
    }
}