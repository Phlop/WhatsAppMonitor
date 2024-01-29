var clickHandler = function(elem){
		/* Toggle between adding and removing the "active" class,
		to highlight the button that controls the panel */
		//alert("Button clicked, id "+elem.id+", text"+elem.innerHTML + " Tag: "+ elem.tagName);
		elem.classList.toggle("active");
		/* Toggle between hiding and showing the active panel */
		var panel = elem.previousElementSibling;
		if (panel.className === "collapsed") {
		  panel.className = "open";
		  elem.innerHTML = "<a class=\'link_btn blue\'>MOSTRAR MENOS</a> ";

		} else {
		  panel.className = "collapsed";
		  elem.innerHTML = "<a class=\'link_btn blue\'>MAIS DETALHES</a> ";

		}
	  
};

var element = document.getElementById('expand_button');
element.onclick = clickHandler();
