const conversationsOuterWrapper = document.getElementById('conversationsListWrapper')
const allConversationPreviews = document.getElementsByClassName('conversationWrapper')
const messagePreviewInfo = document.getElementsByClassName('messagePreviewAndTimeAgoWrapper')

window.addEventListener('DOMContentLoaded', () => {
    
    if(allConversationPreviews) {

        conversationsOuterWrapper.style.width = 'fit-content'

        for(let i=0; i < allConversationPreviews.length; i++) {

            if(screen.width < 650) {
                messagePreviewInfo[i].style.display = 'none'
               // allConversationPreviews[i].style.width = 'fit-content'
            } else {
                messagePreviewInfo[i].style.display = 'initial'
            }
        }
    }
})

window.addEventListener("resize", () => {

    if(allConversationPreviews) {

        conversationsOuterWrapper.style.width = 'fit-content'

        for(let i=0; i < allConversationPreviews.length; i++) {

            if(screen.width < 650) {
                messagePreviewInfo[i].style.display = 'none'
               // allConversationPreviews[i].style.width = 'fit-content'
            } else {
                messagePreviewInfo[i].style.display = 'initial'
            }
        }
    }
});