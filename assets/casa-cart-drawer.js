(function () {
  var SECTION = 'casa-cart-drawer';
  var root = (window.Shopify && Shopify.routes && Shopify.routes.root) || '/';
  var busy = false;
  var lastFocus = null;

  function el() { return document.getElementById('casaCartDrawer'); }

  function open() {
    var d = el(); if (!d) return;
    lastFocus = document.activeElement;
    d.classList.add('is-open');
    d.setAttribute('aria-hidden', 'false');
    document.body.classList.add('casa-cd-lock');
    var p = d.querySelector('.casa-cd__panel'); if (p) p.focus();
  }
  function close() {
    var d = el(); if (!d) return;
    d.classList.remove('is-open');
    d.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('casa-cd-lock');
    if (lastFocus && lastFocus.focus) { try { lastFocus.focus(); } catch (e) {} }
  }

  function setCount(n) {
    document.querySelectorAll('[data-casa-cart-count]').forEach(function (s) { s.textContent = n; });
  }

  function refresh() {
    return fetch(root + '?sections=' + SECTION, { headers: { Accept: 'application/json' } })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        var tmp = document.createElement('div');
        tmp.innerHTML = data[SECTION];
        var fresh = tmp.querySelector('#casaCartDrawer');
        var d = el();
        if (!fresh || !d) return;
        d.innerHTML = fresh.innerHTML;
        setCount(fresh.getAttribute('data-count'));
      });
  }

  function post(url, body) {
    return fetch(root + url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify(body)
    }).then(function (r) { if (!r.ok) throw new Error('cart ' + r.status); return r.json(); });
  }

  function work(fn) {
    if (busy) return Promise.resolve();
    busy = true;
    var d = el(); if (d) d.classList.add('is-busy');
    return fn().then(refresh).catch(function () {}).then(function () {
      busy = false;
      var d2 = el(); if (d2) d2.classList.remove('is-busy');
    });
  }

  document.addEventListener('click', function (e) {
    var t = e.target;
    if (!t.closest) return;
    var opener = t.closest('[data-casa-cart-open]');
    if (opener && el()) { e.preventDefault(); refresh().then(open, open); return; }
    if (t.closest('[data-casa-close]')) { close(); return; }
    var q = t.closest('[data-casa-qty]');
    if (q) { work(function () { return post('cart/change.js', { line: +q.getAttribute('data-casa-qty'), quantity: Math.max(0, +q.getAttribute('data-to')) }); }); return; }
    var rm = t.closest('[data-casa-remove]');
    if (rm) { work(function () { return post('cart/change.js', { line: +rm.getAttribute('data-casa-remove'), quantity: 0 }); }); return; }
    var add = t.closest('[data-casa-add]');
    if (add) { work(function () { return post('cart/add.js', { id: +add.getAttribute('data-casa-add'), quantity: 1 }); }); return; }
  });

  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });

  // Product forms: add via AJAX then slide the cart open. Falls back to a normal submit on any error.
  document.addEventListener('submit', function (e) {
    var form = e.target;
    if (!form || !form.getAttribute || !/\/cart\/add/.test(form.getAttribute('action') || '') || !el()) return;
    e.preventDefault();
    if (busy) return;
    busy = true;
    var btn = e.submitter || form.querySelector('[type=submit]');
    var label = btn ? btn.textContent : '';
    if (btn) { btn.disabled = true; btn.textContent = 'Adding…'; }
    fetch(root + 'cart/add.js', { method: 'POST', headers: { Accept: 'application/json' }, body: new FormData(form) })
      .then(function (r) { if (!r.ok) throw new Error('add ' + r.status); return r.json(); })
      .then(refresh)
      .then(function () { busy = false; open(); })
      .catch(function () { busy = false; HTMLFormElement.prototype.submit.call(form); })
      .then(function () { if (btn) { btn.disabled = false; btn.textContent = label; } });
  }, true);
})();
