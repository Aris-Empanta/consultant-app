// This function returns a profile avatar's link, depending if 
// it is an absolut internet url or an image in our static files.
function profileAvatarLink(image_name) {

    let avatarLink;

    if(image_name.startsWith('https') || image_name.startsWith('http')) {
        avatarLink = `${image_name}`;
    } else {
        avatarLink = `../img/profile-pics/${image_name}`;
    }    

    return avatarLink;
}

export { profileAvatarLink }