# Design - harness_base_files

Este documento detalla las decisiones técnicas y el diseño de la solución para la implementación de los archivos base del arnés.

## Componentes y Archivos Impactados

### Archivos Nuevos
1. `init.ps1` (PowerShell Script):
   - Punto de entrada para entornos Windows.
   - Detecta de manera jerárquica:
     1. `.venv\Scripts\python.exe`
     2. `venv\Scripts\python.exe`
     3. `python` (sistema)
   - Ejecuta `validate_harness.py` pasando `@args` y propaga `$LASTEXITCODE`.
2. `init.sh` (Shell Script):
   - Punto de entrada para entornos Linux/WSL/macOS.
   - Detecta de manera jerárquica:
     1. `.venv/bin/python`
     2. `venv/bin/python`
     3. `python3` (sistema)
     4. `python` (sistema)
   - Ejecuta `validate_harness.py` pasando `"$@"` y propaga `$?`.
3. `docs/engineering/conventions/shared.md`:
   - Define las convenciones de codificación estándar: UTF-8, fin de línea LF, nombres en snake_case para archivos Python/scripts y camelCase/kebab-case para Node.js, y commits estructurados.
4. `docs/engineering/verification/shared.md`:
   - Define el flujo de verificación y comandos típicos para correr tests (`pytest`, `npm test`, etc.) y smoke tests.

## Firmas y Contratos
No se crean firmas de código Python ni endpoints nuevos en esta feature. Los scripts de shell actúan como adaptadores transparentes de CLI hacia `scripts/validate_harness.py`.

## Alternativas Descartadas
1. **Ejecutar `python` directamente sin buscar venv:**
   - *Por qué se descartó:* Si el proyecto tiene dependencias específicas instaladas en su venv (como `pytest` u otras bibliotecas), ejecutar con el intérprete global del sistema fallará o usará dependencias obsoletas.
2. **Forzar al usuario a activar manualmente el entorno virtual (`source .venv/bin/activate`):**
   - *Por qué se descartó:* Incrementa la fricción de inicio. El comando `./init.ps1` o `./init.sh` debe funcionar directamente "out of the box" para el usuario y para los agentes automáticos.

## Dudas y Asunciones
- **Asunción:** Si no existe `.venv` o `venv` en la raíz del proyecto, se asume que Python está disponible de forma global como `python` (en Windows) o `python3`/`python` (en Unix).
- **Asunción:** Los archivos de documentación técnica (`shared.md` de convenciones y verificación) se estructuran como plantillas genéricas transversales de alta calidad, listas para ser extendidas por cualquier proyecto que herede este arnés.
