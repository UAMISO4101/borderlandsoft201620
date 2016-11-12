/**
 * Created by William on 12/10/2016.
 */

$(document).ready(function () {
     $.validator.messages.required = "";
     $.validator.messages.number = "";
     $.validator.addMethod("valueNotEquals", function(value, element, arg){
        return arg !== value;
     }, "");
    $("#registro_form").validate({
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
                minlength: 9,
            },
            password2:{
                required:true,
                minlength: 9,
                equalTo: "#password1",
            },
        }, messages: {
            first_name: "Por favor ingrese su nombre completo",
            last_name: "Por favor ingrese sus apellidos",
            //aniosExperiencia: "Por favor indique cuantos a&ntilde;os de experiencia tiene",
            //tiposDeServicio: "Por favor seleccione el tipo de servicio que ofrecer&aacute;",
            //telefono: "Por favor ingrese un tel&eacute;fono v&aacute;alido",
            email: "Por favor ingrese un correo v&aacute;lido",
            //imagen: "Por favor suba una foto",
            username: "Por favor ingrese su usuario",
            password1: {
                required:"Por favor ingrese su contrase&ntilde;a",
                minlength:"La longitud m&iacute;nima es de 9 caracteres",
            },
            password2: {
                required:"Por favor confirme su contrase&ntilde;a",
                minlength:"La longitud m&iacute;nima es de 9 caracteres",
                equalTo: "La confirmaci&oacute;n no es v&aacute;lida"
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
