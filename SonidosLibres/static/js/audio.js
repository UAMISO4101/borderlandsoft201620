$(function () {
    $('[data-toggle="tooltip"]').tooltip();
    $("[data-hover='tooltip']").tooltip();
    getAudios();
});

function getAudios() {
    var songId = backVars.songId; // $("#songId").val();
    $.ajax({
        type:"GET",
        contentType:"application/json; charset=utf8",
        url:"/api/audios/" + songId + "/?format=json",
        success:function (response) {
            var listArtistas = response.artistas;
            var listAlbums = response.albums;
            if(listArtistas != null && listArtistas != undefined && listArtistas != "") {
                for (var i = 0; i <= listArtistas.length - 1; i++) {
                    getArtistas(listArtistas[i]);
                }
            }

            if(listAlbums != null && listAlbums != undefined && listAlbums != "") {
                for (i = 0; i <= listArtistas.length - 1; i++) {
                    getAlbums(listAlbums[i]);
                }
            }
            $('#spanNumArtistas').append(listArtistas.length);
            $('#spanNumAlbums').append(listAlbums.length);
        }

    });
}

function getArtistas(artista) {
    $.ajax({
        type:"GET",
        contentType:"application/json; charset=utf8",
        url:"/api/audiosbyartista/"+artista.id+"/?format=json",
        success: function (response) {
            var conteoObras = response.length;
            var divArtistas = '<div class="media">' +
                '<div class="media-left">';
            if(artista.val_imagen == null || artista.val_imagen == "") {
                divArtistas = divArtistas + '<div class="detail-img artist-img si50 text-center">' +
                    '<i class="fa fa-user"></i>' +
                    '</div>';
            }
            else {
                divArtistas = divArtistas + '<img class="detail-img si50" src="'+artista.val_imagen+'">';
            }
            divArtistas = divArtistas +  '</div>' +
                '<div class="media-body">' +
                '<span class="media-heading artist-detail-title"><a href="/user/'+ artista.id + '">'+ artista.nom_artistico +'</a></span>' +
                conteoObras + ' obras' +
                '</div>' +
                '</div>';


            $('#divArtistas').append(divArtistas);
        }
    });
}

function getAlbums(album) {
    var divAlbums = '<div class="col-xs-6 col-sm-4 col-md-3 col-lg-2">'+
        '<div class="box album-box">'+
        '<a href="/album/'+ album.id + '">';
    if(album.val_imagen == null || album.val_imagen == undefined || album.val_imagen.trim() == "") {
        divAlbums = divAlbums + '<div class="detail-img album-img album-big text-center">' +
            '<i class="fa fa-music"></i>' +
            '<i class="fa fa fa-circle-thin"></i>' +
            '</div>';
    }
    else{
        divAlbums = divAlbums + '<img class="detail-img album-img album-big" src="' + album.val_imagen + '"  >';
    }
    divAlbums = divAlbums + '<div class="details-box">'+
        '<span>'+album.nom_album+'</span>'+
        '<br>'+
        '<div class="text-right"><small>'+new Date(album.fec_creacion_album).getFullYear()+'</small></div>'+
        '</div>'+
        '</a>'+
        '</div>'+
        '</div>';

    $('#divAlbums').append(divAlbums);

}
