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
					switch (element.neighborhood) {
					  case 'MTA':
						var tag1 = '<p value="' + element.neighborhood + '"> MARTENSSON A </p>'
						$('#current-neighborhood').append(tag1)
						break;
					  case 'MTB':
						var tag1 = '<p value="' + element.neighborhood + '"> MARTENSSON B </p>'
						$('#current-neighborhood').append(tag1)
						break;
					  case 'CH1':
						var tag1 = '<p value="' + element.neighborhood + '"> CHIODO 1 </p>'
						$('#current-neighborhood').append(tag1)
						break;
					  case 'CH2':
						var tag1 = '<p value="' + element.neighborhood + '"> CHIODO 2 </p>'
						$('#current-neighborhood').append(tag1)
						break;
					  case 'MSN':
						var tag1 = '<p value="' + element.neighborhood + '"> MAISONETTES </p>'
						$('#current-neighborhood').append(tag1)
						break;
					  case 'NRV':
						var tag1 = '<p value="' + element.neighborhood + '"> NERVOSO </p>'
						$('#current-neighborhood').append(tag1)
						break;
					  case 'MON':
						var tag1 = '<p value="' + element.neighborhood + '"> MONACI </p>'
						$('#current-neighborhood').append(tag1)
						break;
					  case 'SNG':
						var tag1 = '<p value="' + element.neighborhood + '"> SAN GENNARO </p>'
						$('#current-neighborhood').append(tag1)
						break;
					  case 'MLA':
						var tag1 = '<p value="' + element.neighborhood + '"> MOLICELLE A </p>'
						$('#current-neighborhood').append(tag1)
						break;
					  case 'MLB':
						var tag1 = '<p value="' + element.neighborhood + '"> MOLICELLE B </p>'
						$('#current-neighborhood').append(tag1)
						break;
					}
					switch (element.room_type) {
					  case 'SIN':
						var tag2 = '<p value="' + element.room_type + '"> SINGLE </p>'
						$('#current-roomtype').append(tag2)
						break;
					  case 'DBL':
						var tag2 = '<p value="' + element.room_type + '"> DOUBLE </p>'
						$('#current-roomtype').append(tag2)
						break;
					}
				});
			}
        },
        error: function () {
            alert("You do not have permissions, you will logout")
			logout()
        }
    });
}

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
			alert("Something bad happened to your reservation update")
        }
    });
}

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
			alert("Something bad happened to your reservation update")
        }
    });
}
