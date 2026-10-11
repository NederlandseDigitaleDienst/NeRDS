// Search in a sheet, on top of the index and the worker of the MkDocs search plugin.

document.addEventListener('DOMContentLoaded', () => {
  const sheet = document.getElementById('search-sheet');
  const opener = document.getElementById('search-open');
  const field = document.getElementById('search-query');
  const results = document.getElementById('search-results');
  if (!sheet || !opener || !field || !results) return;

  // Without a trailing slash: on the 404 page of a site at the domain root the
  // base is "/", and "//search/worker.js" would point at another host.
  const base_url = (document.documentElement.dataset.baseUrl || '.').replace(/\/+$/, '');
  const emptyState = results.querySelector('[slot="empty"]');
  const status = document.getElementById('search-status');
  let announcement = null;
  let worker = null;
  let ready = false;
  let pendingQuery = '';

  function startWorker() {
    if (worker) return;
    worker = new Worker(base_url + '/search/worker.js');
    worker.addEventListener('message', (event) => {
      if (event.data.allowSearch) {
        ready = true;
        if (pendingQuery) worker.postMessage({ query: pendingQuery });
      } else if (event.data.results) {
        render(event.data.results);
      }
    });
    worker.postMessage({ init: true });
  }

  function search(query) {
    pendingQuery = query.trim();
    if (!pendingQuery) {
      render(null);
      return;
    }
    if (ready) worker.postMessage({ query: pendingQuery });
  }

  // Focus stays in the field while the list changes, so the outcome goes to
  // a status region. After a pause: one message per query, not one per key.
  function announce(message) {
    clearTimeout(announcement);
    if (!status) return;
    announcement = setTimeout(() => { status.textContent = message; }, 600);
  }

  function render(found) {
    results.querySelectorAll('nldd-list-item').forEach((item) => item.remove());
    if (found === null) {
      emptyState.text = 'Typ om te zoeken';
      emptyState.supportingText = "Je zoekt in alle richtlijnen en pagina's.";
      announce('');
      return;
    }
    emptyState.text = 'Geen resultaten';
    emptyState.supportingText = 'Probeer een ander zoekwoord.';
    // A page and its first section share a title; one row is enough.
    const seen = new Set();
    const unique = found.filter((result) => {
      const key = result.location.split('#')[0] + '|' + result.title;
      return seen.has(key) ? false : seen.add(key);
    });
    const shown = unique.slice(0, 20);
    if (shown.length === 0) announce('Geen resultaten');
    else if (shown.length < unique.length) announce(`De eerste ${shown.length} van ${unique.length} resultaten`);
    else announce(shown.length === 1 ? '1 resultaat' : `${shown.length} resultaten`);
    shown.forEach((result) => {
      const item = document.createElement('nldd-list-item');
      item.setAttribute('href', base_url + '/' + result.location);
      const cell = document.createElement('nldd-text-cell');
      cell.setAttribute('text', result.title);
      cell.setAttribute('supporting-text', summarize(result.summary || result.text || ''));
      item.append(cell);
      results.append(item);
    });
  }

  function summarize(text) {
    const plain = text.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
    return plain.length > 140 ? plain.slice(0, 140) + '…' : plain;
  }

  // The sheet does not bubble its close event, so the listener sits on the sheet.
  opener.addEventListener('click', () => {
    startWorker();
    sheet.show();
  });
  sheet.addEventListener('open', () => {
    opener.expanded = true;
    field.focus();
  });
  sheet.addEventListener('close', () => { opener.expanded = false; });

  // The field has its own input in a shadow root and reports the value in the event detail.
  field.addEventListener('input', (event) => search(event.detail?.value ?? field.value ?? ''));
  field.addEventListener('search', (event) => search(event.detail?.value ?? field.value ?? ''));
});
