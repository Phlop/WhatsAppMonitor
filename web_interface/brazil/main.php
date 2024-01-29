    <?php
/**
 * The main functions
 *
 * @author Johnnatan Messias <johnme@mpi-sws.org>
 */

require_once 'vendor/camspiers/porter-stemmer/src/Porter.php';



function is_email_registered($db=null, $email){
    $sql = "SELECT EXISTS (SELECT 1 FROM whatsapp_user WHERE email = ?);";
    $reply = db_query($db, $sql, $email);
    $ret = $reply->fetch();
    return $ret['exists'];
}


function is_user_registered($db=null, $email, $passwd){
    $sql = "SELECT EXISTS (SELECT 1 FROM whatsapp_user WHERE email = ? AND passwd = ?);";
    $reply = db_query($db, $sql, $email, $passwd);
    $ret = $reply->fetch();
    return $ret['exists'];
}

function get_user_personal_data($db=null, $email){
    $sql = "SELECT id, email, first_name, last_name, company, superuser, registered_at FROM whatsapp_user WHERE email = ?;";
    $reply = db_query($db, $sql, $email);
    $ret = $reply->fetch();

    if ($ret === false){
        return null;
    }
    return $ret;
}

function insert_user($db=null, $email, $passwd, $first_name, $last_name, $company, $superuser){
    $sql = "INSERT INTO whatsapp_user(email, passwd, first_name, last_name, company, superuser, registered_at) values(?, ?, ?, ?, ?, ?, ?);";
    if(!is_user_registered($db, $email, $passwd)){
        db_query($db, $sql, $email, $passwd, $first_name, 
        $last_name, $company, $superuser, date("Y-m-d"));
        return true;
    }
    return false;
}

function get_user_personal_data_by_id($db=null, $id){
    $sql = "SELECT id, email, first_name, last_name, company, superuser, registered_at FROM whatsapp_user WHERE id = ?;";
    $reply = db_query($db, $sql, $id);
    $ret = $reply->fetch();

    if ($ret === false){
        return null;
    }
    return $ret;
}

function get_images_by_date($db = null, $obtained_at, $offset = 0){
    $sql = "SELECT imageID, rankingDay, shareNumber, shareNumberUsers, shareNumberGroups, obtained_at, nsfw_score FROM whatsapp_image WHERE obtained_at = TO_DATE('" . $obtained_at . "', 'YYYY-MM-DD') ORDER BY rankingday ASC, sharenumber DESC, sharenumberusers DESC, sharenumbergroups DESC LIMIT " . MAX_IMAGES . " OFFSET " . $offset . ";";
    $reply = db_query($db, $sql);

    $ret = $reply->fetchAll();

    if ($ret === false) {
        return null;
    }

    return $ret;
}

function get_links_by_date($db = null, $obtained_at){
    $sql = "SELECT link, rankingDay, shareNumber, shareNumberUsers, shareNumberGroups FROM whatsapp_link WHERE obtained_at = TO_DATE('" . $obtained_at . "', 'YYYY-MM-DD') ORDER BY rankingday ASC LIMIT " . MAX_IMAGES . ";";
    $reply = db_query($db, $sql);

    $ret = $reply->fetchAll();

    if ($ret === false) {
        return null;
    }

    return $ret;
}



function insert_tag($db=null, $email, $passwd, $first_name, $last_name, $company, $superuser){
    $sql = "INSERT INTO whatsapp_tag(email, imageid, tag_verdadeira, tag_suspeita_verdadeira, tag_suspeita_falsa, tag_falsa, tag_noticia, tag_satira, tag_campanha_politica, tag_disseminacao_odio, tag_conteudo_improprio, tag_violencia, tag_selfie, tag_promocao_produtos_ilicitos, tag_outros, registered_at) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);";
    
    if(!is_tag_registered($db, $email, $imageid)){
        db_query($db, $sql, $email, $imageid, $tag_verdadeira, $tag_suspeita_verdadeira,
        $tag_suspeita_falsa, $tag_falsa, $tag_noticia, $tag_satira, $tag_campanha_politica, 
        $tag_disseminacao_odio, $tag_conteudo_improprio, $tag_violencia, $tag_selfie, 
        $tag_promocao_produtos_ilicitos, $tag_outros, date("Y-m-d"));
        return true;
    }
    return false;
}


function is_tag_registered($db=null, $email, $imageid){
    $sql = "SELECT EXISTS (SELECT 1 FROM whatsapp_tag WHERE email = ? AND imageid = ?);";
    $reply = db_query($db, $sql, $email, $imageid);
    $ret = $reply->fetch();
    return $ret['exists'];
}

function get_last_update_date($db=null){
    $sql = "SELECT obtained_at FROM whatsapp_image ORDER BY obtained_at DESC LIMIT 1";
    $reply = db_query($db, $sql);
    $ret = $reply->fetch();

    if ($ret === false){
        return null;
    }
    return $ret;
}

// Don't close the PHP tag

