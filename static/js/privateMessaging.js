//The client's websocket that handles the message exchanging with the websocket server (consumer) 
const webHost = window.location.host;
const websocket = new WebSocket(`ws://${webHost}/ws/private-messaging/`);

//The necessary functions imports
import { showMessage, isEmptyOrWhiteSpace, 
         getUncheckedMessagesAmount, markMessagesAsChecked,
         fetchConversations } from "./privateMessagingHelpers.js";

// We check if it is the private messaging page to put the listener to 
// the send message button, so that we avoid any malfunction on message 
// receiving if we are on other pages.
const currentUrl = window.location.href;
const origin = window.location.origin
const messagingPageUrl = `${origin}/messages/`

// The messages modal mechanism
const messagesNotificationButton = document.getElementById('messagesNotificationButton')
const messagesPreviewModal = document.getElementById('messagesPreviewModal')
const appointmentsModal = document.getElementById('appointmentsModal')
const uncheckedMessagesWrapper = document.getElementById('uncheckedMessagesWrapper')
const uncheckedMessages = document.getElementById('uncheckedMessages')

// When a user clicks on the messages notification button, all the messages of the 
// user are marked as checked, and the messages previewmodal appears.
messagesNotificationButton.addEventListener('click', async () => {

    if(messagesPreviewModal.style.display !== 'flex') {
        await markMessagesAsChecked()
        uncheckedMessagesWrapper.style.display = 'none'
        messagesPreviewModal.style.display = 'flex'
        const conversations = await fetchConversations()
        console.log(conversations)
    } else {
        messagesPreviewModal.style.display = 'none'
    }
})

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
        let senderUsername = data.sender
        let currentUser = document.getElementById('user-info').value
        let avatar = data.avatar
        let time_sent = data.time_sent
        let senderInUrl = window.location.pathname.replace('/messages/', '')

        senderInUrl = senderInUrl.slice(0, senderInUrl.length-1)
        
        // We will show the newly receive message only in the conversation 
        // screen with the sender
        if(senderUsername===senderInUrl || senderUsername===currentUser) {
            showMessage(message, senderUsername, avatar, time_sent)
        }
    }
} else {
    
    websocket.onmessage = async (event) => {
        //We close the apointments modal
        appointmentsModal.style.display = 'none';

        // If the messagesPreviewModal is  closed, just fetch and show the 
        // amount of all the user's unchecked messages.
        if(messagesPreviewModal.style.display !== 'flex') {
           let uncheckedMessagesAmount = await getUncheckedMessagesAmount()
           uncheckedMessagesWrapper.style.display = 'initial'
           uncheckedMessages.innerText = uncheckedMessagesAmount
        }

        // If the messagesPreviewModal is open, re-fetch all the messages
        // and mark them all as checked.

        // 
    }
}