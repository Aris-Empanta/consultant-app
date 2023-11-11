let conversationScreen = document.getElementById('conversationScreen')




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

export {showMessage, isEmptyOrWhiteSpace}