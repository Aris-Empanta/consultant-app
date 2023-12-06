let chooseClient = document.getElementById("chooseClient")
let chooseLawyer = document.getElementById("chooseLawyer")
let joinButton = document.getElementById("joinButton")

chooseClient.addEventListener("click", () => {

    joinButton.value = "Join as Client";
    joinButton.style.opacity = 1;
    joinButton.style.cursor = "pointer";
    joinButton.disabled = false;
})

chooseLawyer.addEventListener("click", () => {

    joinButton.value = "Join as Lawyer";
    joinButton.style.opacity = 1;
    joinButton.style.cursor = "pointer";
    joinButton.disabled = false;
})