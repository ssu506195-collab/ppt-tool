(() => {
  const key = 'ansys-lab-notes-read-v1';
  let read;
  try { read = new Set(JSON.parse(localStorage.getItem(key) || '[]')); } catch { read = new Set(); }
  const button = document.querySelector('.mark-read');
  function refresh() {
    document.querySelectorAll('[data-status]').forEach(el => { el.textContent = read.has(el.dataset.status) ? '已讀 ✓' : '開始閱讀 ↗'; });
    const count = document.querySelector('#reading-count');
    if (count) { const ids = [...document.querySelectorAll('[data-status]')].map(el => el.dataset.status); count.textContent = `${ids.filter(id => read.has(id)).length} / ${ids.length}`; }
    if (button) { const done = read.has(button.dataset.slug); button.textContent = done ? '已讀 ✓ · 點擊取消' : '標記為已讀'; button.setAttribute('aria-pressed', String(done)); }
  }
  button?.addEventListener('click', () => {
    read.has(button.dataset.slug) ? read.delete(button.dataset.slug) : read.add(button.dataset.slug);
    try { localStorage.setItem(key, JSON.stringify([...read])); } catch { /* Reading remains usable without storage. */ }
    refresh();
  });
  refresh();
  window.addEventListener('storage', event => {
    if (event.key === key) { try { read = new Set(JSON.parse(event.newValue || '[]')); refresh(); } catch {} }
  });
  document.querySelector('[data-print]')?.addEventListener('click', () => window.print());
  const menu = document.querySelector('.menu-button');
  function closeMenu() { document.body.classList.remove('menu-open'); menu?.setAttribute('aria-expanded', 'false'); }
  menu?.addEventListener('click', () => { const open = document.body.classList.toggle('menu-open'); menu.setAttribute('aria-expanded', String(open)); });
  document.querySelector('[data-close-menu]')?.addEventListener('click', closeMenu);
  document.querySelectorAll('.sidebar a').forEach(el => el.addEventListener('click', closeMenu));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') { closeMenu(); menu?.focus(); } });
  let filter = 'all';
  const input = document.querySelector('#article-search');
  const filters = document.querySelectorAll('[data-filter]');
  const cards = [...document.querySelectorAll('[data-search]')];
  function search() {
    const words = (input?.value || '').trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    let n = 0;
    cards.forEach(card => { const show = (filter === 'all' || card.dataset.kind === filter) && words.every(word => card.dataset.search.toLocaleLowerCase().includes(word)); card.hidden = !show; if (show) n++; });
    const status = document.querySelector('#search-status');
    if (status) status.textContent = `顯示 ${n} / ${cards.length} 篇筆記`;
    const empty = document.querySelector('.empty-state'); if (empty) empty.hidden = n !== 0;
  }
  filters.forEach(el => el.addEventListener('click', () => { filter = el.dataset.filter; filters.forEach(x => { const active = x === el; x.classList.toggle('active', active); x.setAttribute('aria-pressed', String(active)); }); search(); }));
  input?.addEventListener('input', search);
})();
