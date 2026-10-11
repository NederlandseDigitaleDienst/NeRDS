// Feedback form in a sheet. Feedback leaves the site as an e-mail draft or
// as a prefilled GitHub issue; nothing is sent from the page itself.

const FEEDBACK_EMAIL = 'bureau.architectuur@minbzk.nl';
const FEEDBACK_REPOSITORY = 'https://github.com/NederlandseDigitaleDienst/NeRDS';
const FEEDBACK_TYPES = {
  bug_report: { label: 'Fout/Bug', prefix: '[Bug] ', template: 'bug-report.md' },
  feature_request: { label: 'Voorstel', prefix: '[Voorstel] ', template: 'feature-request.md' },
  general_feedback: { label: 'Algemene feedback', prefix: '[Feedback] ', template: 'general-feedback.md' },
  question: { label: 'Vraag', prefix: '[Vraag] ', template: 'question.md' },
};

document.addEventListener('DOMContentLoaded', () => {
  const sheet = document.getElementById('feedback-sheet');
  const opener = document.getElementById('feedback-open');
  const form = document.getElementById('feedback-form');
  if (!sheet || !opener || !form) return;

  const guideline = document.getElementById('feedback-guideline');
  const type = document.getElementById('feedback-type');
  const text = document.getElementById('feedback-text');
  const links = document.getElementById('feedback-related-docs-container');
  const success = document.getElementById('feedback-success');
  const errors = document.getElementById('feedback-errors');

  opener.addEventListener('click', () => {
    success.hidden = true;
    errors.hidden = true;
    selectCurrentGuideline();
    sheet.show();
  });
  sheet.addEventListener('open', () => { opener.expanded = true; });
  sheet.addEventListener('close', () => { opener.expanded = false; });

  // Preselect the guideline of the page you are on; any other page is about NeRDS in general.
  function selectCurrentGuideline() {
    const match = window.location.pathname.match(/\/richtlijnen\/([a-z-]+)\//);
    const option = match && guideline.querySelector(`option[data-slug="${match[1]}"]`);
    guideline.value = option ? option.value : '0';
  }

  document.getElementById('feedback-add-link').addEventListener('click', () => {
    // A copy of the first field, without what that field holds: its value and
    // a verdict on that value.
    const field = links.firstElementChild.cloneNode(true);
    const input = field.querySelector('nldd-text-field');
    input.value = '';
    input.invalid = false;
    field.querySelector('nldd-validation-list').removeAttribute('judging');
    field.querySelectorAll('nldd-validation-item').forEach((item) => item.removeAttribute('unmet'));
    links.append(field);
    input.focus();
  });

  function normalizeUrl(url) {
    return /^https?:\/\//i.test(url) ? url : 'https://' + url;
  }

  // The rule under the link field in feedback.html. The component checks the
  // raw value against it and blocks the form when it fails, so whatever it
  // rejects has to fail here too, or the form stays put without a message.
  const linkRule = new RegExp(links.querySelector('nldd-validation-item').getAttribute('match'), 'u');

  function isValidUrl(url) {
    if (!url.includes('.')) return false;
    try {
      return ['http:', 'https:'].includes(new URL(normalizeUrl(url)).protocol);
    } catch (error) {
      return false;
    }
  }

  // Marks what does not hold, names every failing field in one message and
  // moves focus to the first of them. Focus lands on one field only; the
  // message is what tells a screen reader user about the others.
  function validate() {
    const failing = [];
    const messages = [];
    const feedback = (text.value || '').trim();

    type.closest('nldd-dropdown').invalid = !type.value;
    if (!type.value) {
      failing.push(type);
      messages.push('Soort feedback: kies een soort.');
    }

    text.invalid = feedback.length < 10 || text.value.length > 5000;
    if (text.invalid) {
      failing.push(text);
      messages.push(`Uw feedback: ${feedback.length < 10 ? 'minimaal 10 tekens' : 'maximaal 5000 tekens'}.`);
    }

    links.querySelectorAll('nldd-text-field').forEach((field) => {
      const value = (field.value || '').trim();
      field.invalid = !linkRule.test(field.value || '') || (value !== '' && !isValidUrl(value));
      if (field.invalid) {
        failing.push(field);
        messages.push('Link naar een relevant document: vul een webadres in, bijvoorbeeld https://www.rijksoverheid.nl/onderwerpen.');
      }
    });

    errors.setAttribute('supporting-text', [...new Set(messages)].join(' '));
    errors.hidden = failing.length === 0;
    if (failing.length) failing[0].focus();
    return failing.length === 0;
  }

  // The browser rejects an empty required field before the submit event, so
  // the submit handler never runs. `invalid` does not bubble; capture it.
  let judging = false;
  form.addEventListener('invalid', () => {
    if (judging) return;
    judging = true;
    queueMicrotask(() => {
      validate();
      judging = false;
    });
  }, true);

  function collect() {
    const selected = guideline.selectedOptions[0];
    const number = guideline.value ? parseInt(guideline.value, 10) : null;
    return {
      type: type.value,
      text: text.value,
      relatedDocs: Array.from(links.querySelectorAll('nldd-text-field'))
        .map((field) => (field.value || '').trim())
        .filter(Boolean)
        .map(normalizeUrl)
        .join('\n'),
      guidelineNumber: number,
      guidelineName: number !== null && selected ? selected.textContent.trim() : null,
      pageTitle: document.querySelector('h1')?.textContent.trim() || document.title,
    };
  }

  function browserName() {
    const agent = navigator.userAgent;
    const browsers = [['Firefox', /Firefox\/([0-9.]+)/], ['Edge', /Edg\/([0-9.]+)/], ['Chrome', /Chrome\/([0-9.]+)/], ['Safari', /Version\/([0-9.]+)/]];
    for (const [name, pattern] of browsers) {
      const match = agent.match(pattern);
      if (match) return `${name} ${match[1]}`;
    }
    return 'Onbekend';
  }

  function systemName() {
    const agent = navigator.userAgent;
    if (agent.includes('Win')) return 'Windows';
    if (agent.includes('Android')) return 'Android';
    if (/iPhone|iPad|iOS/.test(agent)) return 'iOS';
    if (agent.includes('Mac')) return 'macOS';
    if (agent.includes('Linux')) return 'Linux';
    return 'Onbekend';
  }

  function finish(message) {
    form.querySelector('form').reset();
    text.value = '';
    while (links.children.length > 1) links.lastElementChild.remove();
    links.querySelector('nldd-text-field').value = '';
    errors.hidden = true;
    success.setAttribute('supporting-text', message);
    success.hidden = false;
  }

  // The component renders a real form in the light DOM; its submit event
  // bubbles to the component.
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    if (!validate()) return;

    const data = collect();
    const typeLabel = FEEDBACK_TYPES[data.type].label;
    const hasGuideline = data.guidelineNumber > 0;

    let subject = `[NeRDS Feedback] ${typeLabel}`;
    if (hasGuideline) subject += ` - Richtlijn ${data.guidelineNumber}`;

    let body = `Type: ${typeLabel}\n\n`;
    if (hasGuideline) body += `Richtlijn: ${data.guidelineName}\n`;
    body += `Pagina: ${data.pageTitle} (${window.location.pathname})\n\n`;
    body += `--- Feedback ---\n${data.text}\n\n`;
    if (data.relatedDocs) body += `--- Relevante documenten ---\n${data.relatedDocs}\n\n`;
    body += '--- Metadata ---\n';
    body += `Ingediend: ${new Date().toLocaleString('nl-NL')}\n`;
    body += `Browser: ${navigator.userAgent}\n`;

    window.location.href = `mailto:${FEEDBACK_EMAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    finish("Uw e-mailclient is geopend. Klik op 'Verzenden' in uw e-mail om de feedback te versturen.");
  });

  document.getElementById('feedback-github').addEventListener('click', () => {
    if (!validate()) return;

    const data = collect();
    let body = '**Over welke richtlijn gaat dit?**\n';
    if (data.guidelineName) body += `- [x] ${data.guidelineName}\n`;
    body += '\n';

    if (data.type === 'bug_report') {
      body += `**Beschrijf de fout**\n${data.text}\n\n**Verwacht gedrag**\n\n**Screenshots**\n\n`;
      body += `**Browser en versie**\n${navigator.userAgent}\n\n`;
    } else if (data.type === 'feature_request') {
      body += `**Beschrijf je suggestie**\n${data.text}\n\n**Waarom is dit een goede toevoeging?**\n\n`;
    } else if (data.type === 'question') {
      body += `**Beschrijf je vraag**\n${data.text}\n\n**Context**\n\n`;
    } else {
      body += `**Jouw feedback**\n${data.text}\n\n`;
    }
    if (data.relatedDocs && ['feature_request', 'general_feedback'].includes(data.type)) {
      body += `**Relevante documenten of links**\n${data.relatedDocs}\n\n`;
    }
    body += '---\n**Metadata**\n';
    body += `- **Pagina:** [${data.pageTitle}](${window.location.href})\n`;
    body += `- **Browser:** ${browserName()}\n`;
    body += `- **Systeem:** ${systemName()}\n`;
    body += `- **Ingediend:** ${new Date().toLocaleString('nl-NL')}\n`;

    const title = FEEDBACK_TYPES[data.type].prefix + data.text.substring(0, 60) + (data.text.length > 60 ? '...' : '');
    const parameters = new URLSearchParams({ template: FEEDBACK_TYPES[data.type].template, title, body });
    window.open(`${FEEDBACK_REPOSITORY}/issues/new?${parameters.toString()}`, '_blank', 'noopener');
    finish('GitHub is geopend in een nieuw tabblad. Dien het issue daar in.');
  });
});
