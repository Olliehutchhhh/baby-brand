#!/usr/bin/env python3
"""Generates, from pages/bottle-warmer-pdp.html (the source of truth for layout/CSS/JS):
   - pages/bottle-warmer-bundle-pdp.html   (warmer + cooler bundle)
   - pages/breast-milk-cooler-pdp.html     (cooler product page; images in assets/cooler/)
Run after every edit to the warmer page:  python3 build.py"""
import pathlib, re, io, base64
from PIL import Image
root = pathlib.Path(__file__).parent
d = root / "pages"
src = (d / "_source" / "bottle-warmer-pdp.src.html").read_text()  # pristine source; pages/bottle-warmer-pdp.html is generated output

# ---------- cart drawer block (re-injected into the warmer source on every build) ----------
_blk = (root / "cart_block.html").read_text()
_w_main = re.search(r'<img id="mainImageImg" src="(data:image/[a-z]+;base64,[^"]+)"', src).group(1)
_wi = Image.open(io.BytesIO(base64.b64decode(_w_main.split(",", 1)[1])))
def _thumb(im, w=220):
    im = im.convert("RGB").copy(); im.thumbnail((w, w), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, "JPEG", quality=80, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
_blk = _blk.replace("__CCD_IMG_W__", _thumb(_wi)).replace("__CCD_IMG_C__", _thumb(Image.open(root / "assets/cooler/main.jpg")))
if "<!--CASA_CART-->" in src:
    src = re.sub(r"<!--CASA_CART-->.*?<!--/CASA_CART-->", lambda m: _blk, src, flags=re.S)
else:
    src = src.replace("</body>", _blk + "\n</body>", 1)

# ---------- "Key Product Features" section (generated for every page) ----------
FEATURES = {
  "warmer": [
    ("Warms milk and water, anywhere", "Heat a bottle of milk or water at the park, in the car or mid-flight. No kettle, hob or microwave needed."),
    ("Heats fast, with a long battery life", "Quick heating means a hungry baby isn’t left waiting, and a long-lasting rechargeable battery keeps it ready for days out and long journeys."),
    ("Easy for everyone to use", "Simple buttons and a clear temperature display make it effortless for anyone, from new parents to grandparents on babysitting duty."),
  ],
  "cooler": [
    ("Iceless 360° cooling", "Keeps breast milk cold for up to 24 hours without needing any ice, so it’s ready whenever you are."),
    ("650ml capacity, fits two 300ml bottles", "Room for two full 300ml bottles, so you can carry a whole day’s feeds in one bottle."),
    ("Leak-proof lid", "A secure leak-proof lid keeps your milk safely inside and your bag dry, so you can pack it with everything else without a second thought."),
  ],
}
KPF_CSS = """
  /* ===== Key Product Features ===== */
  .kpf{ max-width:1240px; margin:64px auto 110px; padding:0 24px; }
  .kpf-title{ text-align:center; font-size:32px; font-weight:800; margin:0 0 28px; letter-spacing:-0.01em; }
  .kpf-group + .kpf-group{ margin-top:44px; }
  .kpf-label{ font-size:22px; font-weight:800; margin:0 0 16px; padding-bottom:10px; border-bottom:2px solid var(--pastel-pink); }
  .kpf-grid{ display:grid; grid-template-columns:repeat(3,1fr); gap:28px; }
  .kpf-img{ aspect-ratio:4/3; border-radius:14px; overflow:hidden; background:linear-gradient(135deg, var(--pastel-pink-soft), var(--pastel-blue-soft)); }
  .kpf-img img{ width:100%; height:100%; object-fit:cover; object-position:center 38%; display:block; }
  .kpf-card h3{ font-size:22px; line-height:1.2; font-weight:800; margin:14px 0 8px; }
  .kpf-card p{ font-size:16px; line-height:1.55; margin:0; color:#2a2a2a; }
  @media (max-width:749px){
    .kpf{ margin:44px auto 100px; padding:0 16px; }
    .kpf-title{ font-size:26px; margin-bottom:20px; }
    .kpf-grid{ display:flex; gap:14px; overflow-x:auto; scroll-snap-type:x mandatory; scroll-padding-left:16px; scrollbar-width:none; margin:0 -16px; padding:0 16px; }
    .kpf-grid::-webkit-scrollbar{ display:none; }
    .kpf-card{ flex:0 0 min(78%, 320px); scroll-snap-align:start; }
    .kpf-card h3{ font-size:19px; }
  }
"""

SET_IMGS = {"warmer": _thumb(_wi, 520), "cooler": _thumb(Image.open(root / "assets/cooler/main.jpg"), 520), "bundle": _thumb(Image.open(root / "assets/bundle/set-card.jpg"), 520)}
# ---------- Story sections: feature banner, how it works, choose your set ----------
STORY = {
  "warmer": {
    "banner": ("Feeding on the go, made easy.", "Whether you’re at the local park, on a long car journey or 30,000 feet up in the middle of a flight, it makes preparing a bottle just as effortless as it is in your own kitchen."),
    "steps": [("Fill", "Add your milk or water to the warmer."), ("Warm", "Press the button and let it heat. A quiet beep lets you know your milk or water has reached the temperature you chose."), ("Feed", "Check the temperature and feed your baby, wherever you are.")],
  },
  "cooler": {
    "banner": ("Made for pumping mums.", "Take your milk to work without the worry. It stays properly cold all day, so there’s no need to trust a shared office fridge, and its discreet design looks just like an everyday water bottle."),
    "steps": [("Freeze", "Pop the two cooling cylinders in the freezer for 12 hours, so they’re ready whenever you need them."), ("Load", "Slide the frozen cylinders into the cooler, ready to keep everything inside cold."), ("Chill", "Add your bottles and close the leak-proof lid. Your milk stays cold for up to 24 hours, wherever the day takes you.")],
  },
  "bundle": {
    "banner": ("Everything you need for feeding on the move.", "Warm milk or water with the portable warmer, then keep bottles fresh and cool with the matching portable cooler. Both are small enough for the nappy bag, car cup holder or carry-on."),
    "steps": [("Cool it", "Freeze the cooling cylinders for 12 hours, pop them in the cooler, and your milk stays cold for up to 24 hours."), ("Carry it", "Both are small enough for the nappy bag, car cup holder or carry-on."), ("Warm it", "When your baby is hungry, the warmer heats a bottle wherever you are.")],
  },
}
SETS = [
  ("warmer", "Portable Warmer", ["Warms milk and water", "Heats fast", "Long battery life"], "bottle-warmer-pdp.html", "£89.99", "£104.99"),
  ("cooler", "Portable Cooler", ["Iceless 360° cooling", "Cold for up to 24 hours", "650ml, fits two 300ml bottles"], "breast-milk-cooler-pdp.html", "£79.99", "£94.99"),
  ("bundle", "Warmer & Cooler Set", ["Portable warmer + portable cooler", "Save 21% vs buying separately", "Free shipping"], "bottle-warmer-bundle-pdp.html", "£134.99", "£169.98"),
]
STORY_CSS = """
  .kpf-band{ max-width:1240px; margin:0 auto 64px; padding:0 24px; }
  .kpf-band-in{ display:grid; grid-template-columns:1fr 1fr; align-items:center; background:var(--pastel-pink-soft); border-radius:20px; overflow:hidden; }
  .kpf-band-img{ aspect-ratio:4/3; background:linear-gradient(135deg, var(--pastel-pink), var(--pastel-blue)); }
  .kpf-band-img img{ width:100%; height:100%; object-fit:cover; display:block; }
  .kpf-band-txt{ padding:40px 48px; }
  .kpf-band-txt h2{ font-size:36px; line-height:1.1; font-weight:800; margin:0 0 14px; letter-spacing:-0.01em; }
  .kpf-band-txt p{ font-size:17px; line-height:1.6; margin:0; color:#2a2a2a; }
  .kpf-steps{ max-width:1240px; margin:0 auto 64px; padding:0 24px; }
  .kpf-num{ display:inline-flex; align-items:center; justify-content:center; width:28px; height:28px; border-radius:50%; background:#1c1c1c; color:#fff; font-size:14px; font-weight:700; margin-right:10px; vertical-align:2px; }
  .kpf-sets{ max-width:1240px; margin:0 auto 110px; padding:0 24px; }
  .kpf-set{ position:relative; border:1px solid var(--line); border-radius:18px; padding:18px; display:flex; flex-direction:column; background:#fff; }
  .kpf-set.best{ border:2px solid #1c1c1c; }
  .kpf-ribbon{ position:absolute; top:-12px; left:18px; background:#1c1c1c; color:#fff; font-size:12px; font-weight:800; letter-spacing:.04em; padding:5px 12px; border-radius:99px; }
  .kpf-set-img{ aspect-ratio:1/1; border-radius:12px; background:linear-gradient(135deg, var(--pastel-pink-soft), var(--pastel-blue-soft)); overflow:hidden; }
  .kpf-set-img img{ width:100%; height:100%; object-fit:cover; display:block; }
  .kpf-set h3{ font-size:21px; font-weight:800; margin:16px 0 10px; line-height:1.2; }
  .kpf-set ul{ margin:0 0 16px; padding:0; list-style:none; flex:1; }
  .kpf-set li{ font-size:15px; line-height:1.4; padding:5px 0 5px 24px; position:relative; }
  .kpf-set li::before{ content:"\\2713"; position:absolute; left:0; color:var(--accent); font-weight:800; }
  .kpf-set .kpf-price{ font-size:20px; font-weight:800; margin-bottom:12px; }
  .kpf-set .kpf-price s{ font-weight:500; font-size:15px; color:var(--muted); margin-right:6px; }
  .kpf-btn{ display:block; text-align:center; text-decoration:none; font-weight:700; font-size:15px; padding:13px 16px; border-radius:99px; border:2px solid #1c1c1c; color:#1c1c1c; background:#fff; }
  .kpf-set.best .kpf-btn{ background:#1c1c1c; color:#fff; }
  .kpf-here{ text-align:center; font-weight:700; font-size:15px; padding:15px 16px; border-radius:99px; background:#f3f1ef; color:#555; }
  @media (max-width:749px){
    .kpf-band{ margin-bottom:44px; padding:0 16px; }
    .kpf-band-in{ grid-template-columns:1fr; }
    .kpf-band-txt{ padding:26px 22px 30px; }
    .kpf-band-txt h2{ font-size:26px; }
    .kpf-steps{ margin-bottom:44px; padding:0 16px; }
    .kpf-sets{ padding:0 16px; margin-bottom:100px; }
    .kpf-sets .kpf-grid{ padding-top:14px; }
  }
"""
def story_html(page):
    st = STORY[page]
    h = '<!--STORY-->\n'
    _bp = ' style="object-position:center 68%"' if page == "bundle" else ''
    _bi = f'<img src="{_img_uri(BANNER_IMGS[page])}" alt="{st["banner"][0]}" loading="lazy"{_bp}>' if page in BANNER_IMGS else ''
    h += f'  <section class="kpf-band"><div class="kpf-band-in"><div class="kpf-band-img">{_bi}</div><div class="kpf-band-txt"><h2>{st["banner"][0]}</h2><p>{st["banner"][1]}</p></div></div></section>\n'
    h += '  <section class="kpf-steps"><h2 class="kpf-title">How it works</h2><div class="kpf-grid">\n'
    for i, (t, x) in enumerate(st["steps"], 1):
        _sp = ' style="object-position:center 10%"' if (i == 1 or page == "cooler") else (' style="object-position:center 18%"' if (page == "bundle" and i == 3) else '')
        _si = f'<img src="{_img_uri(STEP_IMGS[page][i-1])}" alt="{t}" loading="lazy"{_sp}>' if (page in STEP_IMGS and STEP_IMGS[page][i-1]) else ''
        h += f'    <div class="kpf-card"><div class="kpf-img">{_si}</div><h3><span class="kpf-num">{i}</span>{t}</h3><p>{x}</p></div>\n'
    h += '  </div></section>\n'
    h += '  <section class="kpf-sets"><h2 class="kpf-title">Choose your set</h2><div class="kpf-grid">\n'
    for key, name, bl, href, now, was in SETS:
        best = ' best' if key == 'bundle' else ''
        h += f'    <div class="kpf-set kpf-card{best}">' + ('<span class="kpf-ribbon">BEST VALUE</span>' if key == 'bundle' else '')
        img = SET_IMGS.get(key)
        h += '<div class="kpf-set-img">' + (f'<img src="{img}" alt="{name}">' if img else '') + '</div>'
        h += f'<h3>{name}</h3><ul>' + ''.join(f'<li>{x}</li>' for x in bl) + '</ul>'
        h += f'<div class="kpf-price"><s>{was}</s>{now}</div>'
        h += ('<div class="kpf-here">You’re viewing this</div>' if key == page else f'<a class="kpf-btn" href="{href}">View {name.lower()}</a>')
        h += '</div>\n'
    h += '  </div></section>\n<!--/STORY-->'
    return h

KPF_CSS = KPF_CSS.rstrip("\n") + "\n" + STORY_CSS

def _img_uri(path):
    import base64 as _b64
    return "data:image/jpeg;base64," + _b64.b64encode(open(path, "rb").read()).decode()
FEAT_IMGS = {"warmer": [root / "assets/warmer" / f"feature-{i}.jpg" for i in (1, 2, 3)],
             "cooler": [root / "assets/cooler" / f"feature-{i}.jpg" for i in (1, 2, 3)]}
STEP_IMGS = {"warmer": [root / "assets/warmer" / f"step-{i}.jpg" for i in (1, 2, 3)],
             "cooler": [root / "assets/cooler" / f"step-{i}.jpg" for i in (1, 2, 3)],
             "bundle": [root / "assets/bundle/step-1.jpg", root / "assets/bundle/step-2.jpg", root / "assets/bundle/step-3.jpg"]}
BANNER_IMGS = {"warmer": root / "assets/warmer/banner.jpg", "cooler": root / "assets/cooler/banner.jpg", "bundle": root / "assets/bundle/banner.jpg"}
def kpf_html(groups):
    out = '<!--KPF--><section class="kpf" id="keyFeatures">\n  <h2 class="kpf-title">Key Product Features</h2>\n'
    for grp in groups:
        label, items = grp[0], grp[1]
        imgkey = grp[2] if len(grp) > 2 else None
        out += '  <div class="kpf-group">\n'
        if label: out += f'    <h3 class="kpf-label">{label}</h3>\n'
        out += '    <div class="kpf-grid">\n'
        for n, (t, x) in enumerate(items):
            im = ''
            if imgkey in FEAT_IMGS and n < len(FEAT_IMGS[imgkey]):
                _fp = ' style="object-position:center 6%"' if (imgkey == "cooler" and n == 0) else ''
                im = f'<img src="{_img_uri(FEAT_IMGS[imgkey][n])}" alt="{t}" loading="lazy"{_fp}>'
            out += f'      <div class="kpf-card"><div class="kpf-img">{im}</div><h3>{t}</h3><p>{x}</p></div>\n'
        out += '    </div>\n  </div>\n'
    return out + '</section><!--/KPF-->'
def put_kpf(html, groups):
    new = kpf_html(groups)
    if '<!--KPF-->' in html:
        return re.sub(r'<!--KPF-->.*?<!--/KPF-->', lambda m: new, html, flags=re.S)
    return html.replace('  </main>\n', '  </main>\n\n  ' + new + '\n', 1)
def put_story(html, page):
    new = story_html(page)
    if '<!--STORY-->' in html:
        return re.sub(r'<!--STORY-->.*?<!--/STORY-->', lambda m: new, html, flags=re.S)
    return html.replace('<!--/KPF-->', '<!--/KPF-->\n  ' + new, 1)
def put_kpf_css(html):
    if '/* ===== Key Product Features ===== */' in html:
        return re.sub(r'\n  /\* ===== Key Product Features ===== \*/.*?(?=\n  /\* =====|\n</style>)', lambda m: KPF_CSS.rstrip('\n'), html, count=1, flags=re.S)
    return html.replace('  /* ===== Review lightbox ===== */', KPF_CSS.lstrip('\n') + '\n  /* ===== Review lightbox ===== */', 1)
src = put_kpf_css(put_story(put_kpf(src, [(None, FEATURES["warmer"], "warmer")]), "warmer"))
(d / "bottle-warmer-pdp.html").write_text(src)

# review slider arrows + script (everything after the row, up to and including its script) from the warmer source
RS_TAIL = src[src.index('      <button type="button" class="rs-btn rs-prev"'): src.index('</script>', src.index('rs-prev')) + len('</script>')]

# ---------- bundle page ----------
s = src
assert s.count("var PAGE = 'single';") == 1
s = s.replace("var PAGE = 'single';", "var PAGE = 'bundle';")
s = s.replace("<title>Superfast Portable Bottle Warmer for Travel</title>", "<title>Portable Bottle Warmer &amp; Cooler Set</title>")
# bundle: its own review placeholders (not the warmer's photos) + a "Just the cooler" link card
import base64, io
def _rvb(n):
    im = Image.open(root / "assets/bundle" / f"review-{n}.jpg"); buf = io.BytesIO(); im.save(buf, "JPEG", quality=82)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
_ph = ''
for _n in range(1, 4):
    _u = _rvb(_n)
    _ph += f'        <button type="button" class="video-card review-card" data-idx="{_n-1}" aria-label="Open customer review {_n}"><img src="{_u}" data-full="{_u}" alt="Customer review {_n}" loading="lazy"></button>\n'
_a = s.index('<div class="video-row" id="reviewRow">'); _b = s.index('      <div class="discount-box">', _a)
s = s[:_a - len('<div class="review-slider">\n      ')] + '<div class="review-slider">\n      <div class="video-row" id="reviewRow">\n' + _ph + '      </div>\n' + RS_TAIL + '\n\n' + s[_b:]
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
# bundle page only: bundle card first, solo items compact (name + "Just the...")
assert s.count('<div class="option-grid" role="radiogroup"') == 1
s = s.replace('<div class="option-grid" role="radiogroup"', '<div class="option-grid bundle-page" role="radiogroup"')
_bcss = ('  .bundle-page #optBundle{ order:-1; }\n'
  '  .bundle-page #optSingle, .bundle-page #optCooler{ padding:14px 16px; }\n'
  '  .bundle-page #optSingle .opt-list, .bundle-page #optSingle .opt-hint, .bundle-page #optCooler .opt-list{ display:none; }\n'
  '  .bundle-page #optSingle .opt-price, .bundle-page #optCooler .opt-price{ font-size:20px; margin:4px 0 0 28px; line-height:1.2; }\n'
  '  .bundle-page #optSingle .opt-head, .bundle-page #optCooler .opt-head{ margin-bottom:0; }\n'
  '  .bundle-page #optSingle .opt-sub, .bundle-page #optCooler .opt-sub{ margin:2px 0 0 28px; }\n'
  '  /* ===== Review lightbox ===== */')
assert s.count('  /* ===== Review lightbox ===== */') == 1
s = s.replace('  /* ===== Review lightbox ===== */', _bcss)
_u = "var PAGE_URLS = { single:'bottle-warmer-pdp.html', bundle:'bottle-warmer-bundle-pdp.html' };"
assert s.count(_u) == 1
s = s.replace(_u, "var PAGE_URLS = { single:'bottle-warmer-pdp.html', cooler:'breast-milk-cooler-pdp.html', bundle:'bottle-warmer-bundle-pdp.html' };")
s = re.sub(r'      <div class="discount-box">.*?</div>\n\n?', '', s, count=1, flags=re.S)
s = put_story(put_kpf(s, [("Warmer", FEATURES["warmer"], "warmer"), ("Cooler", FEATURES["cooler"], "cooler")]), "bundle")
def _guri(path, w, q=86):
    _im = Image.open(path).convert("RGB"); _im.thumbnail((w, w), Image.LANCZOS)
    _b = io.BytesIO(); _im.save(_b, "JPEG", quality=q, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(_b.getvalue()).decode()
_GAL = [("Bundle", "Warmer and cooler together"), ("Compare", "Cooler and warmer compared"), ("Out and about", "Warmer and cooler on a picnic"), ("Warmer features", "Portable warmer features"), ("Cooler features", "Portable cooler features")]
_gt = '<div class="thumb-strip" id="thumbsBundle" style="display:none">\n'
for _i, (_lab, _alt) in enumerate(_GAL, 1):
    _p = root / "assets/bundle" / f"gallery-{_i}.jpg"
    _gt += f'        <div class="thumb{" active" if _i == 1 else " has-img"}" data-label="{_lab}" data-alt="{_alt}" data-full="{_guri(_p, 1100)}" style="background-image:url(\'{_guri(_p, 240, 80)}\');background-size:cover;background-position:center;color:transparent;"></div>\n'
_gt += '      </div>\n      '
_a = s.index('<div class="thumb-strip" id="thumbsBundle"'); _b = s.index('<div class="main-image-wrap" id="mainImage">', _a)
s = s[:_a] + _gt + s[_b:]
s = re.sub(r'(<div class="sticky-thumb" style="background-image:url\(\')[^\']+(\')', lambda m: m.group(1) + _guri(root / "assets/bundle/gallery-1.jpg", 240, 80) + m.group(2), s, count=1)
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
c = rep(c, 'Add the cooler &amp; save 21% ↓', 'Add the warmer &amp; save 21% ↓')
# prices
c = rep(c, '<div class="price-old" id="priceOld">£104.99</div>', '<div class="price-old" id="priceOld">£94.99</div>')
c = rep(c, '<div class="price" id="priceNow">£89.99</div>', '<div class="price" id="priceNow">£79.99</div>')
c = rep(c, '<div class="off-pill" id="priceOff">14% OFF</div>', '<div class="off-pill" id="priceOff">16% OFF</div>')
c = rep(c, "single: { name:'Superfast Portable Bottle Warmer for Travel', old:'£104.99', now:'£89.99',  off:'14% OFF' },",
           "single: { name:'Portable Breast Milk Cooler for Travel', old:'£94.99', now:'£79.99',  off:'16% OFF' },")
# reviews -> placeholders (fill in later)
import base64, io
def _rv(n):
    im = Image.open(root / "assets/cooler" / f"review-{n}.jpg"); buf = io.BytesIO(); im.save(buf, "JPEG", quality=82)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
ph = ''
for _n in range(1, 6):
    _u = _rv(_n)
    ph += f'        <button type="button" class="video-card review-card" data-idx="{_n-1}" aria-label="Open customer review {_n}"><img src="{_u}" data-full="{_u}" alt="Customer review {_n}" loading="lazy"></button>\n'
c = region(c, '<div class="review-slider">', '      <div class="discount-box">', '<div class="review-slider">\n      <div class="video-row" id="reviewRow">\n' + ph + '      </div>\n' + RS_TAIL + '\n\n')
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
c = region(c, '<div class="pair-title">Pair well with:</div>', '<div class="share-row" id="shareRow">', pair)
# sticky bar
c = rep(c, '<div class="name" id="stickyName">Superfast Portable Bottle Warmer for Travel</div>', '<div class="name" id="stickyName">Portable Breast Milk Cooler for Travel</div>')
c = rep(c, '<div class="price" id="stickyPrice">£89.99 GBP</div>', '<div class="price" id="stickyPrice">£79.99 GBP</div>')
c = rep(c, '<option value="single">Portable Warmer · £89.99</option>', '<option value="single">Portable Cooler · £79.99</option>')
c = rep(c, '<button class="btn btn-cart" id="stickyAddToCart">Add to Cart - £89.99</button>', '<button class="btn btn-cart" id="stickyAddToCart">Add to Cart - £79.99</button>')
c = re.sub(r'(<div class="sticky-thumb" style="background-image:url\(\')[^\']+(\')', lambda m: m.group(1) + m_thumb + m.group(2), c, count=1)
c = put_story(put_kpf(c, [(None, FEATURES["cooler"], "cooler")]), "cooler")
(d / "breast-milk-cooler-pdp.html").write_text(c)
print("built breast-milk-cooler-pdp.html")

# ---------- sticky bar: the dropdown picks which product the bar adds (no page change) ----------
def _sticky_block():
    _c = (root / 'shopify-theme/assets/casa-product.css').read_text()
    _css = _c[_c.index('/*SDD-START*/'):_c.index('/*SDD-END*/')]
    _js = (root / 'shopify-theme/assets/casa-sticky-dd.js').read_text()
    _imgs = {
        "warmer": _thumb(_wi, 160),
        "cooler": _thumb(Image.open(root / "assets/cooler/main.jpg"), 160),
        "bundle": _thumb(Image.open(root / "assets/bundle/gallery-1.jpg"), 160),
    }
    return ('<!--STICKY_OPT-->\n<script>\n(function(){\n'
      '  var D = {\n'
      f'    warmer:{{ label:"Portable Warmer", price:"£89.99", url:"bottle-warmer-pdp.html" }},\n'
      f'    cooler:{{ label:"Portable Cooler", price:"£79.99", url:"breast-milk-cooler-pdp.html" }},\n'
      f'    bundle:{{ label:"Bundle And Save (Save 21%)", price:"£134.99", url:"bottle-warmer-bundle-pdp.html" }}\n'
      '  };\n'
      '  var t = (document.getElementById("pdpTitle") || {}).textContent || "";\n'
      '  var cur = /Set|Bundle/i.test(t) ? "bundle" : (/Cooler/i.test(t) ? "cooler" : "warmer");\n'
      '  var old = document.getElementById("stickyOptSelect"); if (!old) return;\n'
      '  var sel = old.cloneNode(false);\n'
      '  sel.innerHTML = ["warmer","cooler","bundle"].map(function(k){ return \'<option value="\'+k+\'">\'+D[k].label+" · "+D[k].price+"</option>"; }).join("");\n'
      '  old.parentNode.replaceChild(sel, old); sel.value = cur;\n'
      '  var embed = /[?&]embed=1/.test(location.search), frames = {};\n'
      '  if (!embed) window.addEventListener("load", function(){ setTimeout(function(){\n'
      '    ["warmer","cooler","bundle"].forEach(function(k){ if (k===cur) return;\n'
      '      var f = document.createElement("iframe"); f.src = D[k].url + "?embed=1"; f.setAttribute("aria-hidden","true"); f.tabIndex = -1; f.dataset.k = k;\n'
      '      f.style.cssText = "position:fixed;inset:0;width:100%;height:100%;border:0;background:#fff;z-index:9999;visibility:hidden;pointer-events:none";\n'
      '      document.body.appendChild(f); frames[k] = f; });\n'
      '  }, 300); });\n'
      '  window.__pdpShow = function(k, y){\n'
      '    var de = document.documentElement;\n'
      '    Object.keys(frames).forEach(function(n){ var on = n === k; frames[n].style.visibility = on ? "visible" : "hidden"; frames[n].style.pointerEvents = on ? "auto" : "none"; frames[n].tabIndex = on ? 0 : -1; });\n'
      '    if (k === cur) { de.style.overflow = ""; window.scrollTo(0, y); }\n'
      '    else { de.style.overflow = "hidden"; frames[k].contentWindow.scrollTo(0, y); }\n'
      '  };\n'
      '  sel.addEventListener("change", function(){\n'
      '    var k = sel.value, y = window.scrollY;\n'
      '    try { if (embed) { parent.__pdpShow(k, y); sel.value = cur; return; } if (frames[k] && frames[k].contentWindow) { window.__pdpShow(k, y); sel.value = cur; return; } } catch(e){}\n'
      '    window.location.href = D[k].url;\n'
      '  });\n'
      '})();\n</script>\n<style>' + _css + '</style>\n<script>' + _js + '</script>\n<!--/STICKY_OPT-->')

# ---- real Shopify prices (warmer 79.99, cooler 69.99, bundle 119.99 was 149.98 = 20% / save 29.99); single products have no compare-at price ----
def _reprice(t, fname):
    for a, z in (("£89.99", "@@W@@"), ("£79.99", "@@C@@"), ("£134.99", "@@B@@"), ("£169.98", "@@S@@")):
        t = t.replace(a, z)
    t = t.replace("<s>£104.99</s>", "").replace("<s>£94.99</s>", "")
    t = t.replace("£104.99", "").replace("£94.99", "").replace("14% OFF", "").replace("16% OFF", "")
    t = t.replace("21% OFF", "20% OFF").replace("21%", "20%")
    t = t.replace("£34.99", "£29.99").replace("£71.47", "£64.00").replace("£63.52", "£55.99")
    t = t.replace("£45.00", "£40.00").replace("£55.00", "£50.00")
    for a, z in (("@@W@@", "£79.99"), ("@@C@@", "£69.99"), ("@@B@@", "£119.99"), ("@@S@@", "£149.98")):
        t = t.replace(a, z)
    if ".price-old:empty" not in t:
        t = t.replace("</style>", ".price-old:empty,.off-pill:empty{display:none}\n</style>", 1)
    return t
import html as _h, sys as _sys
_sys.path.insert(0, str(root))
from faq_data import FAQ as _FAQ, FAQ_TITLE as _FT
_FKEY = {"bottle-warmer-pdp.html": "warmer", "bottle-warmer-bundle-pdp.html": "bundle", "breast-milk-cooler-pdp.html": "cooler"}
def _faq_block(key):
    _c = (root / 'shopify-theme/assets/casa-product.css').read_text()
    _css = _c[_c.index('/*FAQ-START*/'):_c.index('/*FAQ-END*/')]
    _items = "".join('<details class="casa-faq__item"><summary>' + _h.escape(q) + '</summary><div class="casa-faq__a">' + _h.escape(a) + '</div></details>' for q, a in _FAQ[key])
    return '<!--FAQ--><style>' + _css + '</style><section class="casa-faq" id="faq"><div class="casa-faq__inner"><h2 class="casa-faq__title">' + _h.escape(_FT) + '</h2><div class="casa-faq__list">' + _items + '</div></div></section><!--/FAQ-->'
for _f in ("bottle-warmer-pdp.html", "bottle-warmer-bundle-pdp.html", "breast-milk-cooler-pdp.html"):
    _t = (d / _f).read_text()
    _fb = _faq_block(_FKEY[_f])
    if "<!--FAQ-->" in _t:
        _t = re.sub(r"<!--FAQ-->.*?<!--/FAQ-->", lambda m: _fb, _t, flags=re.S)
    else:
        _t = _t.replace("<!--/STORY-->", "<!--/STORY-->\n" + _fb, 1)
    _blk2 = _sticky_block()
    if "<!--STICKY_OPT-->" in _t:
        _t = re.sub(r"<!--STICKY_OPT-->.*?<!--/STICKY_OPT-->", lambda m: _blk2, _t, flags=re.S)
    else:
        _t = _t.replace("</body>", _blk2 + "\n</body>", 1)
    _t = _reprice(_t, _f)
    (d / _f).write_text(_t)
print("sticky bar options wired")
