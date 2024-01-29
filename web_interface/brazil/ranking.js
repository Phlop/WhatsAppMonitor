
function loadrank()
    {
    elem_but = document.getElementById("load_more");
    var value = 0;
    switch (active_tab) {
            case 'images':
                value = total_images;
                break;
            
            default:
                value = total_images;
        }      
    //elem_but.value = value;
    //get_data_from_server_ranking(offset=value);
  }
   

 
function get_data_from_server_ranking(offset=total_images){
    waitingDialog.show(language['gettingdata']);
    var op = 1010;
    //var dt = "<?= $search_for; ?>";
    //var ed = "<?= $end_date; ?>";
    var td = get_today();  //from datepicker
    var dt =  getUrlParam('obtained_at', td);
    var ed =  getUrlParam('end_date', dt);
    ed = ed.split("#")[0];
    var rankelement = document.getElementById("rankselector");
    var rankValue = rankelement.options[rankelement.selectedIndex].value;
    
    var params = "op=" + op + "&date=" + dt + "&offset=" + offset + "&end_date=" +ed +"&type=" + active_tab + "&rselector=" + rankValue;
    //alert(params);
    http.open("POST", "exec_process.php");
    http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    http.onreadystatechange = process_data_response_ranking;
    http.send(params);
}

  
function process_data_response_ranking(){
    if(http.readyState == 4){
        var response = http.responseText;
        data = JSON.parse(response).response;
        if(data.length == 0){
            document.getElementById("load_more").disabled = true;
        }
        else{ 
           
            $(document).ready(function(){
                $('[data-toggle="tooltip"]').tooltip(); 
            });
            
            if (data.images.length > 0  && clicks_images ){
                var elem = document.getElementById("session_tab_images");
                elem.innerHTML = '';
                rank_images(data.images);
            }
           
        }
    }
    waitingDialog.hide();
}




function rank_images(data){
                var html_images = '';
				var elem = document.getElementById("session_tab_images");
				elem_but = document.getElementById("load_more");
				var i = 0;
                //var start = total_images - step_images;
                var start = 0;
			    //value = parseInt(elem_but.value);
			    //i = value - parseInt(<?=MAX_IMAGES?>);
                var max_items = Math.min(data.length, total_images);
                //data.forEach(function(entry) {
				for (var i = start; i < max_items; ++i) {
                        var entry = data[i];
                        //i++; 
						var j =0;
						var index = i.toString();
						var modalId = "openModalImage"+index;
						var modalIdGrupo = "openModalImageGroup"+index;
						var modalIdForm = "openModalImageForm"+index;
						var TermId = "Termometer_"+index;
                        var t_height = (entry['fakeness'] - term_config.minTemp) / (term_config.maxTemp - term_config.minTemp) * 100 + "%";
                        var t_value = (entry['fakeness'] * 100).toFixed(2) + "%";
						var image_path = 'http://150.164.214.48/monitor-de-whatsapp/data/images/' + entry['imageid'];
						if(entry['nsfw_score'] >= 0.99999){
							image_path = 'http://www.monitor-de-whatsapp.dcc.ufmg.br/data/images/improprio.png'
						}
						var htmlGroups = 'Lista de nomes de grupos indisponível para essa imagem!'
						
						if( entry['shared_groups']){
							htmlGroups = '';
							for(j = 0; j < entry['shared_groups'].length; j++){
								htmlGroups += "<li>"+entry['shared_groups'][j]+"</li>";
							}
						}
						html_images += "<!– IMAGEM " +i+ "–>"+
						"<div class='gal-item_video' >"+
						"	  <!- Trigger the modal with a button -> "+
						"	  <a  href='#modalVideo' class='gal_box' >"+
						"			<div class='thumb'>" +
						"           <img src='" +	image_path + "'> </div>"+
						"			"+
						"	  </a>"+
						"	  <a class='item_hover'>"+
						"	  <button type='button' class='gal_btn blue' data-toggle='modal' data-target='#"+modalId+"'>"+ language["details"].toUpperCase() +"</button>"+
						"	  <button type='button' class='gal_btn blue' data-toggle='modal' data-target='#modal-form-" + modalIdForm + "'>"+ language["evaluate"].toUpperCase() +"</button>"+
						"	  </a>"+
						"	</div> "+
						"  <!- Modal ->"+
						"  <div class='modal fade' id='"+modalId+"' role='dialog'>"+
						"    <div class='modal-dialog'>"+
						"    "+
						"      <!- Modal content->"+
						"      <div class='modal-content'>"+
						"        <div class='modal-header'>"+
						"			<a href='#close' title='Close' class='grupos_close' class='grupos_close' data-dismiss='modal'>&times;</a>"+
						"          <h4 class='modal-title'>Top Whatsapp Image "+index+"</h4>"+
						"        </div>"+
						"        <div class='modal-body'>"+
						"			<div class='flex-container_modal'>"+
						"				<div class='box1'>"+
						"           		<img class ='expanded_image' src='" + image_path + "'>"+
						"				</div>"+
						"				<div class='box2'>"+
						"					<!-TABLE WHATSAPP->"+
						"					<div class='content_box'><table class='t1'>"+
						"						<colgroup>"+
						"							<col style='width: 50px'>"+
						"							<col style='width: 22px'>"+
						"						</colgroup>"+
						"						<tr>"+
						"							<th class='WP' colspan='2'>"+ language["sharetable"] +"</th>"+
						"						</tr>"+
						"						<tr>"+
						"							<td class='tab_title'>"+ language["total"] +":</td>"+
						"							<td class='tab_content'>"+entry['shareNumber']+"</td>"+
						"						</tr>"+
						"						<tr>"+
						"							<td class='tab_title'>"+ language["groups"] +":</td>"+
						"							<td class='tab_content'>"+entry['shareNumberGroups']+"</td>"+
						"						</tr>"+
						"						<tr>"+
						"							<td class='tab_title'>"+ language["users"]+":</td>"+
						"							<td class='tab_content'>"+entry['shareNumberUsers']+"</td>"+
						"						</tr>"+
						"					</table>"+
						"						"+
						"						<div class='gal_btn blue large'> <a class='buttonStyle' href='#"+modalIdGrupo+"'>"+ language["groups"].toUpperCase() +"</a> </div>"+
						"						<div class='gal_btn blue large' value='" + image_path + "' onclick='redirect_image(" + '"' + image_path + '"' + ")'><a class='buttonStyle'>"+ language["othersources"].toUpperCase() +"</a></div>"+
						"				        <div class='gal_btn blue large' data-toggle='modal' data-target='#modal-form-" + modalIdForm + "'><a class='buttonStyle'>"+ language["evaluate"].toUpperCase() +"</a></div>"+
						"				</div>" + build_fakeness_term(TermId, entry['imageid'], entry['fakeness'], t_height, t_value)+
                        "           </div>"+
						"			"+
						"			</div>"+
						"       </div>"+
						"        <div class='modal-footer'>"+
						"         <button type='button' class='gal_btn blue' data-dismiss='modal'>"+ language["close"].toUpperCase() +"</button>"+
						"        </div>"+
						"      </div>"+
						"</div>"+
						"		<!-MODAL DOS GRUPOS->"+
						"		<div id='"+modalIdGrupo+"' class='grupos_modalDialog'>"+
						"		<div>"+
						"			<a href='#close' title='Close' class='grupos_close'>&times;</a>"+
						"			"+
						"			<div class='grupos_modal_header'>"+
						"			 <h2>"+ language["groupsmodal"] +"</h2>"+
						"			</div>"+
						"			<p>"+ language["groupslist"] +"</p>"+
						"			<div class='list'>"+
						"				<ul>"+
						"					"+htmlGroups+
						"				</ul>"+
						"			</div>	"+					
						"		</div>"+
						"	</div>"+
					    "</div>" + build_modal_form(modalIdForm, entry['imageid'], 'image')
						}
					elem.innerHTML = html_images;
					
}
