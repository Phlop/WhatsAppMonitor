var active_tab = "images";
var http = createRequestObject();   //call the function to create the XMLHttpRequest object

var step_images   = 100;
var step_videos   = 100;
var step_audios   = 50;
var step_messages = 100;
var step_links    = 50;
var step_stickers = 100;

var total_images   = step_images;
var total_videos   = step_videos;
var total_audios   = step_audios;
var total_messages = step_messages;
var total_links    = step_links;
var total_stickers = step_stickers;

var clicks_images = true;
var clicks_videos = true;
var clicks_audios = true;
var clicks_links  = true;
var clicks_messages = true;
var clicks_stickers = true;

function load_more_data(){
    elem_but = document.getElementById("load_more");
    var value = 0;
    clicks_images = false;
    clicks_videos = false;
    clicks_audios = false;
    clicks_links  = false;
    clicks_messages = false;
    clicks_stickers = false;
    switch (active_tab) {
            case 'images':
                clicks_images = true;
                total_images += step_images;
                value = total_images;
                break;
            case 'videos':  
                clicks_videos = true;
                total_videos += step_videos;
                value = total_videos;
                break;
            case 'messages':
                clicks_messages = true;
                total_messages += step_messages;
                value = total_messages;
                break;
            case 'links':
                clicks_links = true ;
                total_links += step_links;
                value = total_links;
                break;
            case 'audios':
                clicks_audios = true;
                total_audios += step_audios;
                value = total_audios;
                break;
            case 'stickers':
                clicks_stickers = true;
                total_stickers += step_stickers;
                value = total_stickers;
                break;
            default:
                value = total_images;
        }      
    elem_but.value = value;
    get_data_from_server(offset=value);
    
  }

  
function load_initial_data(){
    elem_but = document.getElementById("load_more");
    var value = 0;
    switch (active_tab) {
            case 'images':
                value = total_images;
                break;
            case 'videos':
                value = total_videos;
                break;
            case 'messages':
                value = total_messages;
                break;
            case 'links':
                value = total_links;
                break;
            case 'audios':
                value = total_audios;
                break;
            case 'stickers':
                value = total_stickers;
                break;
            default:
                value = total_images;
        }      
    elem_but.value = value;
    get_data_from_server(offset=value);
  }

 
function get_data_from_server(offset=total_images){
    waitingDialog.show(language['gettingdata']);
    var op = 1010;
    //var dt = "<?= $search_for; ?>";
    //var ed = "<?= $end_date; ?>";
    var td = get_today();  //from datepicker
    var dt =  getUrlParam('obtained_at', td);
    var ed =  getUrlParam('end_date', dt);
    dt = dt.split("#")[0];
    ed = ed.split("#")[0];
    var params = "op=" + op + "&date=" + dt + "&offset=" + offset + "&end_date=" +ed +"&type=" + active_tab;
    //alert(params);
    http.open("POST", "exec_process.php");
    http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    http.onreadystatechange = process_data_response;
    http.send(params);
}

  
function process_data_response(){
    if(http.readyState == 4){
        var response = http.responseText;
        data = JSON.parse(response).response;
        param = JSON.parse(response).param;
        //alert(param);
        //console.log(data);
        if(data.length == 0){
            document.getElementById("load_more").disabled = true;
        }
        else{ 
           
            $(document).ready(function(){
                $('[data-toggle="tooltip"]').tooltip(); 
            });
            
            if (data.images.length > 0  && clicks_images ){	
                 update_images(data.images);
            }
            if (data.audios.length > 0  && clicks_audios ){		
                update_audios(data.audios);
                Amplitude.init({
                    "songs": data.audios
                });
            }
            
            if (data.stickers.length >= 0  && clicks_stickers){
                update_stickers(data.stickers);
            }
            
            if (data.links.length >= 0 && clicks_links){
                update_links(data.links);
            }

            if (data.messages.length >= 0  && clicks_messages){
                update_messages(data.messages);
            }

            if (data.videos.length >= 0  && clicks_videos){
                update_videos(data.videos);
            }

        }
    }
    waitingDialog.hide();
}



function createRequestObject() {
    var tmpXmlHttpObject;
    //depending on what the browser supports, use the right way to create the XMLHttpRequest object
    if (window.XMLHttpRequest) {
        // Mozilla, Safari would use this method ...
        tmpXmlHttpObject = new XMLHttpRequest();
    } else if (window.ActiveXObject) {
        // IE would use this method ...
        tmpXmlHttpObject = new ActiveXObject("Microsoft.XMLHTTP");
    }
    return tmpXmlHttpObject;
}


 $('a[data-toggle="pill"]').bind('click', function (e) {
    //debugger;
    e.preventDefault();
    var tab = $(this).attr("href");
    var url = '';
    switch (tab) {
        case '#imagens':
            active_tab = 'images';
            break;
        case '#videos':
            active_tab = 'videos';
            break;
        case '#mensagens':
            active_tab = 'messages';
            break;
        case '#links':
            active_tab = 'links';
            break;
        case '#audios':
            active_tab = 'audios';
            break;
        case '#stickers':
            active_tab = 'stickers';
            break;
        default:
            active_tab = 'images';
    }
    //alert(active_tab);
});

 function error_message(msg, status){
  var items = document.getElementById('mention-messages');
  var li = document.createElement('li');
  //li.setAttribute('class', 'list-group-item');
  html = "<div class='alert alert-" + status + "' role='alert'>";
  html += "<span class='glyphicon glyphicon-exclamation-sign' aria-hidden='true'></span>";
  html += "<span class='sr-only'>Error:</span>";
  html += msg + "</div>";
  li.innerHTML = html;
  items.appendChild(li);
}

  

  /*
  function get_data_from_server(offset=0){
    waitingDialog.show(language['gettingdata']);
    var op = 1010;
    var dt = "<?= $search_for; ?>";
    var ed = "<?= $end_date; ?>";
    var params = "op=" + op + "&date=" + dt + "&offset=" + offset + "&end_date=" +ed;
    //alert(params);
    http.open("POST", "exec_process.php");
    http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    http.onreadystatechange = process_data_response;
    http.send(params);
  }
  
  
  
  function get_more_images(){
    elem_but = document.getElementById("load_more");
    value = parseInt(elem_but.value);
    load_more_data();
    elem_but.value = parseInt(<?=MAX_IMAGES?>) + value;

  }

 */
 

