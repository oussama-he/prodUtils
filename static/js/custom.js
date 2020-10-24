$(document).ready(function() {

    // Focus first input on show modal
    $(".modal").on('shown.bs.modal', function() {
        $(this).find("[autofocus]:first").focus();
    });

    // Set list group item active on click
    $("#tasks .list-group-item").on("click", function () {
        // Activate list item
        $("#tasks .list-group-item.active").removeClass("active");
        $(this).addClass("active");

        // Set task id
        $("#taskid").val($(this).data("id"));
        // Enable start button
        $("#startButton").prop("disabled", false);
    });

    // remove class active and disable startButton after click on it
    $("#startButton").on("click", function () {
        $("#tasks .list-group-item.active").removeClass("active");
        $(this).prop("disabled", true);
    })

    document.querySelectorAll('[data-href]').forEach(function(el){
        el.addEventListener('click', function() {
            window.location = $(el).data('href')
        })
    })

    // enable tooltip everywhere
    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
      })

});
