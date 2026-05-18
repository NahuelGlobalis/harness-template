from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
VALID_STATUS_DEFAULT = {"pending", "in_progress", "done", "blocked", "cancelled"}
NAME_PATTERN = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$")
MARKDOWN_FIELD_PATTERN = r"(?m)^\*\*{field}:\*\*\s*(.*?)\s*$"
REPORTS_REQUIRED_FROM_ID_DEFAULT = 1

failures: list[str] = []
warnings: list[str] = []


def ok(message: str) -> None:
    print(f"[OK]    {message}")


def warn(message: str) -> None:
    warnings.append(message)
    print(f"[WARN]  {message}")


def fail(message: str) -> None:
    failures.append(message)
    print(f"[FAIL]  {message}")


def read_json(path: Path) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        fail(f"JSON inválido en {path.as_posix()}: {exc}")
        return None


def markdown_field(content: str, field: str) -> str | None:
    pattern = MARKDOWN_FIELD_PATTERN.format(field=re.escape(field))
    match = re.search(pattern, content)
    if match is None:
        return None
    value = match.group(1).strip()
    return value or None


def validate_base_files() -> None:
    base_files = [
        "AGENTS.md",
        "CHECKPOINTS.md",
        "init.ps1",
        "init.sh",
        "feature_list.json",
        "scripts/block_feature.py",
        "scripts/cancel_feature.py",
        "scripts/close_feature.py",
        "scripts/harness_state.py",
        "scripts/open_feature.py",
        "scripts/unblock_feature.py",
        "docs/architecture/overview.md",
        "docs/engineering/conventions/shared.md",
        "docs/quality/gardening.md",
        "docs/harness/lifecycle.md",
        "docs/harness/ticketing.md",
        "docs/engineering/verification/shared.md",
        "docs/harness/templates/progress/current.active.md",
        "docs/harness/templates/progress/current.empty.md",
        "docs/harness/templates/progress/impl.md",
        "docs/harness/templates/progress/review.md",
        "progress/current.md",
        "progress/history.md",
    ]
    role_files = [
        "agents/architect.md",
        "agents/implementer.md",
        "agents/reviewer.md",
        "agents/gardener.md",
    ]

    for relative_path in [*base_files, *role_files]:
        path = ROOT / relative_path
        if path.is_file():
            ok(f"Existe {relative_path}")
        else:
            fail(f"Falta archivo base: {relative_path}")


def _find_report(name: str, prefix: str) -> Path | None:
    filename = f"{prefix}_{name}.md"
    for candidate in (ROOT / "progress" / filename, ROOT / "progress" / "archive" / filename):
        if candidate.is_file():
            return candidate
    return None


def _validate_archive_features(
    features: list[dict[str, Any]],
    reports_required_from_id: int,
    seen_ids: set[int],
    seen_names: set[str],
) -> None:
    for index, feature in enumerate(features, start=1):
        if not isinstance(feature, dict):
            fail(f"Archive feature #{index} debe ser un objeto")
            continue

        feature_id = feature.get("id")
        name = feature.get("name")
        status = feature.get("status")
        acceptance = feature.get("acceptance")

        if not isinstance(feature_id, int) or isinstance(feature_id, bool):
            fail(f"Archive feature #{index} tiene id inválido: {feature_id!r}")
        elif feature_id in seen_ids:
            fail(f"Archive feature id duplicado con feature_list.json: {feature_id}")
        else:
            seen_ids.add(feature_id)

        if not isinstance(name, str) or not NAME_PATTERN.match(name):
            fail(f"Archive feature {feature_id} tiene name inválido: {name!r}")
        elif name in seen_names:
            fail(f"Archive feature name duplicado: {name}")
        else:
            seen_names.add(name)

        if status not in ("done", "cancelled"):
            fail(f"Archive feature {feature_id} tiene status inválido: {status!r} (solo 'done' o 'cancelled' permitido en archivo)")

        title = feature.get("title")
        if not isinstance(title, str) or not title.strip():
            fail(f"Archive feature {feature_id} debe tener title como string no vacío")

        description = feature.get("description")
        if not isinstance(description, str) or not description.strip():
            fail(f"Archive feature {feature_id} debe tener description como string no vacío")

        if not isinstance(acceptance, list) or not acceptance:
            fail(f"Archive feature {feature_id} debe tener acceptance no vacío")
        else:
            for item_index, item in enumerate(acceptance, start=1):
                if not isinstance(item, str) or not item.strip():
                    fail(f"Archive feature {feature_id} tiene acceptance #{item_index} vacío")

        if status == "done" and isinstance(feature_id, int) and feature_id >= reports_required_from_id:
            impl_path = _find_report(name, "impl")
            review_path = _find_report(name, "review")
            if impl_path is None:
                fail(
                    f"Archive feature done {feature_id} no tiene impl_{name}.md"
                    " (buscado en progress/ y progress/archive/)"
                )
            if review_path is None:
                fail(
                    f"Archive feature done {feature_id} no tiene review_{name}.md"
                    " (buscado en progress/ y progress/archive/)"
                )
            elif "Veredicto:** APPROVED" not in review_path.read_text(encoding="utf-8"):
                fail(f"Archive feature done {feature_id} no tiene review APPROVED")


def validate_feature_list() -> tuple[list[dict[str, Any]], set[str]]:
    path = ROOT / "feature_list.json"
    data = read_json(path)
    if not isinstance(data, dict):
        fail("feature_list.json debe ser un objeto JSON")
        return [], VALID_STATUS_DEFAULT

    features = data.get("features")
    if not isinstance(features, list):
        fail("feature_list.json debe contener features como lista")
        return [], VALID_STATUS_DEFAULT

    rules = data.get("rules", {})
    raw_valid_status = rules.get("valid_status") if isinstance(rules, dict) else None
    valid_status = set(raw_valid_status) if isinstance(raw_valid_status, list) else VALID_STATUS_DEFAULT
    if not valid_status:
        fail("rules.valid_status no puede estar vacío")
        valid_status = VALID_STATUS_DEFAULT

    raw_threshold = rules.get("reports_required_from_id") if isinstance(rules, dict) else None
    if isinstance(raw_threshold, int) and not isinstance(raw_threshold, bool) and raw_threshold >= 1:
        reports_required_from_id = raw_threshold
    else:
        reports_required_from_id = REPORTS_REQUIRED_FROM_ID_DEFAULT

    seen_ids: set[int] = set()
    seen_names: set[str] = set()
    previous_id = 0
    in_progress_count = 0
    blocked_count = 0

    for index, feature in enumerate(features, start=1):
        if not isinstance(feature, dict):
            fail(f"Feature #{index} debe ser un objeto")
            continue

        feature_id = feature.get("id")
        name = feature.get("name")
        status = feature.get("status")
        acceptance = feature.get("acceptance")

        if not isinstance(feature_id, int) or isinstance(feature_id, bool):
            fail(f"Feature #{index} tiene id inválido: {feature_id!r}")
        elif feature_id in seen_ids:
            fail(f"Feature id duplicado: {feature_id}")
        else:
            seen_ids.add(feature_id)
            if feature_id <= previous_id:
                fail(f"Feature id fuera de orden: {feature_id} después de {previous_id}")
            previous_id = feature_id

        if not isinstance(name, str) or not NAME_PATTERN.match(name):
            fail(f"Feature {feature_id} tiene name inválido: {name!r}")
        elif name in seen_names:
            fail(f"Feature name duplicado: {name}")
        else:
            seen_names.add(name)

        if status not in valid_status:
            fail(f"Feature {feature_id} tiene status inválido: {status!r}")
        elif status in ("done", "cancelled"):
            fail(
                f"Feature {feature_id} está {status} en feature_list.json; "
                "debe moverse a feature_list.archive.json"
            )
        elif status == "in_progress":
            in_progress_count += 1
        elif status == "blocked":
            blocked_count += 1

        title = feature.get("title")
        if not isinstance(title, str) or not title.strip():
            fail(f"Feature {feature_id} debe tener title como string no vacío")

        description = feature.get("description")
        if not isinstance(description, str) or not description.strip():
            fail(f"Feature {feature_id} debe tener description como string no vacío")

        if not isinstance(acceptance, list) or not acceptance:
            fail(f"Feature {feature_id} debe tener acceptance no vacío")
        else:
            for item_index, item in enumerate(acceptance, start=1):
                if not isinstance(item, str) or not item.strip():
                    fail(f"Feature {feature_id} tiene acceptance #{item_index} vacío")

    if in_progress_count > 1:
        fail(f"Hay {in_progress_count} features en in_progress (máximo 1)")
    if blocked_count > 1:
        fail(f"Hay {blocked_count} features en blocked (máximo 1)")
    if in_progress_count and blocked_count:
        fail("No puede haber features in_progress y blocked al mismo tiempo")
    if (
        in_progress_count <= 1
        and blocked_count <= 1
        and not (in_progress_count and blocked_count)
    ):
        ok("feature_list.json mantiene como máximo una feature in_progress")

    ok(f"feature_list.json parseado ({len(features)} features)")

    archive_path = ROOT / "feature_list.archive.json"
    if archive_path.is_file():
        archive_data = read_json(archive_path)
        if not isinstance(archive_data, dict):
            fail("feature_list.archive.json debe ser un objeto JSON")
        else:
            archive_features = archive_data.get("features")
            if not isinstance(archive_features, list):
                fail("feature_list.archive.json debe contener features como lista")
            elif archive_features:
                _validate_archive_features(
                    archive_features, reports_required_from_id, seen_ids, seen_names
                )
                ok(f"feature_list.archive.json parseado ({len(archive_features)} features archivadas)")
            else:
                ok("feature_list.archive.json existe y está vacío")
    else:
        ok("feature_list.archive.json no existe (opcional)")

    return features, valid_status


def validate_current_progress(features: list[dict[str, Any]], valid_status: set[str]) -> None:
    path = ROOT / "progress" / "current.md"
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        fail(f"No se pudo leer progress/current.md: {exc}")
        return

    current_id_raw = markdown_field(content, "Feature ID")
    current_name = markdown_field(content, "Feature name")
    current_status = markdown_field(content, "Estado")
    current_agent = markdown_field(content, "Agente")
    in_progress = [feature for feature in features if feature.get("status") == "in_progress"]
    blocked = [feature for feature in features if feature.get("status") == "blocked"]
    allowed_current_status = valid_status | {"sin_tarea"}

    if current_status and current_status not in allowed_current_status:
        fail(f"progress/current.md tiene Estado inválido: {current_status}")

    if len(in_progress) > 1:
        fail(f"Hay {len(in_progress)} features in_progress; no se puede validar current.md")
        return

    if len(in_progress) == 1:
        active = in_progress[0]
        active_id = active.get("id")
        active_name = active.get("name")
        failures_before = len(failures)
        if current_status != "in_progress":
            fail("progress/current.md debe tener Estado: in_progress")
        if current_agent is None:
            fail("progress/current.md debe declarar Agente")
        if current_id_raw is None:
            fail("progress/current.md debe declarar Feature ID")
        else:
            try:
                current_id = int(current_id_raw)
            except ValueError:
                fail(f"progress/current.md tiene Feature ID no numérico: {current_id_raw}")
            else:
                if current_id != active_id:
                    fail(f"Feature ID activa no coincide: current={current_id}, feature_list={active_id}")
        if current_name != active_name:
            fail(f"Feature name activa no coincide: current={current_name}, feature_list={active_name}")
        if len(failures) == failures_before:
            ok("progress/current.md coincide con la feature in_progress")
        return

    if current_status == "in_progress":
        fail("progress/current.md declara in_progress pero feature_list.json no")
        return

    if current_status == "blocked":
        matching_blocked = [
            feature
            for feature in blocked
            if str(feature.get("id")) == str(current_id_raw) and feature.get("name") == current_name
        ]
        if len(matching_blocked) != 1:
            fail("progress/current.md declara blocked sin feature blocked coincidente")
        else:
            ok("progress/current.md coincide con la feature blocked")
        return

    if blocked:
        fail("feature_list.json tiene una feature blocked pero progress/current.md no refleja el bloqueo")
        return

    if current_status in (None, "sin_tarea"):
        ok("progress/current.md no declara tarea activa")
    else:
        fail("progress/current.md debe estar limpio o en Estado: sin_tarea")


def validate_progress_hygiene(features: list[dict[str, Any]]) -> None:
    progress_dir = ROOT / "progress"
    always_allowed = {"current.md", "history.md"}

    active_features = [f for f in features if f.get("status") in ("in_progress", "blocked")]
    has_active_feature = bool(active_features)
    active_name = active_features[0].get("name") if active_features else None

    unexpected = []
    for path in progress_dir.iterdir():
        if path.is_dir():
            continue
        filename = path.name
        if filename in always_allowed:
            continue
        if has_active_feature and active_name:
            if filename in (f"impl_{active_name}.md", f"review_{active_name}.md"):
                continue
            if filename.startswith("brief_") and filename.endswith(".md"):
                continue
            if filename.startswith("gardening_") and filename.endswith(".md"):
                continue
        unexpected.append(filename)

    if unexpected:
        files_str = ", ".join(sorted(unexpected))
        if has_active_feature:
            warn(f"Archivos inesperados en progress/ durante sesión activa: {files_str}")
        else:
            fail(f"Archivos huérfanos en progress/ sin sesión activa: {files_str}")
    else:
        ok("progress/ contiene solo archivos permitidos")


def main() -> int:
    os.chdir(ROOT)
    validate_base_files()
    features, valid_status = validate_feature_list()
    validate_current_progress(features, valid_status)
    validate_progress_hygiene(features)

    if failures:
        print(f"[FAIL]  Arnés inválido: {len(failures)} error(es), {len(warnings)} warning(s)")
        return 1
    print(f"[OK]    Arnés válido: 0 errores, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
