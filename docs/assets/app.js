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

/* SVG figures remain links without JavaScript; with JS they open a zoomable dialog. */
(function(){
  var links=document.querySelectorAll('[data-figure-zoom]');if(!links.length||typeof HTMLDialogElement==='undefined')return;
  var dialog=document.createElement('dialog');dialog.className='figure-dialog';
  var toolbar=document.createElement('div');toolbar.className='figure-dialog-toolbar';
  var title=document.createElement('h2');title.id='figure-dialog-title';toolbar.appendChild(title);
  var close=document.createElement('button');close.type='button';close.textContent='關閉 ✕';close.setAttribute('aria-label','關閉放大圖解');toolbar.appendChild(close);
  var scroll=document.createElement('div');scroll.className='figure-dialog-scroll';scroll.tabIndex=0;scroll.setAttribute('aria-label','放大圖解，可左右捲動');
  var image=document.createElement('img');scroll.appendChild(image);
  var caption=document.createElement('p');caption.className='figure-dialog-caption';
  dialog.appendChild(toolbar);dialog.appendChild(scroll);dialog.appendChild(caption);dialog.setAttribute('aria-labelledby',title.id);document.body.appendChild(dialog);
  links.forEach(function(link){link.addEventListener('click',function(event){event.preventDefault();title.textContent=link.dataset.figureTitle;image.src=link.href;image.alt=link.querySelector('img').alt;caption.textContent=link.closest('figure').querySelector('figcaption').textContent;dialog.showModal();});});
  close.addEventListener('click',function(){dialog.close();});
  dialog.addEventListener('click',function(event){if(event.target===dialog)dialog.close();});
})();
