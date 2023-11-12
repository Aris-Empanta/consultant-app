let conversationScreen = document.getElementById('conversationScreen')
import { getCsrfToken } from './csrf.js';

function showMessage(message, username, avatar, time_sent) {

    avatar = formatAvatarUrl(avatar)

    conversationScreen.insertAdjacentHTML('beforeend', 
                                          `<div class="privateMessage">
                                              <p>${username}</p>
                                              <img src=${avatar} >
                                              <p>${message}</p>
                                              <p>${time_sent}</p>
                                           </div>`)

    // Once a new message is appended, the screen  shoud scroll down to show it.
    let privateMessages = conversationScreen.querySelectorAll('.privateMessage');
    let lastElement = privateMessages[privateMessages.length - 1];
    
    lastElement.scrollIntoView({ behavior: 'smooth', block: 'end' });
}

function formatAvatarUrl(avatar) {

    // Configuration for google images
    if(avatar.startsWith('/media/http')) {
      let decodedURL = decodeURIComponent(avatar.replace('/media/', ''));
      return decodedURL
    }
    console.log('no')
    // Configuration for locally stored images in media folder
    return `${window.location.origin}${avatar}`
}

function isEmptyOrWhiteSpace(str) {
    return str.trim() === '';
  }

// The function to get the Amount of the unchecked messages
async function getUncheckedMessagesAmount() {

  try {
      // We retrieve the amount of the appointments that the lawyer 
      // hasn't checked yet
      let url = `/unchecked-messages/`
      let csrftoken = getCsrfToken()

      const request = new Request(url, {
          method: 'GET',
          headers: {
              'X-CSRFToken': csrftoken,
          },
          credentials: "same-origin"
      })

      const response = await fetch(request)

      // Check if the response status is OK (status code 200)
      if (!response.ok) {
          throw new Error('A Network error occured, please try again later.');
      }

      // We parse the JSON response
      let responseData = await response.json();
      let amount = responseData.amount


      return amount
  } catch (error) {
      // Handle any errors that occur during the fetch or response handling (change it in production)
      console.error('An unexpected error occured, please try again later');
  }
}

async function markMessagesAsChecked() {
    
    try {
        const csrftoken = getCsrfToken();
        const url = '/mark-messages-as-checked/';

        //We define the request attributes:
        const request = new Request(url, {
            method: 'PATCH', // Specify the HTTP method (e.g., GET, POST)
            headers: {
              'X-CSRFToken': csrftoken,
              'Content-Type': 'application/json',
            },
            credentials: "same-origin"
          });

        // Use the Fetch API with async/await to make the GET request
        const response = await fetch(request);

        // Check if the response status is OK (status code 200)
        if (!response.ok) {
            throw new Error('A Network error occured, please try again later.');
        }
        } catch (error) {
            // Handle any errors that occur during the fetch or response handling (change it in production)
            console.error('An unexpected error occured, please try again later');
        }
}

async function fetchConversations() {
    try {
        // We retrieve the amount of the appointments that the lawyer 
        // hasn't checked yet
        let url = `/get-all-conversations/`
        let csrftoken = getCsrfToken()
  
        const request = new Request(url, {
            method: 'GET',
            headers: {
                'X-CSRFToken': csrftoken,
            },
            credentials: "same-origin"
        })
  
        const response = await fetch(request)
  
        // Check if the response status is OK (status code 200)
        if (!response.ok) {
            throw new Error('A Network error occured, please try again later.');
        }
  
        // // We parse the JSON response
        // let responseData = await response.json();
        // let amount = responseData.amount
  
  
        // return amount
    } catch (error) {
        // Handle any errors that occur during the fetch or response handling (change it in production)
        console.error('An unexpected error occured, please try again later');
    }
  }

export {showMessage, isEmptyOrWhiteSpace, getUncheckedMessagesAmount, markMessagesAsChecked, fetchConversations }