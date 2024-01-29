var month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun","Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

function parse_tweet(text) {
        // http://, https://, ftp://
        var urlPattern = /\b(?:https?|ftp):\/\/[a-z0-9-+&@#\/%?=~_|!:,.;]*[a-z0-9-+&@#\/%=~_|]/gim;

        // www. sans http:// or https://
        var pseudoUrlPattern = /(^|[^\/])(www\.[\S]+(\b|$))/gim;

        // Email addresses
        var emailAddressPattern = /[\w.]+@[a-zA-Z_-]+?(?:\.[a-zA-Z]{2,6})+/gim;

        text = text
            .replace(urlPattern, "<a class='text-danger' href='$&' target='_blank'>$&</a>");
           // .replace(pseudoUrlPattern, '$1<a href="http://$2">$2</a>')
           // .replace(emailAddressPattern, '<a href="mailto:$&">$&</a>');
    /*
    text = text.replace(/[@]+[A-Za-z0-9-_]+/g, function(u) {
        var username = u.replace("@","")
        return ('<a class="text-danger" href=content_footprint.php?screen_name='+username+'>@'+username+'</a>');
    });
    */
    text = text.replace(/[#]+[A-Za-z0-9-_]+/g, function(t) {
        var tag = t.replace("#","")
        return ('<a class="text-danger" href="https://twitter.com/hashtag/'+tag+'?src=hash" target="_blank">#'+tag+'</a>');
    });
    return text;
}

function to_local_time(dateString,searched){
   var date = new Date(dateString);
   return date;
}

$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip(); 
  });

/*
$("button").click(function() {
    var $btn = $(this);
    $btn.button('loading');
    // simulating a timeout
    setTimeout(function () {
        $btn.button('reset');
    }, 2000);
});
*/