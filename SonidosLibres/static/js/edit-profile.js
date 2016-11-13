/**
 * Created by William on 13/11/2016.
 */

$(document).ready(function () {
     $.validator.messages.required = '';
     $.validator.messages.number = '';
     $.validator.addMethod("valueNotEquals", function(value, element, arg){
        return arg !== value;
     }, "");
    $('#edit_perfil_form').validate({
        rules: {
            first_name: {
                required: true,
            },
            last_name: {
                required: true,
            },
            upload_user_img: {
                required: false,
                extension: "png|jpg"
            },
            email: {
                required: true,
                email:true,
            },
        }, messages: {
            first_name: "Por favor ingrese su nombre completo",
            last_name: "Por favor ingrese sus apellidos",
            email: "Por favor ingrese un correo v&aacute;lido",
        }, highlight: function(element) {
            $(element).parent().addClass('has-error');
        }, unhighlight: function(element) {
            $(element).parent().removeClass('has-error');
        }, errorPlacement: function(error, element) {
        },
        submitHandler: function () {
            document.getElementById('edit_perfil_form').submit();
            return false;
        }
    });

    $("#editProfile").click(function(ev) { // for each edit item <a>
        ev.preventDefault(); // prevent navigation
        url = ($(this)[0].href); //get the href from <a>
        $.get(url, function(results){
           var form = $("#edit_perfil_form", results);
           //update the dom with the received results
            $('#edit_perfil_form').replaceWith(form);
            $("#editPerfil").modal('show');
         }, "html");
         return false; // prevent the click propagation
   });

});