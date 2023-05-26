window.onload = (event) => {
    var planBtn = document.getElementById("custom-checkbox");
    var plans = document.querySelectorAll(".pricing-body-plans > div");
    if (planBtn){
        planBtn.addEventListener("click", function() {
        this.classList.toggle("quarterly");
        plans[0].classList.toggle("active");
        plans[1].classList.toggle("active");
})
    }
    showToast()
}

let x;
let toast = document.getElementById("toast");
function showToast(){
    clearTimeout(x);
    toast.style.transform = "translateX(0)";
    x = setTimeout(()=>{
        toast.style.transform = "translateX(100%)"
    }, 60000);
}
function closeToast(){
    toast.style.transform = "translateX(100%)";
}