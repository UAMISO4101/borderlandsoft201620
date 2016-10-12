/**
 * Created by William on 12/10/2016.
 */

$(document).ready(function () {
     $.validator.messages.required = '';
     $.validator.messages.number = '';
     $.validator.addMethod("valueNotEquals", function(value, element, arg){
        return arg != value;
     }, "");
    $('#registro_form').validate({
        rules: {
            username: {
                required: true,
            },
            first_name: {
                required: true,
            },
            last_name: {
                required: true,
            },
            email:{
                required: true,
                email:true,
            },
            password1:{
                required:true,
            },
            password2:{
                required:true,
            },
        }, highlight: function(element) {
            $(element).parent().addClass('has-error');
        }, unhighlight: function(element) {
            $(element).parent().removeClass('has-error');
        },
        submitHandler: function (form) {
            document.getElementById('donation_form').submit()
            return false;
        }
    });

});
