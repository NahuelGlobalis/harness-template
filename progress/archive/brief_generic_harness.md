# Brief: Conversión del Arnés a Genérico (Handoff para Implementer)

## Origen

**Rol:** Architect
**Destinatario:** Implementer
**Fecha:** 2026-05-19

## Contexto

El repositorio actual es una plantilla de arnés (`harness-template`) diseñada para ser copiada a nuevos proyectos. Sin embargo, contiene referencias específicas a otros proyectos (`deepagents-api`, `deepagents-web`), faltan scripts de inicialización (`init.ps1`, `init.sh`), faltan archivos de convenciones requeridos, y las pruebas unitarias fallan debido a un acoplamiento directo con la documentación física real de capas que no existen en este repo genérico.

Este brief proporciona el prompt de instrucciones detalladas para que un LLM (en rol de **Implementer**) lea el repositorio y realice las actualizaciones necesarias de manera limpia y robusta, soportando tanto proyectos Python como Node.js y monorepos.

---

## Recomendación (Prompt de Implementación)

Copia y utiliza el siguiente prompt estructurado para la fase de implementación:

```markdown
# PROMPT PARA IMPLEMENTADOR DE ARNÉS GENÉRICO

Actúa como un **Implementer** senior y realiza los cambios necesarios para convertir este arnés en genérico, multi-tecnología (Python, Node.js, monorepos, etc.) y libre de errores. Sigue estrictamente las especificaciones de abajo.

---

## 1. Archivos a Crear

### A. Scripts de Inicialización (Root del Repo)
Crea los archivos iniciales para validar el estado del arnés. Deben buscar intérpretes de Python de forma genérica para ejecutar `scripts/validate_harness.py`.

#### [NEW] `init.ps1` (PowerShell)
- Verifica si existe un entorno virtual local de Python buscando en orden de prioridad:
  1. `.venv\Scripts\python.exe`
  2. `venv\Scripts\python.exe`
- Si existe, ejecuta `& $PATH_AL_VENV scripts/validate_harness.py @args`.
- Si no existe, ejecuta `python scripts/validate_harness.py @args` (usando el Python del sistema).
- Propaga el código de salida (`exit $LASTEXITCODE`).

#### [NEW] `init.sh` (WSL/Linux)
- Verifica si existe un entorno virtual local de Python buscando en orden de prioridad:
  1. `.venv/bin/python`
  2. `venv/bin/python`
- Si existe, ejecuta `$PATH_AL_VENV scripts/validate_harness.py "$@"`.
- Si no existe, ejecuta `python3 scripts/validate_harness.py "$@"` o `python scripts/validate_harness.py "$@"`.
- Propaga el código de salida (`exit $?`).

---

### B. Documentación de Ingeniería Base (`docs/engineering/`)
Crea los archivos que exige el validador del arnés con contenido de alta calidad y genérico.

#### [NEW] `docs/engineering/conventions/shared.md`
- Define convenciones estándar de codificación transversales (por ejemplo: nombres de archivos en `snake_case` o `kebab-case`, codificación UTF-8, fin de línea LF, evitar comentarios redundantes, uso de git commits descriptivos).
- Incluye una sección que aclare que estas convenciones deben ser extendidas y adaptadas para cada tecnología específica del proyecto (Python, Node.js, etc.).

#### [NEW] `docs/engineering/verification/shared.md`
- Define guías genéricas para la verificación del software antes del cierre de una feature (tests automáticos, reviews, smoke tests).
- Proporciona ejemplos de comandos para ejecutar pruebas en diferentes ecosistemas:
  - **Python:** `python -m pytest`
  - **Node.js:** `npm test` o `yarn test` o `pnpm test`
  - **Monorepos:** cómo ejecutar en subcarpetas o usar workspaces (ej. `npm run test --workspaces`).

---

## 2. Archivos a Renombrar o Modificar

### A. Documentación de Operaciones
#### [MODIFY] `docs/operations/docker.md` (anteriormente `docs/operations/example.md`)
- Renombra el archivo `docs/operations/example.md` a `docs/operations/docker.md` para resolver la discrepancia con el índice global `docs/README.md`.
- Mantén el título y contenido del archivo sobre Docker como una guía/plantilla de ejemplo.

#### [MODIFY] `docs/README.md`
- Corrige la referencia de `docs/operations/docker.md` para que el estado sea correcto.
- Revisa las keys de grupo y asegúrate de que no haya referencias a repositorios específicos, utilizando términos generales como "código de producto" o "capas del proyecto".

---

### B. Actualizaciones de Scripts de Calidad e Higiene
#### [MODIFY] `scripts/validate_quality.py`
- Elimina las rutas hardcodeadas de `deepagents-api` y `deepagents-web`.
- Implementa una detección dinámica de carpetas de código de producto:
  - Escanea los directorios en la raíz del repositorio que **no** pertenezcan a la estructura propia del arnés (`.git`, `.venv`, `venv`, `docs`, `scripts`, `progress`, `agents`, `__pycache__`, `node_modules`).
- Soporta múltiples ecosistemas y lenguajes en los escaneos de calidad (para verificar debug output, TODOs y tamaño de archivos):
  - **Extensiones escaneadas:** `.py`, `.ts`, `.tsx`, `.js`, `.jsx`, `.go`, `.java`.
  - **Detección de debug outputs específica:**
    - `.py` -> buscar `print(`
    - `.js`, `.jsx`, `.ts`, `.tsx` -> buscar `console.log` o similar
    - `.go` -> buscar `fmt.Print` o similar
    - `.java` -> buscar `System.out.print`
  - **Ignorar carpetas de build/dependencias:** Asegurar que `node_modules`, `dist`, `build`, `.next`, `target`, `bin`, y directorios similares de caché/venv estén completamente excluidos del escaneo.
- La validación del sentido de las dependencias (`routers` no debe importar de `tools/`) solo se debe ejecutar si se encuentra un directorio llamado `routers` en alguno de los directorios escaneados de forma recursiva.

---

### C. Desacoplamiento de Pruebas Unitarias de Documentación
#### [MODIFY] `scripts/tests/test_docs_for.py`
- Los tests unitarios actualmente fallan porque intentan validar la estructura física de documentación del monorepo (`api`, `client-agents`, etc.) directamente sobre el archivo `docs/README.md` real, el cual ya no contiene estas claves.
- **Implementa un fixture de Pytest** que escriba un `README.md` temporal simulado (mock) con secciones (`harness`, `engineering`), keys (`shared`, `api`, `client-agents`, `system-agents`) y rutas ficticias en un directorio temporal (`tmp_path`).
- Usa `monkeypatch` para redefinir `docs_for.README_PATH` y `docs_for.DOCS_DIR` apuntando al directorio temporal con el mock.
- Asegúrate de que las pruebas unitarias que validan la lógica del parser (`test_parse_implementation_routing_has_api_docs`, `test_engineering_uses_only_technical_keys`, `test_json_payload_shape_for_api_route`, etc.) pasen de forma exitosa usando este entorno simulado.
- Adapta `test_all_canonical_routes_exist` para que se ejecute sobre el `README.md` de producción pero omitiendo o resolviendo correctamente la validación de archivos reales sin causar fallos debido a archivos opcionales.

---

### D. Ajustes de Documentos de Soporte del Arnés
Revisa y limpia las referencias a `deepagents-api` o archivos específicos de Python en la documentación operativa del arnés:
- `docs/harness/lifecycle.md`: Ajusta la sección de inicialización para reflejar la resolución genérica de Python.
- `docs/quality/gardening.md`: Reemplaza la referencia a `deepagents-api/agents/` por términos genéricos de carpetas de código de producto.
- `docs/harness/ticketing.md`: Cambia los ejemplos de aceptación del ticket para que usen una estructura de archivos genérica (ej. `src/` o `apps/` en vez de `deepagents-api/`).

---

## 3. Criterios de Aceptación (Definición de Hecho)

- [ ] **Tests de Pytest:** Ejecutar `python -m pytest` y verificar que el 100% de los tests (incluyendo `test_docs_for.py`) pasen correctamente.
- [ ] **Validación del Arnés:** Ejecutar `python scripts/validate_harness.py` o `./init.ps1` y verificar que el estado sea verde (`0 errores`).
- [ ] **Validación de Calidad:** Ejecutar `python scripts/validate_quality.py` y verificar que no lance fallos de calidad (o que pase exitosamente).
- [ ] **Multi-tecnología:** Los scripts y validaciones no asumen que el código del producto es exclusivamente Python, sino que ignoran directorios estándar de Node (`node_modules`) y realizan escaneos correctos según la extensión del archivo.
```
