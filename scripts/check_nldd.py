#!/usr/bin/env python3
"""
Check the built site against the NLDD Designsysteem package it ships.

Wrong markup for these components fails silently: an unknown attribute, icon
name or CSS variable renders nothing and raises no error. This script makes
that audible.

    check_nldd.py <site_dir>

Checks:
  markup   every nldd-* element, attribute, slot and icon name exists in the package
  tokens   every design system variable in our CSS exists; no literal colors
  classes  every class in the output has a rule, every rule has a user
  markers  nothing of the previous theme is left, and the new shell is there
"""

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src" / "hooks"))

import nldd_assets  # noqa: E402

THEME_ASSETS = REPO_ROOT / "src" / "theme" / "assets"

GLOBAL_ATTRIBUTES = {"id", "class", "slot", "hidden", "role", "tabindex", "lang", "title", "name"}
GLOBAL_ATTRIBUTE_PREFIXES = ("data-", "aria-")
ICON_ATTRIBUTES = {"icon", "start-icon", "end-icon"}
# Classes owned by a plugin that brings no stylesheet of its own.
EXTERNAL_CLASSES = {"git-revision-date-localized-plugin", "git-revision-date-localized-plugin-date"}
# Class and id prefixes of the previous theme. A prefix ends in a dash so a
# word that merely starts the same does not match.
OLD_CLASS_MARKERS = ("md-", "admonition", "task-list", "feedback-widget", "glightbox")
TOKEN = re.compile(r"var\(\s*(--(?:primitives|semantics|components|context)-[\w-]+)\s*(,[^)]*)?\)")
HEX_COLOR = re.compile(r"#[0-9a-fA-F]{3,8}\b")
CLASS_SELECTOR = re.compile(r"\.(-?[_a-zA-Z][\w-]*)")


def load_package():
    package = nldd_assets.package_dir()
    manifest = json.loads((package / "custom-elements.json").read_text(encoding="utf-8"))
    elements = {}
    for module in manifest["modules"]:
        for declaration in module.get("declarations", []):
            tag = declaration.get("tagName")
            if not tag:
                continue
            elements[tag] = {
                "attributes": {item["name"] for item in declaration.get("attributes", [])},
                "slots": {item["name"] for item in declaration.get("slots", [])},
            }
    icon_dir = package / "components" / "content" / "icon"
    icons = set(re.findall(r"^\s*\['([a-z0-9-]+)',", (icon_dir / "icon-registry.js").read_text(encoding="utf-8"), re.M))
    icons |= set(re.findall(r"^\s*'([a-z0-9-]+)':", (icon_dir / "icon-aliases.js").read_text(encoding="utf-8"), re.M))
    tokens = set()
    for css_file in (package / "css").glob("*.css"):
        tokens |= set(re.findall(r"(--[\w-]+)\s*:", css_file.read_text(encoding="utf-8")))
    return elements, icons, tokens


class MarkupParser(HTMLParser):
    """Collects findings and used classes for one page."""

    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}

    def __init__(self, route, elements, icons):
        super().__init__(convert_charrefs=True)
        self.route = route
        self.elements = elements
        self.icons = icons
        self.findings = []
        self.classes = set()
        self.tags = set()
        self.inline_styles = []
        self.stack = []

    def handle_starttag(self, tag, attrs):
        values = {name: (value or "") for name, value in attrs}
        parent = self.stack[-1] if self.stack else None
        if tag not in self.VOID:
            self.stack.append(tag)
        self.tags.add(tag)
        self.classes.update(values.get("class", "").split())
        if "style" in values:
            self.inline_styles.append(values["style"])

        slot = values.get("slot")
        if slot and parent in self.elements and slot not in self.elements[parent]["slots"]:
            self.findings.append(f"{self.route}: <{parent}> has no slot '{slot}' (used on <{tag}>)")

        if not tag.startswith("nldd-"):
            return
        if tag not in self.elements:
            self.findings.append(f"{self.route}: unknown element <{tag}>")
            return
        known = self.elements[tag]["attributes"]
        for name, value in values.items():
            if name in GLOBAL_ATTRIBUTES or name.startswith(GLOBAL_ATTRIBUTE_PREFIXES):
                continue
            if name not in known:
                self.findings.append(f"{self.route}: <{tag}> has no attribute '{name}'")
            elif name in ICON_ATTRIBUTES and value not in self.icons:
                self.findings.append(f"{self.route}: <{tag}> uses unknown icon '{value}'")

    def handle_endtag(self, tag):
        if tag in self.stack:
            while self.stack and self.stack.pop() != tag:
                pass


def check_scripts(elements, icons):
    """Elements and icons that scripts create never appear in the built HTML."""
    findings = []
    for script in sorted(THEME_ASSETS.glob("*.js")):
        source = script.read_text(encoding="utf-8")
        for tag in re.findall(r"createElement\('(nldd-[a-z0-9-]+)'\)", source):
            if tag not in elements:
                findings.append(f"{script.name}: creates unknown element <{tag}>")
        for name in re.findall(r"setAttribute\('(?:icon|start-icon|end-icon)',\s*'([^']+)'\)", source):
            if name not in icons:
                findings.append(f"{script.name}: sets unknown icon '{name}'")
    return findings


def check_tokens(tokens, inline_styles):
    findings = []
    sources = {path.name: path.read_text(encoding="utf-8") for path in sorted(THEME_ASSETS.glob("*.css"))}
    sources["inline style attributes"] = "\n".join(inline_styles)
    for name, css in sources.items():
        css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
        for token, fallback in TOKEN.findall(css):
            if token not in tokens:
                findings.append(f"{name}: variable {token} does not exist in the package")
            if fallback and HEX_COLOR.search(fallback):
                findings.append(f"{name}: {token} has a literal color as fallback, which hides a wrong name")
        for color in HEX_COLOR.findall(re.sub(r"var\([^)]*\)", "", css)):
            findings.append(f"{name}: literal color {color}; use a design system variable")
    return findings


def check_classes(used_classes):
    findings = []
    css = "\n".join(path.read_text(encoding="utf-8") for path in sorted(THEME_ASSETS.glob("*.css")))
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
    selectors = "\n".join(re.findall(r"([^{}]+)\{", css))
    defined = set(CLASS_SELECTOR.findall(selectors))
    scripts = "\n".join(path.read_text(encoding="utf-8") for path in sorted(THEME_ASSETS.glob("*.js")))

    for name in sorted(used_classes - defined - EXTERNAL_CLASSES):
        findings.append(f"class '{name}' is used in the output but has no rule")
    for name in sorted(defined - used_classes):
        if name not in scripts:
            findings.append(f"rule for class '{name}' has no user in the output")
    return findings


def check_markers(pages):
    findings = []
    for route, parser in pages.items():
        for name in sorted(parser.classes):
            if name.startswith(OLD_CLASS_MARKERS):
                findings.append(f"{route}: class '{name}' belongs to the previous theme")
        if "nldd-shell" not in parser.tags:
            findings.append(f"{route}: page has no <nldd-shell>, so the shell did not render")
    return findings


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    site_dir = Path(sys.argv[1])
    html_files = sorted(site_dir.rglob("*.html"))
    if not html_files:
        print(f"No pages found in {site_dir}")
        return 2

    elements, icons, tokens = load_package()
    pages = {}
    for html_file in html_files:
        parser = MarkupParser(html_file.relative_to(site_dir).as_posix(), elements, icons)
        parser.feed(html_file.read_text(encoding="utf-8"))
        pages[parser.route] = parser

    used_classes = set().union(*(parser.classes for parser in pages.values()))
    inline_styles = [style for parser in pages.values() for style in parser.inline_styles]
    checks = {
        "markup": [finding for parser in pages.values() for finding in parser.findings] + check_scripts(elements, icons),
        "tokens": check_tokens(tokens, inline_styles),
        "classes": check_classes(used_classes),
        "markers": check_markers(pages),
    }

    failed = False
    for name, findings in checks.items():
        unique = sorted(set(findings))
        print(f"{name}: {'ok' if not unique else f'{len(unique)} findings'}")
        for finding in unique:
            print(f"  {finding}")
        failed = failed or bool(unique)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
