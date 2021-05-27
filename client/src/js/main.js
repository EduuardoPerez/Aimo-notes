const API_URL = 'http://localhost:8000'

$(document).ready( function () {
    
    let loginSection = $("#login");
    let signupSection = $("#signup");
    let listNotesSection = $("#list-notes");
    let createNoteSection = $("#create-note");

    function hideLoginShowSignup() {
        loginSection.hide('slow');
        signupSection.show('slow');
    }

    function hideSignupShowLogin(params) {
        signupSection.hide('slow');
        loginSection.show('slow');
    }

    function hideLoginShowListNotes() {
        loginSection.hide('slow');
        listNotesSection.show('slow');
    }

    function hideListNotesShowCreateNote() {
        listNotesSection.hide('slow');
        createNoteSection.show('slow');
    }

    function hideCreateNoteShowListNotes() {
        createNoteSection.hide('slow');
        listNotesSection.show('slow');
    }

    $("#btn-signup-txt").click(function () {
        hideLoginShowSignup()
    });

    $("#btn-login-txt").click(function () {
        hideSignupShowLogin()
    });

    $("#login-form").submit(function (e) {
        e.preventDefault();
    });

    $("#signup-form").submit(function (e) {
        e.preventDefault();
    });

    function fillListNotes(userToken) {
        $.ajax({
            url:`${API_URL}/notes/`,
            type:'GET',
            dataType: "json",
            beforeSend: function (xhr) {
                xhr.setRequestHeader ('Authorization', `Token ${userToken}`);
            },
            success: function (response) {
                let notes = response.notes
                if (notes.length > 0) {
                    let listNotes = '';
                    notes.forEach(note => {
                        listNotes += `<strong>${note.title}</strong> <br><p>${note.content}</p><br>`;
                    });
                    $("#user-notes").html(listNotes);
                }
            },
            error: function () {
                alert('Notes could not be loaded');
            },
        });
    }

    $("#btn-login").click(function () {
        let email = $("#login-email-inp").val().trim();
        let password = $("#login-password-inp").val().trim();

        if( email != '' && password != '' ) {
            $.ajax({
                url:`${API_URL}/users/login/`,
                type:'GET',
                dataType: "json",
                beforeSend: function (xhr) {
                    xhr.setRequestHeader ('Authorization', 'Basic ' + btoa(email + ':' + password));
                },
                success: function (response) {
                    hideLoginShowListNotes();
                    let token = response.token
                    localStorage.setItem('aimo-note-token',token)
                    fillListNotes(token);
                },
                error: function (response) {
                    let err = response.responseJSON.message;
                    alert(err);
                },
            });
        }
    });

    $("#btn-signup").click(function () {
        let email = $("#signup-email-inp").val().trim();
        let password = $("#signup-password-inp").val().trim();
        let confirmPassword = $("#signup-confirm-password-inp").val().trim();

        if( email != '' && password != '' && confirmPassword != '' && password == confirmPassword ) {

            let data = {"email":email, "password":password}

            $.ajax({
                url:`${API_URL}/users/signup/`,
                type:'POST',
                dataType: "json",
                contentType: 'application/json',
                data: JSON.stringify(data),
                success: function (response) {
                    alert(response.message);
                    $("#login-email-inp").val(email);
                    hideSignupShowLogin();
                },
                error: function (response) {
                    let errors = response.responseJSON.errors;
                    if (typeof errors == 'string') {
                        alert(errors)
                    } else {
                        let message = ''
                        Object.entries(errors).forEach((err) => {
                            const [key, value] = err;
                            message += `${key}: ${value}\n`;
                          });
                        alert(message);
                    }
                },
            });
        } else {
            alert('Verify the data entered')
        }
    });

    $("#btn-to-create-note").click(function () {
        hideListNotesShowCreateNote();
    });

    $("#btn-create-note").click(function () {
        let userToken = localStorage.getItem('aimo-note-token');
        let title = $("#note-title");
        let content = $("#note-content");
        let data = {
            "title":title.val(),
            "content":content.val(),
        }
        
        $.ajax({
            url:`${API_URL}/notes/`,
            type:'POST',
            dataType: "json",
            contentType: 'application/json',
            data: JSON.stringify(data),
            beforeSend: function (xhr) {
                xhr.setRequestHeader ('Authorization', `Token ${userToken}`);
            },
            success: function (response) {
                alert('Note created');
                hideCreateNoteShowListNotes();
                fillListNotes(userToken);
                title.val('');
                content.val('');
            },
            error: function (response) {
                alert('The note could not be created')  
            },
        });
    });

});
