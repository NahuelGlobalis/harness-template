from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

import block_feature
import cancel_feature
import close_feature
import harness_state
import open_feature
import unblock_feature


@pytest.fixture()
def harness_repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    (tmp_path / "progress" / "archive").mkdir(parents=True)
    (tmp_path / "docs" / "harness" / "templates" / "progress").mkdir(parents=True)

    current_active = (
        "# Sesion activa\n\n"
        "**Feature ID:** <id>\n"
        "**Feature name:** <feature_name>\n"
        "**Agente:** <role>\n"
        "**Inicio:** <yyyy-mm-dd>\n"
        "**Estado:** in_progress\n\n"
        "## Contexto\n"
        "- <contexto breve de la tarea>\n\n"
        "## Plan\n"
        "- <paso verificable>\n\n"
        "## Implementado\n"
        "- <cambio realizado>\n\n"
        "## Bloqueos\n"
        "- Ninguno\n"
    )
    current_empty = (
        "# Sesion activa\n\n"
        "**Feature ID:** 0\n"
        "**Feature name:** sin_tarea\n"
        "**Agente:** -\n"
        "**Inicio:** -\n"
        "**Estado:** sin_tarea\n"
    )
    (tmp_path / "docs" / "harness" / "templates" / "progress" / "current.active.md").write_text(
        current_active,
        encoding="utf-8",
    )
    (tmp_path / "docs" / "harness" / "templates" / "progress" / "current.empty.md").write_text(
        current_empty,
        encoding="utf-8",
    )
    (tmp_path / "progress" / "current.md").write_text(current_empty, encoding="utf-8")
    (tmp_path / "progress" / "history.md").write_text("# Historia\n", encoding="utf-8")

    feature_list = {
        "project": "harness-template",
        "description": "tests",
        "rules": {
            "reports_required_from_id": 1,
            "valid_status": ["pending", "in_progress", "done", "blocked"],
        },
        "features": [],
    }
    (tmp_path / "feature_list.json").write_text(
        json.dumps(feature_list, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(harness_state, "ROOT", tmp_path)
    monkeypatch.setattr(harness_state, "FEATURE_LIST_PATH", tmp_path / "feature_list.json")
    monkeypatch.setattr(harness_state, "ARCHIVE_PATH", tmp_path / "feature_list.archive.json")
    monkeypatch.setattr(harness_state, "CURRENT_PATH", tmp_path / "progress" / "current.md")
    monkeypatch.setattr(harness_state, "HISTORY_PATH", tmp_path / "progress" / "history.md")
    monkeypatch.setattr(harness_state, "PROGRESS_ARCHIVE_PATH", tmp_path / "progress" / "archive")
    monkeypatch.setattr(
        harness_state,
        "CURRENT_ACTIVE_TEMPLATE",
        tmp_path / "docs" / "harness" / "templates" / "progress" / "current.active.md",
    )
    monkeypatch.setattr(
        harness_state,
        "CURRENT_EMPTY_TEMPLATE",
        tmp_path / "docs" / "harness" / "templates" / "progress" / "current.empty.md",
    )

    monkeypatch.setattr(close_feature, "ROOT", tmp_path)
    monkeypatch.setattr(close_feature, "FEATURE_LIST_PATH", tmp_path / "feature_list.json")
    monkeypatch.setattr(close_feature, "ARCHIVE_PATH", tmp_path / "feature_list.archive.json")
    monkeypatch.setattr(close_feature, "CURRENT_PATH", tmp_path / "progress" / "current.md")
    monkeypatch.setattr(close_feature, "HISTORY_PATH", tmp_path / "progress" / "history.md")
    monkeypatch.setattr(close_feature, "PROGRESS_ARCHIVE_PATH", tmp_path / "progress" / "archive")
    monkeypatch.setattr(open_feature, "FEATURE_LIST_PATH", tmp_path / "feature_list.json")
    monkeypatch.setattr(open_feature, "CURRENT_PATH", tmp_path / "progress" / "current.md")
    monkeypatch.setattr(block_feature, "FEATURE_LIST_PATH", tmp_path / "feature_list.json")
    monkeypatch.setattr(block_feature, "CURRENT_PATH", tmp_path / "progress" / "current.md")
    monkeypatch.setattr(unblock_feature, "FEATURE_LIST_PATH", tmp_path / "feature_list.json")
    monkeypatch.setattr(unblock_feature, "CURRENT_PATH", tmp_path / "progress" / "current.md")
    monkeypatch.setattr(cancel_feature, "FEATURE_LIST_PATH", tmp_path / "feature_list.json")
    monkeypatch.setattr(cancel_feature, "ARCHIVE_PATH", tmp_path / "feature_list.archive.json")
    monkeypatch.setattr(cancel_feature, "CURRENT_PATH", tmp_path / "progress" / "current.md")
    monkeypatch.setattr(cancel_feature, "HISTORY_PATH", tmp_path / "progress" / "history.md")

    return tmp_path


def write_feature_list(repo: Path, features: list[dict[str, object]]) -> None:
    payload = json.loads((repo / "feature_list.json").read_text(encoding="utf-8"))
    payload["features"] = features
    (repo / "feature_list.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def read_feature_list(repo: Path) -> dict[str, object]:
    return json.loads((repo / "feature_list.json").read_text(encoding="utf-8"))


def test_open_feature_opens_pending_feature(harness_repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    write_feature_list(
        harness_repo,
        [
            {
                "id": 7,
                "name": "harness_flow",
                "title": "Harness flow",
                "description": "Abrir feature.",
                "acceptance": ["El script abre la feature"],
                "status": "pending",
            }
        ],
    )

    monkeypatch.setattr(sys, "argv", ["open_feature.py", "7", "--agent", "Implementer"])
    assert open_feature.main() == 0

    feature = read_feature_list(harness_repo)["features"][0]
    assert feature["status"] == "in_progress"
    current = (harness_repo / "progress" / "current.md").read_text(encoding="utf-8")
    assert "**Feature ID:** 7" in current
    assert "**Estado:** in_progress" in current


def test_open_feature_rolls_back_if_current_write_fails(
    harness_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    write_feature_list(
        harness_repo,
        [
            {
                "id": 16,
                "name": "open_rollback",
                "title": "Open rollback",
                "description": "Abrir con rollback.",
                "acceptance": ["El script revierte feature_list y current.md"],
                "status": "pending",
            }
        ],
    )
    original_current = (harness_repo / "progress" / "current.md").read_text(encoding="utf-8")

    def explode(*args: object, **kwargs: object) -> None:
        raise OSError("fallo simulado")

    monkeypatch.setattr(open_feature, "write_current", explode)
    monkeypatch.setattr(sys, "argv", ["open_feature.py", "16", "--agent", "Implementer"])

    with pytest.raises(OSError, match="fallo simulado"):
        open_feature.main()

    feature = read_feature_list(harness_repo)["features"][0]
    assert feature["status"] == "pending"
    assert (harness_repo / "progress" / "current.md").read_text(encoding="utf-8") == original_current


def test_block_feature_updates_current_with_block_reason(
    harness_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    write_feature_list(
        harness_repo,
        [
            {
                "id": 8,
                "name": "blocked_flow",
                "title": "Blocked flow",
                "description": "Bloquear feature.",
                "acceptance": ["El script bloquea la feature"],
                "status": "in_progress",
            }
        ],
    )

    monkeypatch.setattr(
        sys,
        "argv",
        ["block_feature.py", "8", "--reason", "Falta credencial", "--agent", "Reviewer"],
    )
    assert block_feature.main() == 0

    feature = read_feature_list(harness_repo)["features"][0]
    assert feature["status"] == "blocked"
    current = (harness_repo / "progress" / "current.md").read_text(encoding="utf-8")
    assert "**Estado:** blocked" in current
    assert "Falta credencial" in current


def test_block_feature_rolls_back_if_current_write_fails(
    harness_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    write_feature_list(
        harness_repo,
        [
            {
                "id": 17,
                "name": "block_rollback",
                "title": "Block rollback",
                "description": "Bloquear con rollback.",
                "acceptance": ["El script revierte feature_list y current.md"],
                "status": "in_progress",
            }
        ],
    )
    original_current = harness_state.render_active_current(
        {
            "id": 17,
            "name": "block_rollback",
            "description": "Bloquear con rollback.",
            "acceptance": ["El script revierte feature_list y current.md"],
        },
        "Implementer",
    )
    (harness_repo / "progress" / "current.md").write_text(original_current, encoding="utf-8")

    def explode(*args: object, **kwargs: object) -> None:
        raise OSError("fallo simulado")

    monkeypatch.setattr(block_feature, "write_current", explode)
    monkeypatch.setattr(
        sys,
        "argv",
        ["block_feature.py", "17", "--reason", "Falta credencial", "--agent", "Reviewer"],
    )

    with pytest.raises(OSError, match="fallo simulado"):
        block_feature.main()

    feature = read_feature_list(harness_repo)["features"][0]
    assert feature["status"] == "in_progress"
    assert (harness_repo / "progress" / "current.md").read_text(encoding="utf-8") == original_current


def test_unblock_feature_to_pending_persists_resolution(
    harness_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    write_feature_list(
        harness_repo,
        [
            {
                "id": 9,
                "name": "unblock_flow",
                "title": "Unblock flow",
                "description": "Desbloquear feature.",
                "acceptance": ["El script desbloquea la feature"],
                "status": "blocked",
            }
        ],
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "unblock_feature.py",
            "9",
            "--agent",
            "Implementer",
            "--resolution",
            "Se cargo el secreto faltante",
            "--to",
            "pending",
        ],
    )
    assert unblock_feature.main() == 0

    feature = read_feature_list(harness_repo)["features"][0]
    assert feature["status"] == "pending"
    current = (harness_repo / "progress" / "current.md").read_text(encoding="utf-8")
    assert "**Estado:** sin_tarea" in current
    history = (harness_repo / "progress" / "history.md").read_text(encoding="utf-8")
    assert "### Desbloqueo" in history
    assert "Resolucion: Se cargo el secreto faltante" in history


def test_unblock_feature_rolls_back_current_if_history_append_fails(
    harness_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    write_feature_list(
        harness_repo,
        [
            {
                "id": 12,
                "name": "unblock_rollback",
                "title": "Unblock rollback",
                "description": "Desbloquear con rollback.",
                "acceptance": ["El script revierte current.md"],
                "status": "blocked",
            }
        ],
    )
    original_current = harness_state.render_active_current(
        {
            "id": 12,
            "name": "unblock_rollback",
            "description": "Desbloquear con rollback.",
            "acceptance": ["El script revierte current.md"],
        },
        "Reviewer",
        status="blocked",
        block_reason="Dependencia externa pendiente",
    )
    (harness_repo / "progress" / "current.md").write_text(original_current, encoding="utf-8")

    def explode(*args: object, **kwargs: object) -> None:
        raise OSError("fallo simulado")

    monkeypatch.setattr(unblock_feature, "append_history_event", explode)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "unblock_feature.py",
            "12",
            "--agent",
            "Implementer",
            "--resolution",
            "Se resolvio la dependencia",
            "--to",
            "pending",
        ],
    )

    with pytest.raises(OSError, match="fallo simulado"):
        unblock_feature.main()

    feature = read_feature_list(harness_repo)["features"][0]
    assert feature["status"] == "blocked"
    assert (harness_repo / "progress" / "current.md").read_text(encoding="utf-8") == original_current


def test_unblock_feature_rolls_back_history_if_append_fails(
    harness_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    write_feature_list(
        harness_repo,
        [
            {
                "id": 15,
                "name": "unblock_history_rollback",
                "title": "Unblock history rollback",
                "description": "Verifica que history.md se revierte.",
                "acceptance": ["El script revierte history.md"],
                "status": "blocked",
            }
        ],
    )
    original_history = (harness_repo / "progress" / "history.md").read_text(encoding="utf-8")

    def explode(*args: object, **kwargs: object) -> None:
        raise OSError("fallo simulado")

    monkeypatch.setattr(unblock_feature, "append_history_event", explode)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "unblock_feature.py",
            "15",
            "--agent",
            "Implementer",
            "--resolution",
            "Se resolvio el bloqueo",
            "--to",
            "pending",
        ],
    )

    with pytest.raises(OSError, match="fallo simulado"):
        unblock_feature.main()

    assert (harness_repo / "progress" / "history.md").read_text(encoding="utf-8") == original_history


def test_unblock_feature_rolls_back_if_history_append_fails_when_to_in_progress(
    harness_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    write_feature_list(
        harness_repo,
        [
            {
                "id": 13,
                "name": "unblock_rollback_ip",
                "title": "Unblock rollback in_progress",
                "description": "Desbloquear hacia in_progress con rollback.",
                "acceptance": ["El script revierte feature_list y current.md"],
                "status": "blocked",
            }
        ],
    )
    original_current = harness_state.render_active_current(
        {
            "id": 13,
            "name": "unblock_rollback_ip",
            "description": "Desbloquear hacia in_progress con rollback.",
            "acceptance": ["El script revierte feature_list y current.md"],
        },
        "Reviewer",
        status="blocked",
        block_reason="Dependencia externa",
    )
    (harness_repo / "progress" / "current.md").write_text(original_current, encoding="utf-8")

    def explode(*args: object, **kwargs: object) -> None:
        raise OSError("fallo simulado")

    monkeypatch.setattr(unblock_feature, "append_history_event", explode)
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "unblock_feature.py",
            "13",
            "--agent",
            "Implementer",
            "--resolution",
            "Se resolvio la dependencia",
            "--to",
            "in_progress",
        ],
    )

    with pytest.raises(OSError, match="fallo simulado"):
        unblock_feature.main()

    feature = read_feature_list(harness_repo)["features"][0]
    assert feature["status"] == "blocked"
    assert (harness_repo / "progress" / "current.md").read_text(encoding="utf-8") == original_current


def test_close_feature_moves_reports_and_resets_current(
    harness_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    write_feature_list(
        harness_repo,
        [
            {
                "id": 10,
                "name": "close_flow",
                "title": "Close flow",
                "description": "Cerrar feature.",
                "acceptance": ["El script cierra la feature"],
                "status": "in_progress",
            }
        ],
    )
    (harness_repo / "progress" / "current.md").write_text(
        harness_state.render_active_current(
            {
                "id": 10,
                "name": "close_flow",
                "description": "Cerrar feature.",
                "acceptance": ["El script cierra la feature"],
            },
            "Reviewer",
        ),
        encoding="utf-8",
    )
    (harness_repo / "progress" / "impl_close_flow.md").write_text(
        "# Implementacion\n\n## Resumen\n\nSe cerro la feature.\n",
        encoding="utf-8",
    )
    (harness_repo / "progress" / "review_close_flow.md").write_text(
        "# Review\n\n**Veredicto:** APPROVED\n\n## Notas\n\nListo.\n",
        encoding="utf-8",
    )
    (harness_repo / "progress" / "brief_close_flow.md").write_text(
        "# Brief\n\nRelacionado con close_flow.\n",
        encoding="utf-8",
    )
    (harness_repo / "progress" / "brief_other_topic.md").write_text(
        "# Brief\n\nRelacionado con otra iniciativa.\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(sys, "argv", ["close_feature.py", "10"])
    assert close_feature.main() == 0

    assert read_feature_list(harness_repo)["features"] == []
    archive = json.loads((harness_repo / "feature_list.archive.json").read_text(encoding="utf-8"))
    assert archive["features"][0]["status"] == "done"
    assert (harness_repo / "progress" / "archive" / "impl_close_flow.md").is_file()
    assert (harness_repo / "progress" / "archive" / "review_close_flow.md").is_file()
    assert (harness_repo / "progress" / "archive" / "brief_close_flow.md").is_file()
    assert (harness_repo / "progress" / "brief_other_topic.md").is_file()
    current = (harness_repo / "progress" / "current.md").read_text(encoding="utf-8")
    assert "**Estado:** sin_tarea" in current


def test_close_feature_rolls_back_if_append_history_fails(
    harness_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    write_feature_list(
        harness_repo,
        [
            {
                "id": 11,
                "name": "rollback_flow",
                "title": "Rollback flow",
                "description": "Rollback.",
                "acceptance": ["El script revierte en error"],
                "status": "in_progress",
            }
        ],
    )
    original_current = harness_state.render_active_current(
        {
            "id": 11,
            "name": "rollback_flow",
            "description": "Rollback.",
            "acceptance": ["El script revierte en error"],
        },
        "Reviewer",
    )
    (harness_repo / "progress" / "current.md").write_text(original_current, encoding="utf-8")
    (harness_repo / "progress" / "impl_rollback_flow.md").write_text(
        "# Implementacion\n\n## Resumen\n\nCambio listo.\n",
        encoding="utf-8",
    )
    (harness_repo / "progress" / "review_rollback_flow.md").write_text(
        "# Review\n\n**Veredicto:** APPROVED\n",
        encoding="utf-8",
    )

    def explode(*args: object, **kwargs: object) -> None:
        raise OSError("fallo simulado")

    monkeypatch.setattr(close_feature, "append_history", explode)
    monkeypatch.setattr(sys, "argv", ["close_feature.py", "11"])

    with pytest.raises(OSError, match="fallo simulado"):
        close_feature.main()

    feature = read_feature_list(harness_repo)["features"][0]
    assert feature["status"] == "in_progress"
    assert not (harness_repo / "feature_list.archive.json").exists()
    assert (harness_repo / "progress" / "impl_rollback_flow.md").is_file()
    assert (harness_repo / "progress" / "review_rollback_flow.md").is_file()
    assert (harness_repo / "progress" / "current.md").read_text(encoding="utf-8") == original_current


def test_close_feature_rolls_back_archive_brief_on_failure(
    harness_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    write_feature_list(
        harness_repo,
        [
            {
                "id": 14,
                "name": "brief_rollback_flow",
                "title": "Brief rollback",
                "description": "Rollback de brief ya archivado.",
                "acceptance": ["El brief pre-existente en archive no se elimina"],
                "status": "in_progress",
            }
        ],
    )
    (harness_repo / "progress" / "impl_brief_rollback_flow.md").write_text(
        "# Implementacion\n\n## Resumen\n\nCambio listo.\n",
        encoding="utf-8",
    )
    (harness_repo / "progress" / "review_brief_rollback_flow.md").write_text(
        "# Review\n\n**Veredicto:** APPROVED\n",
        encoding="utf-8",
    )
    pre_existing_archive_brief = harness_repo / "progress" / "archive" / "brief_preexisting.md"
    pre_existing_archive_brief.write_text("brief preexistente en archive", encoding="utf-8")

    def explode(*args: object, **kwargs: object) -> None:
        raise OSError("fallo simulado")

    monkeypatch.setattr(close_feature, "append_history", explode)
    monkeypatch.setattr(sys, "argv", ["close_feature.py", "14"])

    with pytest.raises(OSError, match="fallo simulado"):
        close_feature.main()

    assert pre_existing_archive_brief.read_text(encoding="utf-8") == "brief preexistente en archive"


def test_cancel_feature_pending_moves_to_archive(
    harness_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    write_feature_list(
        harness_repo,
        [
            {
                "id": 18,
                "name": "cancel_pending",
                "title": "Cancel pending",
                "description": "Feature a cancelar.",
                "acceptance": ["El script cancela la feature"],
                "status": "pending",
            }
        ],
    )

    monkeypatch.setattr(
        sys,
        "argv",
        ["cancel_feature.py", "18", "--reason", "Ya no aplica", "--agent", "Architect"],
    )
    assert cancel_feature.main() == 0

    assert read_feature_list(harness_repo)["features"] == []
    archive = json.loads((harness_repo / "feature_list.archive.json").read_text(encoding="utf-8"))
    assert archive["features"][0]["status"] == "cancelled"
    history = (harness_repo / "progress" / "history.md").read_text(encoding="utf-8")
    assert "Cancelación" in history
    assert "Ya no aplica" in history


def test_cancel_feature_blocked_resets_current(
    harness_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    write_feature_list(
        harness_repo,
        [
            {
                "id": 19,
                "name": "cancel_blocked",
                "title": "Cancel blocked",
                "description": "Feature bloqueada a cancelar.",
                "acceptance": ["El script cancela la feature bloqueada"],
                "status": "blocked",
            }
        ],
    )
    blocked_current = harness_state.render_active_current(
        {
            "id": 19,
            "name": "cancel_blocked",
            "description": "Feature bloqueada a cancelar.",
            "acceptance": ["El script cancela la feature bloqueada"],
        },
        "Implementer",
        status="blocked",
        block_reason="Dependencia externa",
    )
    (harness_repo / "progress" / "current.md").write_text(blocked_current, encoding="utf-8")

    monkeypatch.setattr(
        sys,
        "argv",
        ["cancel_feature.py", "19", "--reason", "Decisión de negocio", "--agent", "Architect"],
    )
    assert cancel_feature.main() == 0

    assert read_feature_list(harness_repo)["features"] == []
    archive = json.loads((harness_repo / "feature_list.archive.json").read_text(encoding="utf-8"))
    assert archive["features"][0]["status"] == "cancelled"
    current = (harness_repo / "progress" / "current.md").read_text(encoding="utf-8")
    assert "**Estado:** sin_tarea" in current


def test_cancel_feature_rolls_back_on_history_failure(
    harness_repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    write_feature_list(
        harness_repo,
        [
            {
                "id": 20,
                "name": "cancel_rollback",
                "title": "Cancel rollback",
                "description": "Feature para probar rollback de cancel.",
                "acceptance": ["El script revierte en error"],
                "status": "pending",
            }
        ],
    )
    original_feature_list = (harness_repo / "feature_list.json").read_text(encoding="utf-8")

    def explode(*args: object, **kwargs: object) -> None:
        raise OSError("fallo simulado")

    monkeypatch.setattr(cancel_feature, "append_history_event", explode)
    monkeypatch.setattr(
        sys,
        "argv",
        ["cancel_feature.py", "20", "--reason", "Rollback test", "--agent", "Architect"],
    )

    with pytest.raises(OSError, match="fallo simulado"):
        cancel_feature.main()

    assert (harness_repo / "feature_list.json").read_text(encoding="utf-8") == original_feature_list
    assert not (harness_repo / "feature_list.archive.json").exists()
