/* Casa de Mamá product page behaviour (gallery, quantity, accordion, sticky bar, review lightbox) */
(function () {
  var root = document.querySelector('.casa-pdp');
  if (!root) return;
  var $ = function (sel, ctx) { return (ctx || root).querySelector(sel); };
  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || root).querySelectorAll(sel)); };

  // ---- Quantity (main + sticky bar stay in sync, feeding the real form field) ----
  var qty = 1;
  var qtyInput = $('#casaQtyInput');
  function renderQty() {
    if (qtyInput) qtyInput.value = qty;
    $$('.js-qty-value').forEach(function (el) { el.textContent = qty; });
  }
  $$('.js-qty-minus').forEach(function (b) { b.addEventListener('click', function () { qty = Math.max(1, qty - 1); renderQty(); }); });
  $$('.js-qty-plus').forEach(function (b) { b.addEventListener('click', function () { qty++; renderQty(); }); });

  // ---- Variant select (only rendered when a product has more than one variant) ----
  var variantSelect = $('#casaVariantSelect');
  if (variantSelect) {
    variantSelect.addEventListener('change', function () {
      var opt = variantSelect.options[variantSelect.selectedIndex];
      var priceEl = $('#casaPriceNow'); if (priceEl && opt.dataset.price) priceEl.textContent = opt.dataset.price;
    });
  }

  // ---- Accordion ----
  $$('.accordion-head').forEach(function (head) {
    head.addEventListener('click', function () { head.parentElement.classList.toggle('open'); });
  });

  // ---- Gallery: thumbnails swap the main image, arrows step through them ----
  var mainImg = $('#mainImageImg');
  var thumbs = $$('.thumb-strip .thumb');
  function showThumb(t) {
    thumbs.forEach(function (x) { x.classList.toggle('active', x === t); });
    if (mainImg && t.dataset.full) { mainImg.src = t.dataset.full; if (t.dataset.alt) mainImg.alt = t.dataset.alt; }
  }
  thumbs.forEach(function (t) { t.addEventListener('click', function () { showThumb(t); }); });
  function step(dir) {
    if (!thumbs.length) return;
    var cur = thumbs.findIndex(function (t) { return t.classList.contains('active'); });
    var next = thumbs[(cur + dir + thumbs.length) % thumbs.length];
    showThumb(next);
    if (next.scrollIntoView) next.scrollIntoView({ block: 'nearest', inline: 'nearest' });
  }
  var prev = $('.gallery-arrow.prev'), next = $('.gallery-arrow.next');
  if (prev) prev.addEventListener('click', function () { step(-1); });
  if (next) next.addEventListener('click', function () { step(1); });
  var expand = $('.expand-btn');
  if (expand) expand.addEventListener('click', function () { if (mainImg && mainImg.src) window.open(mainImg.src, '_blank', 'noopener'); });
  if (thumbs.length < 2) { if (prev) prev.style.display = 'none'; if (next) next.style.display = 'none'; }

  // ---- Delivery date: one week from whenever the customer views the page ----
  var dd = $('#deliveryDate');
  if (dd) {
    var days = parseInt(dd.dataset.days || '7', 10);
    var d = new Date(); d.setDate(d.getDate() + days);
    var day = d.getDate();
    var suffix = (day % 100 >= 11 && day % 100 <= 13) ? 'th' : ({ 1: 'st', 2: 'nd', 3: 'rd' }[day % 10] || 'th');
    var weekday = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][d.getDay()];
    var month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][d.getMonth()];
    dd.textContent = weekday + ', ' + day + suffix + ' ' + month;
  }

  // ---- Copy discount code ----
  var copyBtn = $('#copyCodeBtn');
  if (copyBtn) copyBtn.addEventListener('click', function () {
    try { navigator.clipboard.writeText(copyBtn.dataset.code || ''); } catch (e) {}
    var o = copyBtn.textContent; copyBtn.textContent = 'Copied!';
    setTimeout(function () { copyBtn.textContent = o; }, 1500);
  });

  // ---- Sticky bar: visible whenever the main Add to Cart button is out of view ----
  var mainBtn = $('#casaMainAdd'), bar = $('#stickyBar');
  if (mainBtn && bar && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { bar.classList.toggle('visible', !e.isIntersecting); });
    }, { threshold: 0 }).observe(mainBtn);
  }
  var stickySelect = $('#stickyOptSelect');
  if (stickySelect) stickySelect.addEventListener('change', function () { if (stickySelect.value) window.location.href = stickySelect.value; });

  // ---- Review lightbox ----
  var cards = $$('#reviewRow .review-card');
  var lb = $('#reviewLb'), lbImg = $('#lbImg'), cur = 0;
  if (lb && cards.length) {
    var show = function (i) { cur = (i + cards.length) % cards.length; var t = cards[cur].querySelector('img'); lbImg.src = t.getAttribute('data-full'); lbImg.alt = t.alt; };
    var openLb = function (i) { show(i); lb.classList.add('open'); document.body.style.overflow = 'hidden'; };
    var closeLb = function () { lb.classList.remove('open'); document.body.style.overflow = ''; };
    cards.forEach(function (c, i) { c.addEventListener('click', function () { openLb(i); }); });
    $('#lbClose').addEventListener('click', closeLb);
    $('#lbPrev').addEventListener('click', function (e) { e.stopPropagation(); show(cur - 1); });
    $('#lbNext').addEventListener('click', function (e) { e.stopPropagation(); show(cur + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) closeLb(); });
    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('open')) return;
      if (e.key === 'Escape') closeLb();
      else if (e.key === 'ArrowLeft') show(cur - 1);
      else if (e.key === 'ArrowRight') show(cur + 1);
    });
    var sx = null;
    lb.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', function (e) { if (sx === null) return; var dx = e.changedTouches[0].clientX - sx; sx = null; if (Math.abs(dx) > 50) show(cur + (dx < 0 ? 1 : -1)); });
  }
})();
