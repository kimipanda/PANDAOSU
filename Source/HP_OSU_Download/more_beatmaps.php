<?php
  include_once "DB_info.php";

  $count = 0;
  if ($_POST[p] == '')
  {
    $page1 = 0;
    $page2 = 42;
  } else {
    $page1 = ($_POST['p'] -1) * 43 ;
    $page2 = ($_POST['p'] * 42);

    $query = "select count(*) from osu_beatmaps";
    $result = mysqli_query($conn, $query);
    $row = mysqli_fetch_row($result);
    $count = $row[0];

    if ($count < $page2) {
      $page2 = $count;
    }
  }

  if ($count != $page2)
  {
    $query = "select A.idx, A.name, B.id, B.title from osu_artists A, osu_beatmaps B where B.artist = A.idx order by idx ASC limit ".$page1.", ".$page2."";
    $result = mysqli_query($conn, $query);

    while($row = mysqli_fetch_row($result))
    {
      mysqli_data_seek($result,$row);

      $beatmap_list = "<li style='background: url(http://b.ppy.sh/thumb/".$row[2]."l.jpg) no-repeat; background-size: 160px 120px;'>
            <button id='play_".$row[2]."' class='fa fa-play' onclick='toggleAudio(".$row[2].")'></button>
            <div class='bitmap'>
                <a href='/HDD/OSU/beatmaps/".$row[2].".osz'><p class='title'>".$row[3]."</p></a>
                <a href=./?n=".$row[1]."><p class='artist'>".$row[1]."</p></a>
            </div>
           </li>";
      echo trim(preg_replace('/\s+/',' ',$beatmap_list));
    }
  }
?>
