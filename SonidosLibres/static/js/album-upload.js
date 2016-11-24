$(document).ready(function () {
     $.validator.messages.required = "";
     $.validator.messages.number = "";
     $.validator.addMethod("valueNotEquals", function(value, element, arg){
        return arg !== value;
     }, "");
    $("#album_upload_form").validate({
        rules: {
            upload_album_img: {
                required: true,
                extension: "png|jpg"
            },
            upload_album_name: {
                required: true
            },
            upload_album_year: {
                valueNotEquals: "Año"
            }
        }, highlight: function(element) {
            $(element).parent().addClass("has-error");
        }, unhighlight: function(element) {
            $(element).parent().removeClass("has-error");
        }, errorPlacement: function(error, element) {
        },
        submitHandler: function () {
            document.getElementById("album_upload_form").submit();
            return false;
        }
    });
});