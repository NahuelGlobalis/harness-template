# Ticketing — harness-template

Este documento es la fuente canónica para escribir features en `feature_list.json`.

## Schema

Usa como referencia el ejemplo de la sección **Ejemplo** más abajo o cualquier feature existente en `feature_list.json`.

Cada feature debe tener:

- **`id`:** entero único, ascendente.
- **`name`:** identificador `snake_case` único.
- **`title`:** título legible.
- **`description`:** alcance concreto.
- **`acceptance`:** lista no vacía de criterios verificables.
- **`status`:** `pending`, `in_progress`, `done`, `blocked` o `cancelled`.

El backlog activo no tiene campos especiales para SDD. Si una feature necesita
spec, esa decisión se refleja en `specs/<feature-name>/` y en la documentación
creada por el Arquitecto, no en el schema del JSON.

## Definition of Ready

Una feature está lista para implementación cuando:

- **Campos válidos:** cumple el schema de `docs/harness/feature_list.schema.json`.
- **Acceptance verificable:** cada criterio se puede comprobar con test, comando o archivo.
- **Scope acotado:** una sola tarea, idealmente 2-3 archivos de producto.
- **Dependencias claras:** depende solo de features con `id` menor ya cerradas o no tiene dependencias.
- **Sin ambigüedad crítica:** si falta una decisión, se bloquea con una pregunta concreta.
- **SDD completo cuando aplica:** si el Arquitecto decidió usar SDD, existen
  `requirements.md`, `design.md` y `tasks.md` alineados con el acceptance.

## Acceptance de calidad

Cada criterio debe ser:

- **Verificable:** permite evidencia objetiva.
- **Atómico:** valida un resultado, no una intención general.
- **Específico:** nombra archivos, funciones, endpoints, inputs u outputs cuando aplica.
- **Independiente:** no requiere completar otra feature `pending` salvo dependencia explícita.

## Ejemplo

```json
{
  "id": 1,
  "name": "user_model",
  "title": "Modelo de Usuario",
  "description": "Dataclass User con id, name, email y created_at.",
  "acceptance": [
    "Existe src/models/user.py con la clase User",
    "User.new(name, email) genera id incremental y created_at en ISO 8601",
    "tests/test_user.py valida creación y serialización a dict"
  ],
  "use_sdd": false,
  "status": "pending"
}
```
