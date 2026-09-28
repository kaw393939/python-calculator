/* Progressive enhancement: reading and navigation work without JavaScript. */
(() => {
  const page = document.body.dataset.page;
  const storageKey = 'engineer-field-guide-reading-v1';
  const validPages = [...document.querySelectorAll('#book-nav a')].map(a => a.getAttribute('href').replace('.html', '')).filter(p => p !== 'home');
  let completed = [];
  let canSave = true;
  try {
    const saved = JSON.parse(localStorage.getItem(storageKey) || '[]');
    completed = Array.isArray(saved) ? [...new Set(saved.filter(p => validPages.includes(p)))] : [];
  } catch (_) { canSave = false; }
  const mark = document.querySelector('#mark-read');
  const status = document.querySelector('#completion-status');
  function renderProgress() {
    document.querySelector('.progress-area').hidden = false;
    document.querySelector('#book-progress').value = completed.length;
    document.querySelector('#progress-label').textContent = `${completed.length} of ${validPages.length} pages complete`;
    if (mark) {
      mark.hidden = false;
      mark.textContent = completed.includes(page) ? 'Page complete ✓ — mark unread' : 'Mark this page complete ✓';
      mark.setAttribute('aria-pressed', String(completed.includes(page)));
    }
    if (!canSave) status.textContent = 'Progress is available for this visit only; browser storage is unavailable.';
  }
  function saveProgress() {
    try { localStorage.setItem(storageKey, JSON.stringify(completed)); }
    catch (_) { canSave = false; }
    renderProgress();
  }
  mark?.addEventListener('click', () => {
    completed = completed.includes(page) ? completed.filter(p => p !== page) : [...completed, page];
    status.textContent = completed.includes(page) ? 'Nice work. Your next chapter is just below.' : 'This page is marked unread.';
    saveProgress();
  });
  document.querySelector('#reset-progress').addEventListener('click', () => {
    completed = []; saveProgress();
    status.textContent = canSave ? 'Your reading progress has been reset.' : 'Progress reset for this visit. Browser storage is unavailable.';
  });
  renderProgress();
  document.querySelector('#menu-toggle').addEventListener('click', event => {
    const isOpen = document.querySelector('.sidebar').classList.toggle('open');
    event.currentTarget.setAttribute('aria-expanded', String(isOpen));
  });
  document.querySelectorAll('.prose table').forEach(table => {
    const wrapper = document.createElement('div');
    wrapper.className = 'table-scroll'; wrapper.tabIndex = 0;
    wrapper.setAttribute('role', 'region'); wrapper.setAttribute('aria-label', 'Scrollable reference table');
    table.before(wrapper); wrapper.append(table);
  });
  document.querySelectorAll('pre > code').forEach(code => {
    const button = document.createElement('button');
    button.className = 'copy-code'; button.textContent = 'Copy';
    button.setAttribute('aria-label', 'Copy code to clipboard');
    button.addEventListener('click', async () => {
      try { await navigator.clipboard.writeText(code.textContent); button.textContent = 'Copied ✓'; }
      catch (_) { button.textContent = 'Select code to copy'; }
    });
    code.parentElement.prepend(button);
  });
  const dialog = document.querySelector('#search-dialog');
  const input = document.querySelector('#book-search');
  const results = document.querySelector('#search-results');
  let searchIndex;
  let loadError = false;
  function search() {
    results.replaceChildren();
    const query = input.value.trim().toLowerCase();
    if (!searchIndex) {
      const p = document.createElement('p');
      p.textContent = loadError ? 'Search is unavailable. Use the chapter menu to keep exploring.' : 'Loading the book index…';
      results.append(p); return;
    }
    const terms = query.split(/\s+/).filter(Boolean);
    const found = searchIndex.filter(item => terms.every(term => `${item.title} ${item.text}`.toLowerCase().includes(term)));
    const p = document.createElement('p');
    p.textContent = query ? (found.length ? `${found.length} matching pages` : 'No matching pages. Try a broader term, such as “testing” or “plugin”.') : 'Choose a chapter or search for a concept.';
    results.append(p);
    found.forEach(item => {
      const link = document.createElement('a'); link.href = item.url; link.textContent = item.title;
      if (query) {
        const small = document.createElement('small');
        const offset = Math.max(0, item.text.toLowerCase().indexOf(terms[0]) - 35);
        small.textContent = '…' + item.text.slice(offset, offset + 150).replace(/\s+/g, ' ') + '…';
        link.append(small);
      }
      results.append(link);
    });
  }
  if (typeof dialog.showModal === 'function') {
    document.querySelector('#search-open').hidden = false;
    document.querySelector('#search-open').addEventListener('click', async () => {
      dialog.showModal(); input.focus(); search();
      if (!searchIndex) {
        try {
          const response = await fetch('search.json');
          if (!response.ok) throw new Error('Index unavailable');
          searchIndex = await response.json(); loadError = false;
        } catch (_) { loadError = true; }
        search();
      }
    });
    document.querySelector('#search-close').addEventListener('click', () => dialog.close());
    input.addEventListener('input', search);
  }
})();
