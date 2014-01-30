$(document).ready(function() {
    $("#accordion2").accordion({
        collapsible: true,
        header: "div.accordion-heading",
        heightStyle: "content",
    });
    $(".moreinfo").hide();
    $(".show_hide").show();

    $('a.show_hide').click(function(event){
        rel = event.currentTarget.rel;
        $(rel).slideToggle();
        event.preventDefault();
    });
});
