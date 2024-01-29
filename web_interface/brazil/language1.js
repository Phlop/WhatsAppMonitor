    var language =  JSON.parse(ptbr_data)[0];
    var lang = localStorage.getItem('lang') || 'pt-br'; 
    
    
    function loadlang()
    {
            var lng = document.getElementById("langselector").value;
            var cnt = document.getElementById("contents");
            var mydata;
            switch (lng)
            {
            case "en":
              mydata = JSON.parse(en_data);
              localStorage.setItem('lang', lng);
            break;
            case "pt-br":
                var text = ptbr_data;
                mydata = JSON.parse(text);
                localStorage.setItem('lang', lng);
                
            break;
            }
            //var request = new XMLHttpRequest();
            //alert (mydata[0]["group"]);
             
            language = mydata[0];
            
            //alert(ptbr_data.toString('utf8'));
            //alert("Usuários");
            //alert("Decoded Encode" +  decode_utf8(encode_utf8(language["users"])) +"   " + decode_utf8(encode_utf8("Usuários")) );
            //alert("Decoded " +  decode_utf8(language["users"]) );
            //alert("Encode "  +  encode_utf8(language["users"]) +"   " + encode_utf8("Usuários"));
            //alert("Plain "   +  language["users"] );
            
            setDateLanguage();
            // Change language
            $(".lang").each(function(index, element) {
                var key =  $(this).attr("key");
                //alert (language[key]);
                $(this).text(language[key]);
              });
   }
   

    
   function setDateLanguage()
    {
        var value_date = getUrlParam('obtained_at','None'); 
        var end_date = getUrlParam('end_date','None'); 
        if (value_date == 'None')
            return;
        
        var lng = localStorage.getItem('lang') || 'pt-br';
        var b = document.getElementsByClassName("langdate")[0];
        var D = new Date(value_date)
	    var tkns = value_date.split("-");
        //var y = D.getFullYear();
        //var m = D.getUTCMonth();
        //var d = pad(D.getDate()+1,2);

        var y = parseInt(tkns[0]);
        var m = parseInt(tkns[1])-1;
        var d = pad(parseInt(tkns[2]),2);

        
        if(lng == 'en') {
            var monthNames = ["January", "February", "March", "April", "May", "June",
                            "July", "August", "September", "October", "November", "December"];
            var M = monthNames[m];
            var inputhtml = "" + M + " " + d + ", " + y;
             
            
            if ((value_date != end_date)  && (end_date != 'None') ){
                 var e_tkns = end_date.split("-"); 
                 var ey = parseInt(e_tkns[0]);
                 var em = parseInt(e_tkns[1])-1;
                 var ed = pad(parseInt(e_tkns[2]),2);
                 var eM = monthNames[em];
                 var end_date_text = " to " + eM +" " + ed + ", " + ey; 
                 inputhtml += end_date_text;
            }
            

            b.innerHTML = inputhtml;
            b.setAttribute("value", lng);
        }
        else if (lng == 'pt-br') {
        
            var monthNames = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"];
            var M = monthNames[m];
            var inputhtml = d+" de "+M+" de "+y;

            if ((value_date != end_date)  && (end_date != 'None') ){
                 var e_tkns = end_date.split("-"); 
                 var ey = parseInt(e_tkns[0]);
                 var em = parseInt(e_tkns[1])-1;
                 var ed = pad(parseInt(e_tkns[2]),2);
                 var eM = monthNames[m];
                 var end_date_text = " até " +ed+" de "+eM+" de "+ey; 
                 inputhtml += end_date_text;
            }
 
            b.innerHTML = inputhtml ;
            b.setAttribute("value", lng);
        }
        else{
             var inputhtml = "<?php setlocale(LC_ALL, 'en_US.UTF-8');\n echo strftime('%A, %B %d, %Y', strtotime($search_for));?>";
            b.innerHTML = inputhtml;
            b.setAttribute("value", lng);
            }
   
        }

    function encode_utf8(s) {
        return unescape(encodeURIComponent(s));
    }

    function decode_utf8(s) {
        return decodeURIComponent(escape(s));
    }

   function getUrlVars() {
        var vars = {};
        var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
            vars[key] = value;
        });
        return vars;
    }
    
    function formated_date_language(date){
    var formated_date = date;
    var lng = localStorage.getItem('lang') || 'pt-br';
	var tkns = date.split("-");
        var y = parseInt(tkns[0]);
        var m = parseInt(tkns[1])-1;
        var d = pad(parseInt(tkns[2]),2);

        
        if(lng == 'en') {
            var monthNames = ["January", "February", "March", "April", "May", "June",
                            "July", "August", "September", "October", "November", "December"];
            var M = monthNames[m];
            formated_date = ""+y+", " + M + " " + d;

        }
        else if (lng == 'pt-br') {
        
            var monthNames = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"];
            var M = monthNames[m];
            formated_date = d+" de "+M+" de "+y;

        }
    return formated_date
    }
    
   function getUrlParam(parameter, defaultvalue){
        var urlparameter = defaultvalue;
        if(window.location.href.indexOf(parameter) > -1){
            urlparameter = getUrlVars()[parameter];
            }
        return urlparameter;
    }
    
    function pad(num, size){
    var s = num+"";
    while (s.length < size) s = "0" + s;
    return s;
    }
