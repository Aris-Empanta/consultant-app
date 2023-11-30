import { scrollToLatestMessage, messagePreviewInfo } from "./privateMessagingHelpers.js"

const conversationsOuterWrapper = document.getElementById('conversationsListWrapper')
const allConversationPreviews = document.getElementsByClassName('conversationWrapper')

// We set the dynamicheight of the messages page on content load 
// as well as on resize.
window.addEventListener('DOMContentLoaded', () => {

    setMessagesPageHeight()
    // We also scroll the conversation screen to the latest message
    scrollToLatestMessage()
})

window.addEventListener("resize", () => {    

    setMessagesPageHeight()  
    scrollToLatestMessage()  

    if(allConversationPreviews) {

        if(screen.width < 800) {
            conversationsOuterWrapper.style.width = 'fit-content'
        } else {
            conversationsOuterWrapper.style.width = '400px'
        }
`1`
        for(let i=0; i < allConversationPreviews.length; i++) {

            if(screen.width < 800) {
                messagePreviewInfo[i].style.display = 'none'
            } else {
                messagePreviewInfo[i].style.display = 'initial'
            }
        }
    }
});

// The function to set the height of the messages page dynamically.
function setMessagesPageHeight() {
    // the height of the messages page should always be equal to the total 
    // height of the screen minus the distance of the lawyer searchbar bottom 
    // from the top of the screen.
    const searchBar = document.getElementById('searchLawyerWrapper')
    const messagesPage = document.getElementById('messagesPage')

    let searchBarMartingTop = 87
    let searchBarFromTop = searchBarMartingTop + searchBar.clientHeight
    let screenHeight = window.innerHeight;

    messagesPage.style.height = `${screenHeight - searchBarFromTop}px`
    document.body.style.height = 'auto'
}