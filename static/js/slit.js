$(document).ready(function() {
$(".option").click(function () {
    $(".option").removeClass("active");
    // $(".tab").addClass("active"); // instead of this do the below
    $(this).addClass("active");
});
});