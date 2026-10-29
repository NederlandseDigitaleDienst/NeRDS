#!/usr/bin/env python3
"""Generate the parts of the plugin that are derived from something else.

Two things, each with one source:

- the platform-specific plugin.json files, from the neutral .plugin/plugin.json;
- the guideline text inside each skill, from docs/richtlijnen/.

A skill carries a copy of its guideline so that it is complete on its own:
on a Windows checkout, where a symlink arrives as a one-line text file, and
when a tool copies only the skill folder. Edit the file in docs/ and run this
script; the pre-commit hook does that for you.

Usage:
    python scripts/generate_plugin.py          # generate everything
    python scripts/generate_plugin.py --check  # verify nothing is out of date
"""

import copy
import importlib.util
import json
import re
import sys
import tomllib
from functools import cache
from pathlib import Path

import yaml

ROOT_DIR = Path(__file__).resolve().parent.parent
PYPROJECT_PATH = ROOT_DIR / "pyproject.toml"
MKDOCS_PATH = ROOT_DIR / "mkdocs.yml"
SOURCE_PATH = ROOT_DIR / ".plugin" / "plugin.json"
CLAUDE_PATH = ROOT_DIR / ".claude-plugin" / "plugin.json"
CURSOR_PATH = ROOT_DIR / ".cursor-plugin" / "plugin.json"
SKILLS_DIR = ROOT_DIR / "skills"
DOCS_DIR = ROOT_DIR / "docs"
GUIDELINES_DIR = DOCS_DIR / "richtlijnen"
# First characters of every generated file; also how a stale one is recognised.
GENERATED_MARK = "<!-- Gegenereerd uit "
CODE_FENCE = re.compile(r"(^```.*?^```[^\n]*\n?|^~~~.*?^~~~[^\n]*\n?)", re.DOTALL | re.MULTILINE)

# Skill -> its guideline's folder under docs/richtlijnen, in the order of the guidelines.
SKILL_GUIDELINES = {
    "nerds-gebruikers": "gebruikersbehoeften",
    "nerds-toegankelijkheid": "toegankelijkheid",
    "nerds-opensource": "open-source",
    "nerds-standaarden": "open-standaarden",
    "nerds-cloud": "cloud",
    "nerds-veiligheid": "veiligheid",
    "nerds-privacy": "privacy",
    "nerds-samenwerking": "samenwerking",
    "nerds-integratie": "integratie",
    "nerds-data": "data",
    "nerds-algoritmen": "algoritmen",
    "nerds-inkoop": "inkoop",
    "nerds-duurzaamheid": "duurzaamheid",
}
# File in the guideline's folder -> its name inside the skill.
SKILL_FILES = {"index.md": "richtlijn.md", "fases.md": "fases.md"}
OVERVIEW_PATH = SKILLS_DIR / "nerds" / "richtlijnen.md"

FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n+", re.DOTALL)
ATTRIBUTE_LIST = re.compile(r"\{:[^}]*\}")
# Words in another language, for a screen reader on the site; a skill keeps the words.
LANGUAGE_SPAN = re.compile(r'<span lang="[a-z-]+">(.*?)</span>')
# A Markdown link to another page of the site: a relative path ending in .md.
PAGE_LINK = re.compile(r"\[([^\]]+)\]\((?!https?://|#|mailto:)([^)#\s]*\.md)(#[^)\s]*)?\)")
GUIDELINE_SKILLS = {guideline: skill for skill, guideline in SKILL_GUIDELINES.items()}

ACTIONS_PATH = ROOT_DIR / "docs" / "action-registry" / "actions.yaml"
ACTION_HOOK_PATH = ROOT_DIR / "src" / "hooks" / "action_registry.py"
# The same two shapes the hook looks for: a block with a heading and an
# optional notice around the placeholder, and a placeholder on its own.
ACTION_BLOCK = re.compile(
    r'<div class="direct-aan-de-slag">\s*<h(?P<level>[34])>(?P<heading>.*?)</h(?P=level)>.*?'
    r'<div class="action-cards"(?P<attributes>[^>]*)></div>\s*</div>',
    re.DOTALL,
)
ACTION_PLACEHOLDER = re.compile(r'<div class="action-cards"(?P<attributes>[^>]*)></div>')
ADMONITION = re.compile(r'^(?:!!!|\?\?\?\+?) \S+ "([^"]*)"\s*$')
# What must not survive in a skill: syntax only the site's build understands.
MKDOCS_ONLY = re.compile(
    r"^(?:!!!|\?\?\?).*$|</?(?:div|h[1-6]|span|strong|nldd-[a-z-]+)\b[^>]*>|\{:[^}]*\}|\{\{[^}]*\}\}", re.MULTILINE
)


def load_source() -> dict:
    """Load the neutral .plugin/plugin.json."""
    with open(SOURCE_PATH) as f:
        return json.load(f)


def generate_claude(data: dict) -> dict:
    """Generate Claude Code plugin.json — identical copy of source."""
    return copy.deepcopy(data)


def _display_name(name: str) -> str:
    """Convert a kebab-case plugin name to a human-readable display name.

    Examples:
        "standaarden" -> "Standaarden"
        "zad-actions" -> "Zad Actions"
    """
    return name.replace("-", " ").title()


def generate_cursor(data: dict) -> dict:
    """Generate Cursor plugin.json — adds displayName."""
    result = copy.deepcopy(data)
    # Insert displayName after name
    ordered = {"name": result.pop("name")}
    ordered["displayName"] = _display_name(ordered["name"])
    ordered.update(result)
    return ordered


PLATFORMS: dict[str, tuple[Path, callable]] = {
    "claude": (CLAUDE_PATH, generate_claude),
    "cursor": (CURSOR_PATH, generate_cursor),
}


def write_json(path: Path, data: dict) -> None:
    """Write JSON data to a file with consistent formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def generate_all(source_data: dict) -> None:
    """Generate all platform plugin files."""
    for _name, (path, generator) in PLATFORMS.items():
        generated = generator(source_data)
        write_json(path, generated)
        print(f"Gegenereerd: {path.relative_to(ROOT_DIR)}")


def check_sync(source_data: dict) -> bool:
    """Check if platform files are in sync with the source."""
    all_synced = True
    for _name, (path, generator) in PLATFORMS.items():
        expected = generator(source_data)
        if not path.exists():
            print(f"FOUT: {path.relative_to(ROOT_DIR)} bestaat niet")
            all_synced = False
            continue
        with open(path) as f:
            actual = json.load(f)
        if actual != expected:
            print(f"FOUT: {path.relative_to(ROOT_DIR)} is niet in sync")
            all_synced = False
        else:
            print(f"OK: {path.relative_to(ROOT_DIR)}")
    return all_synced


def check_version(source_data: dict) -> bool:
    """The plugin shares its version with the project; release-please raises both."""
    with open(PYPROJECT_PATH, "rb") as f:
        project_version = tomllib.load(f)["project"]["version"]
    if source_data.get("version") != project_version:
        print(
            f"FOUT: versie in {SOURCE_PATH.relative_to(ROOT_DIR)} is {source_data.get('version')}, "
            f"in pyproject.toml {project_version}"
        )
        return False
    print(f"OK: versie {project_version} gelijk aan pyproject.toml")
    return True


@cache
def site_url() -> str:
    match = re.search(r"^site_url:\s*(\S+)", MKDOCS_PATH.read_text(encoding="utf-8"), re.MULTILINE)
    if not match:
        sys.exit(f"FOUT: geen site_url in {MKDOCS_PATH.relative_to(ROOT_DIR)}")
    return match.group(1).rstrip("/") + "/"


def front_matter(source: Path) -> dict:
    match = FRONT_MATTER.match(source.read_text(encoding="utf-8"))
    fields = yaml.safe_load(match.group(1)) if match else None
    for key in ("title", "summary"):
        if not isinstance(fields, dict) or not fields.get(key):
            sys.exit(f"FOUT: {source.relative_to(ROOT_DIR)} heeft geen `{key}` in de front matter")
    return fields


@cache
def action_registry():
    """
    The site hook that turns a "Direct aan de slag" block into cards. Its
    filter and its order are reused here, so the skill lists the same actions
    as the page.
    """
    spec = importlib.util.spec_from_file_location("action_registry", ACTION_HOOK_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@cache
def actions() -> tuple:
    return tuple(yaml.safe_load(ACTIONS_PATH.read_text(encoding="utf-8"))["actions"])


def action_lists(text: str) -> str:
    """
    Replace each "Direct aan de slag" block by a bold line and a list of its
    actions. On the site the block is an empty placeholder that the hook fills
    with cards; a skill has no hook, so it gets the actions themselves.
    """
    hook = action_registry()

    def render(match: re.Match) -> str:
        attributes = match.group("attributes")
        guideline = re.search(r'data-richtlijn="([^"]+)"', attributes)
        phase = re.search(r'data-fase="([^"]+)"', attributes)
        selected = hook._filter_actions(
            list(actions()), guideline.group(1) if guideline else None, phase.group(1) if phase else None
        )
        # Only what exists. The registry also holds ideas and work in progress
        # without an address; on the site a badge and a notice mark those, but
        # an assistant reading a plain list would recommend them as tools.
        selected = [action for action in selected if action.get("source")]
        if not selected:
            return ""
        heading = match.groupdict().get("heading")
        # A bold line, not a heading: the block sits under headings of
        # different levels, and a fixed level would break the outline.
        lines = [f"**{hook._plain_text(heading)}**", ""] if heading else []
        for action in hook._sort_actions_by_fase(selected):
            status = action.get("status", "beschikbaar")
            suffix = "" if status == "beschikbaar" else f" (status: {status})"
            lines.append(f"- [{action['name']}]({action['source']}): {action.get('description', '')}{suffix}")
        return "\n".join(lines)

    text = ACTION_BLOCK.sub(render, text)
    return ACTION_PLACEHOLDER.sub(render, text)


def plain_admonitions(text: str) -> str:
    """
    `!!! info "Doel"` and `??? expander "Tips"` are MkDocs blocks: a marker
    line, then the content indented by four spaces. In plain Markdown that
    indentation makes the content a code block, so the marker becomes a bold
    line and the content loses its indentation.
    """
    output: list[str] = []
    inside = False
    for line in text.split("\n"):
        marker = ADMONITION.match(line)
        if marker:
            if output and output[-1].strip():
                output.append("")
            output += [f"**{marker.group(1)}**", ""]
            inside = True
        elif inside and (line.startswith("    ") or not line.strip()):
            output.append(line[4:] if line.startswith("    ") else line)
        else:
            inside = False
            output.append(line)
    return "\n".join(output)


def skill_text(source: Path, guideline: str) -> str:
    """
    The guideline as a skill reads it: without the front matter and the
    syntax that only the site's build understands, and with links that work
    from inside the skill folder.

    A link to another guideline becomes the name of that guideline's skill:
    inside the plugin the other guideline is installed too, so there is no
    reason to send the reader to the website for it. The anchor of such a
    link is dropped; a skill is read as a whole.
    """
    origin = source.relative_to(ROOT_DIR).as_posix()

    def relink(match: re.Match) -> str:
        label, anchor = match.group(1), match.group(3) or ""
        resolved = (source.parent / match.group(2)).resolve()
        if not resolved.is_relative_to(DOCS_DIR):
            sys.exit(f"FOUT: {origin} linkt naar {match.group(2)}, buiten de map docs/")
        page = resolved.relative_to(DOCS_DIR)
        if page.parent == source.parent.relative_to(DOCS_DIR) and page.name in SKILL_FILES:
            return f"[{label}]({SKILL_FILES[page.name]}{anchor})"
        if page.parent.parent == GUIDELINES_DIR.relative_to(DOCS_DIR) and page.parent.name in GUIDELINE_SKILLS:
            part = ", de fases" if page.name == "fases.md" else ""
            return f"{label} (skill `/{GUIDELINE_SKILLS[page.parent.name]}`{part})"
        if page == GUIDELINES_DIR.relative_to(DOCS_DIR) / "index.md":
            return f"{label} (skill `/nerds`)"
        # Any other page of the site: MkDocs serves index.md as its folder.
        address = page.parent.as_posix() if page.name == "index.md" else page.with_suffix("").as_posix()
        return f"[{label}]({site_url()}{'' if address == '.' else address + '/'}{anchor})"

    def outside_code(segment: str) -> str:
        segment = PAGE_LINK.sub(relink, LANGUAGE_SPAN.sub(r"\1", ATTRIBUTE_LIST.sub("", segment)))
        return plain_admonitions(action_lists(segment))

    body = FRONT_MATTER.sub("", source.read_text(encoding="utf-8"), count=1)
    # A fenced code block is an example; it is copied as it is.
    parts = CODE_FENCE.split(body)
    body = "".join(part if index % 2 else outside_code(part) for index, part in enumerate(parts))
    # Tidy what the replacements leave behind, so the copy passes the same
    # lint as its source: no trailing spaces, no runs of blank lines.
    body = re.sub(r"[ \t]+$", "", body, flags=re.MULTILINE)
    body = re.sub(r"\n{3,}", "\n\n", body).strip() + "\n"
    for index, part in enumerate(CODE_FENCE.split(body)):
        leftover = None if index % 2 else MKDOCS_ONLY.search(part)
        if leftover:
            sys.exit(
                f"FOUT: {origin} bevat `{leftover.group(0).strip()}`, "
                "dat generate_plugin.py niet naar gewone Markdown omzet"
            )
    return f"<!-- Gegenereerd uit {origin}. Wijzig dat bestand en draai: just plugin -->\n\n{body}"


def overview_text() -> str:
    """The list of guidelines for the skill `nerds`, from each guideline's front matter."""
    lines = [
        "<!-- Gegenereerd uit de front matter in docs/richtlijnen/. Wijzig die bestanden en draai: just plugin -->",
        "",
        "# De richtlijnen van de NeRDS",
        "",
    ]
    for skill, guideline in SKILL_GUIDELINES.items():
        fields = front_matter(GUIDELINES_DIR / guideline / "index.md")
        lines += [f"## {fields['title']}", "", str(fields["summary"]).strip(), "", f"Skill: `/{skill}`", ""]
    return "\n".join(lines)


def skill_files() -> dict[Path, str]:
    """Every generated file under skills/, with the content it should have."""
    unknown = sorted(
        path.name for path in GUIDELINES_DIR.iterdir() if path.is_dir() and path.name not in GUIDELINE_SKILLS
    )
    if unknown:
        sys.exit(
            f"FOUT: docs/richtlijnen/{unknown[0]} heeft geen skill. "
            "Voeg de richtlijn toe aan SKILL_GUIDELINES in scripts/generate_plugin.py"
        )
    files = {OVERVIEW_PATH: overview_text()}
    for skill, guideline in SKILL_GUIDELINES.items():
        for source_name, skill_name in SKILL_FILES.items():
            source = GUIDELINES_DIR / guideline / source_name
            if source.exists():
                files[SKILLS_DIR / skill / skill_name] = skill_text(source, guideline)
    return files


def leftovers(expected: dict[Path, str]) -> list[Path]:
    """
    What the generator once made and no longer does: a symlink, or a file
    with the generated header whose source is gone.
    """
    found = []
    for path in sorted(SKILLS_DIR.rglob("*")):
        if path.is_symlink():
            found.append(path)
        elif path.is_file() and path not in expected and path.suffix == ".md":
            with open(path, encoding="utf-8") as f:
                if f.readline().startswith(GENERATED_MARK):
                    found.append(path)
    return found


def generate_skills() -> None:
    expected = skill_files()
    for path in leftovers(expected):
        path.unlink()
        print(f"Verwijderd: {path.relative_to(ROOT_DIR)}")
    for path, content in expected.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"Gegenereerd: {path.relative_to(ROOT_DIR)}")


def check_skills() -> bool:
    expected = skill_files()
    ok = True
    for path in leftovers(expected):
        kind = "is een symlink" if path.is_symlink() else "heeft geen bron meer in docs/richtlijnen"
        print(f"FOUT: {path.relative_to(ROOT_DIR)} {kind}")
        ok = False
    for path, content in expected.items():
        if not path.is_file() or path.read_text(encoding="utf-8") != content:
            print(f"FOUT: {path.relative_to(ROOT_DIR)} loopt niet gelijk met docs/richtlijnen")
            ok = False
    if ok:
        print("OK: de richtlijnen in skills/ lopen gelijk met docs/richtlijnen")
    return ok


def main() -> None:
    if not SOURCE_PATH.exists():
        print(f"FOUT: {SOURCE_PATH} niet gevonden")
        sys.exit(1)

    source_data = load_source()

    if "--check" in sys.argv:
        synced = check_sync(source_data)
        same_version = check_version(source_data)
        skills_ok = check_skills()
        if not synced or not skills_ok:
            print("\nNiet in sync. Draai: just plugin (of: uv run python scripts/generate_plugin.py)")
        if not same_version:
            print("\nHet versienummer wijzig je niet met de hand: release-please doet dat in de release-PR.")
        if synced and same_version and skills_ok:
            print("\nAlle platform-bestanden en skills zijn in sync")
            sys.exit(0)
        sys.exit(1)
    else:
        generate_all(source_data)
        generate_skills()
        print("\nAlle platform-bestanden en skills gegenereerd")


if __name__ == "__main__":
    main()
