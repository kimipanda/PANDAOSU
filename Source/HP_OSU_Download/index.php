<!DOCTYPE html>
<html>
<head>
    <!-- #2016.01.01 MOE PANDAOSU BEATMAPS // by kimipanda -->
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0 user-scalable=no"/>
    <meta charset="utf-8" />
    <title>MOE PANDA OSU! Bitmap Mirror</title>

    <link href="//maxcdn.bootstrapcdn.com/font-awesome/4.1.0/css/font-awesome.min.css" rel="stylesheet" />
    <link href="CSS/Style.css" rel="stylesheet" />

    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.3.0/jquery.min.js"></script>
</head>
<body>
    <audio id="audio1" style="width:25%" >Audio not supported</audio>
    <header>
        <div id="nav">
            <div><a href="."> PANDA <p>OSU</p> </a></div>
            <ul class="nav_drop1">
                <li><a href="javascript:alert('준비중');">Support</a></li>
                <li><a href="?id=3">Help</a></li>
                <li>
                      <form method="get" action="" autocomplete="off">
                        <input name="n" type="search" placeholder="Search" />
                        <button class="fa fa-search"></button>
                      </form>
                </li>
            </ul>
        </div>
    </header>
    <section>
        <div id="content">
              <ul>
                  <?php
                  include_once "DB_info.php";

                  if ($_GET['n'] == '' && $_GET['id'] == '')
                  {
                    include_once "more_beatmaps.php";
                  } elseif ($_GET['n'] != '') {
                    include_once "search.php";
                  }
                  ?>
              </ul>

              <?php if ($_GET['id'] == 3) {
                include_once "help.php";
              } ?>
        </div>
    </section>
</body>
<script src="./main.js"></script>
</html>
