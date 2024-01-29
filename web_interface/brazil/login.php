<?php
/**
 * The user search page
 *
 * @author Johnnatan Messias <johnme@mpi-sws.org>
 */

require_once 'include/init.php';
require_once 'main.php';

if (isset($_SESSION['user_logged'])){
    header("Location: ./index.php");
    exit();
}

$input_error = get_default($_GET, "input_error", "");

$error_msgs = array(
  "" => null,
  "query_not_found" => "Infelizmente, nesse momento, não temos o resultado pesquisado " . $input_error,
  "date_not_found" => "Infelizmente, nesse momento, não temos nenhum resultado para " . $input_error,
  "empty_search_query" => "Não pudemos encontrar o que você estava procurando.",
  "empty_search_date" => "Não pudemos encontrar a data que você estava procurando.",
  "not_logged_in" => "Primeiramente você precisa realizar o Login!",
  "not_found_user" => "O e-mail ou a senha não estão cadastrados no sitema. Verifique e tente novamente.",
);

$ecode = get_default($_GET, 'ecode', "");
$emsg = get_default($error_msgs, $ecode, null);

?>

<?php include 'header.php'?>
<?php include 'tiles.php'?>


  <?php if ($emsg !== null): ?>
    <script>
    $(document).ready(function(){
      modalMessage.show("Caro Visitante", "<?=$emsg;?>");
    });

    </script>
  <?php endif?>

  <style>
body {font-family: Arial, Helvetica, sans-serif;}
* {box-sizing: border-box}

/* Full-width input fields */
input[type=text], input[type=password] {
    width: 100%;
    padding: 15px;
    margin: 5px 0 22px 0;
    display: inline-block;
    border: none;
    background: #f1f1f1;
}

input[type=text]:focus, input[type=password]:focus {
    background-color: #ddd;
    outline: none;
}

hr {
    border: 1px solid #f1f1f1;
    margin-bottom: 25px;
}

/* Set a style for all buttons */
button {
    background-color: #4CAF50;
    color: white;
    padding: 14px 20px;
    margin: 8px 0;
    border: none;
    cursor: pointer;
    width: 100%;
    opacity: 0.9;
}

button:hover {
    opacity:1;
}

/* Extra styles for the cancel button */
.cancelbtn {
    padding: 14px 20px;
    background-color: #f44336;
}

/* Float cancel and signup buttons and add an equal width */
.cancelbtn, .signupbtn {
  float: left;
  width: 50%;
}

/* Add padding to container elements */
.container {
    padding: 16px;
}

/* Clear floats */
.clearfix::after {
    content: "";
    clear: both;
    display: table;
}

/* Change styles for cancel button and signup button on extra small screens */
@media screen and (max-width: 300px) {
    .cancelbtn, .signupbtn {
       width: 100%;
    }
}
</style>

<script>
        $(document).ready(function() {

            //The default language is English
            var lng = localStorage.getItem('lang') || 'pt-br';
            var allInputs = document.getElementsByTagName("option");
            var results = [];
            for(var x=0;x<allInputs.length;x++)
                if(allInputs[x].value == lng)
                    allInputs[x].selected = "true";
            
            loadlang();
            });
    </script>


  <script src="js/md5/md5.min.js"></script>


  <form onsubmit="return validate_form(this)" method="POST" action="check_credentials.php" style="border:1px solid #ccc">
  <div class="container">
    <h1>Login</h1>
    <p class="lang" key="loginpage"></p>
    <hr>
    <div class="form-inline">
    <div class="form-group col-md-6">
    <label for="email"><b>E-mail</b></label>
    <input type="text" placeholder="E-mail" name="inputEmail" required>
    </div>
    <div class="form-group col-md-6">
    <label for="psw"><b class="lang" key="password"></b></label>
    <input type="password" placeholder="Password" name="inputPassword" required>
    </div>
    </div>
    <div class="clearfix">
      <button type="submit" class="signupbtn">Login</button>
    </div>
  </form>

<script>
  function validate_form(form) {
    var passwd_enc = md5(form.inputPassword.value);
    form.inputPassword.value = passwd_enc;
    return true; 
  }
</script>
</body>
</html>
