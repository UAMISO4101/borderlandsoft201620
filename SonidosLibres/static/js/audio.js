$(function () {
  $('[data-toggle="tooltip"]').tooltip();
  $("[data-hover='tooltip']").tooltip();
})

function test(song_id){

  $.ajax({
    type:"POST",
    url:"/like/",
    data: {
      'song_id': song_id
    },
    success: function(data){
      if(data == "SUCCESS"){
         location.reload();
      }
    },
    error: function (data) {
      alert("Se produjo un error inesperado :(")
    }
  });
}
