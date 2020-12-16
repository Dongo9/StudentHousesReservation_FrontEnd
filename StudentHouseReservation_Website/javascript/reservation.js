$(document).ready(function () {
    showReservation()
});

// Example starter JavaScript for disabling form submissions if there are invalid fields
(function () {
  'use strict'

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  var forms = document.querySelectorAll('.needs-validation')

  // Loop over them and prevent submission
  Array.prototype.slice.call(forms)
    .forEach(function (form) {
      form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
      }, false)
    })
})()

function showReservation() {
		$.ajax({
        type: 'GET',
        url: 'http://localhost:8000/api/v1/reservation-student/',
        xhrFields: {
            withCredentials: true
        },
        success: function (response) {
			if(response.length==0)
			{
				var tag = '<p> NOT EXPRESSED </p>'
				$('#current-neighborhood').append(tag)
				$('#current-roomtype').append(tag)
			}
			else
			{
				response.forEach(element => {
					var tag1 = '<p value="' + element.neighborhood + '">' + element.neighborhood + '</p>'
					$('#current-neighborhood').append(tag1)
					var tag2 = '<p value="' + element.room_type + '">' + element.room_type + '</p>'
					$('#current-roomtype').append(tag2)
					var idtag='<p id="reservation_id" value="' + element.id + '"></p>'
					$('#res_id').append(idtag)
				});
			}
        },
        error: function () {
            alert("You do not have permissions, you will logout")
			logout()
        }
    });
}

function editReservationDEBUG() {
	var reservation_id = 9
	
	alert("reservation_id:"+ reservation_id)
	
	var neighborhood = $('#neighborhood').val()
	alert(neighborhood)
    var room_type
	if($('#roomtype1').is(':checked'))
	{
		room_type = $('#roomtype1').val()
	}
	else
	{
		room_type = $('#roomtype2').val()
	}
	alert(room_type)
    $.ajax({
        type: 'PUT',
        url: 'http://localhost:8000/api/v1/reservation-student/edit/' + reservation_id + '/',
		headers: {
		'X-CSRFToken': cookieValue = document.cookie
			.split('; ')
			.find(row => row.startsWith('csrftoken'))
			.split('=')[1]
        },
        dataType: 'json',
        contentType: 'application/json; charset=UTF-8',
        data: JSON.stringify({
            neighborhood: neighborhood,
            room_type: room_type
        }),
        xhrFields: {
            withCredentials: true
        },
        success: function (response) {
            location.reload()
        },
        error: function () {
        }
    });
}

function addReservationDEBUG() {
	var neighborhood = $('#neighborhood').val()
    var room_type
	if($('#roomtype1').is(':checked'))
	{
		room_type = $('#roomtype1').val()
	}
	else
	{
		room_type = $('#roomtype2').val()
	}
    $.ajax({
        type: 'POST',
        url: 'http://localhost:8000/api/v1/reservation-student/add/',
		headers: {
		'X-CSRFToken': cookieValue = document.cookie
			.split('; ')
			.find(row => row.startsWith('csrftoken'))
			.split('=')[1]
        },
        dataType: 'json',
        contentType: 'application/json; charset=UTF-8',
        data: JSON.stringify({
            neighborhood: neighborhood,
            room_type: room_type
        }),
        xhrFields: {
            withCredentials: true
        },
        success: function (response) {
            location.reload()
        },
        error: function () {
        }
    });
}




//DEBUGGGGGGGGGGGGGGGGGG
function updateReservation() {
		$.ajax({
        type: 'GET',
        url: 'http://localhost:8000/api/v1/reservation-student/',
		async: false,
        xhrFields: {
            withCredentials: true
        },
        success: function (response) {
			if(response.length==0)
			{
				addReservation()
			}
			else
			{
				response.forEach(element => {
					editReservation(element.id)
				});
			}
        },
        error: function () {
            alert("You do not have permissions, you will logout")
			logout()
        }
    });
}

function editReservation(r_id) {
	var reservation_id = r_id
	
	
	var neighborhood = $('#neighborhood').val()
    var room_type
	if($('#roomtype1').is(':checked'))
	{
		room_type = $('#roomtype1').val()
	}
	else
	{
		room_type = $('#roomtype2').val()
	}
	alert(room_type)
    $.ajax({
        type: 'PUT',
        url: 'http://localhost:8000/api/v1/reservation-student/edit/' + reservation_id + '/',
		headers: {
		'X-CSRFToken': cookieValue = document.cookie
			.split('; ')
			.find(row => row.startsWith('csrftoken'))
			.split('=')[1]
        },
        dataType: 'json',
        contentType: 'application/json; charset=UTF-8',
        data: JSON.stringify({
            neighborhood: neighborhood,
            room_type: room_type
        }),
        xhrFields: {
            withCredentials: true
        },
        success: function (response) {
            location.reload()
        },
        error: function () {
        }
    });
}

//FUNZIONA
function addReservation() {
	var neighborhood = $('#neighborhood').val()
	alert(neighborhood)
    var room_type
	if($('#roomtype1').is(':checked'))
	{
		room_type = $('#roomtype1').val()
	}
	else
	{
		room_type = $('#roomtype2').val()
	}
	alert(room_type)
    $.ajax({
        type: 'POST',
        url: 'http://localhost:8000/api/v1/reservation-student/add/',
		headers: {
		'X-CSRFToken': cookieValue = document.cookie
			.split('; ')
			.find(row => row.startsWith('csrftoken'))
			.split('=')[1]
        },
        dataType: 'json',
        contentType: 'application/json; charset=UTF-8',
        data: JSON.stringify({
            neighborhood: neighborhood,
            room_type: room_type
        }),
        xhrFields: {
            withCredentials: true
        },
        success: function (response) {
            location.reload()
        },
        error: function () {
        }
    });
}
