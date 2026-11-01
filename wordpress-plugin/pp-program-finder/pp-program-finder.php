<?php
/**
 * Plugin Name: Parent Possible Program Finder
 * Description: Embeds the PAT and HIPPY Program Finder on any page with the [program_finder] shortcode.
 * Version: 0.1.0
 * Author: Duke Global Research and Consulting
 * License: GPL-2.0-or-later
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

// Where the finder page is hosted. Change this in Settings > Program Finder
// once the page moves to its permanent home.
const PP_FINDER_DEFAULT_URL = 'https://doumifrog.github.io/ppp-finder/';

function pp_finder_url() {
	$url = get_option( 'pp_finder_url' );
	return $url ? $url : PP_FINDER_DEFAULT_URL;
}

/**
 * [program_finder] or [program_finder height="1400"]
 * The height is only the starting height. The iframe grows or shrinks to fit
 * once the finder reports its real height.
 */
function pp_finder_shortcode( $atts ) {
	$atts = shortcode_atts( array( 'height' => '1400' ), $atts, 'program_finder' );
	$id   = 'pp-finder-' . wp_rand( 1000, 9999 );

	ob_start();
	?>
	<iframe
		id="<?php echo esc_attr( $id ); ?>"
		class="pp-program-finder"
		src="<?php echo esc_url( pp_finder_url() ); ?>"
		title="Find a home visiting program"
		loading="lazy"
		style="width:100%;border:0;display:block;height:<?php echo absint( $atts['height'] ); ?>px"
	></iframe>
	<script>
	(function () {
		var frame = document.getElementById(<?php echo wp_json_encode( $id ); ?>);
		window.addEventListener('message', function (e) {
			if (!frame || e.source !== frame.contentWindow) return;
			var d = e.data;
			if (d && d.type === 'pp-finder-height' && d.height > 200) {
				frame.style.height = Math.ceil(d.height) + 'px';
			}
		});
	})();
	</script>
	<?php
	return ob_get_clean();
}
add_shortcode( 'program_finder', 'pp_finder_shortcode' );

// Settings > Program Finder: one field for the hosted page's address.
function pp_finder_settings_init() {
	register_setting( 'pp_finder', 'pp_finder_url', array( 'sanitize_callback' => 'esc_url_raw' ) );
}
add_action( 'admin_init', 'pp_finder_settings_init' );

function pp_finder_settings_menu() {
	add_options_page( 'Program Finder', 'Program Finder', 'manage_options', 'pp-finder', 'pp_finder_settings_page' );
}
add_action( 'admin_menu', 'pp_finder_settings_menu' );

function pp_finder_settings_page() {
	?>
	<div class="wrap">
		<h1>Program Finder</h1>
		<p>Add the finder to any page or post with the shortcode <code>[program_finder]</code>.</p>
		<form method="post" action="options.php">
			<?php settings_fields( 'pp_finder' ); ?>
			<table class="form-table" role="presentation">
				<tr>
					<th scope="row"><label for="pp_finder_url">Finder page address</label></th>
					<td>
						<input type="url" class="regular-text" id="pp_finder_url" name="pp_finder_url"
							value="<?php echo esc_attr( pp_finder_url() ); ?>">
						<p class="description">The web address where the finder page is hosted, such as its GitHub Pages link.</p>
					</td>
				</tr>
			</table>
			<?php submit_button(); ?>
		</form>
	</div>
	<?php
}
