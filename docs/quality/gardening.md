# Gardening — harness-template

Este documento es el runbook canónico del Gardener.

## Responsabilidad

El Gardener detecta drift entre documentación, código y arnés. No implementa código de producto ni aprueba reviews.

## SesiÃ³n de gardening

- **Con feature:** si el Gardener trabaja sobre una feature `doc_fix_` o `refactor_`, usa las transiciones de `docs/harness/lifecycle.md` como cualquier feature.
- **Sin feature:** si el humano pide un escaneo ad-hoc, no declares `Estado: in_progress` en `progress/current.md`; escribe el resultado en `progress/gardening_<date>.md` y archívalo cuando esté resuelto.
- **Bloqueos:** si el escaneo descubre drift no trivial, crea un brief para el
  Arquitecto según la sección «Handoff al Arquitecto».

## Checks de drift

- **Árbol documentado vs real:** compara `docs/engineering/conventions/` contra `deepagents-api/agents/` y `deepagents-web/`.
- **Arquitectura completa:** verifica que `docs/architecture/overview.md` cubre capas y módulos existentes.
- **Referencias rotas:** detecta paths en Markdown que ya no existen.
- **Archivos largos:** busca `.py`, `.ts` y `.tsx` de producto con más de 300 líneas.
- **Dependency direction:** verifica que routers no importan directamente de `tools/`.
- **Debug output:** busca `print()` en backend y `console.log` en frontend de producto.
- **Quality scores:** actualiza `docs/quality/quality-scores.md` si detecta degradación evidente.

## Handoff al Arquitecto

Cuando detecta drift no trivial, crea un brief `progress/brief_gardening_<tema>.md` usando `docs/harness/templates/progress/brief.md`:

- **Destinatario:** Architect.
- **Prefijos sugeridos:** `doc_fix_` o `refactor_`.
- **Acceptance sugerido:** verificable según `docs/harness/ticketing.md`.
- El Arquitecto consume el brief y crea o reprioriza los tickets atómicos en
  `feature_list.json`.

## Higiene de `progress/`

Aplica el ciclo de vida definido en `docs/harness/lifecycle.md`.

- **Activo:** `current.md`, `history.md` y reportes de la sesión en curso.
- **Archivado:** reportes `impl_*`, `review_*`, reportes de gardening resueltos y archivos temáticos ya resumidos.

## Archivado de features done

Cuando `feature_list.json` contenga features `done`, muévelas a `feature_list.archive.json` siguiendo `docs/harness/lifecycle.md` y ejecuta `init`.
