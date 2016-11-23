/**
 * Created by LuisSebastian on 10/25/16.
 */


/**
 * Created by LuisSebastian on 11/22/16.
 */

$(document).ready(function () {
     $.validator.messages.required = "";
     $.validator.messages.number = "";
     $.validator.addMethod("valueNotEquals", function(value, element, arg){
        return arg !== value;
     }, "");
    $("#audio_edit_form").validate({
        rules: {
            edit_song_image_name: {
                required: true,
                extension: "png|jpg"
            },
            edit_song_name: {
                required: true
            },
            edit_song_type: {
                valueNotEquals: "Seleccione un tipo..."
            },
        }, highlight: function(element) {
            $(element).parent().addClass("has-error");
        }, unhighlight: function(element) {
            $(element).parent().removeClass("has-error");
        }, errorPlacement: function(error, element) {
        },
        submitHandler: function () {
            document.getElementById("audio_edit_form").submit();
            return false;
        }
    });

});
