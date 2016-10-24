$(function () {
  $('[data-toggle="tooltip"]').tooltip();
  $("[data-hover='tooltip']").tooltip();
})

function like_song(song_id){

  $.ajax({
    type:"POST",
    url:"/like/",
    data: {
      'song_id': song_id
    },
    success: function(data){
      $('#likeButton').removeClass('inactive').addClass('active');
      $('#likeButton').tooltip('hide').attr('data-original-title', "Ya no me Gusta").tooltip('fixTitle');
      $("#likeButton").attr("onclick","unlike_song("+song_id+")");
      $('#song_likes_val_counter').empty()
      $('#song_likes_val_counter').append('<i class=\"glyphicon glyphicon-thumbs-up\"></i> '+data+'')

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
      $('#likeButton').tooltip('hide').attr('data-original-title', "Me Gusta").tooltip('fixTitle');
      $("#likeButton").attr("onclick","like_song("+song_id+")");
      $('#song_likes_val_counter').empty()
      $('#song_likes_val_counter').append('<i class=\"glyphicon glyphicon-thumbs-up\"></i> '+data+'')

    },
    error: function () {
      alert("Se produjo un error inesperado :(")
    }
  });
}