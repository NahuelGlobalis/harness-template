# CHECKPOINTS — Evaluación del estado final

> En sistemas multi-agente no se evalúa el camino, se evalúa el destino.
> Estos checkpoints separan lo que debe validar `init` de lo que exige juicio humano.

## A — Checkpoints automáticos

Estos controles deben ejecutarse desde `./init.ps1` en Windows o `./init.sh` en WSL/Linux.

### A1 — El arnés está completo

- [ ] Existen `AGENTS.md`, `CHECKPOINTS.md`, `init.ps1`, `init.sh` y `feature_list.json`.
- [ ] Existen los scripts de transición `open_feature.py`, `block_feature.py`, `close_feature.py`, `cancel_feature.py` y `harness_state.py`.
- [ ] Existen `docs/architecture/overview.md`, `docs/engineering/conventions/shared.md`, `docs/harness/lifecycle.md` y `docs/engineering/verification/shared.md`.
- [ ] Existen los 4 roles en `agents/`: architect, implementer, reviewer y gardener.
- [ ] Existen `progress/current.md` y `progress/history.md`.

### A2 — `feature_list.json` es coherente

- [ ] El JSON parsea correctamente.
- [ ] Los `id` son únicos y están ordenados.
- [ ] Los `name` son únicos y cumplen `snake_case`.
- [ ] Todo `status` está permitido.
- [ ] Todo `acceptance` es una lista no vacía.
- [ ] Hay como máximo una feature `in_progress`.

### A3 — `progress/current.md` coincide con el backlog

- [ ] Si hay una feature `in_progress`, `current.md` declara el mismo `Feature ID`.
- [ ] Si hay una feature `in_progress`, `current.md` declara el mismo `Feature name`.
- [ ] Si hay una feature `in_progress`, `current.md` declara `Estado: in_progress`.
- [ ] Si no hay feature activa, `current.md` está limpio o declara `Estado: sin_tarea`.

### A4 — Higiene básica

- [ ] No hay `print()` de debug en Python.
- [ ] No hay `TODO` sin resolver en código de producto.
- [ ] No hay archivos untracked sospechosos fuera de una tarea activa.

### A4b — Golden Principles (warnings)

- [ ] Ningún archivo de producto excede 300 líneas (Golden #8).
- [ ] Routers no importan de tools/ directamente (Golden #7).

### A5 — Tests ejecutables

- [ ] Los tests del proyecto pasan.
- [ ] El init termina con exit code 0.

## H — Checkpoints humanos

Estos controles los evalúa el Reviewer. El cierre lo ejecuta el Reviewer
siguiendo el protocolo de `agents/reviewer.md`.

### H1 — Acceptance real

- [ ] Cada criterio de `acceptance` está satisfecho con evidencia concreta.
- [ ] La evidencia apunta a tests, comandos o archivos específicos.
- [ ] No se cerró trabajo fuera de scope como parte de la misma feature.

### H2 — Arquitectura y mantenibilidad

- [ ] El diseño respeta `docs/architecture/overview.md`.
- [ ] El código respeta `docs/engineering/conventions/`.
- [ ] Las dependencias externas están justificadas.
- [ ] La solución es simple, mantenible y no duplica lógica innecesaria.

### H3 — Seguridad y operación

- [ ] No se exponen secretos, tokens ni datos sensibles.
- [ ] Los errores no filtran detalles internos.
- [ ] Los cambios de infraestructura documentan impactos operativos.

### H4 — Cierre de sesión

- [ ] Existe `progress/impl_<feature_name>.md`.
- [ ] Existe `progress/review_<feature_name>.md` con `Veredicto: APPROVED`.
- [ ] El Reviewer marca `done` en `feature_list.json` solo después de init verde.
- [ ] El Reviewer archiva el contenido de `progress/current.md` en `progress/history.md`.
- [ ] El Reviewer mueve `impl_*` y `review_*` a `progress/archive/`.
- [ ] El archive (`feature_list.archive.json`) acepta solo features `done` o `cancelled`.
- [ ] El Reviewer limpia `progress/current.md` con `Estado: sin_tarea`.

---

**Cómo usar este archivo:** el Reviewer marca los checkpoints humanos en
`progress/review_<feature_name>.md`. Los checkpoints automáticos deben quedar
cubiertos por `init`; si falla cualquiera, no se puede cerrar la feature.
