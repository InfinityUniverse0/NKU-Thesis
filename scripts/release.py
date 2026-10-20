#!/usr/bin/env python3
"""Prepare and package a clean, compilable snapshot of the committed template."""

import argparse
import hashlib
import re
import shutil
import subprocess
import zipfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = "NKU-Thesis"
SOURCE_PATHS = (
    "main.tex",
    "references.bib",
    "NKUThesis.sty",
    "NKUThesis.bbx",
    "NKUThesis.cbx",
    "README.md",
    "LICENSE",
    "fonts",
    "assets",
    "figures",
    "tex",
)
REQUIRED_FILES = (
    "main.tex",
    "references.bib",
    "NKUThesis.sty",
    "NKUThesis.bbx",
    "NKUThesis.cbx",
    "README.md",
    "LICENSE",
    "tex/abstract.tex",
    "tex/body.tex",
    "tex/appendix.tex",
    "tex/acknowledgements.tex",
)


def prepare(work_dir):
    # Refuse to mix a fresh source snapshot with a previous build's caches.
    work_dir.mkdir(parents=True, exist_ok=False)
    source_zip = work_dir / "source.zip"
    subprocess.run(
        [
            "git", "archive", "--format=zip", f"--prefix={PACKAGE_ROOT}/",
            f"--output={source_zip}", "HEAD", "--", *SOURCE_PATHS,
        ],
        cwd=PROJECT_ROOT,
        check=True,
    )
    with zipfile.ZipFile(source_zip) as archive:
        names = set(archive.namelist())
        missing = [
            name for name in REQUIRED_FILES
            if f"{PACKAGE_ROOT}/{name}" not in names
        ]
        if missing:
            raise ValueError(f"Required template files are missing: {missing}")
        archive.extractall(work_dir)
    print(f"Template snapshot: {work_dir / PACKAGE_ROOT}")


def package(work_dir, output_dir, tag):
    # Tags can contain slashes and Unicode; asset filenames must be portable.
    version = re.sub(r"[^A-Za-z0-9._-]+", "-", tag).strip(".-") or "release"
    basename = f"{PACKAGE_ROOT}-{version}"
    source_dir = work_dir / PACKAGE_ROOT
    pdf = source_dir / "main.pdf"
    if not pdf.is_file() or not pdf.read_bytes().startswith(b"%PDF-"):
        raise ValueError("A successfully compiled main.pdf is required")
    log = (source_dir / "main.log").read_text(encoding="utf-8", errors="replace")
    if any(message in log for message in (
        "There were undefined references.",
        "Please (re)run Biber",
        "Missing character:",
    )):
        raise ValueError("Resolve the missing references or characters before releasing")

    output_dir.mkdir(parents=True, exist_ok=True)
    archive_path = output_dir / f"{basename}.zip"
    # Use the original source archive, not the build directory: no .aux/.bbl/logs.
    with zipfile.ZipFile(work_dir / "source.zip") as source:
        with zipfile.ZipFile(
            archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9,
        ) as archive:
            for entry in source.infolist():
                archive.writestr(entry, source.read(entry.filename))
            archive.write(pdf, f"{PACKAGE_ROOT}/main.pdf")
    with zipfile.ZipFile(archive_path) as archive:
        corrupt_file = archive.testzip()
        if corrupt_file:
            raise ValueError(f"Corrupt archive member: {corrupt_file}")

    preview_path = output_dir / f"{basename}.pdf"
    shutil.copyfile(pdf, preview_path)
    checksum_lines = [
        f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n"
        for path in (archive_path, preview_path)
    ]
    (output_dir / "SHA256SUMS").write_text("".join(checksum_lines), encoding="utf-8")
    print(f"Release assets: {archive_path}, {preview_path}, SHA256SUMS")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("prepare", "package"))
    parser.add_argument("--work-dir", type=Path, default=Path(".build/release"))
    parser.add_argument("--output-dir", type=Path, default=Path("dist"))
    parser.add_argument("--tag", help="Git tag used in release asset filenames")
    args = parser.parse_args()
    if args.command == "prepare":
        prepare(args.work_dir.resolve())
    elif args.tag:
        package(args.work_dir.resolve(), args.output_dir.resolve(), args.tag)
    else:
        parser.error("package requires --tag")


if __name__ == "__main__":
    main()
