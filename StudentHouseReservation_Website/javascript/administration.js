$(document).ready(function () {
    showReservationList()
	showStudentList()
	showUserList()
});

function showReservationList() {
	$.ajax({
        type: 'GET',
        url: 'http://localhost:8000/api/v1/reservation-list/',
        xhrFields: {
            withCredentials: true
        },
        success: function (response) {
            response.forEach(element => {
                var tag = '<tr>' + '<td value="' + element.id + '">' + element.id + '</td>' + '<td value="' + element.neighborhood + '">' + element.neighborhood +'</td>' + '<td value="' + element.room_type + '">' + element.room_type +'</td>' + '<td value="' + element.user + '">' + element.user +'</td>' + '</tr>'
                $('#reservation-records').append(tag)
            });
        },
        error: function () {
            alert("You do not have permissions, you will logout")
			logout()
        }
    });
}

function showStudentList() {
	$.ajax({
        type: 'GET',
        url: 'http://localhost:8000/api/v1/student-list/',
        xhrFields: {
            withCredentials: true
        },
        success: function (response) {
            response.forEach(element => {
                var tag = '<tr>' + '<td value="' + element.id + '">' + element.id +'</td>' + '<td value="' + element.username + '">' + element.username +'</td>' + '<td value="' + element.email + '">' + element.email +'</td>' + '</tr>'
                $('#student-records').append(tag)
            });
        },
        error: function () {
            alert("You do not have permissions, you will logout")
			logout()
        }
    });
}

function showUserList() {
	$.ajax({
        type: 'GET',
        url: 'http://localhost:8000/api/v1/user-list/',
        xhrFields: {
            withCredentials: true
        },
        success: function (response) {
            response.forEach(element => {
                var tag = '<tr>' + '<td value="' + element.id + '">' + element.id +'</td>' + '<td value="' + element.username + '">' + element.username +'</td>' + '<td value="' + element.email + '">' + element.email +'</td>' + '<td value="' + element.is_staff + '">' + element.is_staff +'</td>' + '<td value="' + element.groups + '">' + element.groups +'</td>' + '</tr>'
                $('#user-records').append(tag)
            });
        },
        error: function () {
            alert("You do not have permissions, you will logout")
			logout()
        }
    });
}

function boom() {
	alert("BOOM")
}