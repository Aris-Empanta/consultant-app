//A method helping with date and time making even single digits 2 digit format e.g. 5 = 05
const twoDigitFormat = (number) => {

    return number < 10 ? "0" + number : number
}

let startingTime = document.querySelector(".startingTime")
let endingTime = document.querySelector(".endingTime")
let hoursScheduleWrapper = document.querySelector(".hoursScheduleWrapper")

// The first starting hour should be from the current 
// time and on. 
let today = new Date();
let timeNow = twoDigitFormat(today.getHours()) + ":" + twoDigitFormat(today.getMinutes()) + ":" + "00"
startingTime.value = timeNow

//The starting time should start maximum at 22:59
if(timeNow > "22:59") {
    hoursScheduleWrapper.style.display = "none";
}

startingTime.addEventListener("change", () => {
    
    if(startingTime.value > "22:59") {
        startingTime.value = "22:59";
    }
})



endingTime.addEventListener('change', () => {

    startingTimeFullDate = today.getFullYear() + "-" + twoDigitFormat(today.getMonth()) + 
                           "-" + twoDigitFormat(today.getDate()) + " " + startingTime.value
    
    startingTimeDateObject = new Date(startingTimeFullDate)

    // The ending time should be at least one hour later than the starting time.
    let oneHourLaterTimestamp = startingTimeDateObject.setMinutes(startingTimeDateObject.getMinutes() + 60)
    let oneHourLaterDateObject = new Date(oneHourLaterTimestamp);
    let oneHourLater = twoDigitFormat(oneHourLaterDateObject.getHours()) + ":" + twoDigitFormat(oneHourLaterDateObject.getMinutes());
    
    if (endingTime.value < oneHourLater) {
        endingTime.value = oneHourLater;
    }
  }
)

//Now we will apply the same logic for all the other days:
let startingTimes = document.querySelectorAll(".startingTime")
let endingTimes = document.querySelectorAll(".endingTime")

for(let i=1; i<startingTimes.length; i++) {
    //starting time should always be maximum 22:59
    startingTimes[i].addEventListener("change", () => {
        if(startingTimes[i].value > "22:59") startingTimes[i].value = "22:59"
    })
    
    // ending time should have 1 hour distance
    endingTimes[i].addEventListener("change", () => {

        //With the procedure below we estimate the date and time one hour later of the starting time.
        let date = new Date()
        date.setDate(date.getDate() + i)
        let dateString  = date.getFullYear() + "-" + twoDigitFormat(date.getMonth()) + "-" + 
                    twoDigitFormat(date.getDate()) + " " + startingTimes[i].value

        let examinedDate = new Date(dateString)
        examinedDate.setMinutes(examinedDate.getMinutes() + 60)

        let oneHourLater = twoDigitFormat(examinedDate.getHours()) + ":" + twoDigitFormat(examinedDate.getMinutes()) ;

        if(endingTimes[i].value < oneHourLater) {
            endingTimes[i].value = oneHourLater
        }
    })
}

//ADD EVENT LISTENERS TO THE STARTING TIME TO EXAMINE THE ENDING TIME AND IF THEY HAVE 1 HOUR DIFFERENCE TO CONVERT IT.
