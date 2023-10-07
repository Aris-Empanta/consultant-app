//A method helping with date and time making even single digits 2 digit format e.g. 5 = 05
const twoDigitFormat = (number) => {

    return number < 10 ? "0" + number : number
}
//The method to delete an available hours interval
const deleteInterval = () => {
    this.parentElement.remove()
}

let startingTimes = document.querySelectorAll(".startingTime")
let endingTimes = document.querySelectorAll(".endingTime")
let hoursScheduleWrapper = document.querySelector(".hoursScheduleWrapper")

for(let i =0; i<startingTimes.length; i++) {
    
    let examinedDate = new Date()
    examinedDate.setDate(examinedDate.getDate() + i)
    //We will format the year, month and day of the current date
    year = examinedDate.getFullYear()
    month = examinedDate.getMonth() < 12 ? twoDigitFormat(examinedDate.getMonth() + 1) : "01"
    day = twoDigitFormat(examinedDate.getDate())
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
        let endingTimeString = year+ "-" + month + "-" + day + " " + endingTimes[i].value + ":00";
        let endingTimeDateObject = new Date(endingTimeString);  
        let oneHourBeforeTimestamp = endingTimeDateObject.setMinutes(endingTimeDateObject.getMinutes() - 60)
        let oneHourBeforeObject = new Date(oneHourBeforeTimestamp);  
        let oneHourBefore = twoDigitFormat(oneHourBeforeObject.getHours()) + ":" + twoDigitFormat(oneHourBeforeObject.getMinutes());

        if(startingTimes[i].value > oneHourBefore) {
            startingTimes[i].value = oneHourBefore
        }
    })

    endingTimes[i].addEventListener("change", () => {

        let startingTimeDateString  = year + "-" + month + "-" + day + " " + startingTimes[i].value + ":00";

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

        if(endingTimes[i].value < "22:59") {
            addIntervalButton.disabled = false
        }
    })
    
    let startOfInterval = document.querySelectorAll(".startOfInterval" + (i + 1))
    let endOfInterval = document.querySelectorAll(".endOfInterval" + (i + 1))
    let currentHoursScheduleWrapper = document.querySelectorAll(".hoursScheduleWrapper")[i]

    if(endOfInterval < '22:59') {
        addIntervalButton.disabled = false
    }

    //The addIntervalButton for the examined date
    let addIntervalButton = document.querySelector(".addIntervalButton" + (i + 1))

    addIntervalButton.addEventListener("click", () => {

        //We create and append a span element
        let extraInterval = document.createElement("span")
        extraInterval.classList.add(`interval_${i+1}`);
        extraInterval.innerHTML = ` From                 
                                    <input type="time" value = "00:00" class="startingTime startOfInterval${i + 1}" name="time">
                                    To 
                                    <input class="endingTime endOfInterval${i + 1}" type="time" value="23:59">
                                    <button data-counter="${i + 1}" onclick="removeParentElement(this)">Delete</button>
                                   `

        currentHoursScheduleWrapper.appendChild(extraInterval)
        let intervalsStartingTime = document.querySelectorAll(`.startOfInterval${i + 1}`)
        let intervalsEndingTime = document.querySelectorAll(`.endOfInterval${i + 1}`)
        //The span elements of the hoursScheduleWrapper
        intervals = document.querySelectorAll(`.interval_${i+1}`)

        // If there are no intervals, the starting time takes the time now,
        // otherwise, the last ending time.
        if(intervals.length === 1) {
            intervalsStartingTime[0].value = timeNow
        } else {
            intervalsStartingTime[1].value = intervalsEndingTime[0].value
        }

    
        // I will add event listeners to all starting and ending times by 
        // looping through them, in order to validate the values. We technically
        // reapply the validations we applied in the initial tiume inputs.
        for(let j=0; j < intervalsStartingTime.length; j++) {
            
            // Ending time should be at least 1 hour after starting time
            intervalsEndingTime[j].addEventListener('change', () => {

                let startingTimeDateString  = year + "-" + month + "-" + day + " " + intervalsStartingTime[j].value + ":00";

                // We set an ending time 1 hour later from the starting set time, and convert it 
                // to a string format of hh:mm
                let endingTimeDateObject = new Date(startingTimeDateString);
                let oneHourLaterTimestamp = endingTimeDateObject.setMinutes(endingTimeDateObject.getMinutes() + 60);
                let oneHourLaterDateObject = new Date(oneHourLaterTimestamp);        
                let oneHourLater = twoDigitFormat(oneHourLaterDateObject.getHours()) + ":" + twoDigitFormat(oneHourLaterDateObject.getMinutes());
                
                //We restrict the ending time to be one hour later from the starting time.
                if(intervalsEndingTime[j].value < oneHourLater) {
                    intervalsEndingTime[j].value = oneHourLater
                }

                // If this is the last interval's ending time, the add intervals button should
                // be disabled if the time is after 22:59
                if(j === intervals.length - 1 && intervalsEndingTime[j].value > "22:59") {
                    addIntervalButton.disabled = true
                } else if(j === intervals.length - 1 && intervalsEndingTime[j].value <= "22:59"){
                    addIntervalButton.disabled = false
                }
                
                //The ending time should be less or equal to the next interval's starting time
                if(intervals.length === 2 ) {
                    if( j === intervals.length - 2 && 
                        intervalsEndingTime[j].value > intervalsStartingTime[j + 1].value) {
                            intervalsEndingTime[j].value = intervalsStartingTime[j + 1].value
                    }
                }
            })

            //Starting time should be at least the current time and on
            intervalsStartingTime[j].addEventListener('change', () => {

                //We wont let the user choose as starting time after 22:59.
                if(intervalsStartingTime[j].value > "22:59") {
                    intervalsStartingTime[j].value = "22:59";
                }
                //restrict today's time being less than current time, and for the second interval less than last ending time.
                if(intervalsStartingTime[j].value < timeNow && intervalsStartingTime.length === 1) {
                    intervalsStartingTime[j].value = timeNow;                    
                } else if( intervalsStartingTime.length > 1){
                    if(intervalsStartingTime[j].value < intervalsEndingTime[j-1].value) {
                        intervalsStartingTime[j].value = intervalsEndingTime[j-1].value;
                    }
                }

                // The starting time should always be 1 hour prior the ending time, so we apply this 
                // restriction on starting time change.
                let endingTimeString = year+ "-" + month + "-" + day + " " + intervalsEndingTime[j].value + ":00";
                let endingTimeDateObject = new Date(endingTimeString);  
                let oneHourBeforeTimestamp = endingTimeDateObject.setMinutes(endingTimeDateObject.getMinutes() - 60)
                let oneHourBeforeObject = new Date(oneHourBeforeTimestamp);  
                let oneHourBefore = twoDigitFormat(oneHourBeforeObject.getHours()) + ":" + twoDigitFormat(oneHourBeforeObject.getMinutes());

                if(intervalsStartingTime[j].value > oneHourBefore) {
                    intervalsStartingTime[j].value = oneHourBefore
                }
            })
        }
        
        //We will allow only two intervals for the lawyer to choose.
       if(intervals.length >= 2) {
            addIntervalButton.disabled = true
       }
       //The add intervals button will be disabled if the last ending time is after 22:59
       if(intervalsEndingTime[intervals.length-1] > "22:59") {
         addIntervalButton.disabled = true
       } 
    }) 

    
}

function removeParentElement(buttonElement) {
    var counter = buttonElement.getAttribute("data-counter");
    let addIntervalButton = document.querySelector(`.addIntervalButton${counter}`)

    addIntervalButton.disabled = false
    buttonElement.parentElement.remove();

}