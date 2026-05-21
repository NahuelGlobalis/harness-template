# Bitácora histórica (append-only)

> Cada vez que se cierra una sesión, su resumen se añade aquí.
> No edites entradas anteriores. Solo añades al final.

---

## 2026-05-04 — Bootstrap del proyecto
- **Agente:** Bootstrapper
- **Resultado:** arnés multi-agente creado (AGENTS.md, CHECKPOINTS.md, feature_list.json, docs/, agents/, progress/).

---

## 2026-05-05 a 2026-05-08 — Auth Phase 1 completa (features #1–#20)

Resumen por temática en archivos de progreso:
- `progress/auth.md` — OIDC/Authentik: config, sesión web, middleware, proxy (#1, #9, #10, #11, #12)
- `progress/backend.md` — Seguridad JWT, autorización, auditoría (#3, #4, #5, #6, #7, #8)
- `progress/infrastructure.md` — Docker Compose, blueprint, bootstrap, repo hygiene (#2, #12, #16, #20)
- `progress/fixes.md` — Bugs B1–B6 post-review (#13, #14, #15, #16, #17, #18)

**Estado final:** 178+ passed, 2 skipped. Todos los bugs críticos del review resueltos.

---

## 2026-05-09 — Feature #21: harness_consistency_hardening (DONE)

- **Agente:** Implementer / Reviewer / Orchestrator
- **Feature ID:** 21
- **Feature name:** harness_consistency_hardening
- **Inicio:** 2026-05-08
- **Veredicto:** APPROVED

### Resumen
- `scripts/validate_harness.py` centraliza validaciones automáticas del arnés.
- `init.sh` agrega entrada WSL/Linux equivalente a `init.ps1`.
- `docs/feature_list.schema.json` define schema formal para `feature_list.json`.
- `agents/orchestrator.md` formaliza el quinto rol (Orchestrator).
- `docs/harness.md` separa protocolo operativo de `AGENTS.md`.
- `CHECKPOINTS.md` separa controles automáticos de revisión humana.
- `progress/current.md` adopta campos estructurados parseables.

### Resultado del init de cierre
- `.\init.ps1` → exit code 0
- `deepagents-api`: 180 passed, 2 skipped
- `deepagents-web`: Agent fallbacks, Auth session, Auth routing, API bearer proxy y Frontend tests passed
---

## Feature #22 — doc_fix_mb_agents_references (2026-05-09)

**Feature ID:** 22
**Feature name:** doc_fix_mb_agents_references
**Agente:** Implementer
**Inicio:** 2026-05-09
**Estado:** in_progress

## Contexto

El directorio mb-agents/ fue renombrado. Las referencias a ese path deben
actualizarse a infrastructure/ (para .env) o infrastructure/client-agents/
(para markdowns de agentes/skills).

## Plan

- Reemplazar `mb-agents/` → `infrastructure/` en docs/operations.md (archivo .env)
- Reemplazar `mb-agents/` → `infrastructure/client-agents/` en docs/architecture.md (markdowns)
- Reemplazar `mb-agents/` → `infrastructure/` en infrastructure/README.md
- Reemplazar `mb-agents/` → `infrastructure/client-agents/` en deepagents-api/README.md
- Corregir `agents-example` → `client-agents` en AGENTS.md
- Agregar `__main__.py` al árbol en docs/conventions.md
- Verificar grep sin resultados en archivos target

## Implementado

- Todas las referencias `mb-agents/` corregidas en docs/, infrastructure/README.md, deepagents-api/README.md, AGENTS.md
- `__main__.py` agregado al árbol en docs/conventions.md
- `agents-example` → `client-agents` en AGENTS.md
- `infrastructure/.env` como path real en docs/operations.md y architecture.md
- config.py defaults corregidos (bug funcional)
- Test regression `test_auth_required_default_true` corregido con `_env_file=None`
- init.ps1: 180 passed, 2 skipped — verde
- Informe en progress/impl_doc_fix_mb_agents_references.md

## Bloqueos

—
---

## Feature #23 — refactor_large_files (2026-05-09)

**Feature ID:** 23
**Feature name:** refactor_large_files
**Agente:** Implementer
**Inicio:** 2026-05-09
**Estado:** in_progress

## Contexto
- Múltiples archivos violan GP #8 (max 300 líneas).
- api.py (1014), admin.py (773), agent-wizard.tsx (1973), interaction-map.tsx (657), factory.py (662), logging_handler.py (560).

## Plan
- Extraer `agents/schemas/api.py` con los Pydantic models de api.py
- Extraer `agents/service_state.py` con ServiceState y helpers
- Extraer `agents/routes/` con los endpoints en módulos
- Dividir admin.py en sub-routers: agents_router.py, skills_router.py, meta_router.py
- Extraer `agents/model_builder.py` de factory.py
- Extraer helpers de trace en logging_handler.py
- Dividir agent-wizard.tsx en pasos (step components)
- Dividir interaction-map.tsx en sub-componentes

## Implementado
- `agents/schemas/api.py` — Pydantic schemas extraídas de api.py
- `agents/api.py` — ServiceState mantenido inline (monkeypatch tests); GP#8 exception documentada
- `agents/routers/admin.py` — Reescrito como thin aggregator; sub-routers:
  - `admin_agents.py`, `admin_skills.py`, `admin_meta.py`, `admin_schemas.py`, `admin_helpers.py`
- `agents/factory.py` — GP#8 exception documentada; model_builder.py creado como referencia
- `agents/logging_handler.py` — GP#8 exception documentada
- `deepagents-web/components/agents/agent-wizard.tsx` — Reducido a 292 líneas; step components extraídos:
  - `wizard-steps-basic.tsx` (StepBasics, ModeCard, StepPrompt)
  - `wizard-steps-model.tsx` (StepModel)
  - `wizard-steps-permissions.tsx` (StepPermissions, ToolsTogglesEditor, Bash*, Filesystem*, PermissionPicker)
  - `wizard-steps-review.tsx` (StepMcp, StepReview)
- `deepagents-web/components/map/interaction-map.tsx` — GP#8 exception documentada (estado entrelazado no divisible sin Context)

## Correcciones ciclo 1 (post-review CHANGES_REQUESTED)
- `tests/test_admin_audit.py` — 8 patches corregidos de `agents.routers.admin.*` a los sub-módulos reales (`admin_agents`, `admin_skills`, `admin_meta`)
- `tests/test_e2e_errors.py` — monkeypatch corregido de `agents.routers.admin.describe_mcp_servers` a `agents.routers.admin_meta.describe_mcp_servers`
- `deepagents-web/components/agents/wizard-steps-permissions.tsx` — GP#8 exception documentada al inicio del archivo

## Bloqueos
- Ninguno
---

## Feature #24 — progress_archive_lifecycle (2026-05-09)

**Feature ID:** 24
**Feature name:** progress_archive_lifecycle
**Agente:** Implementer
**Inicio:** 2026-05-09
**Estado:** in_progress

## Contexto
- [Harness] Ciclo de vida y archivado de archivos de progreso
- Los archivos impl_*, review_* y reportes de gardening se acumulan sin límite en progress/. Crear progress/archive/ como destino de archivado, actualizar close_feature.py para mover impl_* y review_* al cerrar, documentar la convención de archivos temáticos y de gardening en docs/harness.md, y particionar history.md cuando supere un umbral razonable.

## Plan
- Crear progress/archive/ como directorio de archivado
- Actualizar close_feature.py para mover impl_* y review_* a archive/ al cerrar
- Actualizar validate_harness.py para buscar impl_* y review_* en progress/ y progress/archive/
- Documentar ciclo de vida de archivos en docs/harness.md (tipos, convención temáticos y gardening)

## Implementado
- progress/archive/ creado con .gitkeep
- close_feature.py: ARCHIVE_DIR + move_reports_to_archive()
- validate_harness.py: _find_report() busca en progress/ y archive/
- docs/harness.md: sección "Ciclo de vida de archivos en progress/"
- progress/impl_progress_archive_lifecycle.md escrito

## Bloqueos
- Ninguno
---

## Feature #25 — fix_current_md_template_consistency (2026-05-09)

**Feature ID:** 25
**Feature name:** fix_current_md_template_consistency
**Agente:** Implementer
**Inicio:** 2026-05-09
**Estado:** in_progress

## Contexto
- [Harness] Unificar template de current.md entre scripts
- close_feature.py escribe Feature ID: 0 y Feature name: sin_tarea al resetear current.md, pero el estado actual en disco usa guiones (—). Unificar el template entre close_feature.py, open_feature.py y docs/harness.md para que usen el mismo formato.

## Plan
- Elegir formato canónico para CLEAN_TEMPLATE (usar el de close_feature.py como fuente de verdad)
- Actualizar docs/harness.md para que la plantilla coincida byte a byte con CLEAN_TEMPLATE
- Verificar que validate_harness.py acepta ambas variantes o ajustar si es necesario
- Ejecutar init.ps1 y confirmar verde

## Implementado
- docs/harness.md: plantilla sin_tarea actualizada para coincidir byte a byte con CLEAN_TEMPLATE de close_feature.py (Agente: —, Inicio: —, comentario del header)

## Bloqueos
- Ninguno
---

## Feature #26 — fix_reports_required_threshold (2026-05-09)

**Feature ID:** 26
**Feature name:** fix_reports_required_threshold
**Agente:** Implementer
**Inicio:** 2026-05-09
**Estado:** done
**Veredicto:** APPROVED

### Resumen
- feature_list.json: agregado rules.reports_required_from_id = 21
- scripts/validate_harness.py: eliminado REPORTS_REQUIRED_FROM_ID=21 hardcodeado; se lee desde rules.reports_required_from_id con fallback a 1
- docs/feature_list.schema.json: agregado campo reports_required_from_id (integer, minimum 1, opcional) en rules

### Resultado del init de cierre
- `.\init.ps1` → exit code 0
- Tests pasaron (verdes)
---

## Feature #27 — archive_done_features (2026-05-09)

**Feature ID:** 27
**Feature name:** archive_done_features
**Agente:** Implementer
**Inicio:** 2026-05-09
**Estado:** done
**Veredicto:** APPROVED

### Resumen
- feature_list.json: features #1–#26 movidas a feature_list.archive.json; #27 marcado in_progress (ahora done).
- feature_list.archive.json: creado con 26 features done.
- scripts/validate_harness.py: validación del archivo de archivo integrada.
- docs/feature_list.schema.json: refactorizado con $defs/feature, $defs/archived_feature y $defs/archive_file.
- docs/harness.md: documentado ciclo de vida del archivado.
- deepagents-api/tests/test_harness_archive.py: 8 tests, todos verdes.
- progress/impl_archive_done_features.md: informe escrito.
- progress/review_archive_done_features.md: veredicto APPROVED.

### Resultado del init de cierre
- `.\init.ps1` → exit code 0
- `deepagents-api`: 188 passed, 2 skipped
- `deepagents-web`: Agent fallbacks, Auth session, Auth routing, API bearer proxy y Frontend tests passed

## 2026-05-11 — feature 28 refactor_harness_docs

### Estado
- done

### Resumen
- Feature cerrada mediante `scripts/close_feature.py`.

## 2026-05-11 — feature 29 split_project_docs

### Estado
- done

### Resumen
- Feature cerrada mediante `scripts/close_feature.py`.

## 2026-05-11 — feature 30 harness_role_briefs

### Estado
- done

### Resumen
- Feature cerrada mediante `scripts/close_feature.py`.

## 2026-05-11 — feature 30 harness_role_briefs

### Estado
- done

### Resumen
- Feature cerrada mediante `scripts/close_feature.py`.

## 2026-05-11 — feature 31 doc_fix_api_conventions_tree

### Estado
- done

### Resumen
- Feature cerrada mediante `scripts/close_feature.py`.

## 2026-05-11 — feature 32 doc_fix_golden8_exception_comments

### Estado
- done

### Resumen
- Feature cerrada mediante `scripts/close_feature.py`.

## 2026-05-11 — feature 33 doc_fix_golden8_exception_comments_web

### Estado
- done

### Resumen
- Feature cerrada mediante `scripts/close_feature.py`.

## 2026-05-11 — feature 34 doc_fix_exec_plan_harness_v2_complete

### Estado
- done

### Resumen
- Feature cerrada mediante `scripts/close_feature.py`.

## 2026-05-11 — feature 35 doc_fix_quality_scores_update

### Estado
- done

### Resumen
- Feature cerrada mediante `scripts/close_feature.py`.

## 2026-05-12 — feature 36 unblock_feature_transition

### Estado
- done

### Resumen
- Feature cerrada mediante `scripts/close_feature.py`.

## 2026-05-12 — feature 37 fix_schema_referential_alignment

### Estado
- done

### Resumen
- Feature cerrada mediante `scripts/close_feature.py`.

## 2026-05-12 — feature 38 validator_title_description_check

### Estado
- done

### Resumen
- Feature cerrada mediante `scripts/close_feature.py`.

## 2026-05-12 — feature 39 safe_write_harness

### Estado
- done

### Resumen
- Feature cerrada mediante `scripts/close_feature.py`.

## 2026-05-12 — feature 41 validate_progress_hygiene

### Estado
- done

### Resumen
- Feature cerrada mediante `scripts/close_feature.py`.

## 2026-05-12 — feature 40 rich_history_entries

### Estado
- done

### Resumen implementación
Se enriqueció `append_history` en `scripts/harness_state.py` para recibir `impl_summary` y `review_verdict`. Se agregaron dos helpers de extracción: `extract_impl_summary(name)` busca la sección `## Resumen` del impl report (o los primeros 3 bloques no-vacíos como fallback) y `extract_review_verdict(name)` extrae la línea `Veredicto:` y el cuerpo de `## Notas` si existe. `scripts/close_feature.py` llama a ambos extractores antes de mover los reportes a archive y pasa los valores a `append_history`. Cuando los reportes no existen se indica explícitamente en lugar de fallar.

### Veredicto review
**Veredicto:** APPROVED
Implementación limpia y mínima. Los extractores reutilizan `find_report` y manejan correctamente los casos edge (archivo ausente, sección faltante, fallback a primeras líneas). El orden de operaciones en `close_feature.py` (extraer → mover → append) es correcto. Los parámetros opcionales en `append_history` mantienen retrocompatibilidad. 8 tests con aislamiento real cubren 1:1 los criterios de acceptance (Golden #5).
Observación no bloqueante: el diff incluye `validate_progress_hygiene` en `validate_harness.py` que pertenece a una feature previa (#39 `validate_progress_hygiene`); no es parte de esta feature.

## 2026-05-12 — feature 42 docs_navigation_cleanup

### Estado
- done

### Resumen implementación
- `feature_list.json`
- `progress/current.md`
- `docs/README.md`

### Veredicto review
**Veredicto:** APPROVED

## 2026-05-12 — feature 43 doc_fix_docs_area_indexes

### Estado
- done

### Resumen implementación
- `AGENTS.md`
- `agents/architect.md`
- `agents/lead.md`

### Veredicto review
**Veredicto:** APPROVED

## 2026-05-12 — feature 44 doc_fix_golden8_excepciones

### Estado
- done

### Resumen implementación
- Ninguno (acceptance ya satisfecho por work previo)
- Al inspeccionar los 8 archivos del acceptance, todos contienen ya la excepción GP #8 explícita al inicio:
  - `deepagents-api/agents/api.py` → línea 17: `Excepción GP #8 (>300 líneas):` dentro del docstring del módulo

### Veredicto review
**Veredicto:** APPROVED

## 2026-05-12 — feature 45 refactor_wizard_steps_permissions

### Estado
- done

### Resumen implementación
- `deepagents-web/components/agents/wizard-steps-permissions.tsx` — reducido de 998 a 234 líneas; conserva solo `StepPermissions` y `ToolsTogglesEditor` (composición pura).
- `deepagents-web/components/agents/wizard-permissions-filesystem.tsx` — contiene `FilesystemRulesEditor` y las constantes `DEFAULT_FILESYSTEM_RULES` / `FILESYSTEM_PRESETS` (223 líneas).
- `deepagents-web/components/agents/wizard-permissions-filesystem-row.tsx` — nuevo; contiene `FilesystemRuleRow` y `PathsInput` extraídos de filesystem.tsx para cumplir Golden #8 (220 líneas).

### Veredicto review
**Veredicto:** APPROVED

## 2026-05-12 — feature 46 doc_fix_web_conv_tree

### Estado
- done

### Resumen implementación
- `docs/conventions/web.md`
- Se expandió el árbol de `Estructura de archivos` agregando subdirectorios reales con una responsabilidad breve por directorio.
- `components/` documenta los 7 subdirectorios existentes: `agents/`, `chat/`, `layout/`, `map/`, `skills/`, `system/`, `ui/`.

### Veredicto review
**Veredicto:** APPROVED

## 2026-05-14 — feature 47 doc_fix_readme_verification_templates

### Estado
- done

### Resumen implementación
- `scripts/harness_state.py` - Corregidas rutas de plantillas (docs/templates/progress → docs/harness/templates/progress)
- `docs/README.md` - Agregados todos los archivos de engineering/verification (shared.md, web.md, infra.md, client-agents.md, system-agents.md)
- `docs/README.md` - Listadas todas las plantillas individuales de harness/templates/progress (brief.md, current.empty.md, current.active.md, impl.md, review.md)

### Veredicto review
**Veredicto:** APPROVED

## 2026-05-19 — feature 1 harness_base_files

### Estado
- done

### Resumen implementación
- `init.ps1` (Nuevo)
- `init.sh` (Nuevo)
- `docs/engineering/conventions/shared.md` (Nuevo)

### Veredicto review
**Veredicto:** APPROVED

## 2026-05-19 — feature 2 harness_cleanup_and_dynamic_checks

### Estado
- done

### Resumen implementación
- `docs/operations/docker.md` (renombrado desde `docs/operations/example.md`)
- `scripts/validate_quality.py`
- `scripts/tests/test_docs_for.py`

### Veredicto review
**Veredicto:** APPROVED
