/**
 * Created by William on 24/10/2016.
 */

$(document).ready(function () {
     $.validator.messages.required = "";
     $.validator.messages.number = "";
     $.validator.addMethod("valueNotEquals", function(value, element, arg){
        return arg !== value;
     }, "");
    $("#comment_form").validate({
        rules: {
            texto_comentario: {
                required: true,
            },
        }, highlight(element) {
            $(element).parent().addClass("has-error");
        }, unhighlight(element) {
            $(element).parent().removeClass("has-error");
        },
        submitHandler(form) {
            agregarComentario();
            return false;
        }
    });

});


/**
 * Agregar un comentario a un sonido por usuario
 */
function agregarComentario(){
    var songId = $("#songId").val();
    var userId = $("#userId").val();

    var item = {};
    item ["val_comentario"] = $("#texto_comentario").val();
    item ["ind_publicado"] = "True";
    item ["audio"] = songId;
    item ["fec_creacion_comen"] = new Date();

    if(userId !== null && userId !== "None"){
        var autor = {};
        autor ["id"] = userId;
        item ["autor"] = autor;
    }

    $.ajax({
        type: "POST",
        async: false,
        url: "/api/comment/",
        dataType: "json",
        data:  JSON.stringify(item),
        contentType: "application/json; charset=utf-8",
        success: function (msg)
        {
            $("#texto_comentario").val("");
            $("#commentModal").modal("hide");
            $('a[href="#tab3"]').click();
        },
        error: function (err)
        {
            alert("Se produjo un error inesperado :(");
        }
    });
}

