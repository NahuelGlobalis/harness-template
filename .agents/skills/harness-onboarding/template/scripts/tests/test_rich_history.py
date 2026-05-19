from __future__ import annotations

from pathlib import Path

import pytest

import harness_state


@pytest.fixture()
def isolated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    progress = tmp_path / "progress"
    progress.mkdir()
    archive = progress / "archive"
    archive.mkdir()
    history = progress / "history.md"
    history.write_text("# Historia\n\n---\n", encoding="utf-8")
    monkeypatch.setattr(harness_state, "ROOT", tmp_path)
    monkeypatch.setattr(harness_state, "HISTORY_PATH", history)
    monkeypatch.setattr(harness_state, "PROGRESS_ARCHIVE_PATH", archive)
    return tmp_path


def test_extract_impl_summary_with_resumen_section(isolated: Path) -> None:
    impl = isolated / "progress" / "impl_feature_x.md"
    impl.write_text(
        "# Implementación — feature 99\n\n## Resumen\n\nCambio A fue implementado.\nCambio B también.\n\n## Archivos\n- foo.py\n",
        encoding="utf-8",
    )
    result = harness_state.extract_impl_summary("feature_x")
    assert "Cambio A fue implementado." in result
    assert "Cambio B también." in result
    assert "foo.py" not in result


def test_extract_impl_summary_fallback_no_resumen(isolated: Path) -> None:
    impl = isolated / "progress" / "impl_feature_x.md"
    impl.write_text(
        "# Implementación — feature 99\n\n## Archivos modificados\n- bar.py\n",
        encoding="utf-8",
    )
    result = harness_state.extract_impl_summary("feature_x")
    assert "bar.py" in result


def test_extract_impl_summary_missing_report(isolated: Path) -> None:
    result = harness_state.extract_impl_summary("feature_x")
    assert "No hay reporte" in result


def test_extract_review_verdict_with_verdict_and_notas(isolated: Path) -> None:
    review = isolated / "progress" / "review_feature_x.md"
    review.write_text(
        "# Review — feature 99\n\n**Veredicto:** APPROVED\n\n## Notas\n\nBuen trabajo.\n\n## Checkpoints\n- C1: [x]\n",
        encoding="utf-8",
    )
    result = harness_state.extract_review_verdict("feature_x")
    assert "APPROVED" in result
    assert "Buen trabajo." in result
    assert "C1" not in result


def test_extract_review_verdict_no_notas(isolated: Path) -> None:
    review = isolated / "progress" / "review_feature_x.md"
    review.write_text(
        "# Review — feature 99\n\n**Veredicto:** APPROVED\n",
        encoding="utf-8",
    )
    result = harness_state.extract_review_verdict("feature_x")
    assert "APPROVED" in result


def test_extract_review_verdict_missing_report(isolated: Path) -> None:
    result = harness_state.extract_review_verdict("feature_x")
    assert "No hay reporte" in result


def test_append_history_includes_impl_and_verdict(isolated: Path) -> None:
    feature = {"id": 99, "name": "feature_x"}
    harness_state.append_history(
        feature,
        impl_summary="Se implementó el cambio clave.",
        review_verdict="**Veredicto:** APPROVED",
    )
    text = harness_state.HISTORY_PATH.read_text(encoding="utf-8")
    assert "feature 99 feature_x" in text
    assert "Se implementó el cambio clave." in text
    assert "**Veredicto:** APPROVED" in text
    assert "Resumen implementación" in text
    assert "Veredicto review" in text


def test_append_history_defaults_when_no_reports(isolated: Path) -> None:
    feature = {"id": 99, "name": "feature_x"}
    harness_state.append_history(feature)
    text = harness_state.HISTORY_PATH.read_text(encoding="utf-8")
    assert "No hay reporte de implementación disponible." in text
    assert "No hay reporte de review disponible." in text
