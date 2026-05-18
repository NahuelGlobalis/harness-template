from __future__ import annotations

import argparse
import sys

from harness_state import (
    CURRENT_PATH,
    FEATURE_LIST_PATH,
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
    parser = argparse.ArgumentParser(description="Bloquea la feature in_progress y documenta el bloqueo")
    parser.add_argument("feature", nargs="?", help="id o name de la feature; por defecto usa la in_progress")
    parser.add_argument("--reason", required=True, help="causa concreta del bloqueo y desbloqueo requerido")
    parser.add_argument("--agent", default="Implementer", help="rol que bloquea la feature")
    args = parser.parse_args()

    data = load_feature_list()
    feature = find_feature(features(data), args.feature)
    if feature.get("status") != "in_progress":
        raise ValueError("Solo se puede bloquear una feature in_progress")

    snapshot_fl = snapshot_text(FEATURE_LIST_PATH)
    snapshot_current = snapshot_text(CURRENT_PATH)
    feature["status"] = "blocked"
    try:
        write_feature_list(data)
        write_current(render_active_current(feature, args.agent, status="blocked", block_reason=args.reason))
    except Exception:
        restore_snapshot(FEATURE_LIST_PATH, snapshot_fl)
        restore_snapshot(CURRENT_PATH, snapshot_current)
        raise

    print(f"[OK] Feature {feature.get('id')} {feature.get('name')} bloqueada")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
