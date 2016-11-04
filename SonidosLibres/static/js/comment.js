/**
 * Created by William on 24/10/2016.
 */

$(document).ready(function () {
     $.validator.messages.required = '';
     $.validator.messages.number = '';
     $.validator.addMethod("valueNotEquals", function(value, element, arg){
        return arg != value;
     }, "");
    $('#comment_form').validate({
        rules: {
            texto_comentario: {
                required: true,
            },
        }, highlight: function(element) {
            $(element).parent().addClass('has-error');
        }, unhighlight: function(element) {
            $(element).parent().removeClass('has-error');
        },
        submitHandler: function (form) {
            document.getElementById('comment_form').submit()
            //agregarComentario();
            return false;
        }
    });

});
