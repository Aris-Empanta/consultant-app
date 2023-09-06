window.addEventListener("load", () => {

    if (window.location.pathname === "/successfully-registered/") {
        setTimeout(function () {
            window.location.replace("/");
        }, 2000);
    }
});