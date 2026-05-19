from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXCLUDED_ROOT_DIRS = {
    ".git",
    ".venv",
    "venv",
    "docs",
    "scripts",
    "progress",
    "agents",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    ".next",
    ".pytest_cache",
}

IGNORED_UNTRACKED_PREFIXES = (
    "progress/archive/",
)

IGNORED_SCAN_PARTS = {
    ".venv",
    ".venv-wsl",
    "__pycache__",
    ".pytest_cache",
    ".test-dist",
    "node_modules",
    "dist",
    "build",
    ".next",
    "target",
    "bin",
}

DEBUG_PATTERNS = {
    ".py": "print(",
    ".js": "console.log",
    ".jsx": "console.log",
    ".ts": "console.log",
    ".tsx": "console.log",
    ".go": "fmt.Print",
    ".java": "System.out.print",
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
    product_dirs = [d for d in ROOT.iterdir() if d.is_dir() and d.name not in EXCLUDED_ROOT_DIRS]
    
    product_files = []
    for d in product_dirs:
        for path in d.rglob("*"):
            if path.is_file():
                if not IGNORED_SCAN_PARTS.intersection(path.relative_to(ROOT).parts):
                    if path.suffix in DEBUG_PATTERNS:
                        product_files.append(path)
                        
    debug_outputs = []
    todos = []
    for path in product_files:
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            text = path.read_text(encoding="utf-8", errors="ignore")
            
        suffix = path.suffix
        pattern = DEBUG_PATTERNS[suffix]
        
        for line_number, line in enumerate(text.splitlines(), start=1):
            if pattern in line:
                debug_outputs.append(f"{path.relative_to(ROOT).as_posix()}:{line_number}")
            if re.search(r"(#|//|/\*)\s*TODO\b", line):
                todos.append(f"{path.relative_to(ROOT).as_posix()}:{line_number}")

    if debug_outputs:
        fail("Hay outputs de debug en el código: " + ", ".join(debug_outputs[:10]))
    else:
        ok("No hay outputs de debug en las carpetas de producto")

    if todos:
        fail("Hay TODO en código de producto: " + ", ".join(todos[:10]))
    else:
        ok("No hay TODO en código de producto")


def validate_golden_principles() -> None:
    max_lines = 300
    product_dirs = [d for d in ROOT.iterdir() if d.is_dir() and d.name not in EXCLUDED_ROOT_DIRS]
    
    product_files = []
    for d in product_dirs:
        for path in d.rglob("*"):
            if path.is_file():
                if not IGNORED_SCAN_PARTS.intersection(path.relative_to(ROOT).parts):
                    if path.suffix in DEBUG_PATTERNS:
                        product_files.append(path)
                        
    oversized = []
    for path in product_files:
        try:
            lines = len(path.read_text(encoding="utf-8", errors="ignore").splitlines())
        except Exception:
            lines = 0
        if lines > max_lines:
            oversized.append(f"{path.relative_to(ROOT).as_posix()} ({lines})")

    if oversized:
        warn("Golden #8: archivos >300 líneas: " + ", ".join(oversized[:5]))
    else:
        ok("Golden #8: ningún archivo excede 300 líneas")

    routers_dirs = []
    for d in product_dirs:
        for path in d.rglob("*"):
            if path.is_dir() and path.name == "routers":
                if not IGNORED_SCAN_PARTS.intersection(path.relative_to(ROOT).parts):
                    routers_dirs.append(path)

    dep_violations = []
    if routers_dirs:
        for routers_dir in routers_dirs:
            for path in routers_dir.rglob("*.py"):
                if IGNORED_SCAN_PARTS.intersection(path.relative_to(ROOT).parts):
                    continue
                try:
                    content = path.read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    content = ""
                if re.search(r"from\s+\.\.?tools", content) or re.search(
                    r"from\s+agents\.tools", content
                ):
                    dep_violations.append(path.relative_to(ROOT).as_posix())

        if dep_violations:
            warn("Golden #7: routers importan de tools/: " + ", ".join(dep_violations[:5]))
        else:
            ok("Golden #7: dependency direction correcta")
    else:
        ok("Golden #7: dependency direction no aplicable (sin carpeta routers)")


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
        path_parts = Path(relative_path).parts
        if IGNORED_SCAN_PARTS.intersection(path_parts):
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
