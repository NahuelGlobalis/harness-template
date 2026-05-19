# Harness multi-agente — harness-template

Este documento es la fuente canónica del protocolo operativo del arnés. `AGENTS.md` solo enruta; los prompts en `agents/` solo adaptan cada rol a estas reglas.

## Entradas de verificación

- **Windows PowerShell:** `./init.ps1`
- **WSL/Linux:** `./init.sh`

Ambos comandos ejecutan `scripts/validate_harness.py`. `init.ps1` debe resolver
primero el Python del repo (`.venv`) antes de depender de
`python` o `py` globales. Los comandos detallados de tests viven en
`docs/engineering/verification/`.

## Scripts de transición

Los cambios de estado del backlog se hacen con scripts, no editando JSON o
`progress/current.md` a mano:

- **Abrir feature:** `python scripts/open_feature.py <id|name> --agent Implementer`
- **Bloquear feature:** `python scripts/block_feature.py [id|name] --reason "<motivo>" --agent <rol>`
- **Cerrar feature aprobada:** `python scripts/close_feature.py [id|name]`
- **Desbloquear feature:** `python scripts/unblock_feature.py [id|name] --agent <rol> --resolution "<resolución>" [--to pending]`
- **Cancelar feature:** `python scripts/cancel_feature.py [id|name] --reason "<motivo>" --agent <rol>`
- **Validar estado:** `python scripts/validate_harness.py`

Estos scripts actualizan de forma atómica `feature_list.json`,
`feature_list.archive.json`, `progress/current.md`, `progress/history.md` y los
reportes archivados cuando corresponde. Si una escritura posterior falla, deben
restaurar el estado previo de los archivos ya tocados.

## Estado persistente

- **`feature_list.json`:** backlog activo. Debe contener solo features `pending`, `in_progress` o `blocked`.
- **`feature_list.archive.json`:** archivo de features `done` y `cancelled`.
- **`progress/current.md`:** sesión activa, con campos estructurados parseables.
- **`progress/history.md`:** bitácora append-only de sesiones cerradas.
- **`progress/impl_<feature_name>.md`:** evidencia del Implementer.
- **`progress/review_<feature_name>.md`:** veredicto del Reviewer.

## Plantillas canónicas

Las plantillas viven como archivos reales para que docs, agentes y scripts no divergan:

- **Sesión vacía:** `docs/harness/templates/progress/current.empty.md`
- **Sesión activa:** `docs/harness/templates/progress/current.active.md`
- **Informe de implementación:** `docs/harness/templates/progress/impl.md`
- **Informe de review:** `docs/harness/templates/progress/review.md`

## Estados válidos

- **`pending`:** ticket listo para ser tomado.
- **`in_progress`:** única feature activa.
- **`done`:** feature aprobada, verificada, cerrada y archivada.
- **`blocked`:** feature detenida por bloqueo explícito.
- **`cancelled`:** feature descartada con trazabilidad. Solo puede existir en `feature_list.archive.json`.

## Repriorización y tickets obsoletos

- **Repriorizar:** el Arquitecto puede reordenar features `pending` en
  `feature_list.json` durante curación de backlog. No debe cambiar `id`,
  `name` ni una feature `in_progress`; después debe ejecutar `init`.
- **Cancelar con trazabilidad:** usar `python scripts/cancel_feature.py [id|name] --reason "<motivo>" --agent <rol>`. Acepta features `pending` o `blocked`. Mueve la feature a `feature_list.archive.json` con status `cancelled` y registra el evento en `progress/history.md`. Si la feature estaba `blocked`, resetea `progress/current.md`.
- **Trazabilidad requerida:** si una feature ya tuvo trabajo, reportes o una decisión que deba auditarse, se cancela con el script, no eliminando manualmente.

## Máquina de estados

### `sin_tarea` → `in_progress`

- **Responsable:** Implementer.
- **Precondiciones:** `init` verde, no hay otra feature `in_progress`, y el ticket cumple `docs/harness/ticketing.md`.
- **Acciones:** ejecutar `python scripts/open_feature.py <id|name> --agent Implementer`.
- **Postcondiciones:** `feature_list.json` y `progress/current.md` declaran la misma feature activa.

### `in_progress` → entrega de implementación

- **Responsable:** Implementer.
- **Acciones:** implementar código/tests, verificar según `docs/engineering/verification/`, ejecutar `docs/quality/self-review-checklist.md` y escribir `progress/impl_<feature_name>.md` desde `docs/harness/templates/progress/impl.md`.
- **Postcondiciones:** el Implementer no marca `done`; la entrega queda lista para Reviewer.

### `in_progress` → `in_progress` con cambios requeridos

- **Responsable:** Reviewer.
- **Acciones:** revisar contra `CHECKPOINTS.md`, `docs/architecture/overview.md`, `docs/engineering/conventions/` y el `acceptance`; escribir `progress/review_<feature_name>.md` con `CHANGES_REQUESTED`.
- **Postcondiciones:** la feature permanece `in_progress`; el Implementer corrige solo lo señalado.

### `in_progress` → `done`

- **Responsable:** Reviewer.
- **Precondiciones:** acceptance completo, tests e `init` verdes, y existe `progress/impl_<feature_name>.md`.
- **Acciones:** escribir `review_*` con `APPROVED` y ejecutar `python scripts/close_feature.py [id|name]`.
- **Postcondiciones:** `feature_list.json` no contiene features `done`, `feature_list.archive.json` contiene la feature cerrada, e `init` termina verde.

### `in_progress` → `blocked`

- **Responsable:** Implementer o Reviewer.
- **Acciones:** ejecutar `python scripts/block_feature.py [id|name] --reason "<motivo>" --agent <rol>`.
- **Postcondiciones:** una feature `blocked` impide abrir otra hasta resolver o replanificar explícitamente.

### `blocked` → `in_progress` | `pending`

- **Responsable:** Implementer o Reviewer.
- **Precondiciones:** la feature debe estar en estado `blocked`. Si el destino es `in_progress`, no debe haber otra feature ya `in_progress`.
- **Acciones:** ejecutar `python scripts/unblock_feature.py [id|name] --agent <rol> --resolution "<resolución>" [--to pending]`.
- **Postcondiciones:** si el destino es `in_progress`, `feature_list.json` y `progress/current.md` declaran la feature activa; si el destino es `pending`, la feature queda encolada y `progress/current.md` vuelve a `sin_tarea`.

## Definition of Done

Una feature solo puede cerrarse cuando:

- **Acceptance:** todos los criterios están satisfechos con evidencia concreta.
- **Tests:** hay tests nuevos o actualizados cuando el cambio toca código.
- **Verificación:** `init` termina verde.
- **Implementación:** existe `progress/impl_<feature_name>.md`.
- **Review:** existe `progress/review_<feature_name>.md` con `APPROVED`.
- **Archivo:** la feature está en `feature_list.archive.json`, no en `feature_list.json`.
- **Sesión:** `history.md` contiene el resumen y `current.md` vuelve a `sin_tarea`.

## Invariantes automáticos

`init` debe fallar si se rompe cualquiera de estas reglas:

- Existen los archivos base del arnés.
- Existen los cuatro roles: Architect, Implementer, Reviewer y Gardener.
- `feature_list.json` y `feature_list.archive.json` son JSON válidos cuando existen.
- Los `id` son enteros únicos y están ordenados ascendentemente.
- Los `name` son únicos y cumplen `snake_case`.
- Todo `status` pertenece al conjunto permitido.
- Todo `acceptance` es una lista no vacía de strings no vacíos.
- Hay como máximo una feature `in_progress`.
- Si hay una feature `in_progress`, `progress/current.md` declara el mismo `Feature ID`, `Feature name` y `Estado: in_progress`.
- Si no hay feature activa, `progress/current.md` no declara `Estado: in_progress`.
- Para features cerradas con `id >= reports_required_from_id`, existen `impl_*` y `review_*` aprobado en `progress/` o `progress/archive/`.

## Ciclo de vida de `progress/`

| Archivo | Generado por | Ciclo |
|---|---|---|
| `current.md` | Rol activo | Activo durante la sesión; reseteado al cerrar |
| `history.md` | Reviewer | Append-only; nunca se borra |
| `impl_<name>.md` | Implementer | Movido a `archive/` al cerrar |
| `review_<name>.md` | Reviewer | Movido a `archive/` al cerrar |
| Archivos temáticos | Cualquier agente | Opcionales; Gardener los archiva cuando ya no aportan contexto activo |
| `gardening_*.md` | Gardener | Opcionales; se archivan cuando el drift está resuelto o ticketizado |
| `brief_*.md` | Cualquier rol | Opcionales; creados para handoff entre roles; archivados a `progress/archive/` al cerrar los tickets derivados |

**Invariante:** `progress/` debe contener solo `current.md`, `history.md` y archivos de la sesión activa. Todo lo demás pertenece a `progress/archive/`.

## Higiene de `progress/`

- **Activo:** `current.md`, `history.md` y reportes de la sesión en curso.
- **Archivado:** reportes `impl_*`, `review_*`, reportes de gardening resueltos y archivos temáticos ya resumidos.

## Ciclo de vida de briefs

Los briefs (`progress/brief_<tema>.md`) son archivos de handoff opcionales entre roles. Permiten que un rol deje análisis estructurado para otro sin forzar el contenido en documentos formales como `docs/architecture/overview.md`.

- **Creación:** cualquier rol puede crear un brief usando la plantilla `docs/harness/templates/progress/brief.md`.
- **Consumo:** el rol destinatario lo lee al inicio de su tarea.
- **Archivado:** una vez consumidos y los tickets derivados cerrados, el brief se mueve a `progress/archive/`. `close_feature.py` solo archiva briefs ligados a la feature cerrada; no debe mover handoffs ajenos a esa sesión.
- **Validación:** `validate_harness.py` no exige briefs (son opcionales), pero los incluye en la invariante de limpieza de `progress/`: todo archivo que no sea `current.md` o `history.md` y no pertenezca a la sesión activa debe estar en `progress/archive/`.

## Ciclo de vida de `feature_list.archive.json`

El cierre mueve features `done` y `cancelled` desde `feature_list.json` hacia `feature_list.archive.json`.

- **Formato:** `project`, `description` y `features`.
- **Sin `rules`:** las reglas viven en `feature_list.json`.
- **Validación:** `validate_harness.py` valida ambos archivos. El archive acepta solo `done` y `cancelled`.
- **Unicidad:** un `id` o `name` no puede aparecer en ambos archivos.

## Documentos canónicos relacionados

- **Tickets y Ready:** `docs/harness/ticketing.md`
- **Verificación:** `docs/engineering/verification/`
- **Self-review:** `docs/quality/self-review-checklist.md`
- **Review final:** `CHECKPOINTS.md`
- **Gardening:** `docs/quality/gardening.md`
- **Principios anti-drift:** `docs/quality/golden-principles.md`

## ADRs

Las decisiones de arquitectura duraderas deben registrarse en `docs/architecture/adr/` cuando el proyecto crezca o una decisión pueda reabrirse.

