/**
 * Created by LuisSebastian on 10/25/16.
 */


/**
 * Created by LuisSebastian on 10/8/16.
 */

$(document).ready(function () {
     $.validator.messages.required = "";
     $.validator.messages.number = "";
     $.validator.addMethod("valueNotEquals", function(value, element, arg){
        return arg !== value;
     }, "");
    $("#audio_upload_form").validate({
        rules: {
            upload_song_file: {
                required: true,
                extension: "mp3"
            },
            upload_song_img: {
                required: true,
                extension: "png|jpg"
            },
            upload_song_name: {
                required: true
            },
            upload_song_type: {
                valueNotEquals: "Seleccione un tipo..."
            },
            upload_nombre_artistico: {
                required: true,
                maxlength: 200,
            },
            upload_pais_origen: {
                required: true,
                maxlength: 50,
            },
            upload_ciudad_origen: {
                required: true,
                maxlength: 50,
            },
        }, highlight: function(element) {
            $(element).parent().addClass("has-error");
        }, unhighlight: function(element) {
            $(element).parent().removeClass("has-error");
        }, errorPlacement: function(error, element) {
        },
        submitHandler: function () {
            document.getElementById("audio_upload_form").submit();
            return false;
        }
    });

});
