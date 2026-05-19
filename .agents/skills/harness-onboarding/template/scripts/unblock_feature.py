from __future__ import annotations

import argparse
import sys

from harness_state import (
    CURRENT_PATH,
    FEATURE_LIST_PATH,
    HISTORY_PATH,
    active_features,
    append_history_event,
    features,
    find_feature,
    load_feature_list,
    render_active_current,
    reset_current,
    safe_write,
    write_current,
    write_feature_list,
)

VALID_TARGETS = {"in_progress", "pending"}


def find_blocked(items: list) -> object:
    blocked = active_features(items, "blocked")
    if len(blocked) != 1:
        raise ValueError("Debe existir exactamente una feature blocked o pasar id/name")
    return blocked[0]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Desbloquea una feature blocked y actualiza progress/current.md"
    )
    parser.add_argument("feature", nargs="?", help="id o name de la feature blocked; por defecto la unica blocked")
    parser.add_argument("--agent", required=True, help="rol que desbloquea la feature")
    parser.add_argument("--resolution", required=True, help="descripcion concreta de como se resolvio el bloqueo")
    parser.add_argument(
        "--to",
        default="in_progress",
        choices=list(VALID_TARGETS),
        dest="target",
        help="estado destino: in_progress (default) o pending",
    )
    args = parser.parse_args()

    data = load_feature_list()
    items = features(data)

    feature = find_feature(items, args.feature) if args.feature else find_blocked(items)

    if feature.get("status") != "blocked":
        raise ValueError(
            f"La feature {feature.get('id')} no esta blocked (status actual: {feature.get('status')!r})"
        )

    snapshot_fl = FEATURE_LIST_PATH.read_text(encoding="utf-8")
    snapshot_current = CURRENT_PATH.read_text(encoding="utf-8") if CURRENT_PATH.is_file() else None
    snapshot_history = HISTORY_PATH.read_text(encoding="utf-8") if HISTORY_PATH.is_file() else None

    if args.target == "in_progress":
        if active_features(items, "in_progress"):
            raise ValueError("Ya existe una feature in_progress; no se puede desbloquear hacia in_progress")
        feature["status"] = "in_progress"
        write_feature_list(data)
        write_current(render_active_current(feature, args.agent, status="in_progress"))
    else:
        feature["status"] = "pending"
        write_feature_list(data)
        reset_current()

    try:
        append_history_event(
            feature,
            "Desbloqueo",
            [
                f"Destino: {args.target}",
                f"Agente: {args.agent}",
                f"Resolucion: {args.resolution}",
            ],
        )
    except Exception:
        safe_write(FEATURE_LIST_PATH, snapshot_fl)
        if snapshot_current is None:
            if CURRENT_PATH.exists():
                CURRENT_PATH.unlink()
        else:
            safe_write(CURRENT_PATH, snapshot_current)
        if snapshot_history is None:
            if HISTORY_PATH.exists():
                HISTORY_PATH.unlink()
        else:
            safe_write(HISTORY_PATH, snapshot_history)
        raise

    print(f"[OK] Feature {feature.get('id')} {feature.get('name')} desbloqueada -> {args.target}")
    print(f"[OK] Resolucion: {args.resolution}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
