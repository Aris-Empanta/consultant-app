let areasOfExpertiseButton = document.getElementById("areasOfExpertiseButton");
let areasOfExpertiseList = document.getElementById("areasOfExpertiseList")

areasOfExpertiseButton.addEventListener("click", (event) => {
    
    event.preventDefault();
    
    if (areasOfExpertiseList.style.display !== "flex") {
  
        return areasOfExpertiseList.style.display = "flex";
    }
    
    return areasOfExpertiseList.style.display = "none";
})
 
//We allow only integers in the following fields:
document.addEventListener("keydown", (event) => {

    if (event.target.name === "yearsOfExperience" || event.target.name === "hourlyRate") {

        if(event.key === "e" || event.key === "." ||  
           event.key === "-" || event.key === ","
           || event.key === "+") {

            event.preventDefault();
           }
        }

        if (event.target.name === "yearsOfExperience") {

            if(event.target.value > 80) {
              
                event.target.value = 80
              }
            }   
})

document.addEventListener("change", (event) => {
    if(event.target.name === "hourlyRate") {
        
        if(event.target.value < 0 ) {
          
            event.target.value = 0
          }
        }
})

//I set maximu values or the following fields:
document.addEventListener("change", (event) => {

    if (event.target.name === "yearsOfExperience") {

        if(event.target.value > 80) 
            event.target.value = 80
        }
    
    if (event.target.name === "hourlyRate") {

        if(event.target.value > 100) 
            event.target.value = 100
        }
})

//The areas of expertise window should close if we click anywhere
//in the page. 
document.addEventListener("click", (event) => {
   
    if(event.target.id !== "areasOfExpertiseButton" && 
       event.target.type !== "checkbox") {
        areasOfExpertiseList.style.display = "none";
    }
})

// The listeners to change color depending the profile details area
const infoLink = document.getElementById('lawyerInfoLink')
const availableHoursLink = document.getElementById('lawyerAvailableHoursLink')
const appointmentsLink = document.getElementById('lawyerAppointmentsLink')

infoLink.addEventListener('click', () => {
    highlightProfileLink(infoLink, availableHoursLink, appointmentsLink)
})

availableHoursLink.addEventListener('click', () => {
    highlightProfileLink(availableHoursLink, appointmentsLink, infoLink)
})

appointmentsLink.addEventListener('click', () => {
    highlightProfileLink(appointmentsLink, infoLink, availableHoursLink)
})

function highlightProfileLink(highlightLink, secondLink, thirdLink) {

    highlightLink.style.backgroundColor = 'rgb(218, 228, 235)'
    secondLink.style.backgroundColor = 'transparent'
    thirdLink.style.backgroundColor = 'transparent'
}