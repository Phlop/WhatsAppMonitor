<?php

require_once("include/init.php");
require_once("main.php");

if (!isset($_SESSION['user_logged'])) {
  header("HTTP/1.1 303 See Other");
  header("Location: ./login.php?ecode=not_logged_in");
  exit();
}

$email = trim(get_default($_POST, 'email', ''));
$imageid = trim(get_default($_POST, 'imageid', ''));
$tag_verdadeira = trim(get_default($_POST, 'tag_verdadeira', 'FALSE'));
$tag_suspeita_verdadeira = trim(get_default($_POST, 'tag_suspeita_verdadeira', 'FALSE'));
$tag_suspeita_falsa = trim(get_default($_POST, 'tag_suspeita_falsa', 'FALSE'));
$tag_falsa = trim(get_default($_POST, 'tag_falsa', 'FALSE'));
$tag_noticia = trim(get_default($_POST, 'tag_noticia', 'FALSE'));
$tag_satira = trim(get_default($_POST, 'tag_satira', 'FALSE'));
$tag_campanha_politica = trim(get_default($_POST, 'tag_campanha_politica', 'FALSE'));
$tag_disseminacao_odio = trim(get_default($_POST, 'tag_disseminacao_odio', 'FALSE'));
$tag_conteudo_improprio = trim(get_default($_POST, 'tag_conteudo_improprio', 'FALSE'));
$tag_violencia = trim(get_default($_POST, 'tag_violencia', 'FALSE'));
$tag_selfie = trim(get_default($_POST, 'tag_selfie', 'FALSE'));
$tag_promocao_produtos_ilicitos = trim(get_default($_POST, 'tag_promocao_produtos_ilicitos', 'FALSE'));
$tag_outros = trim(get_default($_POST, 'tag_outros', ''));


if ($email === ''){
  header("Location: ./index.php");
  exit();
}

try{
        $db = db_connect(DSN_MAIN);
}catch (Exception $e){
    header("HTTP/1.1 303 See Other");
    header("Location: ./login.php");
}

if(!is_tag_registered($db, $email, $imageid) === true){
  if(!insert_tag($db, $email, $imageid, $tag_verdadeira, $tag_suspeita_verdadeira,
  $tag_suspeita_falsa, $tag_falsa, $tag_noticia, $tag_satira, $tag_campanha_politica, $tag_disseminacao_odio, 
  $tag_conteudo_improprio, $tag_violencia, $tag_selfie, $tag_promocao_produtos_ilicitos, $tag_outros)){
    header("Location: ./signup.php?ecode=error_registered_user");
  }
  header("Location: ./signup.php?ecode=user_registered");
  exit();
}else{
    header("HTTP/1.1 303 See Other");
    header("Location: ./signup.php?ecode=user_already_registered");
    exit();
}

?>
