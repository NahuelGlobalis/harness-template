from __future__ import annotations

import argparse
import sys

from harness_state import (
    CURRENT_PATH,
    FEATURE_LIST_PATH,
    active_features,
    features,
    find_feature,
    load_feature_list,
    render_active_current,
    restore_snapshot,
    snapshot_text,
    write_current,
    write_feature_list,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Abre una feature pending y actualiza progress/current.md")
    parser.add_argument("feature", help="id o name de la feature pending")
    parser.add_argument("--agent", default="Implementer", help="rol que abre la feature")
    args = parser.parse_args()

    data = load_feature_list()
    items = features(data)
    if active_features(items, "in_progress"):
        raise ValueError("Ya existe una feature in_progress")
    if active_features(items, "blocked"):
        raise ValueError("Existe una feature blocked; resolverla antes de abrir otra")

    feature = find_feature(items, args.feature)
    if feature.get("status") != "pending":
        raise ValueError("Solo se puede abrir una feature pending")

    snapshot_fl = snapshot_text(FEATURE_LIST_PATH)
    snapshot_current = snapshot_text(CURRENT_PATH)
    feature["status"] = "in_progress"
    try:
        write_feature_list(data)
        write_current(render_active_current(feature, args.agent))
    except Exception:
        restore_snapshot(FEATURE_LIST_PATH, snapshot_fl)
        restore_snapshot(CURRENT_PATH, snapshot_current)
        raise

    print(f"[OK] Feature {feature.get('id')} {feature.get('name')} abierta")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
