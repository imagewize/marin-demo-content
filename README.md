# Marin demo content

Sample skincare products and placeholder packshots for the
[Marin](https://github.com/imagewize/marin) WooCommerce theme. The seeder is plain
WP-CLI and works on any WooCommerce store, with or without Marin.

It creates 16 products in 7 categories (Moisturisers, Cleansers, Serums, Sun Care, Body,
Toners and Masks, Kits), including 5 variable products with size options and 3 sale items.
Each product has an illustrated packshot.

## Requirements

- WordPress with WooCommerce active
- [WP-CLI](https://wp-cli.org/)

## Usage

From this directory (or pass the full path to the file):

```bash
wp eval-file seed-skincare-products.php          # create the products
wp eval-file seed-skincare-products.php reset    # delete the demo products, then recreate them
```

On multisite, add `--url=<subsite url>`. Running it again is safe: products whose slug
already exists are skipped.

The product copy is placeholder text. Replace it with your own.

## What's here

| Path | Contents |
|------|----------|
| `seed-skincare-products.php` | The seeder |
| `images/` | 1200px PNG packshots the seeder uploads (WordPress blocks SVG uploads by default) |
| `svg/` | Source SVGs: jar, tube, dropper, pump bottle, toner bottle and kit |
| `generate-product-svgs.py` | Regenerates `svg/` (`python3 generate-product-svgs.py svg`) |

To rebuild the PNGs after changing the generator:

```bash
for f in svg/*.svg; do rsvg-convert -w 1200 "$f" -o "images/$(basename "${f%.svg}").png"; done
```

## License

Code: GNU GPL v3 or later, matching Marin. Artwork in `svg/` and `images/`: CC0.
