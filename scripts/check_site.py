#!/usr/bin/env python3
"""
Build the site and run every check on the result.

    check_site.py            build, then check markup, tokens, classes, the CSP, the outline,
                             behavior and nldd lint
    check_site.py --update   build, then record the behavior surface as the new reference

Pre-commit and CI both run this file, so they cannot drift apart.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
SURFACE = SCRIPTS / "behavior-surface.json"
DESIGN_SYSTEM = REPO_ROOT / "nldd-design-system.json"


def run(*arguments: str) -> int:
    return subprocess.run([sys.executable, *arguments], cwd=REPO_ROOT).returncode


def lint(site_dir: str) -> int:
    """Run nldd lint of the pinned design system version on the built pages.

    A warning fails the check as an error does; a hint only informs.
    """
    npx = shutil.which("npx")
    if npx is None:
        print("nldd lint needs Node 20.19 or newer, with npx on the PATH.")
        return 1
    pin = json.loads(DESIGN_SYSTEM.read_text())
    package = f"{pin['package']}@{pin['version']}"
    # From inside the build, so a finding names the page, such as Over-NeRDS/index.html.
    arguments = [npx, "--yes", package, "lint", ".", "--max-warnings", "0"]
    if os.environ.get("GITHUB_ACTIONS"):
        arguments += ["--format", "github"]
    return subprocess.run(arguments, cwd=site_dir).returncode


def main() -> int:
    update = sys.argv[1:] == ["--update"]
    if sys.argv[1:] and not update:
        print(__doc__)
        return 2

    with tempfile.TemporaryDirectory() as site_dir:
        if run("-m", "mkdocs", "build", "--quiet", "--site-dir", site_dir) != 0:
            print("The site does not build.")
            return 1
        if update:
            return run(str(SCRIPTS / "behavior_surface.py"), "snapshot", site_dir, str(SURFACE))
        results = [
            run(str(SCRIPTS / "check_nldd.py"), site_dir),
            run(str(SCRIPTS / "check_csp.py"), site_dir),
            run(str(SCRIPTS / "check_outline.py"), site_dir),
            run(str(SCRIPTS / "behavior_surface.py"), "check", site_dir, str(SURFACE)),
            lint(site_dir),
        ]
    return 1 if any(results) else 0


if __name__ == "__main__":
    sys.exit(main())
