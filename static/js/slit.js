$(document).ready(function() {
$(".option").click(function () {
    $(".option").removeClass("active");
    // $(".tab").addClass("active"); // instead of this do the below
    $(this).addClass("active");
});
});

$('#slider').owlCarousel({
    loop:true,
    margin:15,
    nav:false,
    autoplay:true,
    responsive:{
        0:{
            items:1
        },
        600:{
            items:2
        },
        1000:{
            items:3
        }
    }
})