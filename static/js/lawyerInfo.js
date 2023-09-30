let areasOfExpertiseButton = document.getElementById("areasOfExpertiseButton");
let areasOfExpertiseList = document.getElementById("areasOfExpertiseList")

areasOfExpertiseButton.addEventListener("click", () => {

    if (areasOfExpertiseList.style.display !== "flex") {
  
        areasOfExpertiseList.style.display = "flex";
    }
    else {
        areasOfExpertiseList.style.display = "none";
    }
})