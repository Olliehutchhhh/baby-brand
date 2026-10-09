# Casa de Mamá – Shopify setup guide

You have two files:
- `casa-de-mama-shopify-theme.zip` – your store theme (Shopify's free Dawn theme + your header and your product page design)
- `product-images.zip` – the product photos, in folders (warmer / cooler / bundle), in the order they should be uploaded

## 1. Upload the theme (10 min)
1. Shopify admin → **Online Store → Themes → Add theme → Upload zip file** → choose `casa-de-mama-shopify-theme.zip`.
2. It appears under "Theme library" and is **not live** yet. Don't publish until step 6.

## 2. Create the three products (Products → Add product)
Create them with these handles so everything connects automatically. (The handle is the end of the page address – edit it under "Search engine listing".)

| Product | Title | Handle | Price | Compare-at price | Theme template |
|---|---|---|---|---|---|
| Warmer | Superfast Portable Bottle Warmer for Travel | `portable-bottle-warmer` | £89.99 | £104.99 | **casa-warmer** |
| Cooler | Portable Breast Milk Cooler for Travel | `portable-breast-milk-cooler` | £79.99 | £94.99 | **casa-cooler** |
| Bundle | Portable Bottle Warmer & Cooler Set | `portable-warmer-cooler-bundle` | £134.99 | £169.98 | **casa-bundle** |

- All prices are the placeholders from the design – change them to your real ones.
- Upload the photos from `product-images.zip` in numbered order (the first image is the main one).
- In the right-hand "Theme template" box on each product, pick the template named in the last column.
- You can leave the product description blank – the page text is already filled in. Edit it later in the theme editor (below), or type a description in the product to override.
- Tick "Track quantity" and set stock as usual.

## 3. Check the page in the theme editor
**Online Store → Themes → Customize**, then use the top dropdown to choose the product page template (casa-warmer / casa-cooler / casa-bundle) and preview each one. In the left panel, click **Casa product page** to edit: subtitle, benefit pills, option-card text, the bundle strip, shipping/guarantee text, "Pair well with", and reviews.

- **Reviews:** the warmer and bundle pages use the 5 review photos. On the cooler page add your own: **Casa product page → Review photo** blocks → pick an image. Empty blocks show the pink placeholders.
- **Header:** click the header in the editor to change the logo, name, tagline and menu.
- If your product handles differ from the table, set **Bundle product / Single product / Product to pair** in the editor instead.

## 4. Menu and pages
- **Content → Menus → Main menu:** keep **Shop** (link to your collection) and **About Us**. Create the About Us page under **Content → Pages**.
- The header also shows a **Cart (n)** link, so customers can reach their cart.

## 5. Free shipping over £100
**Settings → Shipping and delivery →** your shipping profile → add a rate: price £0, "Add conditions → Based on order price" from £100. Add a paid rate for orders under £100.

## 6. Go live
Test an order with **Settings → Payments → Bogus gateway/test mode** (or a 100% discount code), then **Themes → Publish**. Remove the password page under **Online Store → Preferences** when you're ready to launch.

## Things to know
- **The bundle is its own product.** Shopify doesn't know it contains a warmer and a cooler, so stock is not reduced on the individual products. Fix: install Shopify's free **Bundles** app and build it from the warmer + cooler, or manage stock by hand.
- **The free E-Book isn't delivered yet.** The E-Book is a picture on the page only. Set it up with a free app such as "Digital Downloads" (add it to the bundle order), or put the link in your order-confirmation email. The cover image is a placeholder – replace it in the editor (Item 3 image).
- **Removed from the Shopify version** (they didn't work on a live store): Add to Wishlist, Compare, Share icons, the "people viewing now" counter, and the "Autumn Care Event" bar (replaced by a simple free-shipping announcement you can edit or delete under the header).
- **Review stars/count** are hidden until you type a number in "Review count". Use a reviews app (e.g. Judge.me) when you have real reviews.
- **Discount box** ("20% with code…") is hidden until you type a code in the editor. It only displays the code – create the actual code under Discounts.
- **Checkout** uses Shopify's own checkout, so the checkout page doesn't have the Casa de Mamá design unless you customise it (Settings → Checkout → Customize, available on all plans for logo and colours).
- The theme was checked with Shopify's own "Theme Check" tool and rendered locally, but not on a live store, so look through each page once after uploading.

## Auto-linking (no pickers needed)
The theme finds the other products itself using each product's **Theme template** (`casa-warmer`, `casa-cooler`, `casa-bundle`).
Just make sure all three products are Active and each has its template assigned. The "Override" pickers in the theme editor can stay empty.
