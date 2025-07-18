import { getAuth, signInWithPhoneNumber, RecaptchaVerifier } from "https://www.gstatic.com/firebasejs/12.0.0/firebase-auth.js";
import { initializeApp } from "https://www.gstatic.com/firebasejs/12.0.0/firebase-app.js";

const firebaseConfig = {
    apiKey: API_KEY,
    authDomain: AUTH_DOMAIN,
    projectId: PROJECT_ID,
    storageBucket: STORAGE_BUCKET,
    messagingSenderId: MESSAGING_SENDER_ID,
    appId: APP_ID,
    measurementId: MEASUREMENT_ID
};
initializeApp(firebaseConfig);

document.addEventListener('DOMContentLoaded', function () {
    var auth = getAuth();
    //invisible recaptcha0
    window.recaptchaVerifier = new RecaptchaVerifier(auth, 'login', {
        'size': 'invisible',
        'callback': (response) => {
            // reCAPTCHA solved, allow signInWithPhoneNumber.
            onSignInSubmit();
        }
    }, auth);

    window.recaptchaVerifier.render().then(function(widgetId) {
        window.recaptchaWidgetId = widgetId;
    });

    const phoneInputField = document.querySelector("#id_password1");
    const phoneInput = window.intlTelInput(phoneInputField, {
        onlyCountries: ['gb', 'in', 'us', 'nl'],
        initialCountry: 'in',
        utilsScript:
            "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/js/utils.js",
        separateDialCode: true,
    });

    document.getElementById("login").addEventListener('click', phoneAuth);
    function phoneAuth(e) {

        e.preventDefault();
        var phoneNumber = phoneInput.getNumber();
        callDjangoView(phoneNumber)
    }
    function callDjangoView(phNo) {
        var full_name = document.getElementById('full_name').value;
        var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        var phn_no = phoneInput.getSelectedCountryData();
	    var ip = document.getElementById('country_code');
	    ip.value = phn_no['dialCode'];

        // Prepare data for the request
        var data = {
            full_name: full_name,
            phone_number: phNo,
            country_code: ip.value
        };

        // Make an AJAX request to Django view
        fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (data.message === 'Profile verified') {
                    window.location.href = '/success'
                }
                else if (data.message === 'OTP sent successfully') {
                    var appVerifier = window.recaptchaVerifier;
                    signInWithPhoneNumber(auth, phNo, appVerifier)
                    .then((confirmationResult) => {
                        localStorage.setItem("confirmationResult", JSON.stringify(confirmationResult));
                        localStorage.setItem("phNo", JSON.stringify(phNo));
                        alert("OTP sent successfully.")
                        localStorage.setItem("uid", JSON.stringify(data.uid));
                        window.location.href = '/otp/' + data.uid + '/';
                    })
                    .catch((error) => {
                        // Error; SMS not sent
                        // ...
                        document.getElementById('id_password1').value = '';
                        console.log(error);
                        alert(error);
                    });
                }
            }
            else {
                console.error('Error:', data.error);
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
});