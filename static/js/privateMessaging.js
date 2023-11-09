//The client's websocket that handles the message exchanging with the websocket server (consumer) 
const webHost = window.location.host;
const websocket = new WebSocket(`ws://${webHost}/ws/private-messaging/`);

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
          }
    })    

    function isEmptyOrWhiteSpace(str) {
        return str.trim() === '';
      }

    // The receiving messages functionality
    websocket.onmessage = async (event) => {
        console.log(event)
        console.log('received')
    }
} else {
    // The receiving messages functionality
    websocket.onmessage = async (event) => {
        console.log(event)
        console.log('received')
    }
}