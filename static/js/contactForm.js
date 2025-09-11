console.log("2424")
document.getElementById("submit_form").addEventListener('click', sendContactForm);

function sendContactForm(event) {
    event.preventDefault();
//
//    var first_name = getUserInput('first_name');
//    var last_name = getUserInput('last_name');
//    var email = getUserInput('email');
//    var contact = getUserInput('contact');
//    var feedback = getUserInput('feedback');
//
//    console.log(contact.toString().length)

    //Show alert and save feedback

//    saveFeedback(first_name, last_name, email, contact, feedback);
//    resetErrorMsg();
    console.log("In here.")
    document.querySelector(".contact-form-alert").style.display = 'block';

    //Hide alert
    setTimeout(function()
    {
        document.querySelector(".contact-form-alert").style.display = 'none';
    }, 5000);

    //Clear form
    document.getElementById("contactForm").reset();

//    else {
//
//        resetErrorMsg();
//
//        //Empty first name
//        if (first_name === '' || first_name === null) {
//            resetErrorMsg();
//            document.getElementById("f-error-msg").innerHTML = 'Had your say? Nope!';
//            document.getElementById("f-error-msg").style.display = 'block';
//            document.getElementById("first_name").focus();
//            return false;
//        }
//
//        //Empty last name
//        if (last_name === '' || last_name === null) {
//            resetErrorMsg();
//            document.getElementById("l-error-msg").innerHTML = 'Need your last name too.';
//            document.getElementById("l-error-msg").style.display = 'block';
//            document.getElementById("last_name").focus();
//            return false;
//        }
//
//        //Empty contact no.
//        if (contact === '' || contact === null) {
//            resetErrorMsg();
//            document.getElementById("c-error-msg").innerHTML = 'Best means to reach out. Right?';
//            document.getElementById("c-error-msg").style.display = 'block';
//            document.getElementById("contact").focus();
//            return false;
//        }
//
//        //validating ph. no.
//        if (contact.toString().length !== 10){
//            resetErrorMsg();
//            validatePhoneNumber(contact.toString())
//            document.getElementById("c-error-msg").innerHTML = 'Tricky. Seems fishy!';
//            document.getElementById("c-error-msg").style.display = 'block';
//            document.getElementById("contact").focus();
//            document.getElementById("contact").value = '';
//        }
//    }
}

//function resetErrorMsg(){
//    //set error elements' display to none
//    document.getElementById("f-error-msg").style.display = 'none';
//    document.getElementById("l-error-msg").style.display = 'none';
//    document.getElementById("c-error-msg").style.display = 'none';
//}