
  
function create_modal_groups(modalIdGrupo, entry){
  
    var htmlGroups = 'List of groups names!'
    
    if( entry['shared_groups']){
        htmlGroups = '';
        for(j = 0; j < entry['shared_groups'].length; j++){
            htmlGroups += "<li>"+entry['shared_groups'][j]+"</li>";
        }
    }

    modal_html_groups = "		<!-MODAL GROUPS->"+
    "<div id='"+modalIdGrupo+"' class='grupos_modalDialog'>"+
    "	    <div>"+
    "			<a href='#close' title='Close' class='grupos_close'>&times;</a>"+
    "			"+
    "			<div class='grupos_modal_header'>"+
    "		        <h2>"+language['groupsmodal']+"</h2>"+
    "			</div>"+
    "			"+language['groupslist']+
    "			<div class='list'>"+
    "				<ul>"+
    "					"+htmlGroups+
    "				</ul>"+
    "			</div>	"+					
    "		</div>"+
    "</div>";
                        
    return  modal_html_groups;
                        
}
  
  
  
  
function create_modal_context(modalIdContext, entry){
  
    //console.log(entry);
    var htmlPrevious = "<i>"+ language['no_prev_message'] + "</i>";
    var htmlNext     = "<i>"+ language['no_next_message'] + "</i>";
    var htmlNow      = "<i>"+ language['no_next_message'] + "</i>";
    
    if( entry['context_pre'].length > 0){
        htmlPrevious = '';
        for(j = 0; j < entry['context_pre'].length; j++){
            htmlPrevious += "<li>"+entry['context_pre'][j]+"</li>";
        }
    }
   
    if( entry['context_pos'].length > 0){
        htmlNext = '';
        for(j = 0; j < entry['context_pos'].length; j++){
            htmlNext += "<li>"+entry['context_pos'][j]+"</li>";
        }
    }
    if( entry['context_now'].length > 0){
        htmlNow = '';
        for(j = 0; j < entry['context_now'].length; j++){
            htmlNow += "<li>"+entry['context_now'][j]+"</li>";
        }
    }

    modal_html_context = "		<!-CONTEXT MODAL->"+
    "<div id='"+modalIdContext+"' class='context_modalDialog'>"+
    "	    <div>"+
    "			<a href='#close' title='Close' class='context_close'>&times;</a>"+
    "			"+
    "			<div class='context_modal_header'>"+
    "		        <h2>"+language['contextmessage']+"</h2>"+
    "			</div>"+
    "           <h4>" + language['context_explain'] + "</h4>" +
    "			<h4><b>"+language['prevmessage'].toUpperCase()+"</b></h4>"+
    "			<div class='list'>"+
    "				<ul>"+
    "					"+htmlPrevious+
    "				</ul>"+
    "			</div>	"+
    "           <h4><b>"+"Mensagens enviadas junto ao conteudo".toUpperCase() +"</b></h4>"+
    "			<div class='list'>"+
    "				<ul>"+
    "					"+htmlNow+
    "				</ul>"+
    "			</div>	"+
    "			<h4><b>"+language['nextmessage'].toUpperCase()+"</b></h4>"+
    "			<div class='list'>"+
    "				<ul>"+
    "					"+htmlNext+
    "				</ul>"+
    "			</div>	"+					
    "		</div>"+
    "</div>";
                            
    return  modal_html_context
                        
}




  
  
  
function create_modal_context_pre(modalIdContext, entry){
  
    //console.log(entry);
    var htmlPrevious = "<i>"+ language['no_prev_message'] + "</i>";
    
    if( entry['context_pre'].length > 0){
        htmlPrevious = '';
        for(j = 0; j < entry['context_pre'].length; j++){
            htmlPrevious += "<li>"+entry['context_pre'][j]+"</li>";
        }
    }
   
    modal_html_context = "		<!-CONTEXT MODAL->"+
    "<div id='"+modalIdContext+"' class='context_modalDialog'>"+
    "	    <div>"+
    "			<a href='#close' title='Close' class='context_close'>&times;</a>"+
    "			"+
    "			<div class='context_modal_header'>"+
    "		        <h2>"+language['contextmessage']+"</h2>"+
    "			</div>"+
    "           <h4>" + language['context_explain_pre'] + "</h4>" +
    "			<h4><b>"+language['context_pre_message'].toUpperCase()+"</b></h4>"+
    "			<div class='list'>"+
    "				<ul>"+
    "					"+htmlPrevious+
    "				</ul>"+
    "			</div>	"+			
    "		</div>"+
    "</div>";       
    return  modal_html_context                       
}

  
  
  
function create_modal_context_now(modalIdContext, entry){
  
    //console.log(entry);
    var htmlNow      = "<i>"+ language['no_now_message'] + "</i>";
    
    if( entry['context_now'].length > 0){
        htmlNow = '';
        for(j = 0; j < entry['context_now'].length; j++){
            htmlNow += "<li>"+entry['context_now'][j]+"</li>";
        }
    }
   
    modal_html_context = "		<!-CONTEXT MODAL->"+
    "<div id='"+modalIdContext+"' class='context_modalDialog'>"+
    "	    <div>"+
    "			<a href='#close' title='Close' class='context_close'>&times;</a>"+
    "			"+
    "			<div class='context_modal_header'>"+
    "		        <h2>"+language['contextmessage']+"</h2>"+
    "			</div>"+
    "           <h4>" + language['context_explain_now'] + "</h4>" +
    "			<h4><b>"+language['context_now_message'].toUpperCase()+"</b></h4>"+
    "			<div class='list'>"+
    "				<ul>"+
    "					"+htmlNow+
    "				</ul>"+
    "			</div>	"+			
    "		</div>"+
    "</div>";       
    return  modal_html_context                       
}



  
function create_modal_context_pos(modalIdContext, entry){
  
    //console.log(entry);
    var htmlNext     = "<i>"+ language['no_next_message'] + "</i>";
   
    if( entry['context_pos'].length > 0){
        htmlNext = '';
        for(j = 0; j < entry['context_pos'].length; j++){
            htmlNext += "<li>"+entry['context_pos'][j]+"</li>";
        }
    }
   
    modal_html_context = "		<!-CONTEXT MODAL->"+
    "<div id='"+modalIdContext+"' class='context_modalDialog'>"+
    "	    <div>"+
    "			<a href='#close' title='Close' class='context_close'>&times;</a>"+
    "			"+
    "			<div class='context_modal_header'>"+
    "		        <h2>"+language['contextmessage']+"</h2>"+
    "			</div>"+
    "           <h4>" + language['context_explain_pos'] + "</h4>" +
    "			<h4><b>"+language['context_pos_message'].toUpperCase()+"</b></h4>"+
    "			<div class='list'>"+
    "				<ul>"+
    "					"+htmlNext+
    "				</ul>"+
    "			</div>	"+					
    "		</div>"+
    "</div>";
                            
    return  modal_html_context
                        
}
