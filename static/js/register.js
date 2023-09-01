document.getElementById("clientRegisterButton").addEventListener("click", () => {

    let specialtyQuestioningPage = document.getElementById("specialtyQuestioningPage")
    let clientRegisterPage = document.getElementById("clientRegisterPage")

    specialtyQuestioningPage.style.display = "none"

    clientRegisterPage.style.display = "flex"    
})

document.getElementById("lawyerRegisterButton").addEventListener("click", () => {

    let specialtyQuestioningPage = document.getElementById("specialtyQuestioningPage")
    let lawyerRegisterPage = document.getElementById("lawyerRegisterPage")

    specialtyQuestioningPage.style.display = "none"

    lawyerRegisterPage.style.display = "flex"    
})