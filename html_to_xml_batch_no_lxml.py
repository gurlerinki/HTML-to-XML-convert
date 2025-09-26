#!/usr/bin/env python3
"""
Offline batch converter: HTML -> well-formed XML (XHTML) WITHOUT lxml

- Uses html5lib to parse tolerant HTML into an xml.etree.ElementTree
- Produces XML/XHTML (with XHTML namespace) that is well-formed
- No C/C++ derleme (build) gerektirmez; Windows'ta MSVC'ye ihtiyaç yok
"""
import argparse
from pathlib import Path
from typing import Optional
import sys

import html5lib
from xml.etree import ElementTree as ET

def read_text_guess(path: Path) -> str:
    for enc in ("utf-8", "cp1254", "windows-1254", "latin-1"):
        try:
            return path.read_text(encoding=enc, errors="strict")
        except Exception:
            continue
    return path.read_bytes().decode("utf-8", errors="replace")

def to_xhtml_etree(html_text: str) -> ET.ElementTree:
    # html5lib parses broken HTML and returns an ElementTree (etree builder)
    doc = html5lib.parse(html_text, treebuilder="etree")
    if isinstance(doc, ET.Element):
        return ET.ElementTree(doc)
    return doc

def serialize_xml(tree: ET.ElementTree, pretty: bool = True) -> bytes:
    if pretty:
        indent(tree.getroot())
    return ET.tostring(tree.getroot(), encoding="utf-8", xml_declaration=True, method="xml")

def indent(elem, level: int = 0):
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for e in elem:
            indent(e, level + 1)
        if not e.tail or not e.tail.strip():
            e.tail = i
    if level and (not elem.tail or not elem.tail.strip()):
        elem.tail = i

def convert_file(src: Path, dst: Path, pretty: bool = True) -> None:
    html_text = read_text_guess(src)
    tree = to_xhtml_etree(html_text)
    xml_bytes = serialize_xml(tree, pretty=pretty)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(xml_bytes)

def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Batch convert HTML (*.html, *.htm) to XML (XHTML) without lxml.")
    p.add_argument("input", help="Input file or folder containing HTML files")
    p.add_argument("-o", "--output", help="Output folder (default: alongside originals or inside specified folder)")
    p.add_argument("--flat", action="store_true", help="Do not mirror folder structure under output")
    p.add_argument("--no-pretty", action="store_true", help="Disable pretty printing")
    args = p.parse_args(argv)

    in_path = Path(args.input)
    out_root = Path(args.output) if args.output else None
    pretty = not args.no_pretty

    files = []
    if in_path.is_file():
        if in_path.suffix.lower() in (".html", ".htm"):
            files = [in_path]
        else:
            print(f"Skipping non-HTML file: {in_path}", file=sys.stderr)
            return 1
    else:
        files = sorted([*in_path.rglob("*.html"), *in_path.rglob("*.htm")])

    if not files:
        print("No HTML files found.", file=sys.stderr)
        return 1

    converted = 0
    for src in files:
        if out_root:
            if args.flat:
                dst = out_root / (src.stem + ".xml")
            else:
                rel = src.relative_to(in_path if in_path.is_dir() else src.parent)
                dst = out_root / rel.with_suffix(".xml")
        else:
            dst = src.with_suffix(".xml")

        try:
            convert_file(src, dst, pretty=pretty)
            print(f"[OK] {src} -> {dst}")
            converted += 1
        except Exception as e:
            print(f"[FAIL] {src}: {e}", file=sys.stderr)

    print(f"Done. Converted {converted} file(s).")
    return 0 if converted > 0 else 2

if __name__ == "__main__":
    raise SystemExit(main())
