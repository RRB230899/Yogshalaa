window.onload = (event) => {
    showToast()
}

let x;
let toast = document.getElementById("toast");
function showToast(){
    clearTimeout(x);
    toast.style.transform = "translateX(0)";
    x = setTimeout(()=>{
        toast.style.transform = "translateX(100%)"
    }, 2000000);
}
function closeToast(){
    toast.style.transform = "translateX(100%)";
}