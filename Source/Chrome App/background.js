var newDiv = null;
var imgurl = chrome.extension.getURL("images/BeatmapDownload.png");

newDiv = document.createElement("img");
newDiv.src = imgurl;
newDiv.style.cursor = "pointer";
newDiv.addEventListener("click", function(e) {
  var h = window.location;
  var n = h.pathname.split('s/')[1];
  if(h.host == 'osu.ppy.sh' && n){
    h.href='http://osu.euihyun.kim/HDD/OSU/beatmaps/' + n + '.osz';
  }
});

document.querySelector(".beatmapDownloadButton").appendChild(newDiv);
