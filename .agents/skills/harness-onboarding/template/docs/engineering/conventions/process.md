# Proceso de ingeniería y Spec Driven Development (SDD)

> Este repo usa SDD como herramienta de claridad, no como burocracia.
> El flujo base es: descubrir → preguntar → definir → descomponer → implementar.

## Rol principal

En el flujo actual de **harness-template**, el **Arquitecto** concentra:

- interacción con el usuario;
- preguntas proactivas sobre alcance y diseño;
- documentación técnica;
- creación o refinamiento del backlog;
- generación de `requirements.md`, `design.md` y `tasks.md` cuando aplica SDD.

- El Arquitecto es el único responsable de discovery, diseño, SDD y backlog.

## Cuándo usar SDD

Usa SDD cuando el cambio tenga al menos una de estas características:

- abre decisiones de arquitectura o contratos;
- requiere aprobación humana antes de tocar código;
- tiene varias piezas coordinadas o dependencias entre capas;
- necesita trazabilidad fuerte entre requirements, tasks y tests.

No hace falta un campo `"sdd": true` en `feature_list.json`: el schema actual
del backlog no lo contempla. La decisión de usar SDD vive en el criterio del
Arquitecto y en la existencia de la carpeta `specs/<feature-name>/`.

## Estructura

Cuando una feature usa SDD, crea:

```text
specs/<feature-name>/
├── requirements.md
├── design.md
└── tasks.md
```

El `feature-name` coincide con el campo `name` de `feature_list.json`.

## Flujo real del repo

El arnés operativo solo soporta `pending`, `in_progress`, `done` y `blocked`.
Por lo tanto, `spec_ready` **no** es un estado formal del backlog.

El flujo correcto es:

```text
pending → [architect: discovery + design + backlog + optional SDD] → ⏸ humano aprueba → in_progress → [implementer → reviewer] → done
```

Notas:

- Mientras el spec no esté aprobado, la feature puede seguir en `pending`.
- La aprobación humana se registra en la conversación, brief o artefactos del
  spec; no en un status extra de `feature_list.json`.
- El Implementer recién abre `in_progress` cuando ya existe claridad suficiente
  para ejecutar.

## Preguntas proactivas del Arquitecto

El Arquitecto debe preguntar temprano cuando falte una decisión que cambie:

- alcance funcional;
- prioridades o recortes;
- UX o comportamiento visible;
- modelo de datos, contratos o integraciones;
- seguridad, permisos o exposición pública;
- estrategia de rollout, migración o compatibilidad.

Si decide seguir sin respuesta, debe dejar las asunciones explícitas en
`design.md`, en el ticket o en un brief.

## Responsabilidades por rol

| Rol | Archivos | Responsabilidad |
|---|---|---|
| Architect | `requirements.md` | Qué se necesita, en lenguaje verificable |
| Architect | `design.md` | Cómo se construirá y qué alternativas se descartaron |
| Architect | `tasks.md` | Pasos concretos y orden de implementación |
| Implementer | código + tests + `progress/impl_*` | Ejecutar el plan sin rediseñar el alcance |
| Reviewer | `progress/review_*` | Validar trazabilidad, calidad y cierre |

## requirements.md — EARS estricto

Las requirements se redactan en **EARS** (Easy Approach to Requirements
Syntax). Cada requirement es un párrafo numerado con uno de estos cinco
patrones:

| Patrón         | Plantilla                                                   |
|----------------|-------------------------------------------------------------|
| **Ubicuo**     | `El sistema DEBE <acción>.`                                 |
| **Evento**     | `CUANDO <disparador>, el sistema DEBE <acción>.`            |
| **Estado**     | `MIENTRAS <estado>, el sistema DEBE <acción>.`              |
| **Opcional**   | `DONDE <feature opcional>, el sistema DEBE <acción>.`       |
| **No deseado** | `SI <evento no deseado> ENTONCES el sistema DEBE <acción>.` |

Reglas duras:

- Cada requirement tiene un id estable: `R1`, `R2`, ...
- Cada requirement DEBE ser verificable por al menos un test concreto.
- No mezcles varios `DEBE` en un mismo requirement. Si hay más de uno, parte.
- No uses verbos blandos ("podría", "puede", "soporta"). Solo `DEBE` / `NO DEBE`.

Ejemplo:

```markdown
## R1
CUANDO el usuario ejecuta `python -m src.cli recent`, el sistema DEBE
imprimir hasta 5 notas ordenadas por `created_at` descendente.

## R2
SI el flag `--limit` recibe un valor <= 0 ENTONCES el sistema DEBE
imprimir un mensaje de error en stderr y salir con código != 0.
```

## design.md — decisiones técnicas

Captura **antes** de tocar código:

- Qué archivos se crean / modifican.
- Qué firmas nuevas aparecen (funciones, clases, comandos).
- Qué excepciones se reutilizan o se añaden.
- Qué alternativa se descartó y por qué (mínimo una).
- Qué dudas se resolvieron preguntando al usuario y qué asunciones quedaron.

No es ingeniería desde primeros principios: apóyate en
`docs/architecture/overview.md`, `docs/engineering/conventions/`,
`docs/harness/ticketing.md` y el resto del routing canónico.

## tasks.md — checklist ejecutable

Pasos discretos en orden, cada uno con checkbox. Cada task referencia al
menos un `R<n>` que cubre. El `architect` genera este archivo basándose en
`requirements.md` y `design.md`.

Ejemplo:

```markdown
- [ ] T1 — Añadir `cmd_recent` en `src/cli.py`. Cubre: R1, R3.
- [ ] T2 — Registrar subparser `recent` con flag `--limit`. Cubre: R1, R2.
- [ ] T3 — Añadir `test_recent_default_limit` en `tests/test_cli.py`. Cubre: R1.
- [ ] T4 — Añadir `test_recent_invalid_limit` en `tests/test_cli.py`. Cubre: R2.
```

El `implementer` marca `[x]` cada task al completarla. El `reviewer` rechaza
si queda alguna `[ ]` sin justificación documentada.

## Trazabilidad (regla dura)

- Cada test en `tests/` debe poder mapearse a un `R<n>` de su spec.
- Cada `R<n>` debe tener al menos un test concreto.
- El `reviewer` comprueba esta correspondencia explícitamente y rechaza
  si falta.

El `implementer` documenta el mapa en `progress/impl_<name>.md`:

```markdown
## Trazabilidad
- R1 → `test_recent_default_limit`
- R2 → `test_recent_invalid_limit`
- R3 → `test_recent_custom_limit`
```

## Cuándo NO aplica SDD

No hace falta abrir spec para:

- fixes pequeños y localizados;
- gardening menor sin decisiones nuevas;
- ajustes obvios donde el acceptance ya alcanza como contrato;
- consultas o análisis donde todavía no corresponde crear backlog.
