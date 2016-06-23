var audioElm = document.getElementById("audio1");
var now_play_id = null;

function toggleAudio(id) {
  if (document.getElementById("audio1")) {
    if(now_play_id == id && audioElm.paused == false) {
      pauseAudio();
      $("#play_" + id).addClass("fa-play");
      $("#play_" + id).removeClass("fa-stop");
    }
    else {
      now_play_id = id;
      playAudio(id);
      $(".fa-stop").removeClass("fa-stop").addClass("fa-play");

      $("#play_" + id).removeClass("fa-play");
      $("#play_" + id).addClass("fa-stop");
    }
  }
}

function playAudio(id) {
  audioElm.src = "https://b.ppy.sh/preview/" + id + ".mp3";
  audioElm.play();
}

function pauseAudio() {
  audioElm.pause();
}

audioElm.onended = function() {
  pauseAudio();
  $(".fa-stop").removeClass("fa-stop").addClass("fa-play");
};
audioElm.onerror = function() {
  pauseAudio();
  $(".fa-stop").removeClass("fa-stop").addClass("fa-play");
};

function s_copy(){
  var str = ("javascript:(function(h,n){n=h.pathname.split('s/')[1];if(h.host=='osu.ppy.sh'&&n){h.href='http://osu.euihyun.kim/HDD/OSU/beatmaps/'+n+'.osz'}})(window.location)");
  var copyFrom = $('<textarea/>');
  copyFrom.css({
   position: "absolute",
   left: "-1000px",
   top: "-1000px",
  });
   copyFrom.text(str);
   $('body').append(copyFrom);
   copyFrom.select();
   document.execCommand('copy');
}

$(document).ready(function(){
  $(".h_title").click(function(){
      $(this).closest('.content_holder').find('.h_hide').toggle("slow");
  });
});

$(document).ready(function(){
    var page = 1;
    var $_GET = {};

    document.location = '#';
    document.location.search.replace(/\??(?:([^=]+)=([^&]*)&?)/g, function () {
        function decode(s) {
            return decodeURIComponent(s.split("+").join(" "));
        }

        $_GET[decode(arguments[1])] = decode(arguments[2]);
    });

    $(window).scroll(function(){
      if ($('#content').height() - $(window).scrollTop() < $(window).height() && $_GET["id"] == undefined)
      {
          $.ajax({
          type: "POST",
          url: "more_beatmaps.php",
          data: "p="+ (++page),
          cache: false,
          success: function(html){
          $("#content>ul").append(html);
        }
        });
      } return false;
    });
});
