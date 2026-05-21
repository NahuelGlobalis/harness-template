from __future__ import annotations

import argparse
import sys
from pathlib import Path

from harness_state import (
    ARCHIVE_PATH,
    CURRENT_PATH,
    FEATURE_LIST_PATH,
    HISTORY_PATH,
    append_history_event,
    features,
    find_feature,
    load_archive,
    load_feature_list,
    reset_current,
    restore_snapshot,
    snapshot_text,
    write_archive,
    write_feature_list,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Cancela una feature pending o blocked y la mueve al archivo"
    )
    parser.add_argument("feature", nargs="?", help="id o name de la feature")
    parser.add_argument("--reason", required=True, help="Motivo de cancelación")
    parser.add_argument("--agent", required=True, help="Rol que ejecuta la cancelación")
    args = parser.parse_args()

    data = load_feature_list()
    items = features(data)
    feature = find_feature(items, args.feature)

    allowed = ("pending", "blocked")
    if feature.get("status") not in allowed:
        raise ValueError(
            f"Solo se puede cancelar una feature pending o blocked; "
            f"status actual: {feature.get('status')!r}"
        )

    archive = load_archive()
    archive_items = features(archive)
    if any(
        item.get("id") == feature.get("id") or item.get("name") == feature.get("name")
        for item in archive_items
    ):
        raise ValueError("La feature ya existe en feature_list.archive.json")

    snapshots: dict[Path, str | None] = {
        FEATURE_LIST_PATH: snapshot_text(FEATURE_LIST_PATH),
        ARCHIVE_PATH: snapshot_text(ARCHIVE_PATH),
        CURRENT_PATH: snapshot_text(CURRENT_PATH),
        HISTORY_PATH: snapshot_text(HISTORY_PATH),
    }

    was_blocked = feature.get("status") == "blocked"
    feature["status"] = "cancelled"
    archive_items.append(feature)
    archive_items.sort(key=lambda item: item.get("id", 0))
    data["features"] = [item for item in items if item is not feature]

    try:
        write_feature_list(data)
        write_archive(archive)
        if was_blocked:
            reset_current()
        append_history_event(
            feature,
            title="Cancelación",
            details=[
                f"Agente: {args.agent}",
                f"Motivo: {args.reason}",
            ],
        )
    except Exception as exc:
        try:
            for path, content in snapshots.items():
                restore_snapshot(path, content)
        except Exception as rollback_exc:
            print(f"[FAIL] Rollback transaccional falló: {rollback_exc}", file=sys.stderr)
            exc.add_note(f"Rollback transaccional falló: {rollback_exc}")
        raise

    print(f"[OK] Feature {feature.get('id')} {feature.get('name')} cancelada y archivada")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
