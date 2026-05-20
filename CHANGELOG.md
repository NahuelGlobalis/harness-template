# Changelog

Todos los cambios notables de este repositorio se documentan en este archivo.
Formato basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/).

---

## [Unreleased] — 2026-05-20

### Added
- **harness-onboarding skill**: Skill completa para la instalación y configuración automática del arnés de agentes de IA en repositorios destino.
  - Detección automática del stack tecnológico del proyecto.
  - Adaptación de archivos genéricos del template al contexto real del proyecto.
  - Scripts de validación de calidad (`validate_quality.py`) y de harness (`validate_harness.py`).
  - Estructura completa del template desplegable: `docs/`, `progress/`, `scripts/`, `agents/`, `AGENTS.md`, `CHECKPOINTS.md`, `feature_list.json`, `init.ps1`, `init.sh`.
  - Script de copia automatizado `copy-files.ps1`.
  - Definición de la skill en `SKILL.md` con instrucciones para 4 fases: Análisis, Personalización, Validación e Informe.
