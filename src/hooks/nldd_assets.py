"""
MkDocs hook that serves the NLDD Designsysteem from the built site.

The package version and its integrity hash are pinned in
nldd-design-system.json, so an upgrade is a visible commit. The tarball is
downloaded once into .cache/nldd/<version>/ and verified before use.

The script is not the package bundle, which holds every component. After the
build, esbuild (tools/bundle) bundles only the components the pages use. The
script and the stylesheet get a content hash in their name, so nginx can let
browsers keep them for a year.
"""

import base64
import hashlib
import io
import json
import re
import shutil
import subprocess
import tarfile
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PIN_FILE = REPO_ROOT / "nldd-design-system.json"
CACHE_ROOT = REPO_ROOT / ".cache" / "nldd"
# Paths inside the tarball that the site or the checks need.
WANTED = ("package/dist/css/", "package/dist/fonts/",
          "package/dist/favicon.svg", "package/dist/touch-icon.png",
          "package/custom-elements.json", "package/dist/components/content/icon/icon-registry.js",
          "package/dist/components/content/icon/icon-aliases.js")
IMPORT = re.compile(r'@import\s+"\./([^"]+)";\n?')
BUNDLE_DIR = REPO_ROOT / "tools" / "bundle"
THEME_SCRIPTS = REPO_ROOT / "src" / "theme" / "assets"
# A tag in built HTML, or in a string in a theme script that creates one.
TAG = re.compile(r"""[<'"`](nldd-[a-z0-9]+(?:-[a-z0-9]+)*)""")
SCRIPT = re.compile(r'<script type="module" src="(?P<prefix>[^"]*assets/nldd/)nldd\.js"></script>')
STATIC_IMPORT = re.compile(r'(?:from|import)\s*"\./([^"]+\.js)"')


def load_pin() -> dict:
    return json.loads(PIN_FILE.read_text(encoding="utf-8"))


def package_dir() -> Path:
    """Return the extracted package directory, downloading it when needed."""
    pin = load_pin()
    target = CACHE_ROOT / pin["version"]
    if (target / ".complete").exists():
        return target

    name = pin["package"]
    url = f"https://registry.npmjs.org/{name}/-/{name.split('/')[-1]}-{pin['version']}.tgz"
    with urllib.request.urlopen(url, timeout=60) as response:
        tarball = response.read()

    algorithm, expected = pin["integrity"].split("-", 1)
    actual = base64.b64encode(hashlib.new(algorithm, tarball).digest()).decode()
    if actual != expected:
        raise RuntimeError(f"Integrity mismatch for {name}@{pin['version']}")

    target.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(tarball), mode="r:gz") as archive:
        for member in archive.getmembers():
            if not member.isfile() or not member.name.startswith(WANTED):
                continue
            relative = member.name.removeprefix("package/").removeprefix("dist/")
            destination = target / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(archive.extractfile(member).read())
    (target / ".complete").touch()
    return target


def bundle_stylesheet(css_dir: Path, entry: str = "global.css") -> str:
    """Inline the @import chain of the package stylesheet into one file."""
    seen: set[str] = set()

    def inline(name: str) -> str:
        if name in seen:
            return ""
        seen.add(name)
        css = (css_dir / name).read_text(encoding="utf-8")
        return IMPORT.sub(lambda match: inline(match.group(1)), css)

    # The bundle sits one level above css/, next to fonts/.
    return inline(entry).replace("url('../fonts/", "url('fonts/")


def bundle_package() -> Path:
    """Return the design system installed for esbuild, installing it when needed."""
    pin = load_pin()
    installed = BUNDLE_DIR / "node_modules" / pin["package"]
    manifest = json.loads((BUNDLE_DIR / "package.json").read_text(encoding="utf-8"))
    if manifest["dependencies"][pin["package"]] != pin["version"]:
        raise RuntimeError(
            f"tools/bundle/package.json asks for {pin['package']}@"
            f"{manifest['dependencies'][pin['package']]}, nldd-design-system.json "
            f"pins {pin['version']}. Set both to the same version and run npm install there."
        )
    version = None
    if (installed / "package.json").exists():
        version = json.loads((installed / "package.json").read_text(encoding="utf-8"))["version"]
    if version != pin["version"]:
        subprocess.run(["npm", "ci", "--ignore-scripts", "--no-audit", "--no-fund"],
                       cwd=BUNDLE_DIR, check=True)
    return installed


def used_tags(site_dir: Path) -> set[str]:
    """Every design system tag in the built pages and in the theme scripts."""
    tags = set()
    for path in [*site_dir.rglob("*.html"), *THEME_SCRIPTS.glob("*.js")]:
        tags.update(TAG.findall(path.read_text(encoding="utf-8")))
    return tags


def component_modules(package: Path, tags: set[str]) -> list[str]:
    """The built module of each tag, from the custom elements manifest."""
    manifest = json.loads((package / "custom-elements.json").read_text(encoding="utf-8"))
    module_of = {}
    for module in manifest["modules"]:
        for declaration in module.get("declarations", []):
            if declaration.get("tagName"):
                source = module["path"].removeprefix("src/").removesuffix(".ts")
                module_of[declaration["tagName"]] = f"dist/{source}.js"
    unknown = sorted(tags - module_of.keys())
    if unknown:
        raise RuntimeError(f"Not in the design system: {', '.join(unknown)}")
    return sorted({module_of[tag] for tag in tags})


def bundle_script(site_dir: Path, target: Path) -> str:
    """Bundle the components the site uses, and return the name of the entry.

    As modules with splitting: what a component imports only when it needs it,
    such as the grammars of nldd-code-viewer, becomes a chunk of its own that
    loads on the pages that use it. Every file carries its content hash.
    """
    package = bundle_package()
    modules = component_modules(package, used_tags(site_dir))
    entry = BUNDLE_DIR / "nldd.js"
    metafile = BUNDLE_DIR / "meta.json"
    # By file path: the exports map of the package does not list every module.
    imports = (f'import "./{(package / module).relative_to(BUNDLE_DIR).as_posix()}";\n' for module in modules)
    entry.write_text("".join(imports), encoding="utf-8")
    try:
        subprocess.run(
            [str(BUNDLE_DIR / "node_modules" / ".bin" / "esbuild"), str(entry), "--bundle",
             "--minify", "--format=esm", "--splitting", "--target=es2022", "--log-level=warning",
             # The checks for developers only run under a bundler that sets this.
             "--define:import.meta.env.DEV=false",
             "--entry-names=[name]-[hash]", "--chunk-names=chunk-[hash]",
             f"--metafile={metafile}", f"--outdir={target}"],
            cwd=BUNDLE_DIR, check=True,
        )
        outputs = json.loads(metafile.read_text(encoding="utf-8"))["outputs"]
    finally:
        entry.unlink(missing_ok=True)
        metafile.unlink(missing_ok=True)
    # A module that is only imported dynamically is an entry point of its own.
    return next(Path(path).name for path, output in outputs.items()
                if output.get("entryPoint") == entry.name)


def static_chunks(target: Path, entry: str) -> list[str]:
    """The chunks the entry imports statically, directly or through another chunk."""
    found, pending = set(), [entry]
    while pending:
        name = pending.pop()
        for chunk in STATIC_IMPORT.findall((target / name).read_text(encoding="utf-8")):
            if chunk not in found:
                found.add(chunk)
                pending.append(chunk)
    return sorted(found)


def with_hash(path: Path) -> str:
    """Rename a file to carry its content hash, and return the new name."""
    digest = hashlib.sha256(path.read_bytes()).hexdigest()[:10]
    hashed = path.with_name(f"{path.stem}-{digest}{path.suffix}")
    path.replace(hashed)
    return hashed.name


def on_config(config):
    package_dir()
    return config


def on_post_build(config):
    source = package_dir()
    target = Path(config["site_dir"]) / "assets" / "nldd"
    target.mkdir(parents=True, exist_ok=True)

    site_dir = Path(config["site_dir"])
    (target / "nldd.css").write_text(bundle_stylesheet(source / "css"), encoding="utf-8")
    stylesheet = with_hash(target / "nldd.css")
    script = bundle_script(site_dir, target)
    chunks = static_chunks(target, script)

    def script_tags(match):
        # The browser finds the chunks only after reading the entry; a preload
        # fetches them alongside it.
        prefix = match.group("prefix")
        preloads = "".join(f'\n  <link rel="modulepreload" href="{prefix}{chunk}">' for chunk in chunks)
        return f'<script type="module" src="{prefix}{script}"></script>{preloads}'

    for page in site_dir.rglob("*.html"):
        html = page.read_text(encoding="utf-8")
        updated = html.replace("assets/nldd/nldd.css", f"assets/nldd/{stylesheet}")
        updated = SCRIPT.sub(script_tags, updated)
        if updated != html:
            page.write_text(updated, encoding="utf-8")
    shutil.copy2(source / "favicon.svg", target / "favicon.svg")
    shutil.copy2(source / "touch-icon.png", target / "touch-icon.png")
    shutil.copytree(source / "fonts", target / "fonts", dirs_exist_ok=True)
