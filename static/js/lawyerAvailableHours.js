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

        console.log("change starting time")
            
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

        console.log(startOfInterval)

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

        //The span elements of the hoursScheduleWrapper
        intervals = document.querySelectorAll(`.interval_${i+1}`)

        let secondIntervalStartingTime = document.querySelectorAll(`.startOfInterval${i + 1}`)
        let previousEndingIntervalTime = document.querySelector(`.endOfInterval${i + 1}`)

        console.log(previousEndingIntervalTime)
        //The starting time of the new interval will take either the previous ending
        //time or if not exist the current time
        if(previousEndingIntervalTime) {
            secondIntervalStartingTime[intervals.length - 1].value = previousEndingIntervalTime.value
        } else {
            startOfInterval[0].value = timeNow
        }
        
        //We will allow only two intervals for the lawyer to choose.
       if(intervals.length >= 2) {
            addIntervalButton.disabled = true
       }
    }) 

    /*
        The problem starts when I delete all the intervals. It allows to add interval even if ending hour > 22:59,
        and choose ending hour less than starting hour.
    */
}

function removeParentElement(buttonElement) {
    var counter = buttonElement.getAttribute("data-counter");
    let addIntervalButton = document.querySelector(`.addIntervalButton${counter}`)

    addIntervalButton.disabled = false
    buttonElement.parentElement.remove();
}