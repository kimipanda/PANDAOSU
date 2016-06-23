<?php
    $query = "Select osu_beatmaps.id, osu_beatmaps.title, osu_artists.name From osu_beatmaps INNER JOIN osu_artists ON osu_beatmaps.artist = osu_artists.idx
              where LOWER(osu_artists.name) like LOWER('%".$_GET[n]."%') or
              LOWER(osu_beatmaps.title) like LOWER('%".$_GET[n]."%') or
              osu_beatmaps.id like LOWER('%".$_GET[n]."%');";

    $result = mysqli_query($conn, $query);
    
    while($row = mysqli_fetch_row($result))
    {
      mysqli_data_seek($result,$row);
      $beatmap_list = "<li style='background: url(http://b.ppy.sh/thumb/".$row[0]."l.jpg) no-repeat; background-size: 160px 120px;'>
            <button id='play_".$row[0]."' class='fa fa-play' onclick='toggleAudio(".$row[0].")'></button>
            <div class='bitmap'>
                <a href='/HDD/OSU/s/".$row[0].".osz'><p class='title'>".$row[1]."</p></a>
                <a href=./?n=".$row[2]."><p class='artist'>".$row[2]."</p></a>
            </div>
           </li>";
      echo trim(preg_replace('/\s+/',' ',$beatmap_list));
    }

?>
