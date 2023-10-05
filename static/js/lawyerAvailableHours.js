//A method helping with date and time making even single digits 2 digit format e.g. 5 = 05
const twoDigitFormat = (number) => {

    return number < 10 ? "0" + number : number
}

let startingTimes = document.querySelectorAll(".startingTime")
let endingTimes = document.querySelectorAll(".endingTime")
let hoursScheduleWrapper = document.querySelector(".hoursScheduleWrapper")

for(let i =0; i<startingTimes.length; i++) {
    
    let examinedDate = new Date()
    examinedDate.setDate(examinedDate.getDate() + i)
    let timeNow = twoDigitFormat(examinedDate.getHours()) + ":" + twoDigitFormat(examinedDate.getMinutes());

    if(i===0) {
        // The starting hour for today should be from the time now and on.
        startingTimes[i].value = timeNow;

        // The starting time should start maximum at 22:59. Otherwise we don't 
        // let the choise of available hours.
        if(timeNow > "22:59") {
            hoursScheduleWrapper.style.display = "none";
        }

        //restrict today's time being less than current time.
        if(startingTimes[i].value < timeNow) {
            startingTimes[i].value = timeNow;
        }
    }

    startingTimes[i].addEventListener("change", () => {
            
        //We wont let the user choose as starting time after 22:59.
        if(startingTimes[i].value > "22:59") {
            startingTimes[i].value = "22:59";
        }

        //restrict today's time being less than current time.
        if(startingTimes[i].value < timeNow && i===0) {
            startingTimes[i].value = timeNow;
        }
        // The starting time should always be 1 hour prior the ending time, so we apply this 
        // restriction on starting time change.
        let endingTimeString = examinedDate.getFullYear() + "-" + twoDigitFormat(examinedDate.getMonth()) + "-" + 
                               twoDigitFormat(examinedDate.getDate()) + " " + endingTimes[i].value + ":00";
        let endingTimeDateObject = new Date(endingTimeString);  
        let oneHourBeforeTimestamp = endingTimeDateObject.setMinutes(endingTimeDateObject.getMinutes() - 60)
        let oneHourBeforeObject = new Date(oneHourBeforeTimestamp);  
        let oneHourBefore = twoDigitFormat(oneHourBeforeObject.getHours()) + ":" + twoDigitFormat(oneHourBeforeObject.getMinutes());

        if(startingTimes[i].value > oneHourBefore) {
            startingTimes[i].value = oneHourBefore
        }
    })

    endingTimes[i].addEventListener("change", () => {

        let startingTimeDateString  = examinedDate.getFullYear() + "-" + twoDigitFormat(examinedDate.getMonth()) + "-" + 
                                      twoDigitFormat(examinedDate.getDate()) + " " + startingTimes[i].value + ":00";

        // We set an ending time 1 hour later from the starting set time, and convert it 
        // to a string format of hh:mm
        let endingTimeDateObject = new Date(startingTimeDateString);
        let oneHourLaterTimestamp = endingTimeDateObject.setMinutes(endingTimeDateObject.getMinutes() + 60);
        let oneHourLaterDateObject = new Date(oneHourLaterTimestamp);        
        let oneHourLater = twoDigitFormat(oneHourLaterDateObject.getHours()) + ":" + twoDigitFormat(oneHourLaterDateObject.getMinutes());
        
        //We restrict the ending time to be one hour later from the starting time.
        if(endingTimes[i].value < oneHourLater) {
            endingTimes[i].value = oneHourLater
        }
    })
}