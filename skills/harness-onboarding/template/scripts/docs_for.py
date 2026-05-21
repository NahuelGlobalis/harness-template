"""docs_for.py — Concatena documentación relevante por sección y capa del monorepo.

Lee tablas de docs/README.md (delimitadas por marcadores HTML)
y devuelve los documentos concatenados o listados según los pares solicitados.

Uso:
    python scripts/docs_for.py engineering:api              # convenciones backend
    python scripts/docs_for.py engineering:api,web          # backend y frontend
    python scripts/docs_for.py engineering:web              # convenciones frontend
    python scripts/docs_for.py harness:all                  # toda la sección harness
    python scripts/docs_for.py all:api                     # capa api en todas las secciones
    python scripts/docs_for.py all:all                     # todo
    python scripts/docs_for.py docs:shared harness:shared engineering:shared  # múltiples pares
    python scripts/docs_for.py --list engineering:web       # lista rutas sin concatenar
    python scripts/docs_for.py --json operations:shared    # devuelve rutas en JSON
    python scripts/docs_for.py --strict quality:shared     # falla si hay rutas faltantes

Compatibilidad: si se pasa un token sin `:` se interpreta como `seccion:all`.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

# Ensure UTF-8 output on Windows (docs may contain unicode)
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[union-attr]

ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
README_PATH = DOCS_DIR / "README.md"

# No more hardcoded aliases - sections and keys are read from docs/README.md


def discover_sections() -> list[str]:
    """Return all section names from the sections table in docs/README.md."""
    content = README_PATH.read_text(encoding="utf-8")
    begin_marker = "<!-- sections:begin -->"
    end_marker = "<!-- sections:end -->"
    begin_idx = content.find(begin_marker)
    end_idx = content.find(end_marker)
    if begin_idx == -1 or end_idx == -1:
        print("Error: no se encontraron los marcadores sections en docs/README.md", file=sys.stderr)
        sys.exit(1)
    table_text = content[begin_idx + len(begin_marker) : end_idx].strip()
    sections: list[str] = []
    table_lines = [line.strip() for line in table_text.splitlines() if line.strip().startswith("|")]
    if len(table_lines) > 1 and "---" in table_lines[1]:
        table_lines = table_lines[2:]
    for line in table_lines:
        cells = [c.strip() for c in line.split("|")]
        cells = [c for c in cells if c]
        if len(cells) >= 1:
            # Extract section name from backtick-quoted key
            key = cells[0]
            match = re.search(r"`([^`]+)`", key)
            if match:
                sections.append(match.group(1))
    return sections


def discover_keys() -> list[str]:
    """Return all key names from the keys table in docs/README.md."""
    content = README_PATH.read_text(encoding="utf-8")
    begin_marker = "<!-- keys:begin -->"
    end_marker = "<!-- keys:end -->"
    begin_idx = content.find(begin_marker)
    end_idx = content.find(end_marker)
    if begin_idx == -1 or end_idx == -1:
        print("Error: no se encontraron los marcadores keys en docs/README.md", file=sys.stderr)
        sys.exit(1)
    table_text = content[begin_idx + len(begin_marker) : end_idx].strip()
    keys: list[str] = []
    table_lines = [line.strip() for line in table_text.splitlines() if line.strip().startswith("|")]
    if len(table_lines) > 1 and "---" in table_lines[1]:
        table_lines = table_lines[2:]
    for line in table_lines:
        cells = [c.strip() for c in line.split("|")]
        cells = [c for c in cells if c]
        if len(cells) >= 1:
            # Extract key name from backtick-quoted key
            key = cells[0]
            match = re.search(r"`([^`]+)`", key)
            if match:
                keys.append(match.group(1))
    return keys


def normalize_section(section: str) -> str:
    """Normalize section name by stripping and lowercasing."""
    return section.strip().lower()


def normalize_item(item: str) -> str:
    """Normalize item/key name by stripping and lowercasing."""
    return item.strip().lower()


def parse_routing_table(section: str) -> dict[str, dict[str, Any]]:
    """Parse the routing table from docs/README.md between HTML markers.

    New format: | Documento | Contenido | key |

    Special tables (sections, keys) have format: | Key | Contenido |
    """
    section = normalize_section(section)
    content = README_PATH.read_text(encoding="utf-8")

    begin_marker = f"<!-- {section}:begin -->"
    end_marker = f"<!-- {section}:end -->"

    begin_idx = content.find(begin_marker)
    end_idx = content.find(end_marker)
    if begin_idx == -1 or end_idx == -1:
        print(
            f"Error: no se encontraron los marcadores {section} en docs/README.md",
            file=sys.stderr,
        )
        sys.exit(1)

    table_text = content[begin_idx + len(begin_marker) : end_idx].strip()

    routing: dict[str, dict[str, Any]] = {}
    # Also maintain path -> description mapping
    path_descriptions: dict[str, str] = {}

    table_lines = [line.strip() for line in table_text.splitlines() if line.strip().startswith("|")]
    if len(table_lines) > 1 and "---" in table_lines[1]:
        table_lines = table_lines[2:]  # Skip header and separator

    for line in table_lines:
        cells = [c.strip() for c in line.split("|")]
        cells = [c for c in cells if c]
        # Special tables (sections, keys) have 2 columns
        if len(cells) == 2:
            key = cells[0]
            desc = cells[1].strip()
            match = re.search(r"`([^`]+)`", key)
            if match:
                item_key = match.group(1).lower()
                routing[item_key] = {"description": desc, "paths": []}
        # Routing tables have 3 columns
        elif len(cells) >= 3:
            docs_raw = cells[0]
            desc = cells[1].strip()
            # Split item_key by comma to support multiple keys per row
            item_keys = [k.strip().lower() for k in cells[2].split(",")]

            # Extract paths from backtick-quoted strings
            paths = re.findall(r"`([^`]+)`", docs_raw)
            # Store path -> description mapping
            for path in paths:
                path_descriptions[path] = desc

            for item_key in item_keys:
                if not item_key:
                    continue
                # Accumulate paths if key already exists
                if item_key in routing:
                    routing[item_key]["paths"].extend(paths)
                    # Append description if not empty
                    if desc and desc not in routing[item_key]["description"]:
                        routing[item_key]["description"] += f"; {desc}"
                else:
                    routing[item_key] = {"description": desc, "paths": list(paths)}

    if not routing:
        print(
            f"Error: la tabla de routing está vacía en la sección {section} de docs/README.md",
            file=sys.stderr,
        )
        sys.exit(1)

    # Include path descriptions in routing
    routing["_path_descriptions"] = path_descriptions
    return routing


def parse_pair(token: str) -> tuple[str, str]:
    """Parse a 'seccion:capa' token. A bare token without ':' defaults to 'seccion:all'."""
    if ":" in token:
        section_raw, _, item_raw = token.partition(":")
        return normalize_section(section_raw), normalize_item(item_raw) if item_raw else "all"
    return normalize_section(token), "all"


def resolve_pairs(pairs: list[tuple[str, str]]) -> tuple[list[Path], list[dict[str, Any]]]:
    """Resolve a list of (section, item) pairs into deduplicated paths and per-pair metadata."""
    seen_paths: set[str] = set()
    all_paths: list[Path] = []
    payloads: list[dict[str, Any]] = []

    for section, item in pairs:
        if section == "all":
            sections = discover_sections()
        else:
            sections = [section]

        for sec in sections:
            routing = parse_routing_table(sec)
            path_descriptions = routing.pop("_path_descriptions", {})

            if item == "all":
                raw_paths: list[str] = []
                for info in routing.values():
                    raw_paths.extend(info["paths"])
                items_used = list(routing.keys())
                desc = ""
            elif item in routing:
                raw_paths = routing[item]["paths"]
                items_used = [item]
                desc = routing[item]["description"]
            else:
                # If section was expanded from 'all', skip silently
                if section == "all":
                    continue
                available = ", ".join(sorted(routing.keys()))
                print(
                    f"Error: capa '{item}' no encontrada en la sección '{sec}'. Disponibles: {available}, all",
                    file=sys.stderr,
                )
                sys.exit(1)

            resolved = resolve_paths(raw_paths)
            # Deduplicate globally
            new_paths: list[Path] = []
            for p in resolved:
                key = str(p)
                if key not in seen_paths:
                    seen_paths.add(key)
                    all_paths.append(p)
                    new_paths.append(p)

            payloads.append({
                "section": sec,
                "item": item,
                "items": items_used,
                "description": desc,
                "paths": [
                    {
                        "path": p.relative_to(ROOT).as_posix(),
                        "status": "OK" if p.exists() else "MISSING",
                        "description": path_descriptions.get(p.relative_to(DOCS_DIR).as_posix(), ""),
                    }
                    for p in new_paths
                ],
            })

    return all_paths, payloads


def resolve_paths(paths: list[str]) -> list[Path]:
    """Resolve relative doc paths to absolute paths, deduplicating."""
    seen: set[str] = set()
    resolved: list[Path] = []
    for p in paths:
        abs_path = DOCS_DIR / p
        key = str(abs_path)
        if key not in seen:
            seen.add(key)
            resolved.append(abs_path)
    return resolved


def missing_paths(paths: list[Path]) -> list[Path]:
    """Return missing files from a resolved path list."""
    return [path for path in paths if not path.exists()]


def concatenate_docs(paths: list[Path]) -> str:
    """Read and concatenate files with XML separators using filename as tag."""
    parts: list[str] = []
    for path in paths:
        rel = path.relative_to(DOCS_DIR).as_posix()
        # Use filename (with extension) as tag name, replacing invalid XML chars
        tag_name = path.name.replace(".", "_")
        if path.is_dir():
            parts.append(f'<{tag_name} path="docs/{rel}" status="DIR" />\n')
            continue
        if not path.is_file():
            parts.append(f'<{tag_name} path="docs/{rel}" status="MISSING" />\n')
            continue
        content = path.read_text(encoding="utf-8").rstrip()
        parts.append(f'<{tag_name} path="docs/{rel}">\n{content}\n</{tag_name}>\n')
    return "\n".join(parts)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Concatena documentación relevante por pares seccion:capa del monorepo.",
        epilog=(
            "Ejemplos:\n"
            "  python scripts/docs_for.py engineering:api\n"
            "  python scripts/docs_for.py docs:shared harness:shared\n"
            "  python scripts/docs_for.py all:api\n"
            "  python scripts/docs_for.py engineering:all\n"
            "  python scripts/docs_for.py all:all\n"
            "  python scripts/docs_for.py --list engineering:web\n"
            "  python scripts/docs_for.py --json operations:shared\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "pairs",
        nargs="+",
        metavar="seccion:capa",
        help=(
            "Uno o más pares seccion:capa. "
            "Soporta múltiples capas separadas por coma, e.g., 'engineering:api,web'. "
            "Use 'all' en seccion o capa para expandir todas. "
            "Un token sin ':' se interpreta como seccion:all."
        ),
    )
    parser.add_argument(
        "--list",
        action="store_true",
        dest="list_only",
        help="Solo listar rutas sin concatenar contenido",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_only",
        help="Emitir rutas y metadatos en JSON",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fallar si alguna ruta listada no existe",
    )
    args = parser.parse_args()

    parsed_pairs: list[tuple[str, str]] = []
    for token in args.pairs:
        section, item = parse_pair(token)
        if item != "all" and "," in item:
            for sub_item in item.split(","):
                if sub_item.strip():
                    parsed_pairs.append((section, sub_item.strip()))
        else:
            parsed_pairs.append((section, item))

    doc_paths, payloads = resolve_pairs(parsed_pairs)

    missing = missing_paths(doc_paths)
    if args.strict and missing:
        for path in missing:
            rel = path.relative_to(ROOT).as_posix()
            print(f"Error: ruta faltante: {rel}", file=sys.stderr)
        sys.exit(1)

    if args.json_only:
        print(json.dumps(payloads, ensure_ascii=False, indent=2))
    elif args.list_only:
        for payload in payloads:
            header = f"[{payload['section']}:{payload['item']}]"
            if payload["description"]:
                header += f" - {payload['description']}"
            print(header)
            # Special tables (sections, keys) show keys instead of paths
            if payload['section'] in ('sections', 'keys') and not payload['paths']:
                for key, info in [(k, v) for k, v in parse_routing_table(payload['section']).items() if k != '_path_descriptions']:
                    print(f"  {key} - {info['description']}")
            else:
                for entry in payload["paths"]:
                    desc_suffix = f" - {entry['description']}" if entry['description'] else ""
                    print(f"  {entry['status']}  {entry['path']}{desc_suffix}")
    else:
        print(concatenate_docs(doc_paths))


if __name__ == "__main__":
    main()
