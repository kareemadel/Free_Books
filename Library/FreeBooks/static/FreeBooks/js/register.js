
$(document).ready(function() {
    // Initialize form validation on the registration form.
    // It has the name attribute 'registration'
    jQuery.validator.addMethod('allDigits', function(value, element) {
        return this.optional(element) || !(/^\d*$/.test(value));
    }, 'Your password can\'t be entirely numeric');

    jQuery.validator.addMethod('Date', function(value, element) {
        let date = value.split('-');
        let y = parseInt(date[0], 10);
        let m = parseInt(date[1], 10);
        let d = parseInt(date[2], 10);
        date = new Date(y, m, d);
        if (date == 'Invalid Date') {
            return false;
        } else {
            return true;
        }
    }, 'Please provide a valide birthdate e.g. 2000-10-20');

    $('#apply-form').validate({
        // Specify validation rules
        rules: {
            // The key name on the left side is the name attribute
            // of an input field. Validation rules are defined
            // on the right side
            username: 'required',
            first_name: 'required',
            last_name: 'required',
            bio: 'required',
            birth_date: {
                required: true,
                Date: true,
            },
            pic: 'required',
            email: {
                required: true,
                // Specify that email should be validated
                // by the built-in 'email' rule
                email: true,
            },
            password1: {
                required: true,
                minlength: 8,
                allDigits: true,
            },
            password2: {
                required: true,
                equalTo: '#id_password1',
            },
        },
        // Specify validation error messages
        messages: {
            username: 'Please provide a username',
            first_name: 'Please enter your firstname',
            last_name: 'Please enter your lastname',
            password1: {
                required: 'Please provide a password',
                minlength: 'Your password must be at least 8 characters long',
            },
            password2: {
                required: 'Please confirm your password',
                equalTo: 'Your password doesn\'t match',
            },
            email: 'Please enter a valid email address',
            birth_date: {
                required: 'Please provide a date',
            },
        },
        // Make sure the form is submitted to the destination defined
        // in the 'action' attribute of the form when valid
        submitHandler: function(form) {
            form.submit();
        },
    });
});
