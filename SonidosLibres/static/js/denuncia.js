/**
 * Created by William on 20/11/2016.
 */

$(document).ready(function () {
     $.validator.messages.required = "";
     $.validator.messages.number = "";
     $.validator.addMethod("valueNotEquals", function(value, element, arg){
        return arg !== value;
     }, "");
    $("#denuncia_form").validate({
        rules: {
            texto: {
                required: true,
            },
            tipo_denuncia:{
                valueNotEquals: "Seleccione un tipo..."
            }
        }, highlight: function(element) {
            $(element).parent().addClass("has-error");
        }, unhighlight: function(element) {
            $(element).parent().removeClass("has-error");
        },
        submitHandler: function (form) {
            agregarDenuncia();
            return false;
        }
    });

});


/**
 * Agregar un comentario a un sonido por usuario
 */
function agregarDenuncia(){
    var songId = $("#songId").val();
    var userId = $("#userId").val();

    var item = {};
    item ["val_denuncia"] = $("#texto").val();
    item ["ind_tipo_denuncia"] = $('select[name=tipo_denuncia]').val;
    item ["audio"] = songId;
    item ["fec_creacion_denuncia"] = new Date();
    item ["autor"] = userId;

    $.ajax({
        type: "POST",
        async: false,
        url: "/api/denuncia/",
        dataType: "json",
        data:  JSON.stringify(item),
        contentType: "application/json; charset=utf-8",
        success: function (msg)
        {
            $("#texto").val('');
            $('select[name=tipo_denuncia]').val('Seleccione un tipo...');
            $("#reportModal").modal('hide');
        },
        error: function (err)
        {
            console.log(err);
            alert("Se produjo un error inesperado :(");
        }
    });
}