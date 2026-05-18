from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IGNORED_UNTRACKED_PREFIXES = (
    "deepagents-api/.pytest_cache/",
    "deepagents-api/.venv-wsl/",
    "deepagents-web/.test-dist/",
    "progress/archive/",
)
IGNORED_SCAN_PARTS = {
    ".venv",
    ".venv-wsl",
    "__pycache__",
    ".pytest_cache",
    ".test-dist",
    "node_modules",
}

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


def validate_product_hygiene() -> None:
    python_files = [
        path
        for path in (ROOT / "deepagents-api").rglob("*.py")
        if not IGNORED_SCAN_PARTS.intersection(path.relative_to(ROOT).parts)
    ]
    debug_prints = []
    for path in python_files:
        text = path.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if re.search(r"(^|[^\w])print\s*\(", line):
                debug_prints.append(f"{path.relative_to(ROOT).as_posix()}:{line_number}")

    if debug_prints:
        fail("Hay print() de debug en Python: " + ", ".join(debug_prints[:10]))
    else:
        ok("No hay print() de debug en deepagents-api")

    product_paths = [ROOT / "deepagents-api" / "agents", ROOT / "deepagents-web"]
    todos = []
    for base_path in product_paths:
        if not base_path.exists():
            continue
        for path in base_path.rglob("*"):
            if IGNORED_SCAN_PARTS.intersection(path.relative_to(ROOT).parts):
                continue
            if path.is_file() and path.suffix in {".py", ".ts", ".tsx"}:
                text = path.read_text(encoding="utf-8")
                for line_number, line in enumerate(text.splitlines(), start=1):
                    if re.search(r"(#|//|/\*)\s*TODO\b", line):
                        todos.append(f"{path.relative_to(ROOT).as_posix()}:{line_number}")

    if todos:
        fail("Hay TODO en código de producto: " + ", ".join(todos[:10]))
    else:
        ok("No hay TODO en código de producto")


def validate_golden_principles() -> None:
    max_lines = 300
    scan_dirs = [ROOT / "deepagents-api", ROOT / "deepagents-web"]
    oversized = []
    for base_path in scan_dirs:
        if not base_path.exists():
            continue
        for path in base_path.rglob("*"):
            if IGNORED_SCAN_PARTS.intersection(path.relative_to(ROOT).parts):
                continue
            if path.is_file() and path.suffix in {".py", ".ts", ".tsx"}:
                lines = len(path.read_text(encoding="utf-8", errors="ignore").splitlines())
                if lines > max_lines:
                    oversized.append(f"{path.relative_to(ROOT).as_posix()} ({lines})")

    if oversized:
        warn("Golden #8: archivos >300 líneas: " + ", ".join(oversized[:5]))
    else:
        ok("Golden #8: ningún archivo excede 300 líneas")

    routers_dir = ROOT / "deepagents-api" / "agents" / "routers"
    dep_violations = []
    if routers_dir.exists():
        for path in routers_dir.rglob("*.py"):
            if IGNORED_SCAN_PARTS.intersection(path.relative_to(ROOT).parts):
                continue
            content = path.read_text(encoding="utf-8", errors="ignore")
            if re.search(r"from\s+\.\.?tools", content) or re.search(
                r"from\s+agents\.tools", content
            ):
                dep_violations.append(path.relative_to(ROOT).as_posix())

    if dep_violations:
        warn("Golden #7: routers importan de tools/: " + ", ".join(dep_violations[:5]))
    else:
        ok("Golden #7: dependency direction correcta")


def validate_git_hygiene() -> None:
    if not (ROOT / ".git").exists():
        warn("No se encontró .git; se omite higiene de working tree")
        return

    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        warn("git no encontrado; se omite higiene de working tree")
        return

    if result.returncode != 0:
        warn("git status falló; se omite higiene de working tree")
        return

    untracked = []
    for line in result.stdout.splitlines():
        if not line.startswith("?? "):
            continue
        relative_path = line[3:]
        if relative_path.startswith(IGNORED_UNTRACKED_PREFIXES):
            continue
        untracked.append(relative_path)

    if untracked:
        warn("Archivos untracked detectados: " + ", ".join(untracked[:10]))
    else:
        ok("No hay archivos untracked sospechosos")


def main() -> int:
    os.chdir(ROOT)
    validate_product_hygiene()
    validate_golden_principles()
    validate_git_hygiene()

    if failures:
        print(f"[FAIL]  Calidad inválida: {len(failures)} error(es), {len(warnings)} warning(s)")
        return 1
    print(f"[OK]    Calidad válida: 0 errores, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
