<?php
/**
 * Seed a WooCommerce store with demo skincare products.
 *
 * Usage (from this directory, or give the full path to the file):
 *   wp eval-file seed-skincare-products.php          # create products (idempotent)
 *   wp eval-file seed-skincare-products.php reset    # delete the demo products first
 *
 * On multisite add --url=<subsite url>.
 */
if ( ! class_exists( 'WooCommerce' ) ) {
	WP_CLI::error( 'WooCommerce must be active.' );
}

require_once ABSPATH . 'wp-admin/includes/file.php';
require_once ABSPATH . 'wp-admin/includes/media.php';
require_once ABSPATH . 'wp-admin/includes/image.php';

$dir   = __DIR__ . '/images/';
$reset = isset( $args[0] ) && 'reset' === $args[0];

$cats = array(
	'moisturisers' => 'Moisturisers',
	'cleansers'    => 'Cleansers',
	'serums'       => 'Serums',
	'sun-care'     => 'Sun Care',
	'body'         => 'Body',
	'toners-masks' => 'Toners & Masks',
	'kits'         => 'Kits',
);
$cat_ids = array();
foreach ( $cats as $slug => $name ) {
	$t = term_exists( $slug, 'product_cat' );
	if ( ! $t ) {
		$t = wp_insert_term( $name, 'product_cat', array( 'slug' => $slug ) );
	}
	$cat_ids[ $slug ] = is_array( $t ) ? (int) $t['term_id'] : (int) $t;
}

// slug, name, cat, price, sale, short, sizes (null = simple), featured
$products = array(
	array( 'daily-moisturiser', 'Daily Moisturiser', 'moisturisers', 38, null, 'Lightweight daily cream with ceramides and squalane for all-day hydration.', null, true ),
	array( 'night-repair-cream', 'Night Repair Cream', 'moisturisers', 54, 46, 'A rich overnight cream with peptides that supports skin renewal while you sleep.', null, true ),
	array( 'rich-body-butter', 'Rich Body Butter', 'body', 32, null, 'Whipped shea and cocoa butter for dry skin, with a soft vanilla scent.', array( '200 ml' => 32, '400 ml' => 52 ), false ),
	array( 'hydrating-cleanser', 'Hydrating Cleanser', 'cleansers', 24, null, 'A creamy, low-foam cleanser that removes the day without stripping skin.', null, true ),
	array( 'mineral-sunscreen', 'Mineral Sunscreen SPF 50', 'sun-care', 29, null, 'Broad-spectrum zinc sunscreen with a sheer, no-white-cast finish.', array( '50 ml' => 29, '100 ml' => 48 ), true ),
	array( 'clay-mask', 'Rose Clay Mask', 'toners-masks', 28, null, 'A weekly purifying mask with rose clay that clears pores and calms redness.', null, false ),
	array( 'hand-cream', 'Everyday Hand Cream', 'body', 18, null, 'Fast-absorbing hand cream with glycerin and oat extract.', null, false ),
	array( 'vitamin-c-serum', 'Vitamin C Serum', 'serums', 44, null, 'A stable 15% vitamin C serum that brightens dullness and evens out tone.', array( '30 ml' => 44, '50 ml' => 66 ), true ),
	array( 'hyaluronic-serum', 'Hyaluronic Serum', 'serums', 36, 29, 'Three weights of hyaluronic acid for plump, deeply hydrated skin.', array( '30 ml' => 36, '50 ml' => 54 ), false ),
	array( 'retinol-serum', 'Retinol Serum', 'serums', 48, null, 'A gentle 0.3% encapsulated retinol serum for smoother, firmer skin.', null, false ),
	array( 'gentle-body-lotion', 'Gentle Body Lotion', 'body', 26, null, 'Fragrance-free daily body lotion for sensitive skin.', null, false ),
	array( 'foaming-face-wash', 'Foaming Face Wash', 'cleansers', 22, null, 'A fresh gel-to-foam cleanser for combination and oily skin.', null, false ),
	array( 'balancing-toner', 'Balancing Toner', 'toners-masks', 26, null, 'An alcohol-free toner with niacinamide that refines pores and balances oil.', null, false ),
	array( 'micellar-water', 'Micellar Water', 'cleansers', 19, null, 'One-step makeup remover and cleanser, gentle enough for the eyes.', null, false ),
	array( 'essentials-kit', 'The Essentials Kit', 'kits', 79, 68, 'Cleanser, serum and moisturiser in travel sizes: a complete routine in three steps.', null, true ),
	array( 'glow-ritual-kit', 'The Glow Ritual Kit', 'kits', 96, null, 'Vitamin C serum, toner and day cream, our brightening trio.', null, false ),
);

if ( $reset ) {
	foreach ( $products as $p ) {
		$existing = get_page_by_path( $p[0], OBJECT, 'product' );
		if ( $existing ) {
			$product = wc_get_product( $existing->ID );
			if ( $product && $product->get_image_id() ) {
				wp_delete_attachment( $product->get_image_id(), true );
			}
			wp_delete_post( $existing->ID, true );
			WP_CLI::log( "deleted {$p[0]}" );
		}
	}
}

foreach ( $products as $p ) {
	list( $slug, $name, $cat, $price, $sale, $short, $sizes, $featured ) = $p;

	if ( get_page_by_path( $slug, OBJECT, 'product' ) ) {
		WP_CLI::log( "skip $slug" );
		continue;
	}

	$product = $sizes ? new WC_Product_Variable() : new WC_Product_Simple();
	$product->set_name( $name );
	$product->set_slug( $slug );
	$product->set_status( 'publish' );
	$product->set_short_description( $short );
	$product->set_description(
		$short . "\n\n" .
		'Demo product. Replace this copy with your own description and ingredients.' . "\n\n" .
		'How to use: apply to clean skin morning and evening, then follow with the next step in your routine.'
	);
	$product->set_category_ids( array( $cat_ids[ $cat ] ) );
	$product->set_featured( $featured );
	$product->set_sku( 'DEMO-' . strtoupper( substr( str_replace( '-', '', $slug ), 0, 8 ) ) );
	$product->set_manage_stock( false );
	$product->set_stock_status( 'instock' );

	if ( ! $sizes ) {
		$product->set_regular_price( (string) $price );
		if ( $sale ) {
			$product->set_sale_price( (string) $sale );
		}
	} else {
		$attr = new WC_Product_Attribute();
		$attr->set_name( 'Size' );
		$attr->set_options( array_keys( $sizes ) );
		$attr->set_visible( true );
		$attr->set_variation( true );
		$product->set_attributes( array( $attr ) );
	}

	// media_sideload_image() needs http(s), so copy the file and sideload it.
	$tmp = wp_tempnam( $slug . '.png' );
	copy( $dir . $slug . '.png', $tmp );
	$img = media_handle_sideload(
		array( 'name' => $slug . '.png', 'tmp_name' => $tmp ),
		0,
		$name
	);
	if ( ! is_wp_error( $img ) ) {
		update_post_meta( $img, '_wp_attachment_image_alt', $name );
		$product->set_image_id( $img );
	} else {
		WP_CLI::warning( "image failed for $slug: " . $img->get_error_message() );
	}

	$id = $product->save();

	if ( $sizes ) {
		$first = true;
		foreach ( $sizes as $size => $vprice ) {
			$v = new WC_Product_Variation();
			$v->set_parent_id( $id );
			$v->set_attributes( array( 'size' => $size ) );
			$v->set_regular_price( (string) $vprice );
			if ( $sale && $first ) {
				$v->set_sale_price( (string) $sale );
			}
			$v->set_manage_stock( false );
			$v->set_stock_status( 'instock' );
			$v->save();
			$first = false;
		}
		WC_Product_Variable::sync( $id );
	}
	WP_CLI::success( "created $slug ($id)" );
}
