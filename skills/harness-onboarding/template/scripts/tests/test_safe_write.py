from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from harness_state import safe_write


def test_safe_write_creates_file(tmp_path: Path) -> None:
    dest = tmp_path / "out.md"
    safe_write(dest, "hola mundo")
    assert dest.read_text(encoding="utf-8") == "hola mundo"


def test_safe_write_leaves_no_tmp_on_success(tmp_path: Path) -> None:
    dest = tmp_path / "out.md"
    safe_write(dest, "contenido")
    tmp = dest.with_suffix(dest.suffix + ".tmp")
    assert not tmp.exists()


def test_safe_write_original_survives_tmp_write_failure(tmp_path: Path) -> None:
    dest = tmp_path / "data.json"
    dest.write_text("original", encoding="utf-8")

    def exploding_write(self: Path, content: str, **kwargs: object) -> None:
        raise OSError("disco lleno simulado")

    with patch.object(Path, "write_text", exploding_write):
        with pytest.raises(OSError):
            safe_write(dest, "nuevo contenido")

    assert dest.read_text(encoding="utf-8") == "original"


def test_safe_write_overwrites_existing_file(tmp_path: Path) -> None:
    dest = tmp_path / "out.md"
    dest.write_text("viejo", encoding="utf-8")
    safe_write(dest, "nuevo")
    assert dest.read_text(encoding="utf-8") == "nuevo"
