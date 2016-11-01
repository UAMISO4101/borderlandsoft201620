/**
 * Created by William on 12/10/2016.
 */


$(document).ready(function () {
     $.validator.messages.required = '';
     $.validator.messages.number = '';
     $.validator.addMethod("valueNotEquals", function(value, element, arg){
        return arg != value;
     }, "");
    $('#login_form').validate({
        rules: {
            username: {
                required: true,
            },
            password:{
                required:true,
            },
        }, highlight: function(element) {
            $(element).parent().addClass('has-error');
        }, unhighlight: function(element) {
            $(element).parent().removeClass('has-error');
        },
        submitHandler: function (form) {
            form.submit()
            return false;
        }
    });

});
