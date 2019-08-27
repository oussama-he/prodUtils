$(document).ready(function () {
  // This function gets cookie with a given name
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');

  /*
  The functions below will create a header with csrftoken
  */

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
      (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
      // or any other URL that isn't scheme relative or absolute i.e relative.
      !(/^(\/\/|http:|https:).*/.test(url));
  }

  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
        // Send the token to same-origin, relative URLs only.
        // Send the token only if the method warrants CSRF protection
        // Using the CSRFToken value acquired earlier
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });


  $('#new-category-submit').on('click', function() {
    createCategory()
  })

  function createCategory() {
    console.log("create category is working!")
    var endpoint = "/budget/category/new/"
    $.ajax({
      url: endpoint ,
      type: "POST", // http method
      data: new FormData($('#new-category-form')[0]),
      cache: false,
      contentType: false,
      processData: false,
      enctype: 'multipart/form-data',

      // handle a successful response
      success: function (response) {
        $('#new-category-modal').modal('hide')

        $("#new-category-form")[0].reset()
      },

      error: function (xhr, errmsg, err) {
        formErrors = JSON.parse(xhr.responseJSON);
        for (var key in formErrors) {
          var fieldId = "#new-category-form #id_" + key;
          var errorContent = formErrors[key];
          var errorMessage = errorContent[0]['message'];

          var errorFeedback = $("<div class='invalid-feedback'>" + errorMessage + "</div>");
          $(fieldId).addClass("is-invalid");
          $(fieldId).parent().append(errorFeedback);
        }
      }
    });
  };
})








