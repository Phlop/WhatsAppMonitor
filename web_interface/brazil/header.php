    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
    <!-- Meta, title, CSS, favicons, etc. -->
    <meta charset="utf-8">
    <meta charset="UTF-8">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <link rel="shortcut icon" href="http://www.monitor-de-whatsapp.dcc.ufmg.br/brazil/img/favicon-32-32.png" type="image/x-icon"/>

    <title>Monitor de WhatsApp</title>
    
    <!-- Bootstrap core CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">
    <link href='https://fonts.googleapis.com/css?family=Roboto+Slab:400,100,300,700' rel='stylesheet' type='text/css'>
    <link href="http://blackbird.dcc.ufmg.br/projectx/assets/css/style.css?r=1159579074" rel="stylesheet">
    <link href="fonts/css/font-awesome.min.css" rel="stylesheet">
    <link href="css/animate.min.css" rel="stylesheet">
    <link rel="stylesheet" href="css/easy-autocomplete.min.css">
    <link href="css/dp/dp.min.css" rel="stylesheet">
    <link href="css/dp/search.css" rel="stylesheet">

    <!-- Custom styling plus plugins -->
    <!--<link href="css/custom.css" rel="stylesheet">-->

    <link rel="stylesheet" type="text/css" href="css/maps/jquery-jvectormap-2.0.3.css" />
    <link href="css/icheck/flat/green.css" rel="stylesheet" />
    <link href="css/floatexamples.css" rel="stylesheet" type="text/css" />

    <script src="js/jquery.min.js"></script>
    <script src="js/dp/dp.min.js" type="text/javascript" ></script>
    <script src="js/autocomplete/jquery.easy-autocomplete.min.js" type="text/javascript" ></script>
    <script src="js/nprogress.js"></script>
    <script src="js/bootstrap.min.js"></script>

    <script src="js/jquery.min.js"></script>
    <script src="js/jquery-ui.js"></script>
    <script src="js/autocomplete/jquery.easy-autocomplete.min.js" type="text/javascript" ></script>
    <script src="js/bootstrap.min.js"></script>
    <script src="js/dp/dp.min.js"></script>
    <script src="js/locales/bootstrap-datepicker.pt-BR.min.js"></script>
    <link rel="stylesheet" type="text/css" href="css/styles.css"/>
    <link href="https://afeld.github.io/emoji-css/emoji.css" rel="stylesheet">

    <script type="text/javascript" src="js/foundation.min.js"></script>
    <script type="text/javascript" src="js/amplitude.js"></script>
    <script type="text/javascript" src="js/functions.js"></script>

    
    <script type="text/javascript" src="language/ptbr.json"  charset="utf-8"></script>
    <script type="text/javascript" src="language/en.json"  charset="utf-8"></script>
    <script type="text/javascript" src="language1.js"  charset="utf-8"></script>

    </head>
    <body>
    
    <header class="header">
                    <div class="container">
                            <div class="preheader">
                                    <div class="row">
                                            <div class="col-sm-8">
                                                    <div class="lang-section dropdown">
                                                            <div aria-expanded="false">
                                                                <span class="fa fa-globe"></span> <em>Language:</em> <em class="fa fa-angle-down"></em>
                                                                <select id="langselector" name ="lselector" onchange="loadlang()">
                                                                  <option   value="en"   >🇺🇸 English    </option>
                                                                  <option   value="pt-br">🇧🇷 Portuguese </option>
                                                                </select>
                                                            </div> 
                                                    </div>
                                                    <div class="phone-section">
                                                            <a href="#" title=""><span class="fa fa-envelope"></span> <em>eleicoes-sem-fake@dcc.ufmg.br</em></a>
                                                    </div>
                                                    <div class="phone-section">
                                                            <a href="http://www.eleicoessemfake.dcc.ufmg.br" title=""><span class="fa fa-link"></span> <em>www.eleicoessemfake.dcc.ufmg.br</em></a>
                                                    </div>
                                            </div>
                                            <div class="col-sm-4">
                                                    <div class="social-section">
                                                            <a href="#" title="" class="fa fa-facebook"></a>
                                                            <a target="_blank" href="https://twitter.com/eleicoessemfake" title="Twitter Eleições Sem Fake" class="fa fa-twitter"></a>
                                                    </div>
                                            </div>
                                    </div>
                            </div>
                    </div>
            </header>
    <div class="main-header">
                    <div class="container">
                            <nav class="navbar">
                                    <!-- Brand and toggle get grouped for better mobile display -->
                                    <div class="navbar-header">
                                            <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">
                                                    <span class="sr-only">Toggle navigation</span>
                                                    <span class="icon-bar"></span>
                                                    <span class="icon-bar"></span>
                                                    <span class="icon-bar"></span>
                                            </button>
                                            <a class="navbar-logo" href="http://www.eleicoessemfake.dcc.ufmg.br" title=""><img src="http://blackbird.dcc.ufmg.br/projectx/assets/images/logo.jpg" alt="Eleições Sem Fake"></a>
                                    </div>

                                    <!-- Collect the nav links, forms, and other content for toggling -->
                                    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                                    <ul class="nav navbar-nav navbar-right">
		                           <!--                
					    <li><a href="https://chrome.google.com/webstore/detail/monitor-de-propagandas-do/mnbffelpanbfkmkifcbafgopfbmocdao" title="">&raquo; Facebook Ads Monitor</a></li>
                                            <li><a href="http://www.audiencia-dos-politicos.dcc.ufmg.br/" target="_blank" title="">&raquo; Audiência dos Políticos</a></li>
                                            <li><a href="http://www.noticias-lado-a-lado.dcc.ufmg.br/" target="_blank"  title="">&raquo; Notícias Lado a Lado</a></li>
                                            <li><a href="http://www.bot-ou-humano.dcc.ufmg.br/" target="_blank" title="">&raquo; Bot ou Humano?</a></li>
					   -->
                                        </li>
                                    </ul>
                                    </div><!-- /.navbar-collapse --><!-- /.container-fluid -->
                            </nav>
                    </div>
            </div>
    <div class="modal fade" id="mention-modal" data-focus-on="input:first" data-backdrop="static" data-keyboard="false" tabindex="-1" role="dialog" aria-hidden="true" style="overflow-y:visible;">
        <div class="modal-dialog modal-m">
        <div class="modal-content">
            <div class="modal-header">
            <h3 style="margin:0;" id="mention_modal_title"></h3>
            <h4></h4>
            <button type="button" class="close" onClick="mention_modal.hide()">×</button>
            </div>
            <div class="modal-body">
            <!--<h4 style="margin:0;"></h4> -->
            <ul class="messages" id="mention-messages"> </ul>
            <div class="more text-center">
                <button type="button" class="btn btn-primary btn-md" data-loading-text="Carregando..." id="getMoreMentionsButton" value="<?=MAX_IMAGES;?>" onClick="add_more_mentions()">Mais!</button>
                </a> </div>
            </div>
            <div class="modal-footer">
            <button type="button" class="btn btn-default" onClick="mention_modal.hide()">Fechar</button>
            </div>
        </div>
        </div>
    </div>

        <!-- Modal -->
    <div class="modal fade" id="canvas-modal" data-backdrop="static" data-focus-on="input:first" data-keyboard="false" tabindex="1" role="dialog" aria-hidden="true" style="overflow-y:visible;">
        <div class="modal-dialog modal-m">
        <div class="modal-content">
            <div class="modal-header">
            <h3 style="margin:0;"></h3>
            <button type="button" class="close" data-dismiss="modal">×</button>
            </div>
            <div class="modal-body">
            <div id="main-canvas" id="canvas-container" role="main" style="width: 100%;">
                <canvas id="canvas"  width="500" height="250" style="width: 100%; height:270px;"></canvas>
            </div>
            </div>
            <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Fechar</button>
            </div>
        </div>
        </div>
    </div>
    <!-- Modal -->


    <script type="text/javascript">

        // Language initialization code
        $(document).ready(function() {
            // The default language is English
            var lang = "en";
            $(".lang").each(function(index, element) {
                var key =  $(this).attr("key");
                //alert (language[key]);
                $(this).text(language[key]);
            });
        });
    
    var modalIsOpen = false

    var mention_modal = mention_modal || (function ($) {
        'use strict';
        // Creating modal dialog's DOM
        var $modal = $("#mention-modal");

        return {
            show: function (title, hashtag, options) {
                // Assigning defaults
                if (typeof options === 'undefined') {
                    options = {};
                }
                if (typeof title === 'undefined') {
                    title = 'Loading';
                }
                if (typeof hashtag === 'undefined') {
                    hashtag = '';
                }

                var settings = $.extend({
                    dialogSize: 'm',
                    progressType: '',
                    onHide: null // This callback runs after the dialog was hidden
                }, options);

                // Configuring dialog
                $modal.find('.modal-mention').attr('class', 'modal-mention').addClass('modal-' + settings.dialogSize);

                $("#mention_modal_title").text(title);
                $modal.find('h4').text(hashtag);
                // Adding callbacks
                if (typeof settings.onHide === 'function') {
                    $modal.off('hidden.bs.modal').on('hidden.bs.modal', function (e) {
                        settings.onHide.call($modal);
                    });
                }
                // Opening dialog
                $modal.modal();
                modalIsOpen = true;
                document.getElementById("getMoreMentionsButton").value = 20;
                console.log(modalIsOpen);
            },
            /**
            * Closes dialog
            */
            hide: function () {
                $modal.modal('hide');
                modalIsOpen = false;
                console.log(modalIsOpen);
            },
            modal: function(){
            $modal.modal('handleUpdate');
            }
        };

    })(jQuery);


    var modalMessage = modalMessage || (function ($) {
        'use strict';

        // Creating modal dialog's DOM
        var $dialog = $(
        "<div class='modal fade' id='msg-modal' data-backdrop='static' data-keyboard='false' role='dialog' aria-hidden='true'>" +
        "<div class='modal-dialog modal-m'>" +
        "<div class='modal-content' style='border: 5px solid #73879C;margin:40px'>" +
            "<div class='modal-header'>" +
            "<h3 style='margin:0;text-align:center;'></h3>" +
            "<button type='button' class='close' data-dismiss='modal'>×</button>" +
            "</div>" +
            "<div class='modal-body'>" +
            "<div class='modal-text' style='margin:1px; font-size: 120%;'></div>" +
            "</div>" +
            "<div class='modal-footer'>" +
            "<button type='button' class='btn btn-default' data-dismiss='modal'>Close</button>" +
            "</div>" +
        "</div>" +
        "</div>" +
    "</div>");

        return {
            /**
            * Opens our dialog
            * @param message Custom message
            * @param options Custom options:
            *                options.dialogSize - bootstrap postfix for dialog size, e.g. "sm", "m";
            *                options.progressType - bootstrap postfix for progress bar type, e.g. "success", "warning".
            */
            show: function (title, message, options) {
                // Assigning defaults
                if (typeof options === 'undefined') {
                    options = {};
                }
                if (typeof title === 'undefined') {
                    title = 'Loading';
                }
                if(typeof message === 'undefined'){
                message = '';
                }
                var settings = $.extend({
                    dialogSize: 'lg',
                    progressType: '',
                    onHide: null // This callback runs after the dialog was hidden
                }, options);

                // Configuring dialog
                $dialog.find('.modal-dialog').attr('class', 'modal-dialog').addClass('modal-' + settings.dialogSize);
                $dialog.find('h3').html(title);
            $dialog.find('.modal-text').html(message);
                // Adding callbacks
                if (typeof settings.onHide === 'function') {
                    $dialog.off('hidden.bs.modal').on('hidden.bs.modal', function (e) {
                        settings.onHide.call($dialog);
                    });
                }
                // Opening dialog
                $dialog.modal();
            },
            /**
            * Closes dialog
            */
            hide: function () {
                $dialog.modal('hide');
            }
        };

    })(jQuery);



    var waitingDialog = waitingDialog || (function ($) {
        'use strict';

        // Creating modal dialog's DOM
        var $dialog = $(
            '<div class="modal fade" data-backdrop="static" data-keyboard="false" tabindex="-1" role="dialog" aria-hidden="true" style="padding-top:15%; overflow-y:visible;">' +
            '<div class="modal-dialog modal-m">' +
            '<div class="modal-content">' +
                '<div class="modal-header"><h3 style="margin:0;"></h3></div>' +
                '<div class="modal-body">' +
                    '<div class="progress progress-striped active" style="margin-bottom:0;"><div class="progress-bar" style="width: 100%"></div></div>' +
                '</div>' +
            '</div></div></div>');

        return {
            /**
            * Opens our dialog
            * @param message Custom message
            * @param options Custom options:
            *                options.dialogSize - bootstrap postfix for dialog size, e.g. "sm", "m";
            *                options.progressType - bootstrap postfix for progress bar type, e.g. "success", "warning".
            */
            show: function (message, options) {
                // Assigning defaults
                if (typeof options === 'undefined') {
                    options = {};
                }
                if (typeof message === 'undefined') {
                    message = 'Loading';
                }
                var settings = $.extend({
                    dialogSize: 'm',
                    progressType: '',
                    onHide: null // This callback runs after the dialog was hidden
                }, options);

                // Configuring dialog
                $dialog.find('.modal-dialog').attr('class', 'modal-dialog').addClass('modal-' + settings.dialogSize);
                $dialog.find('.progress-bar').attr('class', 'progress-bar');
                if (settings.progressType) {
                    $dialog.find('.progress-bar').addClass('progress-bar-' + settings.progressType);
                }
                $dialog.find('h3').text(message);
                // Adding callbacks
                if (typeof settings.onHide === 'function') {
                    $dialog.off('hidden.bs.modal').on('hidden.bs.modal', function (e) {
                        settings.onHide.call($dialog);
                    });
                }
                // Opening dialog
                $dialog.modal();
            },
            /**
            * Closes dialog
            */
            hide: function () {
                $dialog.modal('hide');
            }
        };

    })(jQuery);

    var word_cloud_modal = word_cloud_modal || (function ($) {
        'use strict';
        var $dialog = $("#canvas-modal");
        return {
            show: function (message, options) {
                // Assigning defaults
                if (typeof options === 'undefined') {
                    options = {};
                }
                if (typeof message === 'undefined') {
                    message = 'Loading';
                }
                var settings = $.extend({
                    dialogSize: 'm',
                    progressType: '',
                    onHide: null // This callback runs after the dialog was hidden
                }, options);
                $dialog.find('.modal-dialog').attr('class', 'modal-dialog').addClass('modal-' + settings.dialogSize);
                $dialog.find('.progress-bar').attr('id', 'canvas');
                $dialog.find('h3').text(message);
                // Adding callbacks
                if (typeof settings.onHide === 'function') {
                    $dialog.off('hidden.bs.modal').on('hidden.bs.modal', function (e) {
                        settings.onHide.call($dialog);
                    });
                }
                $dialog.modal();
            },
            hide: function () {
                $dialog.modal('hide');
            }
        };
    })(jQuery);

    </script>

