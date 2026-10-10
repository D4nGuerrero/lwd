"""Copy only public website files into docs/ for GitHub Pages.

Run `python tools/build_pages.py` after editing the source site, then commit
the updated docs/ directory. GitHub Pages should publish from branch /docs.
"""

from pathlib import Path
from shutil import copy2
from urllib.parse import urlsplit
import re


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs"

FILES = [
    "index.html",
    "styles.css",
    "script.js",
    "css/base.css",
    "css/sections.css",
    "css/responsive.css",
    "assets/laredo-bridge.jpg",
    "assets/underwater-catfish.jpg",
    "assets/lwd-logo.png",
    "assets/river-cutout.png",
    "assets/shoreline-details.png",
    "assets/work-border-brew.jpg",
    "assets/work-rivas.jpg",
    "assets/work-family-care.jpg",
]


def copy_public_files() -> None:
    OUTPUT.mkdir(exist_ok=True)
    for name in FILES:
        source = ROOT / name
        target = OUTPUT / name
        if not source.is_file():
            raise FileNotFoundError(f"Missing source file: {source}")
        target.parent.mkdir(parents=True, exist_ok=True)
        copy2(source, target)
    (OUTPUT / ".nojekyll").touch()


def check_local_paths() -> None:
    """Catch broken paths before committing the Pages publishing folder."""
    references = []
    for name in ("index.html", "styles.css", "css/base.css", "css/sections.css", "css/responsive.css"):
        page = OUTPUT / name
        content = page.read_text(encoding="utf-8")
        references.extend((page, match) for match in re.findall(r'(?:src|href)="([^"]+)"|url\([\'"]?([^\)\'"]+)', content))

    for page, match in references:
        reference = next((part for part in match if part), "")
        if not reference or reference.startswith(("#", "data:", "mailto:")):
            continue
        parsed = urlsplit(reference)
        if parsed.scheme or parsed.netloc:
            continue
        if reference.startswith("/"):
            raise ValueError(f"Root-absolute path would break project Pages: {page}: {reference}")
        target = (page.parent / parsed.path).resolve()
        if not target.is_relative_to(OUTPUT.resolve()) or not target.is_file():
            raise FileNotFoundError(f"Broken local reference: {page}: {reference}")


if __name__ == "__main__":
    copy_public_files()
    check_local_paths()
    print(f"GitHub Pages folder ready: {OUTPUT} ({len(FILES)} files plus .nojekyll)")
