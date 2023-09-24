/*
    In the password reset confirm form, the default is to show as a list
    all the possible authentication-related errors that may arise. We hide 
    them. Also, if more than 1 error arises, we need to show only the first 
    one, for a better UX.
*/
let form = document.getElementById("password-reset-form")

document.addEventListener("DOMContentLoaded", () => {
  
    form.querySelectorAll("ul").forEach((ul) => {

        if(!ul.classList.contains("errorlist")) {
                
                ul.style.display = "none";
            }
        else {
            
            let li = ul.querySelectorAll('li')

            for(let i = 0; i < li.length; i++) {

                if(i !== 0)
                    li[i].style.display = "none";
            }
        }
    })
})