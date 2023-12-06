export function getCsrfToken() {

    // We extract the csrf token to include it to the sent body.
    const cookies = document.cookie.split(";").map(cookie => cookie.trim());
    let csrftoken
    
    for (let cookie of cookies) {

        if (cookie.startsWith("csrftoken=")) {
            csrftoken = cookie.substring("csrftoken=".length, cookie.length);
            return csrftoken
        }
    }
}