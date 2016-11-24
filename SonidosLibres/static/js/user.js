$(function () {
    $("[data-toggle='tooltip']").tooltip();
    $("[data-hover='tooltip']").tooltip();
});


function follow_artist(artistId){
  $.ajax({
    type:"POST",
    url:"/follow/",
    data: {
      "artist_id": artistId
    },
    success: function(data){
      $("#followButton").removeClass("inactive").addClass("active");
      $("#followButton").attr("data-original-title", "Estas siguiendo");
      $("#artist_followers_val_counter").empty();
      $("#artist_followers_val_counter").append(data);
    },
    error: function () {
      alert("Se produjo un error inesperado :(");
    }
  });
}