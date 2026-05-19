# Design - harness_cleanup_and_dynamic_checks

Este documento detalla las decisiones técnicas y el diseño de la solución para la limpieza, flexibilización y desacoplamiento de tests.

## Componentes y Archivos Impactados

### Archivos Modificados / Renombrados
1. `docs/operations/example.md` renombrado a `docs/operations/docker.md`.
2. `docs/README.md`:
   - Reemplazar la referencia de `docs/operations/example.md` por `docs/operations/docker.md`.
   - Limpiar claves de grupo y cualquier mención a `deepagents-*`.
3. `scripts/validate_quality.py`:
   - Implementar escaneo dinámico de directorios raíz del repositorio:
     - `dirs = [d for d in Path(".").iterdir() if d.is_dir() and d.name not in EXCLUDED_DIRS]`
     - Donde `EXCLUDED_DIRS = {".git", ".venv", "venv", "docs", "scripts", "progress", "agents", "__pycache__", "node_modules", "dist", "build", ".next", ".pytest_cache"}`.
   - En la función de escaneo de calidad de archivos, buscar patrones específicos según extensión:
     - `.py` -> `print(`
     - `.js`, `.jsx`, `.ts`, `.tsx` -> `console.log`
     - `.go` -> `fmt.Print`
     - `.java` -> `System.out.print`
   - Ejecutar la verificación de dependencias de `routers` (que no importe de `tools/`) de forma condicional, usando `any(d.name == "routers" for d in path.glob("**/routers"))` o similar.
4. `scripts/tests/test_docs_for.py`:
   - Agregar una fixture en pytest:
     ```python
     @pytest.fixture
     def mock_docs_env(tmp_path, monkeypatch):
         # Crear README.md mockeado
         # Crear archivos mockeados en tmp_path
         # Aplicar monkeypatch sobre docs_for.README_PATH y docs_for.DOCS_DIR
     ```
   - Modificar las pruebas para que dependan de este fixture mockeado.
   - Asegurarse de que `test_all_canonical_routes_exist` valida solo rutas genéricas existentes o se adapta para no fallar con archivos opcionales.
5. Ajustar referencias genéricas en:
   - `docs/harness/lifecycle.md`
   - `docs/quality/gardening.md`
   - `docs/harness/ticketing.md`

## Alternativas Descartadas
1. **Eliminar `example.md` en vez de renombrarlo:**
   - *Por qué se descartó:* Mantener un archivo de operaciones de ejemplo como Docker sirve de plantilla valiosa para nuevos proyectos creados a partir de este template.
2. **Hardcodear carpetas excluidas de cada framework en el script de calidad:**
   - *Por qué se descartó:* Se prefiere excluir dinámicamente la estructura conocida del arnés, tratando de forma genérica cualquier otra carpeta raíz como código de producto.
3. **Mantener `test_docs_for.py` acoplado al `README.md` real:**
   - *Por qué se descartó:* Si el `README.md` del nuevo proyecto se modifica (por ejemplo, eliminando capas o secciones que no existen), los tests unitarios del arnés fallarían innecesariamente. El mockeo con `tmp_path` aísla los tests del contenido real.

## Dudas y Asunciones
- **Asunción:** El script de calidad debe seguir buscando debug logs (prints/console.logs) y TODOs pero solo en las extensiones definidas.
- **Asunción:** Cualquier proyecto que herede este arnés mantendrá la estructura base de carpetas (`docs/`, `scripts/`, `progress/`, `agents/`, etc.).
