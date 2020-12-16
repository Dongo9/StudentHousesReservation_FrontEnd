// Example starter JavaScript for disabling form submissions if there are invalid fields
(function() {
  'use strict';
  window.addEventListener('load', function() {
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.getElementsByClassName('needs-validation');
    // Loop over them and prevent submission
    var validation = Array.prototype.filter.call(forms, function(form) {
      form.addEventListener('submit', function(event) {
        if (form.checkValidity() === false) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
      }, false);
    });
  }, false);
})();

function loginStudent() {
    var username = $('#inputID-Student').val()
    var password = $('#inputPassword-Student').val()
    $.ajax({
        type: 'POST',
        url: 'http://localhost:8000/api/v1/auth/login/',
        dataType: 'json',
        contentType: 'application/json; charset=UTF-8',
        data: JSON.stringify({
            username: username,
            password: password
        }),
        xhrFields: {
            withCredentials: true
        },
        success: function (response) {
            location.replace("reservation.html")
        },
        error: function () {
        }
    });
}

function loginEmployee() {
    var username = $('#inputID-Employee').val()
    var password = $('#inputPassword-Employee').val()
    $.ajax({
        type: 'POST',
        url: 'http://localhost:8000/api/v1/auth/login/',
        dataType: 'json',
        contentType: 'application/json; charset=UTF-8',
        data: JSON.stringify({
            username: username,
            password: password
        }),
        xhrFields: {
            withCredentials: true
        },
        success: function (response) {
            location.replace("administration.html")
        },
        error: function () {
        }
    });
}