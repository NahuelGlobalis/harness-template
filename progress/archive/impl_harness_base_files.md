# Implementación — feature 1 (harness_base_files)

## Archivos modificados
- `init.ps1` (Nuevo)
- `init.sh` (Nuevo)
- `docs/engineering/conventions/shared.md` (Nuevo)
- `docs/engineering/verification/shared.md` (Nuevo)
- `progress/current.md` (Actualizado)

## Decisiones de diseño relevantes
- **init.ps1 / init.sh**: Se implementó una lógica de búsqueda genérica de entornos virtuales (`.venv` y `venv`) en el directorio raíz. Si existen, se utiliza el intérprete correspondiente para ejecutar el script de validación. Si no, se recurre al Python del sistema global. Los códigos de salida se propagan correctamente.
- **shared.md (Conventions)**: Se redactó un documento de convenciones de codificación abstracto y aplicable a cualquier tecnología (UTF-8, LF, nombres de archivo) con indicación explícita de que debe extenderse para cada tecnología específica.
- **shared.md (Verification)**: Se redactó una guía de verificación de software multitecnología proporcionando ejemplos concretos para Python (`pytest`), Node.js (`npm`/`yarn`/`pnpm`) y monorepos/workspaces.

## Output de validación
- `python scripts/validate_harness.py` corre exitosamente con 0 errores y 0 warnings:
```text
[OK]    Existe AGENTS.md
[OK]    Existe CHECKPOINTS.md
[OK]    Existe init.ps1
[OK]    Existe init.sh
...
[OK]    progress/ contiene solo archivos permitidos
[OK]    Arnés válido: 0 errores, 0 warning(s)
```
