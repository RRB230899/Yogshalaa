//const navEl = document.getElementById("nav-mobile-menu");
//const nav = document.getElementsByTagName("nav");
//
//navEl.addEventListener("click", () => {
//    nav[1].classList.toggle("active");
//});

window.onload = function() {
var planBtn = document.getElementById("custom-checkbox");
var plans = document.querySelectorAll(".pricing-body-plans > div");
console.log(planBtn, plans[0])

if (planBtn) {
    planBtn.addEventListener("click", function() {
        this.classList.toggle("quarterly");
        plans[0].classList.toggle("active");
        plans[1].classList.toggle("active");
})}};