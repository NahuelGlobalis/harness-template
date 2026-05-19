# Execution Plan — Harness v2 (inspirado en OpenAI Harness Engineering)

> **Fecha:** 2025-05-09
> **Autor:** Architect + Human
> **Estado:** completed
> **Cierre:** 2026-05-11
> **Scope:** Reestructurar el harness multi-agente aplicando lecciones del artículo
> "Harness engineering: leveraging Codex in an agent-first world" de OpenAI.

---

## Objetivo

Evolucionar el harness de harness-template para:
1. Eliminar burocracia innecesaria (Orchestrator como rol separado).
2. Aumentar la autonomía del agente con self-review.
3. Codificar "golden principles" que prevengan drift.
4. Agregar quality scoring para guiar priorización.
5. Soportar execution plans versionados para features complejas.
6. Agregar doc-gardening automatizado.

---

## Fases

### Fase 1 — Reestructuración de roles (eliminar Orchestrator)

**Problema:** El Orchestrator es un agente que solo mueve estado entre archivos.
No aporta juicio, solo ejecuta transiciones determinísticas que un script puede
hacer mejor y que los otros roles pueden asumir.

**Cambios:**

| Archivo | Acción |
|---------|--------|
| `agents/orchestrator.md` | Eliminar |
| `agents/implementer.md` | Absorbe apertura de feature (pasos 1-5 del Orchestrator) |
| `agents/reviewer.md` | Absorbe cierre de feature (marca done + archiva) |
| `scripts/close_feature.py` | **Nuevo** — automatiza: validar review APPROVED → init verde → marcar done → archivar en history → limpiar current |
| `scripts/open_feature.py` | **Nuevo** — automatiza: elegir primer pending → marcar in_progress → inicializar current.md |
| `AGENTS.md` | Actualizar tabla de roles (4 roles), flujo, sección 7 |
| `docs/harness/lifecycle.md` | Actualizar "Flujo por rol" y quitar referencias al Orchestrator |
| `CHECKPOINTS.md` | Quitar mención del Orchestrator |
| `scripts/validate_harness.py` | Cambiar `role_files` para no requerir `orchestrator.md` |
| `.windsurf/workflows/orchestrator.md` | Refactorizar: ahora invoca scripts, no un "rol" |

**Nuevo flujo simplificado:**
```
Architect → docs/architecture/overview.md + docs/engineering/conventions/
    │
    ▼
Tech Lead → feature_list.json (tickets atómicos)
    │
    ▼
┌────────── CICLO POR TICKET ──────────┐
│                                        │
│  Implementer:                          │
│    1. open_feature.py (o manual)       │
│    2. Implementar + tests              │
│    3. Self-review (nuevo paso)         │
│    4. Escribir impl_*                  │
│       ▼                                │
│  Reviewer:                             │
│    1. Revisar + init                   │
│    2. Si APPROVED → close_feature.py   │
│    3. Si REJECTED → devolver           │
└────────────────────────────────────────┘
```

---

### Fase 2 — Self-review del Implementer

**Problema:** El Implementer entrega trabajo sin revisarse a sí mismo, lo que
genera rechazos evitables.

**Cambios:**

| Archivo | Acción |
|---------|--------|
| `agents/implementer.md` | Agregar paso 5.5: "Self-review checklist" |
| `docs/quality/self-review-checklist.md` | **Nuevo** — checklist mecánica que el Implementer ejecuta antes de entregar |

**Contenido del self-review checklist:**
- [ ] Init pasa verde
- [ ] Cada criterio de acceptance tiene test
- [ ] No hay print/console.log de debug
- [ ] No hay TODOs sin contexto
- [ ] Imports organizados (stdlib → external → local)
- [ ] Nombres siguen convenciones (snake_case Python, PascalCase React)
- [ ] Archivos nuevos agregados al árbol en docs/engineering/conventions/ si aplica
- [ ] No hay archivos >300 líneas sin justificación
- [ ] No hay helpers duplicados si ya existe shared utility
- [ ] Shapes validadas en boundaries (no acceso YOLO a datos)

---

### Fase 3 — Golden Principles

**Problema:** Sin reglas anti-drift explícitas, los agentes replican patrones
subóptimos que ya existen en el repo.

**Cambios:**

| Archivo | Acción |
|---------|--------|
| `docs/quality/golden-principles.md` | **Nuevo** — principios dorados inmutables |
| `scripts/validate_harness.py` | Agregar checks de golden principles |
| `AGENTS.md` | Agregar al mapa del repositorio |

**Golden Principles propuestos:**

1. **Parse, don't validate.** Validar shapes en boundaries con Pydantic/Zod. No
   acceder a datos con `dict["key"]` sin schema previo.
2. **Shared utilities over hand-rolled.** Si una utilidad ya existe en el repo,
   usarla. No crear helpers duplicados.
3. **Structured logging only.** Usar `logging` con niveles, nunca `print()`.
   Frontend: nunca `console.log` en producción.
4. **Boundaries own validation.** Routers validan input, services asumen datos
   válidos. No mezclar capas.
5. **Config from env, never hardcoded.** Toda config vive en `.env` y se lee
   via `config.py` (Python) o `process.env` (Next.js).
6. **Tests mirror acceptance.** Cada criterio de acceptance del ticket tiene un
   test nombrado 1:1.
7. **No opaque dependencies.** Preferir implementaciones in-repo cuando la
   dependencia externa es opaca o inestable. Preferir stdlib cuando cubre el caso.
8. **File size limit: 300 lines.** Si un archivo crece >300 líneas, refactorizar.
   Excepciones documentadas explícitamente.
9. **Dependency direction.** `routers/ → services/ → tools/`. Nunca al revés.
   Routers no importan tools directamente.
10. **Docs reflect code.** Si un cambio agrega/elimina un módulo, actualizar
    `docs/engineering/conventions/` y `docs/architecture/overview.md` en el mismo commit.

**Validación mecánica (en `validate_harness.py`):**
- Check de imports invertidos (routers importando de tools).
- Check de archivos >300 líneas.
- Check de `print()` / bare `console.log`.
- Check de accesos a dict sin typing (heurístico, warn no fail).

---

### Fase 4 — Execution Plans versionados

**Problema:** Para features complejas, el único artefacto de planificación es el
campo `description` del ticket (1-2 líneas). No hay espacio para decisiones de
diseño, alternativas descartadas ni progreso incremental.

**Cambios:**

| Archivo | Acción |
|---------|--------|
| `docs/exec-plans/active/` | **Nuevo directorio** — planes de features complejas en curso |
| `docs/exec-plans/completed/` | **Nuevo directorio** — planes cerrados (archivo histórico) |
| `docs/harness/lifecycle.md` | Documentar cuándo crear un exec-plan vs ir directo |
| `AGENTS.md` | Agregar al mapa |

**Template de execution plan:**
```markdown
# Exec Plan — <feature_name>

**Feature ID:** N
**Autor:** Architect / Lead
**Estado:** active | completed
**Inicio:** YYYY-MM-DD

## Objetivo
<1-2 párrafos>

## Decisiones de diseño
- Decisión 1: <qué> porque <por qué>
- Alternativa descartada: <qué> porque <por qué>

## Subtareas
- [ ] Subtarea 1
- [ ] Subtarea 2

## Log de progreso
- YYYY-MM-DD: <evento>
```

**Regla:** Se crea un exec-plan cuando:
- La feature tiene >3 criterios de acceptance, O
- Requiere cambios en >2 módulos/capas, O
- El Architect o Lead lo solicita explícitamente.

---

### Fase 5 — Quality Scoring por dominio

**Problema:** Sin una puntuación visible, el agente no sabe dónde priorizar
refactoring ni qué módulos tienen deuda alta.

**Cambios:**

| Archivo | Acción |
|---------|--------|
| `docs/quality/quality-scores.md` | **Nuevo** — scoring por módulo/dominio |
| `AGENTS.md` | Agregar al mapa |

**Formato:**

```markdown
# Quality Scores — harness-template

> Actualizado: YYYY-MM-DD
> Escala: A (excelente) → D (deuda crítica)

| Dominio / Módulo | Score | Notas |
|------------------|-------|-------|
| deepagents-api/agents/security.py | A | Tests completos, typed |
| deepagents-api/agents/routers/admin.py | B | Falta split por recurso |
| deepagents-api/agents/loader.py | B | Funcional pero sin types internos |
| deepagents-web/app/ | C | Falta testing e2e |
| infrastructure/ | C | Docker ok, falta health probes |
| docs/ | B | Actualizado pero sin gardening automático |
```

**Regla:** El Reviewer actualiza quality-scores.md si detecta degradación o
mejora significativa durante un review.

---

### Fase 6 — Doc-Gardening Agent

**Problema:** Los docs se desactualizan silenciosamente conforme el código cambia.

**Cambios:**

| Archivo | Acción |
|---------|--------|
| `agents/gardener.md` | **Nuevo** — rol de mantenimiento |
| `scripts/doc_gardening.py` | **Nuevo** — scan de docs vs código |
| `AGENTS.md` | Agregar rol al mapa |

**Responsabilidades del Gardener:**
1. Comparar árbol de archivos real vs documentado en `docs/engineering/conventions/`.
2. Verificar que `docs/architecture/overview.md` menciona todos los módulos existentes.
3. Detectar docs que referencian archivos eliminados.
4. Verificar freshness (archivos .md no actualizados en >N features).
5. Abrir tickets de tipo `doc_fix` en `feature_list.json` con prioridad baja.

**Cuándo se ejecuta:**
- Manualmente, cuando el humano lo invoca.
- Opcionalmente, como paso final del Reviewer (si el review aprueba, correr
  gardening scan y reportar warns).

---

## Orden de implementación

| # | Fase | Dependencia | Esfuerzo estimado |
|---|------|-------------|-------------------|
| 1 | Golden Principles (`docs/quality/golden-principles.md`) | Ninguna | Bajo |
| 2 | Execution Plans (estructura + template) | Ninguna | Bajo |
| 3 | Quality Scoring (`docs/quality/quality-scores.md`) | Ninguna | Bajo |
| 4 | Self-review checklist | Ninguna | Bajo |
| 5 | Eliminar Orchestrator + scripts de apertura/cierre | Fases 1-4 | Medio |
| 6 | Validaciones de golden principles en `validate_harness.py` | Fase 1 | Medio |
| 7 | Doc-Gardening agent + script | Fase 1 | Medio |

**Propuesta:** Implementar como **2-3 features** en `feature_list.json`:
- Feature 22: `harness_v2_docs` — Fases 1-4 (docs nuevos, sin cambio de flujo)
- Feature 23: `harness_v2_roles` — Fase 5 (eliminar orchestrator, scripts, actualizar harness)
- Feature 24: `harness_v2_automation` — Fases 6-7 (validaciones + gardener)

---

## Riesgos y mitigaciones

| Riesgo | Mitigación |
|--------|-----------|
| Eliminar Orchestrator rompe validate_harness.py | Actualizar en la misma feature |
| Golden principles demasiado estrictos | Empezar con warn, promover a fail tras 1 sprint |
| Quality scores se desactualizan | El Reviewer lo actualiza como parte de su protocolo |
| Exec plans se vuelven burocracia | Solo obligatorios para features complejas (regla explícita) |

---

## Decisiones abiertas

1. ¿El Gardener es un "rol" formal (archivo en `agents/`) o solo un script + workflow?
2. ¿Los golden principles arrancan como warns o como fails directamente?
3. ¿El close_feature.py se ejecuta automáticamente post-review o lo invoca el humano?

---

## Log de progreso

- 2025-05-09: Plan creado (Architect + Human).
- 2026-05-11: Todas las fases completadas (features #22–#30 cerradas). Plan movido a completed.
