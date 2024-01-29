<div class="row">
	<div class="large-8 medium-10 small-11 large-centered medium-centered small-centered columns" id="amplitude-player">
		<div class="row">
			<div class="large-6 medium-6 small-12 columns" id="amplitude-left">
				<div id="player-left-bottom">
					<div id="time-container">
						<span class="current-time">
							<span class="amplitude-current-minutes" amplitude-main-current-minutes="true"></span>:
							<span class="amplitude-current-seconds" amplitude-main-current-seconds="true"></span>
						</span>
						<input type="range" class="amplitude-song-slider" amplitude-main-song-slider="true" step=".1" />
						<span class="duration">
							<span class="amplitude-duration-minutes" amplitude-main-duration-minutes="true"></span>:
							<span class="amplitude-duration-seconds" amplitude-main-duration-seconds="true"></span>
						</span>
					</div>

					<div id="control-container">
						<div id="repeat-container">
							<div class="amplitude-repeat" id="repeat"></div>
						</div>

						<div id="central-control-container">
							<div id="central-controls">
								<div class="amplitude-prev" id="previous"></div>
								<div class="amplitude-play-pause" amplitude-main-play-pause="true" id="play-pause"></div>
								<div class="amplitude-next" id="next"></div>
							</div>
						</div>

						<div id="shuffle-container">
							<div class="amplitude-shuffle amplitude-shuffle-off" id="shuffle"></div>
						</div>
					</div>

					<div id="meta-container">
						<span amplitude-song-info="name" amplitude-main-song-info="true" class="song-name"></span>

						<div class="song-artist-album">
							<span amplitude-song-info="artist" amplitude-main-song-info="true"></span>
							<span amplitude-song-info="album" amplitude-main-song-info="true"></span>
						</div>
					</div>
				</div>
			</div>
			<div class="large-6 medium-6 small-12 columns" id="amplitude-right">

			</div>
		</div>
	</div>
</div>