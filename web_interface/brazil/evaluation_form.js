    function get_html_button(modalIdForm, imageid, item_name, item_description, item_value, n){
        html_item = '<div class="col-md-6 col-sm-6 col-xs-12 [ form-group ]">';
        html_item += '<input type="checkbox" name="tags" value="'+ item_value +'"  id="fancy-checkbox-' + imageid + '_' + modalIdForm + '_'+ n +'" autocomplete="off" />'
        html_item += '<div class="[ btn-group ]">'
        html_item += '<label for="fancy-checkbox-' + imageid + '_' + modalIdForm + '_'+ n +'" class="[ btn btn-info ]">'
        html_item += '<span class="[ glyphicon glyphicon-ok ]"></span>'
        html_item += '<span> </span>'
        html_item += '</label>'
        html_item += '<label for="fancy-checkbox-' + imageid + '_' + modalIdForm + '_'+ n +'" class="[ btn btn-default ]" data-toggle="tooltip" title="'+item_description+'"> '+ item_name +'</label>'
        html_item += '</div>'
        html_item += '</div>'
        
        return html_item
    
    }



  function build_modal_form(modalIdForm, imageid, data_type){
	
    html_nsfw        = get_html_button(modalIdForm, imageid, language["form_item_name_nsfw"],       language["form_item_description_nsfw"], 'conteudo_improprio', 1);
    html_political   = get_html_button(modalIdForm, imageid, language["form_item_name_political"],  language["form_item_description_political"], 'conteudo_politico', 2);
    html_hate        = get_html_button(modalIdForm, imageid, language["form_item_name_hate"],       language["form_item_description_hate"], 'disseminacao_de_odio', 3);
    html_fake        = get_html_button(modalIdForm, imageid, language["form_item_name_fake"],       language["form_item_description_fake"], 'falsa', 4);
    html_investigate = get_html_button(modalIdForm, imageid, language["form_item_name_investigate"],language["form_item_description_investigate"], 'merece_investigacao', 5);
    html_news        = get_html_button(modalIdForm, imageid, language["form_item_name_news"],       language["form_item_description_news"], 'noticia', 6);
    html_illegal     = get_html_button(modalIdForm, imageid, language["form_item_name_illegal"],    language["form_item_description_illegal"], 'promocao_de_produtos_ilicitos', 18);
    html_ads         = get_html_button(modalIdForm, imageid, language["form_item_name_ads"],        language["form_item_description_ads"], 'propaganda', 7);
    html_humour      = get_html_button(modalIdForm, imageid, language["form_item_name_satire"],     language["form_item_description_satire"], 'satira', 8);
    html_selfie      = get_html_button(modalIdForm, imageid, language["form_item_name_selfie"],     language["form_item_description_selfie"], 'selfie', 9);
    html_sfake       = get_html_button(modalIdForm, imageid, language["form_item_name_sfake"],      language["form_item_description_sfake"], 'suspeita_a_ser_falsa', 10);
    html_strue       = get_html_button(modalIdForm, imageid, language["form_item_name_strue"],      language["form_item_description_strue"], 'suspeita_a_ser_verdadeira', 11);
    html_true        = get_html_button(modalIdForm, imageid, language["form_item_name_true"],       language["form_item_description_true"], 'verdadeira', 12);
    html_violence    = get_html_button(modalIdForm, imageid, language["form_item_name_violence"],   language["form_item_description_violence"], 'violencia', 13);
    html_activism    = get_html_button(modalIdForm, imageid, language["form_item_name_activism"],   language["form_item_description_activism"], 'ativismo', 14);
    html_opinion     = get_html_button(modalIdForm, imageid, language["form_item_name_opinion"],    language["form_item_description_opinion"], 'opinion', 15);
    html_photo       = get_html_button(modalIdForm, imageid, language["form_item_name_photo"],      language["form_item_description_photo"], 'foto', 16);
    html_other       = get_html_button(modalIdForm, imageid, language["form_item_name_other"],      language["form_item_description_other"], 'diversos', 17);
  
    html_modal_form = '<div class="modal fade" id="modal-form-' + modalIdForm +'" role="dialog">'
    html_modal_form += '<div class="modal-dialog">'
    html_modal_form += '<div class="modal-content">'
    html_modal_form += '<div class="modal-header">'
    html_modal_form += '<button type="button" class="close" data-dismiss="modal">&times;</button>'
    html_modal_form += '<h4 class="modal-title">'+language["evaluation"]+'</h4>'
    html_modal_form += '</div>'
    html_modal_form += '<div class="modal-body">'
    html_modal_form += '<p>'+language["evaluation_description"]+'</p>'
    html_modal_form += '<div class="row">'
    html_modal_form += '<form name="form-' + imageid + '">'

    html_modal_form += html_political
    html_modal_form += html_news
    html_modal_form += html_ads
    html_modal_form += html_humour
    html_modal_form += html_activism
	html_modal_form += html_opinion
    html_modal_form += html_nsfw
    html_modal_form += html_hate
    html_modal_form += html_fake
    html_modal_form += html_true
    html_modal_form += html_sfake
    html_modal_form += html_strue
    html_modal_form += html_investigate
    //html_modal_form += html_violence
    //html_modal_form += html_illegal
    //html_modal_form += html_selfie
    //html_modal_form += html_photo
	html_modal_form += html_other
			
    html_modal_form += '<div class="col-md-12 col-sm-12 col-xs-12 [ form-group ]">'
    html_modal_form += '<label class="col-md-12 col-sm-12 col-xs-12 " data-toggle="tooltip" title="'+language["form_item_description_comment"]+'">'
    html_modal_form += language["form_item_name_comment"] + ': <textarea row="5" name="outros" class="form-control"></textarea>'
    html_modal_form += '</label>'
    html_modal_form += '</div>'
    html_modal_form += '</div>'
    html_modal_form += '</div>'

    html_modal_form += '<div class="modal-footer">'
    html_modal_form += '<button type="button" class="btn btn-default" data-dismiss="modal">'+language["close"]+'</button>'
    html_modal_form += '<button type="button" class="btn btn-primary" value="' + imageid + '" onclick="send_form(this.value, \'' + data_type + '\')" data-dismiss="modal">'+language["send"]+'</button>'
    html_modal_form += '</div>'
    html_modal_form += '</div>'
    html_modal_form += '</form>'

    html_modal_form += '</div>'
    html_modal_form += '</div>'
    
    return html_modal_form
  }
  
  
  
  
function send_form(id, data_type) {
    var tags_dict = {};
    form_name = "form-" + id;
    form = document.forms[form_name];
    comments = form.outros.value;
    tags = form.tags;
    type = data_type.replace("'", "_");
    tags.forEach(function(tag) {
        tags_dict[tag.value] = tag.checked ? 'TRUE' : 'FALSE';
    });

    var op = 102312;
    var email = "<?= $_SESSION['user']['email'] ?>";
    var params = "op=" + op + "&email=" + email + "&imageid=" + id + "&comments=" + comments + "&tags=" + JSON.stringify(tags_dict) + "&type=" + type;
    http.open("POST", "exec_process.php");
    http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    http.onreadystatechange = process_form_response;
    http.send(params);
}


function process_form_response() {
    if (http.readyState == 4) {
        var response = http.responseText;
        data = JSON.parse(response);

        //document.getElementById("load_more").disabled = true;
    }

}