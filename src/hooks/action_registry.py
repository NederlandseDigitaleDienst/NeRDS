"""
MkDocs hook to dynamically generate action cards from central YAML registry.
Filters actions by richtlijn and fase, and injects NLDD markup into guideline pages.
"""

import os
import re
from html import escape

import yaml


def _validate_action_labels(actions):
    """
    Validate that actions have a 'fase' field and warn if missing.
    Only checks for richtlijnen that commonly use fase-based filtering.

    Args:
        actions: List of action dictionaries
    """
    # Richtlijnen that commonly use fase-based filtering
    fase_using_richtlijnen = ['gebruikersbehoeften', 'toegankelijkheid', 'open-source', 'cloud']

    for action in actions:
        action_id = action.get('id', 'unknown')
        richtlijn = action.get('richtlijn')

        # Only check actions from richtlijnen that use fase
        if richtlijn in fase_using_richtlijnen:
            if 'fase' not in action or not action.get('fase'):
                print(f"⚠️  WARNING: Action '{action_id}' in richtlijn '{richtlijn}' is missing a 'fase' field")


def on_page_content(html, page, config, files):
    """
    Process page content and inject dynamic action cards.
    Runs after page content is converted to HTML.
    """

    # Only process guideline pages (both index.md and fases.md)
    if not page.file.src_path.startswith('richtlijnen/'):
        return html

    # Load the action registry
    registry_path = os.path.join(config['docs_dir'], 'action-registry', 'actions.yaml')

    if not os.path.exists(registry_path):
        return html

    try:
        with open(registry_path, 'r', encoding='utf-8') as f:
            registry_data = yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading action registry: {e}")
        return html

    # Validate and warn about missing labels
    _validate_action_labels(registry_data.get('actions', []))

    if not registry_data or 'actions' not in registry_data:
        return html

    # A "Direct aan de slag" block is a div with a heading, an optional notice
    # and an empty action-cards placeholder that carries the filters:
    # <div class="action-cards" data-richtlijn="..." data-fase="..."></div>
    # Both data-richtlijn and data-fase are optional. The heading is an h3
    # under a page section and an h4 under a phase, so the block is part of
    # what it sits in; the card titles go one level below it.
    pattern = (
        r'<div class="direct-aan-de-slag">\s*<h(?P<level>[34])>(?P<heading>.*?)</h(?P=level)>(?P<notice>.*?)'
        r'<div class="action-cards"(?P<attributes>[^>]*)></div>\s*</div>'
    )

    def replace_block(match):
        """Replace each block with a box of cards, or drop it when it has no actions."""
        attributes = match.group('attributes')

        richtlijn_match = re.search(r'data-richtlijn="([^"]+)"', attributes)
        richtlijn_filter = richtlijn_match.group(1) if richtlijn_match else None

        fase_match = re.search(r'data-fase="([^"]+)"', attributes)
        fase_filter = fase_match.group(1) if fase_match else None

        filtered_actions = _filter_actions(
            registry_data['actions'],
            richtlijn_filter,
            fase_filter
        )

        if not filtered_actions:
            return ''

        level = int(match.group('level'))

        return f'''<nldd-box data-rich-text-width="main">
  <nldd-container padding="16" gap="16">
    <nldd-title size="4" heading-level="{level}" text="{escape(_plain_text(match.group('heading')))}"></nldd-title>
{_generate_notice_html(match.group('notice'))}    <nldd-collection layout="grid" item-width="240px" gap="12"{attributes}>
{_generate_action_cards_html(filtered_actions, level + 1)}
    </nldd-collection>
  </nldd-container>
</nldd-box>'''

    html = re.sub(pattern, replace_block, html, flags=re.DOTALL)

    # A placeholder on its own, outside a "Direct aan de slag" block, becomes
    # the cards without the box around them.
    def replace_placeholder(match):
        attributes = match.group('attributes')
        richtlijn_match = re.search(r'data-richtlijn="([^"]+)"', attributes)
        fase_match = re.search(r'data-fase="([^"]+)"', attributes)
        filtered_actions = _filter_actions(
            registry_data['actions'],
            richtlijn_match.group(1) if richtlijn_match else None,
            fase_match.group(1) if fase_match else None
        )
        if not filtered_actions:
            return ''
        return f'''<nldd-collection layout="grid" item-width="240px" gap="12"{attributes}>
{_generate_action_cards_html(filtered_actions)}
</nldd-collection>'''

    html = re.sub(r'<div class="action-cards"(?P<attributes>[^>]*)></div>', replace_placeholder, html)

    return html


def _plain_text(html):
    """Strip tags and collapse whitespace."""
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', html)).strip()


def _generate_notice_html(notice):
    """
    Turn the optional notice of a block into a banner.
    The notice reads `<strong>Label:</strong> explanation`.
    """
    match = re.search(r'<div class="warning-banner"[^>]*>(.*?)</div>', notice, flags=re.DOTALL)
    if not match:
        return ''

    label_match = re.search(r'<strong>(.*?)</strong>(.*)', match.group(1), flags=re.DOTALL)
    if label_match:
        text = _plain_text(label_match.group(1)).rstrip(':')
        supporting_text = _plain_text(label_match.group(2))
    else:
        text = _plain_text(match.group(1))
        supporting_text = ''

    return (
        f'    <nldd-banner variant="warning" size="sm" text="{escape(text)}" '
        f'supporting-text="{escape(supporting_text)}"></nldd-banner>\n'
    )


def _filter_actions(actions, richtlijn_filter=None, fase_filter=None):
    """
    Filter actions based on richtlijn and fase.

    Args:
        actions: List of action dictionaries
        richtlijn_filter: Richtlijn name to filter by (or None)
        fase_filter: Fase name to filter by (or None)

    Returns:
        List of filtered actions
    """
    filtered = []

    for action in actions:
        # Filter by richtlijn
        if richtlijn_filter:
            action_richtlijn = action.get('richtlijn')

            # Handle richtlijn as string or list
            if isinstance(action_richtlijn, list):
                if richtlijn_filter not in action_richtlijn:
                    continue
            elif action_richtlijn != richtlijn_filter:
                continue

        # Filter by fase
        if fase_filter:
            action_fase = action.get('fase')

            # Skip if action has no fase defined
            if not action_fase:
                continue

            # Handle fase as string or list
            if isinstance(action_fase, list):
                if fase_filter not in action_fase:
                    continue
            elif action_fase != fase_filter:
                continue

        filtered.append(action)

    return filtered


def _generate_action_cards_html(actions, heading_level=4):
    """
    Generate a card per action.
    """
    # The status is a state the registry keeps, so it is a badge. The text
    # carries the meaning; the color only supports it.
    # It sits below the title, not beside it: beside it the badge takes width
    # from the title, and a long name then breaks in the middle of a word.
    # Not above it either: then the status comes before the heading in the
    # DOM, and whoever jumps from heading to heading never hears it.
    status_colors = {
        'beschikbaar': 'success',
        'ontwikkeling': 'warning',
        'demo': 'accent',
        'concept': 'neutral',
    }

    cards_html = []

    for action in _sort_actions_by_fase(actions):
        status = action.get('status', 'beschikbaar')
        color = status_colors.get(status, 'neutral')

        card_html = f'''      <nldd-card>
        <nldd-container padding="16" gap="8">
          <nldd-title size="5" heading-level="{heading_level}" text="{escape(action.get('name', ''))}">
            <nldd-badge slot="supporting-text" size="sm" color="{color}" text="{escape(status)}"></nldd-badge>
          </nldd-title>
          <nldd-rich-text><p>{escape(action.get('description', ''))}</p></nldd-rich-text>
        </nldd-container>
        <nldd-container slot="footer" padding="16">
          {_generate_button_html(action)}
        </nldd-container>
      </nldd-card>'''

        cards_html.append(card_html)

    return '\n'.join(cards_html)


def _sort_actions_by_fase(actions):
    """
    Sort actions by fase in the order: verkenning, ontwerp, bouw, productie, live.
    Actions without a fase or with unlisted fases come last.

    Args:
        actions: List of action dictionaries

    Returns:
        Sorted list of actions
    """
    # Define the fase order
    fase_order = {
        'verkenning': 1,
        'ontwerp': 2,
        'bouw': 3,
        'productie': 4,
        'live': 5,
    }

    def get_sort_key(action):
        fase = action.get('fase')

        # No fase means it should come last
        if not fase:
            return (999, '')

        # Get the first fase if it's a list
        first_fase = fase[0] if isinstance(fase, list) else fase

        # Return the order number, or 999 if not in our list
        return (fase_order.get(first_fase, 999), first_fase)

    return sorted(actions, key=get_sort_key)


def _generate_button_html(action):
    """
    Generate the button of a card based on action type and source.
    """
    action_type = action.get('type', '')
    action_label = escape(action.get('action', ''))
    name = escape(action.get('name', ''))
    source = action.get('source')
    component = action.get('component')
    label = f'accessible-label="{action_label}: {name}"'

    # For form type actions with a component
    if action_type == 'form' and component:
        if component == 'kubernetes-cluster-form':
            return (
                f'<nldd-button id="open-cluster-form" appearance="secondary" size="sm" '
                f'popup-type="dialog" text="{action_label}" {label}></nldd-button>'
            )

    # For actions without a source
    if not source:
        return f'<nldd-button appearance="secondary" size="sm" disabled text="{action_label}" {label}></nldd-button>'

    # For actions with a source
    return (
        f'<nldd-button appearance="secondary" size="sm" href="{escape(source)}" target="_blank" '
        f'end-icon="external-link" text="{action_label}" {label}></nldd-button>'
    )
