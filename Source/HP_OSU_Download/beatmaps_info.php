<?php
    $query = "select A.idx, A.name, B.id, B.title from osu_artists A, osu_beatmaps B where B.artist = A.idx order by idx ASC limit 42";
    $result = mysqli_query($conn, $query);
?>
