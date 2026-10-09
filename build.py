#!/usr/bin/env python3
"""Generates, from pages/bottle-warmer-pdp.html (the source of truth for layout/CSS/JS):
   - pages/bottle-warmer-bundle-pdp.html   (warmer + cooler bundle)
   - pages/breast-milk-cooler-pdp.html     (cooler product page; images in assets/cooler/)
Run after every edit to the warmer page:  python3 build.py"""
import pathlib, re, io, base64
from PIL import Image
root = pathlib.Path(__file__).parent
d = root / "pages"
src = (d / "bottle-warmer-pdp.html").read_text()

# ---------- bundle page ----------
s = src
assert s.count("var PAGE = 'single';") == 1
s = s.replace("var PAGE = 'single';", "var PAGE = 'bundle';")
s = s.replace("<title>Superfast Portable Bottle Warmer for Travel</title>", "<title>Portable Bottle Warmer &amp; Cooler Set</title>")
# bundle: its own review placeholders (not the warmer's photos) + a "Just the cooler" link card
_ph = ''.join('        <div class="video-card ph"><span class="bag">🛍</span><span class="play">▶</span></div>\n' for _ in range(5))
_a = s.index('<div class="video-row" id="reviewRow">'); _b = s.index('      <div class="discount-box">', _a)
s = s[:_a] + '<div class="video-row" id="reviewRow">\n' + _ph + '      </div>\n\n' + s[_b:]
_css = ('  .video-card.ph{ cursor:default; border-radius:0; background:repeating-linear-gradient(45deg, #FFE9F6, #FFE9F6 10px, #FFD6EE 10px, #FFD6EE 20px); border:1px dashed #F6B9DF; display:flex; align-items:center; justify-content:center; }\n'
  '  .video-card.ph .play{ width:36px; height:36px; border-radius:50%; background:rgba(255,255,255,0.85); display:flex; align-items:center; justify-content:center; font-size:14px; }\n'
  '  .video-card.ph .bag{ position:absolute; top:10px; right:10px; width:26px; height:26px; border-radius:50%; background:rgba(255,255,255,0.85); display:flex; align-items:center; justify-content:center; font-size:12px; }\n'
  '  /* ===== Review lightbox ===== */')
assert s.count('  /* ===== Review lightbox ===== */') == 1
s = s.replace('  /* ===== Review lightbox ===== */', _css)
_cooler_card = ('''        <!-- MIDDLE: the cooler on its own (links to its page) -->
        <div class="opt-card" id="optCooler" role="radio" aria-checked="false" tabindex="0" data-opt="cooler">
          <div class="opt-head">
            <span class="opt-radio"></span>
            <span class="opt-title">Portable Cooler</span>
          </div>
          <div class="opt-price">£79.99</div>
          <div class="opt-sub">Just the cooler</div>
          <ul class="opt-list">
            <li>Portable Breast Milk Cooler (650ml)</li>
            <li>2 Cooling Cylinders Included</li>
            <li>30 Days Guarantee</li>
          </ul>
        </div>

''')
_m = '        <!-- RIGHT: Bundle And Save, with free gifts -->'
assert s.count(_m) == 1
s = s.replace(_m, _cooler_card + _m)
_u = "var PAGE_URLS = { single:'bottle-warmer-pdp.html', bundle:'bottle-warmer-bundle-pdp.html' };"
assert s.count(_u) == 1
s = s.replace(_u, "var PAGE_URLS = { single:'bottle-warmer-pdp.html', cooler:'breast-milk-cooler-pdp.html', bundle:'bottle-warmer-bundle-pdp.html' };")
(d / "bottle-warmer-bundle-pdp.html").write_text(s)
print("built bottle-warmer-bundle-pdp.html")

# ---------- cooler page ----------
def uri(img, w, q=84):
    im = img.convert("RGB").copy(); im.thumbnail((w, w), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, "JPEG", quality=q, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()

def rep(text, old, new, count=1):
    assert text.count(old) == count, (old[:70], text.count(old))
    return text.replace(old, new)

def region(text, start, end, new):
    a = text.index(start); b = text.index(end, a)
    return text[:a] + new + text[b:]

img = {k: Image.open(root / "assets/cooler" / f"{k}.jpg") for k in ("main", "features", "lifestyle")}
m_full, m_thumb = uri(img["main"], 1000), uri(img["main"], 240)
f_full, f_thumb = uri(img["features"], 1000), uri(img["features"], 240)
l_full, l_thumb = uri(img["lifestyle"], 1000), uri(img["lifestyle"], 240)

# warmer photo for the "Pair well with" card (taken from the warmer page's own main image)
warmer_main = re.search(r'<img id="mainImageImg" src="(data:image/[a-z]+;base64,[^"]+)"', src).group(1)
w_img = Image.open(io.BytesIO(base64.b64decode(warmer_main.split(",", 1)[1])))
w_thumb = uri(w_img, 260)

c = src
c = rep(c, "<title>Superfast Portable Bottle Warmer for Travel</title>", "<title>Portable Breast Milk Cooler for Travel</title>")
# page identity
c = rep(c, "var PAGE = 'single';", "var PAGE = 'single';")
c = rep(c, "var PAGE_URLS = { single:'bottle-warmer-pdp.html', bundle:'bottle-warmer-bundle-pdp.html' };",
           "var PAGE_URLS = { single:'breast-milk-cooler-pdp.html', bundle:'bottle-warmer-bundle-pdp.html' };")
# breadcrumb
c = rep(c, '<a href="#">Bottle Warmers</a> &gt; <a href="#" id="crumbCat">Portable Bottle Warmer</a> &gt; <span class="current" id="crumbName">Superfast Portable Bottle Warmer for Travel</span>',
           '<a href="#">Breast Milk Coolers</a> &gt; <a href="#" id="crumbCat">Portable Breast Milk Cooler</a> &gt; <span class="current" id="crumbName">Portable Breast Milk Cooler for Travel</span>')
# gallery thumbnails
thumbs = ('<div class="thumb-strip" id="thumbsSingle">\n'
  f'        <div class="thumb active" data-label="Main shot" data-full="{m_full}" style="background-image:url(\'{m_thumb}\');background-size:cover;background-position:center;color:transparent;"></div>\n'
  f'        <div class="thumb has-img" data-label="Features" data-full="{f_full}" style="background-image:url(\'{f_thumb}\');background-size:cover;background-position:center;color:transparent;"></div>\n'
  f'        <div class="thumb has-img" data-label="Out and about" data-full="{l_full}" style="background-image:url(\'{l_thumb}\');background-size:cover;background-position:center;color:transparent;"></div>\n'
  '      </div>\n      ')
c = region(c, '<div class="thumb-strip" id="thumbsSingle">', '<div class="thumb-strip" id="thumbsBundle"', thumbs)
c = re.sub(r'(<img id="mainImageImg" src=")[^"]+(" alt=")[^"]+(")', lambda m: m.group(1) + m_full + m.group(2) + "Portable Breast Milk Cooler for Travel" + m.group(3), c, count=1)
# title / subtitle / pills / description
c = rep(c, '<h1 id="pdpTitle">Superfast Portable Bottle Warmer for Travel</h1>', '<h1 id="pdpTitle">Portable Breast Milk Cooler for Travel</h1>')
c = rep(c, '<div class="subtitle" id="pdpSub">Warm bottles on the go, without the hassle.</div>', '<div class="subtitle" id="pdpSub">Fresh milk, wherever life takes you.</div>')
pills = ('<div class="benefit-pills" id="pdpPills">\n'
  '        <div class="pill"><span class="check">✓</span> 24 Hour Cooling</div>\n'
  '        <div class="pill"><span class="check">✓</span> Large 650ml Capacity</div>\n'
  '        <div class="pill"><span class="check">✓</span> Leak-Proof Lid</div>\n'
  '        <div class="pill"><span class="check">✓</span> 360° Iceless Cooling</div>\n'
  '      </div>\n\n      ')
c = region(c, '<div class="benefit-pills" id="pdpPills">', '<hr class="section-divider">', pills)
desc = ("The Casa de Mamá Portable Breast Milk Cooler is designed to safely store cold breast milk while you&rsquo;re out of the house. "
        "With a large 650ml capacity that fits two 300ml bottles, a leak-proof lid and even, iceless 360&deg; cooling, it keeps milk cold for up to 24 hours &mdash; "
        "perfect for days out, holidays and travelling. Two cooling cylinders are included: use them together to keep milk cold all day.")
c = re.sub(r'(<p class="desc-text" id="pdpDesc">).*?(</p>)', lambda m: m.group(1) + desc + m.group(2), c, count=1, flags=re.S)
# option cards
c = rep(c, '<!-- LEFT: warmer on its own -->', '<!-- LEFT: cooler on its own -->')
c = rep(c, '<span class="opt-title">Portable Warmer</span>', '<span class="opt-title">Portable Cooler</span>')
c = rep(c, '<div class="opt-price">£89.99</div>\n          <div class="opt-sub">Just the warmer</div>', '<div class="opt-price">£79.99</div>\n          <div class="opt-sub">Just the cooler</div>')
c = rep(c, '<li>Portable Milk &amp; Water Warmer</li>\n            <li>30 Days Guarantee</li>', '<li>Portable Breast Milk Cooler (650ml)</li>\n            <li>2 Cooling Cylinders Included</li>\n            <li>30 Days Guarantee</li>')
c = rep(c, 'Add the cooler &amp; save 21% →', 'Add the warmer &amp; save 21% →')
# prices
c = rep(c, '<div class="price-old" id="priceOld">£104.99</div>', '<div class="price-old" id="priceOld">£94.99</div>')
c = rep(c, '<div class="price" id="priceNow">£89.99</div>', '<div class="price" id="priceNow">£79.99</div>')
c = rep(c, '<div class="off-pill" id="priceOff">14% OFF</div>', '<div class="off-pill" id="priceOff">16% OFF</div>')
c = rep(c, "single: { name:'Superfast Portable Bottle Warmer for Travel', old:'£104.99', now:'£89.99',  off:'14% OFF' },",
           "single: { name:'Portable Breast Milk Cooler for Travel', old:'£94.99', now:'£79.99',  off:'16% OFF' },")
# reviews -> placeholders (fill in later)
ph = ''.join('        <div class="video-card ph"><span class="bag">🛍</span><span class="play">▶</span></div>\n' for _ in range(5))
c = region(c, '<div class="video-row" id="reviewRow">', '      <div class="discount-box">', '<div class="video-row" id="reviewRow">\n' + ph + '      </div>\n\n')
c = rep(c, '  /* ===== Review lightbox ===== */',
  '  .video-card.ph{ cursor:default; border-radius:0; background:repeating-linear-gradient(45deg, #FFE9F6, #FFE9F6 10px, #FFD6EE 10px, #FFD6EE 20px); border:1px dashed #F6B9DF; display:flex; align-items:center; justify-content:center; }\n'
  '  .video-card.ph .play{ width:36px; height:36px; border-radius:50%; background:rgba(255,255,255,0.85); display:flex; align-items:center; justify-content:center; font-size:14px; }\n'
  '  .video-card.ph .bag{ position:absolute; top:10px; right:10px; width:26px; height:26px; border-radius:50%; background:rgba(255,255,255,0.85); display:flex; align-items:center; justify-content:center; font-size:12px; }\n'
  '  /* ===== Review lightbox ===== */')
# pair well with -> the warmer
pair = ('<div class="pair-title">Pair well with:</div>\n'
  '        <div class="pair-card pair-single">\n'
  f'          <a class="pair-img" href="bottle-warmer-pdp.html" aria-label="View the Portable Bottle Warmer" style="display:block;background:#fff url(\'{w_thumb}\') center/cover no-repeat;"></a>\n'
  '          <div class="pair-info">\n'
  '            <div class="name"><a href="bottle-warmer-pdp.html">Portable Bottle Warmer</a></div>\n'
  '            <div class="p"><span class="was">£89.99</span> £55.00 GBP</div>\n'
  '            <div class="pair-note">Bundle discount</div>\n'
  '            <button class="quick" id="addCoolerBtn">Add to bundle</button>\n'
  '          </div>\n        </div>\n      </div>\n\n      ')
c = region(c, '<div class="pair-title">Pair well with:</div>', '<div class="share-row">', pair)
# sticky bar
c = rep(c, '<div class="name" id="stickyName">Superfast Portable Bottle Warmer for Travel</div>', '<div class="name" id="stickyName">Portable Breast Milk Cooler for Travel</div>')
c = rep(c, '<div class="price" id="stickyPrice">£89.99 GBP</div>', '<div class="price" id="stickyPrice">£79.99 GBP</div>')
c = rep(c, '<option value="single">Portable Warmer · £89.99</option>', '<option value="single">Portable Cooler · £79.99</option>')
c = rep(c, '<button class="btn btn-cart" id="stickyAddToCart">Add to Cart - £89.99</button>', '<button class="btn btn-cart" id="stickyAddToCart">Add to Cart - £79.99</button>')
c = re.sub(r'(<div class="sticky-thumb" style="background-image:url\(\')[^\']+(\')', lambda m: m.group(1) + m_thumb + m.group(2), c, count=1)
(d / "breast-milk-cooler-pdp.html").write_text(c)
print("built breast-milk-cooler-pdp.html")
