from __future__ import annotations

import json
import os
import shutil
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FEATURE_LIST_PATH = ROOT / "feature_list.json"
ARCHIVE_PATH = ROOT / "feature_list.archive.json"
CURRENT_PATH = ROOT / "progress" / "current.md"
HISTORY_PATH = ROOT / "progress" / "history.md"
PROGRESS_ARCHIVE_PATH = ROOT / "progress" / "archive"
CURRENT_ACTIVE_TEMPLATE = ROOT / "docs" / "harness" / "templates" / "progress" / "current.active.md"
CURRENT_EMPTY_TEMPLATE = ROOT / "docs" / "harness" / "templates" / "progress" / "current.empty.md"


def safe_write(path: Path, content: str) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    os.replace(tmp, path)


def snapshot_text(path: Path) -> str | None:
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def restore_snapshot(path: Path, content: str | None) -> None:
    if content is None:
        if path.exists():
            path.unlink()
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    safe_write(path, content)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    safe_write(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def load_feature_list() -> dict[str, Any]:
    return load_json(FEATURE_LIST_PATH)


def write_feature_list(data: dict[str, Any]) -> None:
    write_json(FEATURE_LIST_PATH, data)


def load_archive() -> dict[str, Any]:
    if ARCHIVE_PATH.is_file():
        return load_json(ARCHIVE_PATH)
    feature_list = load_feature_list()
    return {
        "project": feature_list.get("project", "harness-template"),
        "description": "Features cerradas archivadas",
        "features": [],
    }


def write_archive(data: dict[str, Any]) -> None:
    write_json(ARCHIVE_PATH, data)


def features(data: dict[str, Any]) -> list[dict[str, Any]]:
    value = data.get("features")
    if not isinstance(value, list):
        raise ValueError("feature_list.json debe contener features como lista")
    return value


def find_feature(items: list[dict[str, Any]], selector: str | None) -> dict[str, Any]:
    if selector is None:
        matches = [feature for feature in items if feature.get("status") == "in_progress"]
        if len(matches) != 1:
            raise ValueError("Debe existir exactamente una feature in_progress o pasar id/name")
        return matches[0]

    for feature in items:
        if str(feature.get("id")) == selector or feature.get("name") == selector:
            return feature
    raise ValueError(f"No existe feature: {selector}")


def active_features(items: list[dict[str, Any]], status: str) -> list[dict[str, Any]]:
    return [feature for feature in items if feature.get("status") == status]


def render_active_current(feature: dict[str, Any], agent: str, status: str = "in_progress", block_reason: str | None = None) -> str:
    template = CURRENT_ACTIVE_TEMPLATE.read_text(encoding="utf-8")
    acceptance = feature.get("acceptance") if isinstance(feature.get("acceptance"), list) else []
    plan = "\n".join(f"- {item}" for item in acceptance) if acceptance else "- Verificar acceptance"
    implemented = f"- Feature #{feature.get('id')} abierta."
    blockers = f"- {block_reason}" if block_reason else "- Ninguno"
    return (
        template.replace("<id>", str(feature.get("id")))
        .replace("<feature_name>", str(feature.get("name")))
        .replace("<role>", agent)
        .replace("<yyyy-mm-dd>", date.today().isoformat())
        .replace("in_progress", status, 1)
        .replace("- <contexto breve de la tarea>", f"- {feature.get('description')}")
        .replace("- <paso verificable>", plan)
        .replace("- <cambio realizado>", implemented)
        .replace("- Ninguno", blockers)
    )


def reset_current() -> None:
    safe_write(CURRENT_PATH, CURRENT_EMPTY_TEMPLATE.read_text(encoding="utf-8"))


def write_current(content: str) -> None:
    safe_write(CURRENT_PATH, content)


def report_path(name: str, prefix: str) -> Path:
    return ROOT / "progress" / f"{prefix}_{name}.md"


def archived_report_path(name: str, prefix: str) -> Path:
    return PROGRESS_ARCHIVE_PATH / f"{prefix}_{name}.md"


def find_report(name: str, prefix: str) -> Path | None:
    for path in (report_path(name, prefix), archived_report_path(name, prefix)):
        if path.is_file():
            return path
    return None


def ensure_approved_review(name: str) -> Path:
    path = find_report(name, "review")
    if path is None:
        raise ValueError(f"Falta progress/review_{name}.md")
    content = path.read_text(encoding="utf-8")
    if "Veredicto:** APPROVED" not in content:
        raise ValueError(f"review_{name}.md no tiene Veredicto APPROVED")
    return path


def move_report_to_archive(name: str, prefix: str) -> None:
    source = report_path(name, prefix)
    if not source.is_file():
        return
    PROGRESS_ARCHIVE_PATH.mkdir(parents=True, exist_ok=True)
    target = archived_report_path(name, prefix)
    if target.exists():
        raise ValueError(f"Ya existe {target.relative_to(ROOT).as_posix()}")
    shutil.move(str(source), str(target))


def feature_briefs(feature: dict[str, Any]) -> list[Path]:
    feature_id = str(feature.get("id", "")).strip()
    feature_name = str(feature.get("name", "")).strip().lower()
    if not feature_id and not feature_name:
        return []

    tokens = {
        feature_name,
        f"feature {feature_id}",
        f"feature #{feature_id}",
        f"feature_id: {feature_id}",
        f"feature id: {feature_id}",
        f"**feature id:** {feature_id}",
        f"**feature name:** {feature_name}",
    }

    progress_dir = ROOT / "progress"
    matches: list[Path] = []
    for brief in sorted(progress_dir.glob("brief_*.md")):
        haystack = f"{brief.name.lower()}\n{brief.read_text(encoding='utf-8').lower()}"
        if any(token and token in haystack for token in tokens):
            matches.append(brief)
    return matches


def archive_feature_briefs(feature: dict[str, Any]) -> None:
    PROGRESS_ARCHIVE_PATH.mkdir(parents=True, exist_ok=True)
    for brief in feature_briefs(feature):
        target = PROGRESS_ARCHIVE_PATH / brief.name
        if target.exists():
            continue
        shutil.move(str(brief), str(target))


def append_history_event(feature: dict[str, Any], title: str, details: list[str]) -> None:
    body = "\n".join(f"- {detail}" for detail in details if detail.strip()) or "- Sin detalle"
    entry = (
        f"\n## {date.today().isoformat()} — feature {feature.get('id')} {feature.get('name')}\n\n"
        f"### {title}\n"
        f"{body}\n"
    )
    existing = HISTORY_PATH.read_text(encoding="utf-8") if HISTORY_PATH.is_file() else ""
    safe_write(HISTORY_PATH, existing + entry)


def extract_impl_summary(name: str) -> str:
    path = find_report(name, "impl")
    if path is None:
        return "No hay reporte de implementación disponible."
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    in_resumen = False
    collected: list[str] = []
    for line in lines:
        if line.strip().lower().startswith("## resumen"):
            in_resumen = True
            continue
        if in_resumen:
            if line.startswith("## "):
                break
            collected.append(line)
    body = [l for l in collected if l.strip()]
    if body:
        return "\n".join(body[:3])
    body_all = [l for l in lines if l.strip() and not l.startswith("#")]
    if body_all:
        return "\n".join(body_all[:3])
    return "No hay reporte de implementación disponible."


def extract_review_verdict(name: str) -> str:
    path = find_report(name, "review")
    if path is None:
        return "No hay reporte de review disponible."
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    verdict_line = ""
    for line in lines:
        if "Veredicto:" in line:
            verdict_line = line.strip()
            break
    notas: list[str] = []
    in_notas = False
    for line in lines:
        if line.strip().lower().startswith("## notas"):
            in_notas = True
            continue
        if in_notas:
            if line.startswith("## "):
                break
            notas.append(line)
    notas_body = [l for l in notas if l.strip()]
    parts = []
    if verdict_line:
        parts.append(verdict_line)
    if notas_body:
        parts.append("\n".join(notas_body))
    return "\n".join(parts) if parts else "No hay reporte de review disponible."


def append_history(
    feature: dict[str, Any],
    impl_summary: str | None = None,
    review_verdict: str | None = None,
) -> None:
    impl_text = impl_summary or "No hay reporte de implementación disponible."
    verdict_text = review_verdict or "No hay reporte de review disponible."
    entry = (
        f"\n## {date.today().isoformat()} — feature {feature.get('id')} {feature.get('name')}\n\n"
        "### Estado\n"
        "- done\n\n"
        "### Resumen implementación\n"
        f"{impl_text}\n\n"
        "### Veredicto review\n"
        f"{verdict_text}\n"
    )
    existing = HISTORY_PATH.read_text(encoding="utf-8") if HISTORY_PATH.is_file() else ""
    safe_write(HISTORY_PATH, existing + entry)
