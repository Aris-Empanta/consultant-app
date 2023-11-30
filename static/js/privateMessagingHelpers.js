import { getCsrfToken } from './csrf.js';

const messagePreviewInfo = document.getElementsByClassName('messagePreviewAndTimeAgoWrapper')
let outerPrivateMessageWrapper = document.getElementById('outerPrivateMessageWrapper')
let conversationScreen = document.getElementById('conversationScreen')

function showMessage(message, username, avatar, time_sent) {

    avatar = formatAvatarUrl(avatar)

    outerPrivateMessageWrapper.insertAdjacentHTML('beforeend', 
                                                `<div class="privateMessageWrapper">
                                                    <div class="privateMessageAvatarAndUsernameWrapper">
                                                        <img class="privateMessageAvatar" src=${avatar} >
                                                        <a class="privateMessageUsername" href=/profile/${username}
                                                            target="_blank">
                                                            ${username}
                                                        </a>
                                                    </div>
                                                    <p class="privateMessage">${message}</p>
                                                    <p class="privateMessageTimeSent">${time_sent}</p>
                                                </div>`)

    // Once a new message is appended, the screen  shoud scroll down to show it.
    scrollToLatestMessage()
}

function formatAvatarUrl(avatar) {

    // Configuration for google images
    if(avatar.startsWith('/media/http')) {
      let decodedURL = decodeURIComponent(avatar.replace('/media/', ''));
      return decodedURL
    }

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
        let responseData = await response.json();
        let conversations = responseData.conversations

        return conversations  
    } catch (error) {
        // Handle any errors that occur during the fetch or response handling (change it in production)
        console.error('An unexpected error occured, please try again later');
    }
  }

function renderConversations(conversations, messagesPreviewModal) {    

    messagesPreviewModal.innerHTML = ''   

    for(let i=0; i<conversations.length; i++) {
        let sender = conversations[i].sender
        let avatar = conversations[i].avatar
        let message = conversations[i].message
        let timeAgo = conversations[i].time_sent
        let read =  conversations[i].read

        let readStatusClass = read ? 'messageRead' : 'messageUnread'

        let conversationPreview = `<a href='/messages/${sender}/'  class="conversationWrapper ${readStatusClass}">
                                      <img src='${avatar}' class="messagePreviewAvatar" >
                                      <div class="messagePreviewAndTimeAgoWrapper">
                                         <p class="messagePreviewInModal">${formatMessagePreview(message)}</p>
                                         <p class="timeAgoMessagePreview">${timeAgo} ago </p> 
                                      </div>
                                   </a>`
        messagesPreviewModal.insertAdjacentHTML('beforeend', conversationPreview)

        if(screen.width < 800) {
            messagePreviewInfo[i].style.display = 'none'
        } else {
            messagePreviewInfo[i].style.display = 'initial'
        }
    }
}

function formatMessagePreview(message) {
    if(message.length > 20) {
        message = message.slice(0,20) + '...'
    }

    return message
}


async function markMessagesAsRead() {
    
    try {
        const csrftoken = getCsrfToken();
        const url = '/mark-messages-as-read/';

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

function scrollToLatestMessage() {

    conversationScreen.scrollTop = conversationScreen.scrollHeight;
}

export {showMessage, isEmptyOrWhiteSpace, 
        getUncheckedMessagesAmount, markMessagesAsChecked, 
        fetchConversations, renderConversations, 
        markMessagesAsRead, scrollToLatestMessage, messagePreviewInfo }