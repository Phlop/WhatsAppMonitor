
<div class="clearfix"></div>
<section>
	<h3 class="page-header" style="border-bottom: solid #5A738E;">
		<a class="lang" key="topcontent"></a>
		<em name='langdate' class='langdate' value='en'>  Waiting data from server... </em>  
	</h3>
        
	<ul class="nav nav-tabs">
		<li class="active">
			<a data-toggle="pill" href="#imagens"><div class="lang" key="images"></div></a>
		</li>
		<li>
			<a data-toggle="pill" href="#videos"><div class="lang" key="videos"></div></a>
		</li>
		<li>
			<a data-toggle="pill" href="#mensagens"><div class="lang" key="messages"></div></a>
		</li>

		<!-- <li>
			<a data-toggle="pill" href="#links"><div class="lang" key="urls"></div></a>
		</li> -->
		<li>
			<a data-toggle="pill" href="#audios"><div class="lang" key="audios"></div></a> 
		</li>
		
		<li>
			<a data-toggle="pill" href="#stickers"><div class="lang" key="stickers"></div></a>
		</li>
		
	</ul>
    
	<div class="tab-content">
         <!-- .......... TAB CONTENT FOR IMAGES .......... -->
		<div id="imagens" class="tab-pane fade in active">
			<div class="container gal-container" id="session_tab_images">
				<h3>
					<font color="red">
						<i class='fa fa-spinner fa-spin '></i>
					</font> <div class="lang" key="nodata"></div></h3>
			</div>
		</div>
        
        <!-- .......... TAB CONTENT FOR AUDIOS .......... -->
		<div id="audios" class="tab-pane fade">
			<div class="container gal-container" id="session_tab_audios">
				<h3>  </h3>
				<?php include "player.php" ?>
			</div>
			
		</div>
        
        <!-- .......... TAB CONTENT FOR MESSAGES .......... -->
		<div id="mensagens" class="tab-pane fade">
			<div class="container gal-container" id="session_tab_mensagem">
				<h3>  <div class="lang" key="nodata"></div> </h3>
				<!-- <h3><font color="red"><i class='fa fa-spinner fa-spin '></i></font> Carregando...</h3> -->
			</div>
		</div>
        
        <!-- .......... TAB  CONTENT FOR VIDEOS .......... -->
		<div id="videos" class="tab-pane fade">
			<div class="container gal-container" id="session_tab_videos">
				<h3> <div class="lang" key="nodata"></div></h3>
				<!-- <h3><font color="red"><i class='fa fa-spinner fa-spin '></i></font> Carregando...</h3> -->
			</div>
		</div>
        
        <!-- .......... TAB CONTENT FOR URLS .......... -->
		<div id="links" class="tab-pane fade">
			<div class="container gal-container" id="session_tab_links">
				<h3> <div class="lang" key="nodata"></div></h3>
				<!-- <h3><font color="red"><i class='fa fa-spinner fa-spin '></i></font> Carregando...</h3> -->
			</div>
		</div>
        
        <!-- .......... TAB CONTENT FOR STICKERS .......... -->
		<div id="stickers" class="tab-pane fade">
			<div class="container gal-container" id="session_tab_stickers">
				<h3> <div class="lang" key="nodata"></div></h3>
				<!-- <h3><font color="red"><i class='fa fa-spinner fa-spin '></i></font> Carregando...</h3> -->
			</div>
		</div>
	</div>



</section>
