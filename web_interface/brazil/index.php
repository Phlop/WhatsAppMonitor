  <?php
  /**
   * The user index
   *
   * @author Johnnatan Messias <johnme@mpi-sws.org>
   */


  require_once 'include/init.php';
  require_once 'main.php';

  $index_q = get_default($_SESSION, "index_q", null);

  $input_error = get_default($_GET, "input_error", "");
  $input_error = utf8_decode($input_error);

  if ($index_q !== null) {
    if (session_status() == PHP_SESSION_NONE) {
      session_start();
    }
    unset($_SESSION['index_q']);
    header("Location: app.php");
    exit();
  }

  $key = trim(get_default($_GET, 'key', ''));

  //if($key == "LOgIN_AccePted_BY_John_123")
  //    $_SESSION['allowed'] = 1;

  $get_q = trim(get_default($_GET, "q", ""));
  if ($get_q !== "") {
    $get_q = urlencode($get_q);
    if ($logged_in) {
      header("Location: app.php");
      exit();
    } else {
      if (session_status() == PHP_SESSION_NONE) {
        session_start();
      }
      $_SESSION['index_q'] = $get_q;
      header("Location: oauth-redirect.php");
      exit();
    }
  }

  $error_msgs = array(
    "" => null,
    "query_not_found" => "Infelizmente, nesse momento, não temos o resultado pesquisado " . $input_error,
    "date_not_found" => "Infelizmente, nesse momento, não temos nenhum resultado para " . $input_error,
    "empty_search_query" => "Não pudemos encontrar o que você estava procurando.",
    "empty_search_date" => "Não pudemos encontrar a data que você estava procurando.",
    "not_logged_in" => "Primeiramente você precisa realizar o Login!",
    "not_found_user" => "O email ou a senha não possuem cadastro nesse sistema. Verifique e tente novamente.",
  );

  $ecode = get_default($_GET, 'ecode', "");
  $emsg = get_default($error_msgs, $ecode, null);
  ?>


  <style>
    import url('https://fonts.googleapis.com/css?family=Roboto+Slab');

    /* Full-width input fields */
    input[type=text],
    input[type=password] {
      width: 100%;
      padding: 15px;
      margin: 5px 0 22px 0;
      display: inline-block;
      border: none;
      background: #f1f1f1;
    }

    .log_button {
      float: right;
      border-radius: 8px;
      padding: 8px 15px;
      margin: 5px;
      position: relative;
      display: inline-block;
      color: #fff;
      font-family: 'Roboto Slab', sans-serif;
      font-size: 14px;
      font-weight: bold;
    }

    .blue {
      background-color: steelblue;
    }

    .blue:hover {
      background-color: darkblue;


      .bottom_space {
        margin-bottom: 5cm;
        padding-bottom: 3cm;
      }
    }
  </style>


  <?php include 'header.php' ?>

  <div class="container paper-ref">
    <div class="clearfix">
      <?php if (isset($_SESSION['user_logged'])) : ?>
        <a href="logout.php"><button type="button" class="log_button btn-warning">Logout</button></a>
        <?php if ($_SESSION['user']['superuser'] === true) : ?>
          <a href="signup.php"><button type="button" class="log_button btn-primary">
              <p class="lang" key="signup"></p>
            </button></a>
        <?php endif ?>
      <?php else : ?>
        <a href="login.php"><button type="button" class="log_button blue">Login</button></a>
      <?php endif ?>
    </div>
  </div>

  <?php include 'tiles.php' ?>
  <div class="container">

    <?php include_once "include/analyticstracking.php" ?>
    <br>


    <?php if ($emsg !== null) : ?>
      <script>
        $(document).ready(function() {
          modalMessage.show("Caro Visitante", "<?= $emsg; ?>");
        });
      </script>
    <?php endif ?>
    <?php if (isset($_SESSION['user_logged'])) : ?>
      <div class="col-md-12 col-sm-12 col-xs-12">
        <div class="input-group col-md-8 col-sm-8 col-xs-8 center-block">
          <div class="row">
            <div class="col-md-12 col-sm-12 col-xs-12">
              <center style="margin-bottom: 9px;">
                <strong class="lang" key="findcontent"></strong>
                <?php if (isset($_SESSION['last_upd_date'])) : ?>
                  <div>
                    <h5>Last update: <?= DateTime::createFromFormat('Y-m-d', $_SESSION['last_upd_date'])->format('m/d/Y'); ?></h5>
                  </div>
                <?php endif ?>
              </center>
              <div class="input-group">
                <span class="input-group-addon"><i class="glyphicon glyphicon-calendar"></i></span>
                <input type="text" class="form-control date-picker date" placeholder="mm/dd/yyyy" id="datepicker" />
              </div>
            </div>

          </div>
        </div>
      </div>
    <?php endif ?>

    <!--
    <font style="font-size: 18.75px; font-weight:bold;color: #527bbd; margin-bottom: 8px;">  
    <center style="margin-bottom: 9px;">
      Amostra de ...
    </center>
    </font>
    <center>Em breve...</center>
   -->
  </div>


  <div class="container paper-ref">
    <h1 class="lang" key="howitworks"></h1>

    <p class="lang" key="sitedescription"></p>
    <p class="lang" key="nsfwcontent"></p>
    <a href="https://yahooeng.tumblr.com/post/151148689421/open-sourcing-a-deep-learning-solution-for" target="_blank">Yahoo Open NSFW Model</a>
  </div>

  <div class="bottom_space"> <br> <br> <br> </div>
  <script language="Javascript" type="text/javascript">
    $('#datepicker').datepicker({
      format: 'mm/dd/yyyy',
      language: 'pt-BR',
      todayHighlight: true,
      startDate: '22/03/2018',
      endDate: '<?= DateTime::createFromFormat('Y-m-d', $_SESSION['last_upd_date'])->format('m/d/Y'); ?>',
      language: 'pt-BR',
      // datesDisabled: ['12/04/2018']
    }).on("changeDate", function(e) {
      var day = (e.date.getDate() > 9 ? "" : "0") + (e.date.getDate());
      var month = (e.date.getMonth() + 1 > 9 ? "" : "0") + (e.date.getMonth() + 1);
      var year = e.date.getFullYear();
      value_date = year + "-" + month + "-" + day;
      document.location.href = "app.php?flag=images&obtained_at=" + value_date;
    });

    function search_trends() {
      var value = document.getElementsByName('query')[0].value.trim().toLowerCase();
      if (value) {
        if (value[0] == "#")
          value = value.substring(1);
        document.location.href = "app.php?query=" + value;
      } else {
        $(document).ready(function() {
          modalMessage.show("Caro Visitante", "A entrada é inválida");
        });
      }
    }
  </script>
  <script>
    $(document).ready(function() {

      //The default language is English
      var lng = localStorage.getItem('lang') || 'pt-br';
      var allInputs = document.getElementsByTagName("option");
      var results = [];
      for (var x = 0; x < allInputs.length; x++)
        if (allInputs[x].value == lng)
          allInputs[x].selected = "true";

      loadlang();
    });
  </script>

  <?php include 'footer.php'; ?>
