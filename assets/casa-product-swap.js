/* Casa product pages: switching product from the sticky bar swaps the page content in place (no full page load).
   The other product pages are fetched quietly in the background, so a switch is a straight DOM swap. */
(function () {
  if (window.casaSwap) return;
  var cache = {}, token = 0;
  var main = function () { return document.getElementById('MainContent'); };
  var path = function (u) { try { return new URL(u, location.href).pathname; } catch (e) { return u; } };

  function load(url) {
    var k = path(url);
    if (!cache[k]) {
      cache[k] = fetch(k, { credentials: 'same-origin', headers: { Accept: 'text/html' } })
        .then(function (r) { if (!r.ok) throw new Error('http ' + r.status); return r.text(); })
        .catch(function (e) { delete cache[k]; throw e; });
    }
    return cache[k];
  }

  function copyHead(doc) {
    document.title = doc.title;
    ['link[rel="canonical"]', 'meta[name="description"]', 'meta[property="og:title"]', 'meta[property="og:url"]', 'meta[property="og:description"]', 'meta[property="og:image"]'].forEach(function (sel) {
      var a = document.head.querySelector(sel), b = doc.head.querySelector(sel);
      if (a && b) { var attr = a.tagName === 'LINK' ? 'href' : 'content'; a.setAttribute(attr, b.getAttribute(attr) || ''); }
    });
  }

  function track() {
    var r = document.querySelector('.casa-pdp'); if (!r) return;
    var id = r.getAttribute('data-product-id'), title = r.getAttribute('data-product-title') || document.title;
    var price = parseFloat(r.getAttribute('data-price') || '0'), cur = r.getAttribute('data-currency') || 'GBP';
    try { if (window.fbq) window.fbq('track', 'ViewContent', { content_ids: [id], content_type: 'product', content_name: title, value: price, currency: cur }); } catch (e) {}
    try { if (window.gtag) { window.gtag('event', 'page_view', { page_location: location.href, page_title: document.title }); window.gtag('event', 'view_item', { currency: cur, value: price, items: [{ item_id: id, item_name: title, price: price }] }); } } catch (e) {}
    try { if (window.dataLayer) window.dataLayer.push({ event: 'casa_product_view', product_id: id, product_title: title, value: price, currency: cur }); } catch (e) {}
  }

  function swap(url, push) {
    var my = ++token, y = window.scrollY;
    return load(url).then(function (html) {
      if (my !== token) return;
      var doc = new DOMParser().parseFromString(html, 'text/html');
      var next = doc.getElementById('MainContent'), cur = main();
      if (!next || !cur || !next.querySelector('.casa-pdp')) throw new Error('no content');
      cur.innerHTML = next.innerHTML;
      copyHead(doc);
      if (push !== false) history.pushState({ casaSwap: 1 }, '', path(url));
      if (window.casaProductInit) window.casaProductInit();
      if (window.casaStickyDD) window.casaStickyDD();
      window.scrollTo(0, y);
      track();
      warm();
    }).catch(function () { if (my === token) window.location.href = url; });
  }

  // fetch the sibling product pages shortly after load so the swap itself needs no network
  function warm() {
    var sel = document.getElementById('stickyOptSelect'); if (!sel) return;
    Array.prototype.forEach.call(sel.options, function (o) { if (o.value && path(o.value) !== location.pathname) load(o.value).catch(function () {}); });
  }
  var idle = window.requestIdleCallback || function (f) { setTimeout(f, 600); };
  idle(warm);
  document.addEventListener('pointerdown', function (e) { if (e.target.closest && e.target.closest('.sdd-btn')) warm(); }, true);

  try { history.replaceState({ casaSwap: 1 }, '', location.href); } catch (e) {}
  window.addEventListener('popstate', function (e) { if (e.state && e.state.casaSwap) swap(location.href, false); });
  window.casaSwap = function (url) { return swap(url, true); };
})();
