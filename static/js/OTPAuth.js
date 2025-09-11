import { getAuth, signInWithCredential, PhoneAuthProvider, RecaptchaVerifier, signInWithPhoneNumber } from "https://www.gstatic.com/firebasejs/9.12.1/firebase-auth.js";
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.12.1/firebase-app.js";

const firebaseConfig = {
    apiKey: API_KEY,
    authDomain: AUTH_DOMAIN,
    projectId: PROJECT_ID,
    storageBucket: STORAGE_BUCKET,
    messagingSenderId: MESSAGING_SENDER_ID,
    appId: APP_ID,
    measurementId: MEASUREMENT_ID
};

var app = initializeApp(firebaseConfig);
var auth = getAuth(app);

window.recaptchaVerifier = new RecaptchaVerifier('resend_otp', {
        'size': 'invisible',
        'callback': (response) => {
            // reCAPTCHA solved, allow signInWithPhoneNumber.
            onSignInSubmit();
        }
    }, auth);

document.getElementById("verify_otp").addEventListener('click', verifyOTP);
document.getElementById("resend_otp").addEventListener('click', resendOTP);

function verifyOTP(e){
    e.preventDefault();
    var confirmationResult = JSON.parse(localStorage.getItem('confirmationResult'));
    var code = document.getElementById("otp").value;
    var verificationId = confirmationResult.verificationId;
    var credential = PhoneAuthProvider.credential(verificationId, code);
    var otpExpiry = document.cookie.includes('can_otp_enter')
    if (otpExpiry){
        signInWithCredential(auth, credential)
        .then((userCredentials) => {
            $('#message-error').fadeOut();
            djangoView();
        }).catch((error) => {
            $('#message-error').html("OTP invalid. Please try again or resend the code.").fadeIn();
            console.log(error);
        })
    }
    else{
        $('#message-error').html("10 minutes passed. Please resend the code.").fadeIn();
    }
}

function resendOTP(e){
    e.preventDefault();
    var appVerifier = window.recaptchaVerifier;
    var phNo = JSON.parse(localStorage.getItem('phNo'));
    signInWithPhoneNumber(auth, phNo, appVerifier)
    .then((confirmationResult) => {
        localStorage.setItem("confirmationResult", JSON.stringify(confirmationResult));
        localStorage.setItem("phNo", JSON.stringify(phNo));
        setOTPExpiryCookie();
    })
    .catch((error) => {
        // Error; SMS not sent
        // ...
        console.log(error);
        $('#message-error').html("OTP invalid. Please try again or resend the code.").fadeIn();
    });
}

function setOTPExpiryCookie() {
    var expirationDate = new Date();
    expirationDate.setTime(expirationDate.getTime() + (600 * 1000));

    // Create the cookie string
    var cookieString = `can_otp_enter=true; max-age=600; expires=${expirationDate.toUTCString()}; path=/`;

    // Set the cookie
    document.cookie = cookieString;
}

function djangoView(){
    var uid = JSON.parse(localStorage.getItem('uid'))
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    console.log('otp/' + uid + '/')
    $.ajax({
        url: "/otp/" + uid + "/",
        type: "POST",
        dataType: "json",
        headers: {
            'X-CSRFToken': csrfToken
        },
        success: function(response) {
            if (response.success){
                window.location.href = "/success";
            }
            else{
                console.log("AJAX Call error", response.error);
            }
        },
        error: function(xhr, status, error) {
            console.log("AJAX error", error);
        }
    })
}
