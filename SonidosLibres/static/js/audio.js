function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

/**
 * Obtiene la última calificación de un audio por usuario
 */
function getUltimaCalificacion(){
        var numStarts = 0;
        var songId = $('#songId').val();
        var userId = $('#userId').val();
        $.ajax({
            type:"GET",
            contentType:"application/json; charset=utf8",
            url:"/api/ratebyuseraudio/" + songId + "/"+ userId + "/?format=json",
            success:function (response) {
                for (var i = 0; i <= response.length - 1; i++) {
                    numStarts = response[i].val_rating;
                    break;
                }
                for(var i=1;i<=5;i++)
                {
                    if(i<=numStarts)
                        $('.rating-input').append('<i class="fa fa-star" data-value="'+ i +'"></i>')
                    else
                        $('.rating-input').append('<i class="fa fa-star-o" data-value="'+ i +'"></i>')
                }
                $('.rating').val(numStarts);
            }
        });
 }

/**
 * Obtiene los Ratings por audio
 */
function getRatingsByAudio(){
        var songId = backVars.songId; // $("#songId").val();
        $.ajax({
            type:"GET",
            contentType:"application/json; charset=utf8",
            url:"/api/ratebyaudio/" + songId + "/?format=json",
            success:function (response) {
                var txtCalificacion;
                var average = 0;
                var sumatoria = 0;

                if(response.length === 1)
                    txtCalificacion = response.length + " calificación";
                else
                    txtCalificacion = response.length + " calificaciones";

                for(var i=0;i<response.length;i++) {
                    sumatoria =  sumatoria + response[i].val_rating;
                }

                if(sumatoria > 0) {
                    average = Math.round((sumatoria / i) * 10) / 10;
                    $('#classPromedio').empty();
                    $('#classPromedio').append(average);
                }
                else{
                    $('#classPromedio').empty();
                }
                $('#smallCalificaciones').empty();
                $('#smallCalificaciones').append(txtCalificacion);
            }
        });
    }

/**
 * Obtener audios de un artista
 */
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
                for (var i = 0; i <= listAlbums.length - 1; i++) {
                    getAlbums(listAlbums[i]);
                }
            }
            $('#spanNumArtistas').append(listArtistas.length);
            $('#spanNumAlbums').append(listAlbums.length);
        }

    });
}

/**
 * Obtiene los artistas relacionados con un audio
 * @param artista
 */
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

/**
 * Se obtiene la lista de albums
 * @param album
 */
function getAlbums(album) {
    console.log(album);
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

function like_song(song_id){
  $.ajax({
    type:"POST",
    url:"/like/",
    data: {
      'song_id': song_id
    },
    success: function(data){
      $('#likeButton').removeClass('inactive').addClass('active');
      // $('#likeButton').tooltip('hide').attr('data-original-title', "Ya no me Gusta").tooltip('fixTitle');
      $('#likeButton').attr('data-original-title', "Ya no me Gusta");
      $("#likeButton").attr("onclick","unlike_song("+song_id+")");
      $('#song_likes_val_counter').empty();
      $('#song_likes_val_counter').append(data)

    },
    error: function () {
      alert("Se produjo un error inesperado :(")
    }
  });
}


function unlike_song(song_id){
  $.ajax({
    type:"POST",
    url:"/unlike/",
    data: {
      'song_id': song_id
    },
    success: function(data){
      $('#likeButton').removeClass('active').addClass('inactive');
      // $('#likeButton').tooltip('hide').attr('data-original-title', "Me Gusta").tooltip('fixTitle');
      $('#likeButton').attr('data-original-title', "Ya no me Gusta");
      $("#likeButton").attr("onclick","like_song("+song_id+")");
      $('#song_likes_val_counter').empty()
      $('#song_likes_val_counter').text(data)

    },
    error: function () {
      alert("Se produjo un error inesperado :(")
    }
  });
}

/**
 * Agregar un comentario a un sonido por usuario
 */
function agregarComentario(){
    var songId = $('#songId').val();
    var userId = $('#userId').val();

    item = {}
    item ["val_comentario"] = $('#texto_comentario').val();
    item ["ind_publicado"] = 'True';
    item ["audio"] = songId;

    if(userId != null && userId != undefined && userId != 'None'){
        item ["autor"] = userId;
    }

    $.ajax({
        type: "POST",
        async: false,
        url: '/api/comment/',
        dataType: "json",
        data:  JSON.stringify(item),
        contentType: "application/json; charset=utf-8",
        success: function (msg)
        {
            mostrarComentarios();
        },
        error: function (err)
        { alert(err.responseText);}
    });
}


/**
 * Consume api rate, para calificar un artista
 */
function calificar() {
    var calificacion = $('.rating').val();
    var songId = $('#songId').val();
    var userId = $('#userId').val();

    var calificacionAnterior = getRatingsByAudioAutor(songId, userId);
    if(calificacionAnterior != undefined && calificacion === calificacionAnterior.toString()){
        $('.rating-input').empty();
        getRatingsByAudio();
        getUltimaCalificacion();
        return;
    }

    item = {}
    item ["val_rating"] = calificacion;
    item ["audio"] = songId;

    if (userId != null && userId != undefined && userId != 'None') {
        item ["autor"] = userId;
    }

    $.ajax({
        type: "POST",
        url: '/api/rate/',
        dataType: "json",
        data: JSON.stringify(item),
        contentType: "application/json; charset=utf-8",
        "beforeSend": function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        success: function (msg) {
            getRatingsByAudio();
            console.log(calificacion);
        },
        error: function (err) {
            console.log(err.responseText);
        }
    });

    /**
     * elimina la calificación de un audio por usuario
     * @param idRating
     */
    function eliminarCalificacion(idRating) {
        $.ajax({
            type: "DELETE",
            url: '/api/rate-delete/' + idRating,
            dataType: "json",
            //data: JSON.stringify(item),
            contentType: "application/json; charset=utf-8",
            "beforeSend": function (xhr, settings) {
                $.ajaxSettings.beforeSend(xhr, settings);
            },
            success: function (msg) {
                console.log(calificacion);
            },
            error: function (err) {
                console.log(err.responseText);
            }
        });
    }

    /**
     * Obtiene las calificaciones de un audio por usuario
     * @param audioId
     * @param autorId
     * @param calificacion
     */
    function getRatingsByAudioAutor(audioId, autorId) {
        var calificacionAnterior;
        $.ajax({
            type: "GET",
            contentType: "application/json; charset=utf8",
            url: "/api/ratebyuseraudio/" + audioId + "/" + autorId + "/?format=json",
            success: function (response) {
                for (var i = 0; i <= response.length - 1; i++) {
                    eliminarCalificacion(response[i].id);
                    calificacionAnterior = response[i].val_rating;
                }
            },
            async: false,
        });
        return calificacionAnterior;
    }
}

    function getComentarios() {
        var songId = backVars.songId; // $("#songId").val();
        var monthNames = [
            "Enero", "Febrero", "Marza",
            "Abril", "Mayo", "Junio", "Julio",
            "Agosto", "Septiembre", "Octubre",
            "Noviembre", "Deciembre"
        ];

        $.ajax({
            type: "GET",
            contentType: "application/json; charset=utf8",
            url: "/api/comments-list/" + songId + "/?format=json",
            success: function (response) {
                var conteoComentarios = response.length;
                var divComments = '';
                for (var i = 0; i <= response.length - 1; i++) {
                    var comentario = response[i];

                    divComments = divComments + '<div class="media">' +
                        '<div class="media-left">';

                    if (comentario.autor == null || comentario.autor == "" ||
                        comentario.autor.val_imagen == null || comentario.autor.val_imagen == "") {
                        divComments = divComments + '<div class="detail-img artist-img si50 text-center">' +
                            '<i class="fa fa-user"></i>' +
                            '</div>';
                    }
                    else {
                        divComments = divComments + '<img class="detail-img si50" src="' + comentario.autor.val_imagen + '">';
                    }
                    divComments = divComments + '</div>' +
                        '<div class="media-body">' +
                        '<span class="media-heading artist-detail-title"> ';
                    if (comentario.autor == null || comentario.autor == "" ||
                        comentario.autor.full_name == null || comentario.autor.full_name == "") {

                        divComments = divComments + '<a href="#">Desconocido</a>';

                    } else {
                        divComments = divComments + '<a href="#">' + comentario.autor.full_name + '</a>';
                    }
                    divComments = divComments + '</span>';
                    divComments = divComments + comentario.val_comentario;
                    //divComments = divComments + '<div class="date-comment"><small> ' + $.datepicker.parseDate( "yy-mm-dd", new DateTime(comentario.fec_creacion_comen)) + '| Octubre 12 de 2016, 3:08 PM ' + '</small></div>' ;
                    divComments = divComments +
                        '</div>' +
                        '</div>';

                }

                $('#divComments').html(divComments);
                $('#spanNumComentarios').html(conteoComentarios);
            }
        });
    }


    $(function () {
        $('[data-toggle="tooltip"]').tooltip();
        $("[data-hover='tooltip']").tooltip();
        $('.rating-input').empty();
        getRatingsByAudio();
        getAudios();
        getComentarios();
        getUltimaCalificacion();
    });



    $(document).ready(function(){
      $("#calificar").on('click', function(e){
        var $el = $(this);
        if($el.data('clicked')){
          // Previously clicked, stop actions
          e.preventDefault();
          e.stopPropagation();
        }else{
          calificar();
          // Mark to ignore next click
          $el.data('clicked', true);
          // Unmark after 1 second
          window.setTimeout(function(){
            $el.removeData('clicked');
          }, 300)
        }
      });
    });