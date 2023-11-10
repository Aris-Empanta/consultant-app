//The client's websocket that handles the message exchanging with the websocket server (consumer) 
const webHost = window.location.host;
const websocket = new WebSocket(`ws://${webHost}/ws/private-messaging/`);

//The necessary functions imports
import { showMessage, isEmptyOrWhiteSpace } from "./privateMessagingHelpers.js";

websocket.onopen = () => {
    console.log('user in to send messages')
}

websocket.onmessage = async (event) => {
    console.log(event)
    console.log('received')
}

// We check if it is the private messaging page to put the listener to 
// the send message button, so that we avoid any malfunction on message 
// receiving if we are on other pages.
const currentUrl = window.location.href;
const origin = window.location.origin
const messagingPageUrl = `${origin}/messages/`

if(currentUrl.startsWith(messagingPageUrl)) {

    // The send message functionality
    const sendMessageButton = document.getElementById('sendMessageButton')
    const messageInputField = document.getElementById('messageInputField')
    let receiverWithSlashes = window.location.pathname.replace('/messages', '')
    let receiver = receiverWithSlashes.slice(1, receiverWithSlashes.length - 1)

    sendMessageButton.addEventListener('click', () => {

        let message = messageInputField.value

        if (!isEmptyOrWhiteSpace(message)) {

            let data = {
                'message': message,
                'receiver': receiver,
            }

            websocket.send(JSON.stringify(data))
            messageInputField.value = ''
          }
    })    

    //We will make the send button clickable with enter
    window.onkeydown = function(event){
        if(event.keyCode === 13) {
            event.preventDefault();
            sendMessageButton.click(); //This will trigger a click on the first <a> element.
        }
    };

    // The receiving messages functionality
    websocket.onmessage = async (event) => {
        let data = JSON.parse(event.data)

        let message = data.message
        let senderUsername = data.username
        let receiverUsername = data.receiver
        let avatar = data.avatar
        let time_sent = data.time_sent
        let senderInUrl = window.location.pathname.replace('/messages/', '')
        senderInUrl = senderInUrl.slice(0, senderInUrl.length-1)
        
        // We will show the newly receive message only in the conversation 
        // screen with the sender
        if(senderUsername===senderInUrl || receiverUsername===senderInUrl) {
            showMessage(message, senderUsername, avatar, time_sent)
        }
    }
} else {
}