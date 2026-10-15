/* Sticky bar product picker: replaces the browser's plain <select> with a branded dropdown. The real <select> stays (hidden) and still drives navigation. */
function casaStickyDD() {
  var sel = document.getElementById('stickyOptSelect');
  if (!sel || sel.getAttribute('data-dd')) return;
  sel.setAttribute('data-dd', '1');
  var wrap = document.createElement('div'); wrap.className = 'sdd';
  var btn = document.createElement('button'); btn.type = 'button'; btn.className = 'sdd-btn';
  btn.setAttribute('aria-haspopup', 'listbox'); btn.setAttribute('aria-expanded', 'false');
  var menu = document.createElement('ul'); menu.className = 'sdd-menu'; menu.setAttribute('role', 'listbox');
  function parts(o) { var t = o.textContent.split(' · '); return { n: t[0], p: t[1] || '' }; }
  Array.prototype.forEach.call(sel.options, function (o, i) {
    var li = document.createElement('li'); li.setAttribute('role', 'option'); li.setAttribute('data-i', i);
    var x = parts(o); li.innerHTML = '<span class="sdd-n"></span><span class="sdd-p"></span>';
    li.firstChild.textContent = x.n; li.lastChild.textContent = x.p;
    menu.appendChild(li);
  });
  function paint() {
    var o = sel.options[sel.selectedIndex]; if (!o) return; var x = parts(o);
    btn.innerHTML = '<span class="sdd-t"><span class="sdd-n"></span><span class="sdd-p"></span></span><svg class="sdd-c" width="12" height="8" viewBox="0 0 12 8" aria-hidden="true"><path d="M1 7l5-5 5 5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
    btn.querySelector('.sdd-n').textContent = x.n; btn.querySelector('.sdd-p').textContent = x.p;
    Array.prototype.forEach.call(menu.children, function (li, i) { li.setAttribute('aria-selected', i === sel.selectedIndex ? 'true' : 'false'); });
  }
  function setOpen(v) { wrap.classList.toggle('is-open', v); btn.setAttribute('aria-expanded', v ? 'true' : 'false'); }
  btn.addEventListener('click', function (e) { e.stopPropagation(); setOpen(!wrap.classList.contains('is-open')); });
  menu.addEventListener('click', function (e) {
    var li = e.target.closest && e.target.closest('li'); if (!li) return;
    setOpen(false); var i = +li.getAttribute('data-i');
    if (i !== sel.selectedIndex) { sel.selectedIndex = i; paint(); sel.dispatchEvent(new Event('change', { bubbles: true })); }
  });
  if (!window.__sddGlobal) {
    window.__sddGlobal = true;
    var closeAll = function () { Array.prototype.forEach.call(document.querySelectorAll('.sdd.is-open'), function (w) { w.classList.remove('is-open'); var b = w.querySelector('.sdd-btn'); if (b) b.setAttribute('aria-expanded', 'false'); }); };
    document.addEventListener('click', closeAll);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeAll(); });
  }
  sel.parentNode.insertBefore(wrap, sel); wrap.appendChild(sel); wrap.appendChild(btn); wrap.appendChild(menu);
  paint();
}
window.casaStickyDD = casaStickyDD;
casaStickyDD();
