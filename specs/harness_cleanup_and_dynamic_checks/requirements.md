# Requirements - harness_cleanup_and_dynamic_checks

Este documento define los requisitos funcionales y no funcionales para la limpieza y flexibilización del arnés, redactados bajo el estándar EARS.

## R1
El archivo `docs/operations/example.md` DEBE ser renombrado a `docs/operations/docker.md`.

## R2
El archivo `docs/README.md` DEBE ser modificado para apuntar a `docs/operations/docker.md` en lugar de `docs/operations/example.md`.

## R3
Las claves de grupo y referencias en `docs/README.md` NO DEBEN contener nombres de proyectos específicos como `deepagents-api` o `deepagents-web`.

## R4
El script `scripts/validate_quality.py` DEBE detectar dinámicamente las carpetas de código de producto en la raíz del repositorio, excluyendo las carpetas estructurales del arnés (`.git`, `.venv`, `venv`, `docs`, `scripts`, `progress`, `agents`, `__pycache__`, `node_modules`).

## R5
El script `scripts/validate_quality.py` DEBE escanear archivos con extensiones `.py`, `.ts`, `.tsx`, `.js`, `.jsx`, `.go` y `.java` para verificar debug outputs, TODOs y tamaño de archivos.

## R6
SI se procesa un archivo `.py`, ENTONCES `scripts/validate_quality.py` DEBE buscar debug outputs usando la cadena `print(`.

## R7
SI se procesa un archivo `.js`, `.jsx`, `.ts` o `.tsx`, ENTONCES `scripts/validate_quality.py` DEBE buscar debug outputs usando la cadena `console.log`.

## R8
SI se procesa un archivo `.go`, ENTONCES `scripts/validate_quality.py` DEBE buscar debug outputs usando la cadena `fmt.Print`.

## R9
SI se procesa un archivo `.java`, ENTONCES `scripts/validate_quality.py` DEBE buscar debug outputs usando la cadena `System.out.print`.

## R10
El script `scripts/validate_quality.py` DEBE ignorar completamente los directorios de compilación/dependencias (como `node_modules`, `dist`, `build`, `.next`, `target`, `bin`, `.pytest_cache`).

## R11
La validación de dirección de dependencias en `scripts/validate_quality.py` DEBE ejecutarse únicamente si se encuentra un directorio llamado `routers` recursivamente dentro de los directorios de producto escaneados.

## R12
Las pruebas unitarias en `scripts/tests/test_docs_for.py` DEBEN ejecutarse sobre un entorno mockeado utilizando un fixture de Pytest (`tmp_path` y `monkeypatch` sobre `docs_for.README_PATH` y `docs_for.DOCS_DIR`) para desacoplarse del README.md real de producción.

## R13
Los documentos de soporte del arnés (`docs/harness/lifecycle.md`, `docs/quality/gardening.md`, `docs/harness/ticketing.md`) DEBEN ser modificados para remover referencias a `deepagents-api` o rutas específicas de Python y usar términos genéricos (como `src/`, `apps/`, etc.).
