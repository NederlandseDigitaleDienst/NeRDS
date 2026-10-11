// Demo flow for creating a Kubernetes cluster: sign in, fill in the form,
// see the result. Nothing is created; every step is simulated.

document.addEventListener('DOMContentLoaded', () => {
  const sheet = document.getElementById('cluster-modal');
  const opener = document.getElementById('open-cluster-form');
  if (!sheet || !opener) return;

  const byId = (id) => document.getElementById(id);
  const form = byId('create-cluster-form');
  const steps = {
    auth: byId('auth-container'),
    form: byId('form-container'),
    progress: byId('spinner'),
    result: byId('result-container'),
  };
  const organization = byId('organization');
  const tier = byId('cluster-tier');
  const size = byId('cluster-size');
  const multiAz = byId('multi-az');
  const region = byId('cluster-region');
  const secondaryRegion = byId('cluster-region-secondary');
  const secondaryRegionField = byId('secondary-region-row');
  const name = byId('cluster-name');
  const errors = byId('cluster-errors');
  const status = byId('cluster-status');

  const ORGANIZATIONS = [
    { value: 'minbzk', text: 'Ministerie van Binnenlandse Zaken', oin: '00000001800866472000' },
    { value: 'cibg', text: 'CIBG', oin: '00000004003214345000' },
    { value: 'rijkswaterstaat', text: 'Rijkswaterstaat', oin: '00000001800459126000' },
  ];
  const SIZES = [
    { value: 'small', text: 'Klein (1-5 nodes)' },
    { value: 'medium', text: 'Middel (6-20 nodes)' },
    { value: 'large', text: 'Groot (21-50 nodes)' },
    { value: 'custom', text: 'Aangepast' },
  ];
  const TIER_NAMES = { free: 'Free-tier', basic: 'Basis (pay-as-you-go)', reserved: 'Gereserveerde capaciteit' };
  const COSTS = {
    free: { small: { monthly: 0, yearly: 0 } },
    basic: {
      small: { monthly: 59.99, yearly: 719.88 },
      medium: { monthly: 149.99, yearly: 1799.88 },
      large: { monthly: 399.99, yearly: 4799.88 },
      custom: { monthly: 249.99, yearly: 2999.88 },
    },
    reserved: {
      small: { monthly: 49.99, yearly: 599.88 },
      medium: { monthly: 129.99, yearly: 1559.88 },
      large: { monthly: 349.99, yearly: 4199.88 },
      custom: { monthly: 199.99, yearly: 2399.88 },
    },
  };
  const MULTI_AZ_MULTIPLIER = 1.5;

  function showStep(name) {
    Object.entries(steps).forEach(([key, element]) => { element.hidden = key !== name; });
  }

  function showProgress(text) {
    byId('spinner-indicator').setAttribute('text', text);
    showStep('progress');
  }

  function setOptions(select, options, placeholder) {
    select.replaceChildren();
    if (placeholder) {
      const first = new Option(placeholder, '', true, true);
      first.disabled = true;
      select.add(first);
    }
    options.forEach((option) => {
      const element = new Option(option.text, option.value);
      if (option.oin) element.dataset.oin = option.oin;
      select.add(element);
    });
  }

  function updateCosts() {
    const price = COSTS[tier.value]?.[size.value];
    const factor = multiAz.value === 'true' && tier.value !== 'free' ? MULTI_AZ_MULTIPLIER : 1;
    const euro = (amount) => `€${(amount * factor).toFixed(2).replace('.', ',')}`;
    const monthly = euro(price ? price.monthly : 0);
    const yearly = euro(price ? price.yearly : 0);
    byId('monthly-cost').setAttribute('text', monthly);
    byId('yearly-cost').setAttribute('text', yearly);
    // The amounts change far from the field that changed them.
    if (price) status.textContent = `Geschatte kosten: ${monthly} per maand, ${yearly} per jaar.`;
  }

  // Names every field that is still empty in one message. The browser moves
  // focus to the first of them; the message tells about the others.
  function validate() {
    const label = (field) => field.closest('nldd-form-field').getAttribute('label');
    const messages = [organization, tier, region, secondaryRegion, size]
      .filter((select) => select.required && !select.value)
      .map((select) => `${label(select)}: kies een waarde.`);
    name.invalid = !(name.value || '').trim();
    if (name.invalid) messages.splice(organization.value ? 0 : 1, 0, `${label(name)}: vul een naam in.`);
    errors.setAttribute('supporting-text', messages.join(' '));
    errors.hidden = messages.length === 0;
    return messages.length === 0;
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

  function updateRegions() {
    const multiRegion = multiAz.value === 'true';
    secondaryRegionField.hidden = !multiRegion;
    secondaryRegion.required = multiRegion;
    if (!multiRegion) secondaryRegion.value = '';
    Array.from(secondaryRegion.options).forEach((option) => {
      option.hidden = option.value !== '' && option.value === region.value;
      option.disabled = option.value === '' || option.hidden;
    });
    if (secondaryRegion.value && secondaryRegion.value === region.value) secondaryRegion.value = '';
    updateCosts();
  }

  // The free tier has one size and no high availability.
  function updateTier() {
    const free = tier.value === 'free';
    const previousSize = size.value;
    if (free) {
      setOptions(size, [{ value: 'small', text: 'Klein (1 node, beperkte resources)' }]);
      multiAz.value = 'false';
    } else {
      setOptions(size, SIZES, 'Selecteer een grootte');
      if (SIZES.some((option) => option.value === previousSize)) size.value = previousSize;
    }
    multiAz.closest('nldd-dropdown').disabled = free;
    byId('cluster-size-field').toggleAttribute('supporting-label', false);
    byId('multi-az-field').toggleAttribute('supporting-label', false);
    if (free) {
      byId('cluster-size-field').setAttribute('supporting-label', 'Beperkt');
      byId('multi-az-field').setAttribute('supporting-label', 'Niet beschikbaar in free-tier');
    }
    updateRegions();
  }

  function reset() {
    form.querySelector('form').reset();
    name.value = '';
    name.invalid = false;
    errors.hidden = true;
    status.textContent = '';
    setOptions(organization, [], 'Selecteer een organisatie');
    updateTier();
    showStep('auth');
  }

  function simulateLogin(method) {
    showProgress(`Authenticeren met ${method}...`);
    setTimeout(() => {
      setOptions(
        organization,
        ORGANIZATIONS.map((item) => ({ ...item, text: `${item.text} (OIN: ${item.oin})` })),
        'Selecteer een organisatie',
      );
      showStep('form');
    }, 1500);
  }

  function showResult(values) {
    const chosen = organization.selectedOptions[0];
    const clusterId = 'k8s-' + Math.random().toString(36).substring(2, 10);
    const endpoint = `https://${clusterId}.${values.organization}.k8s.rijkscloud.nl`;
    const regions = values.multiRegion && values.secondaryRegion ? `${values.region} + ${values.secondaryRegion}` : values.region;
    const rows = {
      'result-cluster-name': values.name,
      'result-organization': chosen ? chosen.textContent.split(' (OIN:')[0] : 'Onbekend',
      'result-organization-oin': chosen?.dataset.oin || '-',
      'result-cluster-id': clusterId,
      'result-cluster-region': regions,
      'result-cluster-size': values.size,
      'result-cluster-tier': TIER_NAMES[values.tier] || 'Onbekend',
      'result-multi-az': values.multiRegion ? 'Ja' : 'Nee',
      'result-cluster-version': values.version,
      'result-creation-time': new Date().toLocaleString('nl-NL'),
      'result-cluster-endpoint': endpoint,
    };
    Object.entries(rows).forEach(([id, value]) => byId(id).setAttribute('text', value));
    byId('kubectl-instructions').textContent = [
      '# Configureer kubectl voor je nieuwe cluster',
      `kubectl config set-cluster rijkscloud --server=${endpoint}`,
      '',
      '# Download kubeconfig voor dit cluster en pas toe',
      `curl -o kubeconfig.yaml https://rijkscloud.nl/api/v1/clusters/${clusterId}/kubeconfig`,
      'export KUBECONFIG=./kubeconfig.yaml',
      '',
      '# Controleer connectiviteit',
      'kubectl get nodes',
    ].join('\n');
    showStep('result');
    // The button that was pressed is gone; without this, focus is nowhere.
    status.textContent = 'Cluster succesvol aangemaakt.';
    byId('cluster-created').focus();
  }

  opener.addEventListener('click', () => {
    reset();
    sheet.show();
  });
  sheet.addEventListener('open', () => { opener.expanded = true; });
  sheet.addEventListener('close', () => { opener.expanded = false; });

  byId('sso-login').addEventListener('click', () => simulateLogin('SSO Rijksoverheid'));
  byId('yubikey-login').addEventListener('click', () => simulateLogin('YubiKey'));
  byId('cert-login').addEventListener('click', () => simulateLogin('PKIoverheid Certificaat'));
  byId('back-to-auth').addEventListener('click', () => showStep('auth'));
  byId('reset-cluster-form').addEventListener('click', reset);

  // A dropdown stops the native change of its select and sends its own event
  // from the component, so the listeners sit on the dropdown.
  const onChange = (select, handler) => select.closest('nldd-dropdown').addEventListener('change', handler);
  onChange(tier, updateTier);
  onChange(size, updateCosts);
  onChange(multiAz, updateRegions);
  onChange(region, updateRegions);

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    if (!validate()) return;
    const data = new FormData(form.querySelector('form'));
    const values = {
      organization: data.get('organization'),
      name: name.value,
      region: data.get('cluster-region'),
      secondaryRegion: data.get('cluster-region-secondary'),
      size: data.get('cluster-size'),
      tier: data.get('cluster-tier'),
      version: data.get('cluster-version'),
      multiRegion: data.get('multi-az') === 'true',
    };
    showProgress('Kubernetes cluster wordt aangemaakt...');
    setTimeout(() => showResult(values), 3000);
  });

  updateTier();
});
