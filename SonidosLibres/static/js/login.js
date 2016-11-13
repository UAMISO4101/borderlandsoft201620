/**
 * Created by William on 12/10/2016.
 */


$(document).ready(function () {
     $.validator.messages.required = "";
     $.validator.messages.number = "";
     $.validator.addMethod("valueNotEquals", function(value, element, arg){
        return arg !== value;
     }, "");
    $("#login_form").validate({
        rules: {
            username: {
                required: true,
            },
            password: {
                required: true,
                minlength: 9,
            },
        }, messages: {
            username: "Por favor ingrese su usuario",
            password: {
                required:"Por favor ingrese su contrase&ntilde;a",
                minlength:"La longitud m&iacute;nima es de 9 caracteres",
            },
        }, highlight: function(element) {
            $(element).parent().addClass("has-error");
        }, unhighlight: function(element) {
            $(element).parent().removeClass("has-error");
        },
        submitHandler: function (form) {
            form.submit();
            return false;
        }
    });

});
