from __future__ import annotations

import json
from pathlib import Path

import pytest

import validate_harness


@pytest.fixture()
def isolated_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    (tmp_path / "progress").mkdir()
    (tmp_path / "progress" / "archive").mkdir()
    (tmp_path / "progress" / "history.md").write_text("# Historia\n", encoding="utf-8")
    (tmp_path / "progress" / "current.md").write_text(
        "# Sesion activa\n\n**Estado:** sin_tarea\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(validate_harness, "ROOT", tmp_path)
    validate_harness.failures.clear()
    validate_harness.warnings.clear()
    return tmp_path


def write_feature_file(root: Path, features: list[dict[str, object]]) -> None:
    payload = {
        "project": "harness-template",
        "description": "tests",
        "rules": {
            "reports_required_from_id": 99,
            "valid_status": ["pending", "in_progress", "done", "blocked"],
        },
        "features": features,
    }
    (root / "feature_list.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def test_validate_feature_list_fails_if_in_progress_and_blocked_coexist(isolated_root: Path) -> None:
    write_feature_file(
        isolated_root,
        [
            {
                "id": 1,
                "name": "feature_one",
                "title": "One",
                "description": "Primera feature",
                "acceptance": ["ok"],
                "status": "in_progress",
            },
            {
                "id": 2,
                "name": "feature_two",
                "title": "Two",
                "description": "Segunda feature",
                "acceptance": ["ok"],
                "status": "blocked",
            },
        ],
    )

    validate_harness.validate_feature_list()

    assert "No puede haber features in_progress y blocked al mismo tiempo" in validate_harness.failures


def test_validate_feature_list_does_not_emit_ok_for_mutual_exclusion_violation(
    isolated_root: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    write_feature_file(
        isolated_root,
        [
            {
                "id": 1,
                "name": "feature_one",
                "title": "One",
                "description": "Primera feature",
                "acceptance": ["ok"],
                "status": "in_progress",
            },
            {
                "id": 2,
                "name": "feature_two",
                "title": "Two",
                "description": "Segunda feature",
                "acceptance": ["ok"],
                "status": "blocked",
            },
        ],
    )
    ok_messages: list[str] = []
    monkeypatch.setattr(validate_harness, "ok", ok_messages.append)

    validate_harness.validate_feature_list()

    assert "feature_list.json mantiene como máximo una feature in_progress" not in ok_messages


def test_validate_current_progress_requires_blocked_state_to_be_reflected(
    isolated_root: Path,
) -> None:
    features = [
        {
            "id": 3,
            "name": "feature_three",
            "title": "Three",
            "description": "Feature bloqueada",
            "acceptance": ["ok"],
            "status": "blocked",
        }
    ]
    write_feature_file(isolated_root, features)
    (isolated_root / "progress" / "current.md").write_text(
        "# Sesion activa\n\n**Feature ID:** 0\n**Feature name:** sin_tarea\n**Estado:** sin_tarea\n",
        encoding="utf-8",
    )

    validate_harness.validate_current_progress(features, {"pending", "in_progress", "done", "blocked"})

    assert (
        "feature_list.json tiene una feature blocked pero progress/current.md no refleja el bloqueo"
        in validate_harness.failures
    )


def test_validate_progress_hygiene_detects_orphan_files_without_active_session(
    isolated_root: Path,
) -> None:
    write_feature_file(isolated_root, [])
    (isolated_root / "progress" / "impl_orphan.md").write_text("orphan", encoding="utf-8")

    validate_harness.validate_progress_hygiene([])

    assert "Archivos huérfanos en progress/ sin sesión activa: impl_orphan.md" in validate_harness.failures


def test_validate_feature_list_detects_duplicate_archive_entries(isolated_root: Path) -> None:
    write_feature_file(
        isolated_root,
        [
            {
                "id": 4,
                "name": "feature_four",
                "title": "Four",
                "description": "Activa",
                "acceptance": ["ok"],
                "status": "pending",
            }
        ],
    )
    archive = {
        "project": "harness-template",
        "description": "archive",
        "features": [
            {
                "id": 4,
                "name": "feature_four",
                "title": "Four",
                "description": "Archivada",
                "acceptance": ["ok"],
                "status": "done",
            }
        ],
    }
    (isolated_root / "feature_list.archive.json").write_text(
        json.dumps(archive, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    validate_harness.validate_feature_list()

    assert "Archive feature id duplicado con feature_list.json: 4" in validate_harness.failures
