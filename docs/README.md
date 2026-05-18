# Documentacion - harness-template

Este archivo es el indice global de `docs/` y el contrato de routing que consume `scripts/docs_for.py`. Describe que documentacion existe, donde vive y como pedir paquetes por seccion/capa. No hay indices locales por carpeta: si una ruta documental cambia, se actualiza este README y las tablas de routing en el mismo cambio.

## Organizacion

<!-- sections:begin -->
| Key | Contenido | 
|---|---|
| `harness` | Ciclo de vida multi-agente, backlog, schema y plantillas de progreso | 
| `architecture` | Arquitectura tecnica estable y ADRs |
| `engineering` | Convenciones de implementacion y verificacion por capa | 
| `operations` | Runbooks para stack local, auth, referencias y troubleshooting | 
| `quality` | Principios anti-drift, gardening, scores y checklist de review |
| `exec-plans` | Planes largos, plantilla y planes completados | 
<!-- sections:end -->

## Keys

<!-- keys:begin -->
| Key | Contenido | 
|---|---|
| `shared` | Documentacion que aplica a multiples capas o es transversal. |
| `api` | Documentacion especifica del backend. |
| `web` | Documentacion especifica del frontend. | 
| `infra` | Documentacion especifica de infraestructura. |
| `fullstack` | Documentacion que combina backend y frontend. | 
| `design` | Paquete transversal para Arquitecto y, si existiera, una futura orquestación. |
| `delivery` | Paquete transversal para Implementer y Reviewer. |
| `gardening` | Paquete transversal para Gardener y deteccion de drift. |
<!-- keys:end -->

## Mapa documental

### Harness

<!-- harness:begin -->
| Documento | Contenido | key |
|---|---|---|
| `harness/lifecycle.md` | Estados, transiciones y cierre del arnes | shared,delivery,gardening |
| `harness/ticketing.md` | Definition of Ready, acceptance y escritura de tickets | shared,design,delivery,gardening |
| `harness/templates/progress/brief.md` | Plantilla para briefs de gardening y arquitectura | shared,design,gardening |
| `harness/templates/progress/current.empty.md` | Plantilla para sesion vacia | shared,delivery,gardening |
| `harness/templates/progress/current.active.md` | Plantilla para sesion activa | shared,delivery,gardening |
| `harness/templates/progress/impl.md` | Plantilla para informe de implementacion | shared,delivery |
| `harness/templates/progress/review.md` | Plantilla para informe de review | shared,delivery |
<!-- harness:end -->

### Architecture

<!-- architecture:begin -->
| Documento | Contenido | key |
|---|---|---|
| `architecture/overview.md` | Diseno tecnico estable, capas, integraciones y decisiones vigentes | shared,design,delivery,gardening,fullstack |
| `architecture/adr/` | ADRs para decisiones duraderas o reabribles | shared,design,gardening |
<!-- architecture:end -->

### Engineering

<!-- engineering:begin -->
| Documento | Contenido | key |
|---|---|---|
| `engineering/conventions/shared.md` | Convenciones transversales de codigo y cambios | shared |
| `engineering/conventions/process.md` | Convenciones de procesos de ingeniería, Spec Driven Development (SDD) y especificaciones | shared |
| `engineering/verification/shared.md` | Verificacion transversal | shared |
<!-- engineering:end -->

### Operations

<!-- operations:begin -->
| Documento | Contenido | key |
|---|---|---|
| `operations/docker.md` | Ejemplo de formato para documentos de operaciones | shared,design,delivery,gardening |
<!-- operations:end -->

### Quality

<!-- quality:begin -->
| Documento | Contenido | key |
|---|---|---|
| `quality/golden-principles.md` | Principios anti-drift | shared,design,delivery,gardening |
| `quality/gardening.md` | Runbook de deteccion y reporte de drift | shared,gardening,design |
| `quality/quality-scores.md` | Scores de calidad vigentes | shared,gardening,design,delivery |
| `quality/self-review-checklist.md` | Checklist de revision | shared,delivery |
<!-- quality:end -->

### Exec Plans

<!-- exec-plans:begin -->
| Documento | Contenido | key |
|---|---|---|
| `exec-plans/template.md` | Plantilla para planes largos | shared,design |
| `exec-plans/completed/` | Planes completados historicos | shared,design,gardening |
<!-- exec-plans:end -->

## Regla de consumo

- Las keys de grupo (`design`, `delivery`, `gardening`) se usan solo en secciones transversales.
- No usar keys de grupo dentro de `engineering`; ahi solo aplican keys tecnicas.
- Las keys tecnicas no reemplazan a las transversales: se combinan entre secciones cuando un rol necesita contexto de proceso y de capa.

## Mantenimiento

No crear `README.md` dentro de subcarpetas de `docs/`. Este archivo es el unico indice. Si se crea, renombra o elimina un documento, actualizar este README y las referencias en prompts, scripts y tests.

## Regla de precedencia

Si dos documentos parecen contradecirse, crea un brief de resolucion y comunicalo al equipo.

