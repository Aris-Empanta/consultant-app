let hoursScheduleWrapper = document.querySelectorAll(".hoursScheduleWrapper")

// We have to loop through each parent element of the available days for appointments 
// (hoursScheduleWrapper):
for(let i = 0; i < hoursScheduleWrapper.length; i++) {

    //We will format the year, month and day of the current date. This is the 
    //date we need for all the processes below.
    let examinedDate = new Date()
    examinedDate.setDate(examinedDate.getDate() + i)
    year = examinedDate.getFullYear()
    month = examinedDate.getMonth() < 12 ? twoDigitFormat(examinedDate.getMonth() + 1) : "01"
    day = twoDigitFormat(examinedDate.getDate())
    let timeNow = twoDigitFormat(examinedDate.getHours()) + ":" + twoDigitFormat(examinedDate.getMinutes());

    // The addIntervals button should be clickable only if the there is no interval or if the last interval's ending time is 
    //  <= 22:59 and the existing intervals are less than 2.
    let addIntervalsButton = document.querySelector(`.addIntervalButton${i+1}`)
    let currentHoursScheduleWrapper = document.getElementById(`hoursScheduleWrapperOfDay${i+1}`)
    let intervals = document.querySelectorAll(`.intervalOfDay${i+1}`)
    //The classes for the starting and ending time interval:
    let startingTime = document.querySelectorAll(`.startOfInterval${i+1}`)
    let endingTime = document.querySelectorAll(`.endOfInterval${i+1}`)

    //For the first starting time today, we give the current time as the initial value. 
    if(i===0) {
        startingTime[0].value = timeNow;

        // The initial value of the starting time today should examine that it has 1 hour difference from the ending time.
       // If that is not the case, we change the ending time.
       let startingTimeDateString  = year + "-" + month + "-" + day + " " + startingTime[0].value;
       let endingTimeDateString  = year + "-" + month + "-" + day + " " + endingTime[0].value;

        // We calculate the difference of starting and ending timestamp
        let startingTimestamp = new Date(startingTimeDateString).getTime();
        let endingTimestamp = new Date(endingTimeDateString).getTime();
        //We convert their difference to minutes
        let differenceInMinutes = (endingTimestamp - startingTimestamp) / 60000;
        
        // If they have difference more than 1 hour, we adjust the ending hour to 
        // be one hour after the starting time.
        if(differenceInMinutes < 60) {

            let endingTimeDateObject = new Date(startingTimeDateString)
            let oneHourLaterTimestamp = endingTimeDateObject.setMinutes(endingTimeDateObject.getMinutes() + 60);
            let oneHourLaterDateObject = new Date(oneHourLaterTimestamp);        
            let oneHourLater = twoDigitFormat(oneHourLaterDateObject.getHours()) + ":" + 
                               twoDigitFormat(oneHourLaterDateObject.getMinutes());

            endingTime[0].value = oneHourLater
        }

        // If the current time is after 22:59, we delete the date div.
        if(timeNow > '22:59') {

            hoursScheduleWrapper[i].remove();
        }

    }

    startingTime[0].addEventListener('change', () => {

        //The starting time can be >= the current time (for today) and <= the ending time
        
        //restrict today's time being less than current time.
        if(startingTime[0].value < timeNow && i===0) {
            startingTime[0].value = timeNow;
        }

        // The starting time should always be 1 hour prior the ending time, so we apply this 
        // restriction on starting time change.
        let endingTimeString = year+ "-" + month + "-" + day + " " + endingTime[0].value + ":00";
        let endingTimeDateObject = new Date(endingTimeString);  
        let oneHourBeforeTimestamp = endingTimeDateObject.setMinutes(endingTimeDateObject.getMinutes() - 60)
        let oneHourBeforeObject = new Date(oneHourBeforeTimestamp);  
        let oneHourBefore = twoDigitFormat(oneHourBeforeObject.getHours()) + ":" + twoDigitFormat(oneHourBeforeObject.getMinutes());

        if(startingTime[0].value > oneHourBefore) {
            startingTime[0].value = oneHourBefore
        }
        
    })

    //We set the validations and restrictions for the starting and ending time inputs that already 
    //exist before we use the addIntervalButton.
    endingTime[0].addEventListener('change', () => {

        //We can add an extra interval only if the ending time is <= 22:59
        if(endingTime[0].value <= "22:59") {
            addIntervalsButton.disabled = false
        } else {
            addIntervalsButton.disabled = true   
        }
        //The ending time should be at least one hour after the starting time.
        let startingTimeDateString  = year + "-" + month + "-" + day + " " + startingTime[0].value;

        // We set an ending time 1 hour later from the starting set time, and convert it 
        // to a string format of hh:mm
        let endingTimeDateObject = new Date(startingTimeDateString);
        let oneHourLaterTimestamp = endingTimeDateObject.setMinutes(endingTimeDateObject.getMinutes() + 60);
        let oneHourLaterDateObject = new Date(oneHourLaterTimestamp);        
        let oneHourLater = twoDigitFormat(oneHourLaterDateObject.getHours()) + ":" + twoDigitFormat(oneHourLaterDateObject.getMinutes());

        //We restrict the ending time to be one hour later from the starting time.
        if(endingTime[0].value < oneHourLater) {
            endingTime[0].value = oneHourLater
        }
    })

    // When we click the addIntervalsButton, a new pair of time intervals input should be created.
    addIntervalsButton.addEventListener("click", () => {
    
            //We create and append a span element to the div that contains the intervals
            let extraInterval = document.createElement("span")
            extraInterval.classList.add(`intervalOfDay${i+1}`);
            extraInterval.innerHTML = ` From                 
                                        <input type="time" value = "00:00" class="startingTime startOfInterval${i + 1}" name="time">
                                        To 
                                        <input class="endingTime endOfInterval${i + 1}" type="time" value="23:59">
                                        <button data-counter="${i + 1}" onclick="removeParentElement(this)">Remove</button>
                                        `
            currentHoursScheduleWrapper.appendChild(extraInterval);

            //We set the intervals variable again after the new added element.
            intervals = document.querySelectorAll(`.intervalOfDay${i+1}`)

            //If the intervals are 2 we disable the button.
            if(intervals.length === 2) {
                addIntervalsButton.disabled = true
            }

            //We will set event listeners for the newly created starting and ending time inputs.
    }) 
}

/*-----> WE SET SOME HELPER FUNCTIONS BELOW <------*/

//The function to remove an interval.
function removeParentElement(buttonElement) {
    var counter = buttonElement.getAttribute("data-counter");
    let addIntervalButton = document.querySelector(`.addIntervalButton${counter}`)

    // We enable the addIntervalButton once we remove an interval, since it will always 
    // be less than 2.
    addIntervalButton.disabled = false
    buttonElement.parentElement.remove();
}

//A method helping with date and time making even single digits 2 digit format e.g. 5 = 05
function twoDigitFormat(number){

    return number < 10 ? "0" + number : number
}