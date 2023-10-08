let hoursScheduleWrapper = document.querySelectorAll(".hoursScheduleWrapper")
// We have to loop through each parent element of the available days for appointments 
// (hoursScheduleWrapper):
for(let i = 0; i < hoursScheduleWrapper.length; i++) {
    // The addIntervals button should be clickable only if the there is no interval or if the last interval's ending time is 
    //  <= 22:59 and the existing intervals are less than 2.
    let addIntervalsButton = document.querySelector(`.addIntervalButton${i+1}`)
    let currentHoursScheduleWrapper = document.getElementById(`hoursScheduleWrapperOfDay${i+1}`)
    let intervals = document.querySelectorAll(`.intervalOfDay${i+1}`)
    //The classes for the starting and ending time interval:
    let startingTime = document.querySelectorAll(`.startOfInterval${i+1}`)
    let endingTime = document.querySelectorAll(`.endOfInterval${i+1}`)

    // The addIntervals button should be clickable only if the there is no interval or if the last interval's ending time is 
    // <= 22:59 and the existing intervals are <2. We set it for the first ending time once the page load, considering that no
    //extra intervals have been added. Also we set all the other validation for time needed.
    endingTime[0].addEventListener('change', () => {

        if(endingTime[0].value <= "22:59") {
            addIntervalsButton.disabled = false
        } else {
            addIntervalsButton.disabled = true   
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
    }) 
}

//The function to remove an interval.
function removeParentElement(buttonElement) {
    var counter = buttonElement.getAttribute("data-counter");
    let addIntervalButton = document.querySelector(`.addIntervalButton${counter}`)

    // We enable the addIntervalButton once we remove an interval, since it will always 
    // be less than 2.
    addIntervalButton.disabled = false
    buttonElement.parentElement.remove();
}