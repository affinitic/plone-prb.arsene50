$(document).ready(function() {
    $(".moreinfo").hide();
    $(".show_hide").show();

    $('a.show_hide').click(function(event){
        rel = event.currentTarget.rel;
        $(rel).slideToggle();
        event.preventDefault();
    });
});
