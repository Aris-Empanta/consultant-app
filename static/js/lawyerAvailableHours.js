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

// The ending time should be at least one hour later than the starting time.
let oneHourLaterTimestamp = today.setMinutes(today.getMinutes() + 60)
let oneHourLaterDateObject = new Date(oneHourLaterTimestamp);
let oneHourLater = twoDigitFormat(oneHourLaterDateObject.getHours()) + ":" + twoDigitFormat(oneHourLaterDateObject.getMinutes()) + ":" + "00";

endingTime.min = oneHourLater

endingTime.addEventListener('change', () => {
    
    if (endingTime.value < endingTime.min) {
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

    })
}
