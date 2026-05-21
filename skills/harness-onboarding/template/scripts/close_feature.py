from __future__ import annotations

import argparse
import sys
from pathlib import Path

from harness_state import (
    ARCHIVE_PATH,
    CURRENT_PATH,
    FEATURE_LIST_PATH,
    HISTORY_PATH,
    PROGRESS_ARCHIVE_PATH,
    ROOT,
    append_history,
    archive_feature_briefs,
    ensure_approved_review,
    extract_impl_summary,
    extract_review_verdict,
    features,
    feature_briefs,
    find_feature,
    find_report,
    load_archive,
    load_feature_list,
    move_report_to_archive,
    reset_current,
    restore_snapshot,
    snapshot_text,
    write_archive,
    write_feature_list,
)

def collect_transaction_snapshots(feature: dict[str, object]) -> dict[Path, str | None]:
    name = str(feature.get("name"))
    snapshots: dict[Path, str | None] = {
        FEATURE_LIST_PATH: snapshot_text(FEATURE_LIST_PATH),
        ARCHIVE_PATH: snapshot_text(ARCHIVE_PATH),
        CURRENT_PATH: snapshot_text(CURRENT_PATH),
        HISTORY_PATH: snapshot_text(HISTORY_PATH),
    }

    tracked_reports = [
        Path("progress") / f"impl_{name}.md",
        Path("progress") / f"review_{name}.md",
        Path("progress/archive") / f"impl_{name}.md",
        Path("progress/archive") / f"review_{name}.md",
    ]
    for relative_path in tracked_reports:
        path = ROOT / relative_path
        snapshots[path] = snapshot_text(path)

    for brief in feature_briefs(feature):
        archived_brief = PROGRESS_ARCHIVE_PATH / brief.name
        snapshots[brief] = snapshot_text(brief)
        snapshots[archived_brief] = snapshot_text(archived_brief)

    return snapshots


def rollback_transaction(snapshots: dict[Path, str | None]) -> None:
    for path, content in snapshots.items():
        restore_snapshot(path, content)


def main() -> int:
    parser = argparse.ArgumentParser(description="Cierra una feature aprobada, la archiva y resetea current.md")
    parser.add_argument("feature", nargs="?", help="id o name de la feature; por defecto usa la in_progress")
    args = parser.parse_args()

    data = load_feature_list()
    items = features(data)
    feature = find_feature(items, args.feature)
    if feature.get("status") != "in_progress":
        raise ValueError("Solo se puede cerrar una feature in_progress")

    name = str(feature.get("name"))
    if find_report(name, "impl") is None:
        raise ValueError(f"Falta progress/impl_{name}.md")
    ensure_approved_review(name)

    archive = load_archive()
    archive_items = features(archive)
    if any(item.get("id") == feature.get("id") or item.get("name") == name for item in archive_items):
        raise ValueError("La feature ya existe en feature_list.archive.json")

    snapshots = collect_transaction_snapshots(feature)
    impl_summary = extract_impl_summary(name)
    review_verdict = extract_review_verdict(name)

    feature["status"] = "done"
    archive_items.append(feature)
    archive_items.sort(key=lambda item: item.get("id", 0))
    data["features"] = [item for item in items if item is not feature]

    try:
        write_feature_list(data)
        write_archive(archive)
        move_report_to_archive(name, "impl")
        move_report_to_archive(name, "review")
        archive_feature_briefs(feature)
        append_history(feature, impl_summary=impl_summary, review_verdict=review_verdict)
        reset_current()
    except Exception as exc:
        try:
            rollback_transaction(snapshots)
        except Exception as rollback_exc:
            print(f"[FAIL] Rollback transaccional falló: {rollback_exc}", file=sys.stderr)
            exc.add_note(f"Rollback transaccional falló: {rollback_exc}")
        raise

    print(f"[OK] Feature {feature.get('id')} {name} cerrada y archivada")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
