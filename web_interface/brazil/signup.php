<?php
/**
 * The user search page
 *
 * @author Johnnatan Messias <johnme@mpi-sws.org>
 */

require_once 'include/init.php';
require_once 'main.php';

if (!isset($_SESSION['user_logged'])) {
  header("HTTP/1.1 303 See Other");
  header("Location: ./login.php?ecode=not_logged_in");
  exit();
}

if ($_SESSION['user']['superuser'] === false){
    header("Location: ./index.php");
    exit();
}

$input_error = get_default($_GET, "input_error", "");

$error_msgs = array(
  "" => null,
  "user_already_registered" => "O usuário já possui cadastro no sistema.",
  "error_registered_user" => "Erro ao cadastar o usuário.",
  "user_registered" => "Usuário cadastrado com sucesso.",
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
  <script src="js/md5/md5.min.js"></script>

  <form onsubmit="return validate_form(this)" method="POST" action="signup_user.php" style="border:1px solid #ccc">
  <div class="container">
    <h1 class="lang" key="signup"> </h1>
    <p class="lang" key="loginpage"></p>
    <hr>
    <div class="form-inline">
    <div class="form-group col-md-6">
    <label for="email"><b>E-mail</b></label>
    <input type="text" placeholder="Enter a valid e-mail" name="email" required>
    </div>
    <div class="form-group col-md-6">
    <label><b class="lang" key="afiliation"></b></label>
    <input type="text" placeholder="Work, University, etc" name="company" required>
    </div>
    </div>

    <div class="form-inline">
    <div class="form-group col-md-6">
    <label for="psw"><b class="lang" key="password"></b></label>
    <input type="password" placeholder="Type a password" name="psw" required>
    </div>
    <div class="form-group col-md-6">
    <label for="psw-repeat"><b class="lang" key="rewritepassword"></b></label>
    <input type="password" placeholder="Rewrite password" name="psw_repeat" required>
    </div>
    </div>

    <div class="form-inline">
    <div class="form-group col-md-6">
    <label><b class="lang" key="firstname"></b></label>
    <input type="text" placeholder="First Name" name="first-name" required>
    </div>
    <div class="form-group col-md-6">
    <label><b class="lang" key="lastname"></b></label>
    <input type="text" placeholder="Last Name" name="last-name" required>
    </div>
    </div>


    <label>
      <input type="checkbox" name="superuser" value="TRUE" style="margin-bottom:15px"> Admin User?
    </label>
    
    <div class="clearfix">
      <button type="submit" class="signupbtn">Subscribe</button>
    </div>
  </div>
</form>

<script>
  function validate_form(form) {
    if(form.psw.value == form.psw_repeat.value){
    var passwd_enc = md5(form.psw.value);
    form.psw.value = passwd_enc;
    
    return true;
    }
    modalMessage.show("Caro Visitante", "As senhas são diferentes.");
    return false; 
  }
</script>
</body>
</html>