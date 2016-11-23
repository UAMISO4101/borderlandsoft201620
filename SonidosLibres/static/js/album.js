$(function () {
  $("[data-toggle='tooltip']").tooltip();
  $("[data-hover='tooltip']").tooltip();

});

function AgregarAAlbum() {
    var songId = $("#songId").val();
    var albums = [];
    $("#table-album-list .chk-album").each(function (i, checkBox) {
        albums.push({
            id: $(checkBox).val(),
            checked: $(checkBox).is(":checked")
        });
    });

    var request = {
        audioId: songId,
        albums: albums
    };
    console.log(request);
    $.ajax({
        type: "PUT",
        url: "/api/audio/" + songId + "/albums",
        dataType: "json",
        data:  JSON.stringify( request ),//{ albums: albums }),
        contentType: "application/json; charset=utf-8",
        success: function ()
        {
            getAudios();
            $("#addToAlbumModal").modal('hide');
        },
        error: function (err)
        {
            console.log("Oh no!");
            console.log(err);
            console.log(err.responseText);
        }
    });
}
