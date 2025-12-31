#!/usr/bin/env python3
"""Generate markdown documentation for YAML files in a directory."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml


def render_value(value: Any) -> str:
    if isinstance(value, str):
        return value
    return str(value)


def format_file_section(path: Path) -> list[str]:
    lines: list[str] = [f"# {path.name}", ""]
    try:
        content = path.read_text(encoding="utf-8")
        data = yaml.safe_load(content)
    except Exception as exc:  # noqa: BLE001 - report parse errors verbatim
        lines.append(f"- YAML parse error: {exc}")
        return lines

    if not isinstance(data, dict):
        data = {}

    if "name" in data:
        lines.append(f"- name: {render_value(data['name'])}")
    else:
        lines.append("- name: Missing name attribute")

    if "values" in data:
        lines.append(f"- values: {render_value(data['values'])}")
    else:
        lines.append("- values: Missing values attribute")

    return lines


def generate_docs(input_dir: Path, output_file: Path) -> None:
    yaml_files = sorted(
        [path for path in input_dir.iterdir() if path.is_file() and path.suffix in {".yml", ".yaml"}],
        key=lambda path: path.name,
    )

    sections: list[str] = []
    for path in yaml_files:
        sections.extend(format_file_section(path))
        sections.append("")

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text("\n".join(sections).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("yaml"),
        help="Directory containing YAML files.",
    )
    parser.add_argument(
        "--output-file",
        type=Path,
        default=Path("docs/yaml-docs.md"),
        help="Path to write the generated markdown.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    generate_docs(args.input_dir, args.output_file)


if __name__ == "__main__":
    main()
