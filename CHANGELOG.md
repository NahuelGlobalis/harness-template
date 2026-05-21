# Changelog

Todos los cambios notables de este repositorio se documentan en este archivo.
Formato basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/).

---

## [Unreleased] — 2026-05-21 (MR !4)

### Changed
- **Estructura del repositorio**: Reorganización completa de la skill `harness-onboarding`.
  - Todos los archivos movidos desde `.agents/skills/harness-onboarding/` a `skills/harness-onboarding/` para alinearse con la convención de estructura del catálogo.
  - Archivos relocados: `SKILL.md`, `copy-files.ps1`, y todo el contenido de `template/` (incluyendo docs, scripts, progreso, y archivos de configuración).

### Added
- **harness-onboarding/README.md**: Nuevo archivo de documentación local para la skill, dirigido a desarrolladores humanos. Explica el propósito, stack requerido, y uso de la skill.

### Fixed
- **README.md** (raíz): Correcciones menores en la estructura de carpetas documentada.

---

## [Unreleased] — 2026-05-20 (MR !3)

### Changed
- **harness-onboarding/SKILL.md**: Actualización de la sección de compatibilidad por IDE — se reemplazó la lista anterior (Antigravity, Windsurf, Cursor, Cline, VS Code, OpenAI) por tabla y guías para 7 IDEs modernos: Windsurf (Cascade), Cursor, VS Code (GitHub Copilot), Cline, Roo Code, Claude Code y fallback universal `.agents/skills/`.
- **README.md**: Corrección de sintaxis en diagrama Mermaid y actualización de la sección "Cómo usar" para reflejar el descubrimiento automático de la skill en múltiples IDEs, con tabla de rutas por herramienta.

---

## [Initial] — 2026-05-20

### Added
- **harness-onboarding skill**: Skill completa para la instalación y configuración automática del arnés de agentes de IA en repositorios destino.
  - Detección automática del stack tecnológico del proyecto.
  - Adaptación de archivos genéricos del template al contexto real del proyecto.
  - Scripts de validación de calidad (`validate_quality.py`) y de harness (`validate_harness.py`).
  - Estructura completa del template desplegable: `docs/`, `progress/`, `scripts/`, `agents/`, `AGENTS.md`, `CHECKPOINTS.md`, `feature_list.json`, `init.ps1`, `init.sh`.
  - Script de copia automatizado `copy-files.ps1`.
  - Definición de la skill en `SKILL.md` con instrucciones para 4 fases: Análisis, Personalización, Validación e Informe.
