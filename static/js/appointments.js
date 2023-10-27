const bookAppointmentButton = document.querySelectorAll('.bookAppointmentButton')

for(let i=0; i < bookAppointmentButton.length; i++) {

    bookAppointmentButton[i].addEventListener('click', async () => {  

        try {
            // First we extract the csrf token to include it to the sent body.
            const cookies = document.cookie.split(";").map(cookie => cookie.trim());
            let csrftoken
            for (let cookie of cookies) {

                if (cookie.startsWith("csrftoken=")) {
                    csrftoken = cookie.substring("csrftoken=".length, cookie.length);
                    break;
                }
            }
            // We define the backend's url as relative, since it has the same origin as the frontend.
            const url = '/book-appointment/';
            // We extract the lawyer's username from the url
            let lawyerUsernameWithSlashes = window.location.href.split('profile')[1]
            // We remove the remaining slashes forward and after
            let lawyerUsername = lawyerUsernameWithSlashes.substring(1, lawyerUsernameWithSlashes.length - 1)

            //We define the request attributes:
            const request = new Request(url, {
                method: 'POST', // Specify the HTTP method (e.g., GET, POST)
                headers: {
                  'X-CSRFToken': csrftoken,
                  'Content-Type': 'application/json', 
                },
                // Include the request body, if applicable
                body: JSON.stringify({ 'lawyer': lawyerUsername }),
                credentials: "same-origin"
              });

            // Use the Fetch API with async/await to make the GET request
            const response = await fetch(request);

            // Check if the response status is OK (status code 200)
            if (!response.ok) {
                throw new Error('A Network error occured, please try again later.');
            }

            // We parse the JSON response
            const data = await response.json();

            // Handle the JSON data
            console.log(data);

            // You can perform further operations with the data here
        } catch (error) {
            // Handle any errors that occur during the fetch or response handling (change it in production)
            console.error('An unexpected error occured, please try again later');
        }
    })
}