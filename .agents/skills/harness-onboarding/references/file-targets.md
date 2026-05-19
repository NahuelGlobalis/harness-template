# File Targets — Qué editar en cada archivo genérico

Para cada archivo se indica: el estado actual en el template, qué sustituir y la regla de edición.

---

## 1. `feature_list.json`

**Estado actual:**
```json
{
  "project": "harness-template",
  "description": "harness-template",
  "features": []
}
```

**Qué cambiar:**
- `project` → nombre real del proyecto (snake_case)
- `description` → descripción corta del proyecto (una línea)
- `features` → lista con 1–5 features iniciales derivadas del análisis del repo

**Regla:** Mantener intacto el bloque `rules`. Solo editar `project`, `description` y `features`.

**Formato de cada feature inicial:**
```json
{
  "id": 1,
  "name": "nombre_en_snake_case",
  "title": "Título legible",
  "description": "Qué hace esta feature, alcance concreto.",
  "acceptance": [
    "Criterio verificable 1",
    "Criterio verificable 2"
  ],
  "status": "pending"
}
```

---

## 2. `feature_list.archive.json`

**Estado actual:** el archivo existe con `"project": "harness-template"`.

**Qué cambiar:**
- `project` → nombre real del proyecto
- `description` → descripción corta del proyecto

**Regla:** No tocar el array `features`. Solo los campos de cabecera.

---

## 3. `docs/architecture/overview.md`

**Estado actual:** Solo contiene `# Arquitectura` (dos líneas).

**Qué completar:**

```markdown
# Arquitectura — <nombre del proyecto>

## Stack

- **Lenguaje principal:** <Python 3.12 / Node.js 20 / Go 1.22 / etc.>
- **Framework:** <FastAPI / Next.js / Gin / etc.>
- **Base de datos:** <PostgreSQL / MongoDB / SQLite / ninguna>
- **Infraestructura:** <Docker / Railway / Vercel / bare metal / etc.>

## Capas

| Capa | Responsabilidad | Carpeta/módulo |
|---|---|---|
| Entrada | <HTTP / CLI / eventos> | <src/routes / cmd / app/> |
| Lógica | <servicios, casos de uso> | <src/services / internal/> |
| Persistencia | <repositorios, modelos> | <src/models / db/> |
| Infraestructura | <Docker, CI/CD> | <infra/ / .github/> |

## Flujo principal

<Descripción de 2–4 líneas del flujo típico: entrada → procesamiento → salida.>

## Decisiones vigentes

- <Decisión 1: e.g., "Se usa PostgreSQL por X razón">
- <Decisión 2>

## Anti-patrones conocidos

- <Lo que NO se debe hacer en este proyecto>
```

**Regla:** Solo documentar lo que se puede inferir con certeza del código real. Usar `<!-- TODO: completar -->` para secciones sin información suficiente.

---

## 4. `docs/engineering/conventions/shared.md`

**Estado actual:** Convenciones genéricas multi-tech.

**Qué ajustar:**
- Sección "Nombres de Archivo": confirmar o corregir según el ecosistema real (ej: si es Go, usar la convención de Go)
- Sección "Espaciado": ajustar al estándar real (ej: 2 espacios para Node, 4 para Python)
- Sección "Adaptabilidad por Tecnología": reemplazar los ejemplos genéricos por los archivos de convenciones que realmente aplican al stack

**Regla:** No reescribir el documento entero. Solo ajustar los valores que contradicen las convenciones reales del proyecto.

Si el proyecto tiene un linter/formatter configurado (`.editorconfig`, `ruff.toml`, `.eslintrc`, `prettier.config.js`, etc.), mencionar explícitamente esos archivos como la fuente de verdad.

---

## 5. `docs/engineering/verification/shared.md`

**Estado actual:** Comandos genéricos para Python, Node.js y monorepos.

**Qué reemplazar:**

Simplificar a solo la sección relevante para el stack real. Añadir los comandos exactos encontrados en la Fase 4 del detection-guide.

Estructura objetivo:

```markdown
# Verificación — <nombre del proyecto>

## Comandos de test

```bash
<comando exacto para correr tests>
```

## Linting / análisis estático

```bash
<comando exacto para lint>
```

## Arnés

- **Windows:** `./init.ps1`
- **Linux/WSL:** `./init.sh`
```

**Regla:** Eliminar las secciones de otros ecosistemas que no aplican. El documento debe ser accionable sin ambigüedad.

---

## 6. `docs/harness/lifecycle.md`

**Ocurrencias a reemplazar:** `harness-template` (aparece en el título y en la primera línea del cuerpo).

```
# Harness multi-agente — harness-template
→
# Harness multi-agente — <nombre del proyecto>

Este documento es la fuente canónica del protocolo operativo del arnés. `AGENTS.md` solo enruta; los prompts en `agents/` solo adaptan cada rol a estas reglas.
→ (sin cambios en el cuerpo; solo el título)
```

**Regla:** Reemplazar solo la ocurrencia del nombre en el título H1. No modificar nada más.

---

## 7. `docs/harness/ticketing.md`

**Ocurrencias a reemplazar:** `harness-template` en el título y en la primera línea del cuerpo.

```
# Ticketing — harness-template
→
# Ticketing — <nombre del proyecto>
```

**Regla:** Igual que lifecycle.md. Solo el título H1.

---

## 8. `init.ps1` y `init.sh`

**Estado actual:** Solo invocan `scripts/validate_harness.py`.

**Cuándo modificar:** Si el proyecto tiene su propio runner de tests que debe ejecutarse en cada `init` (ej: `pytest`, `npm test`, `go test ./...`).

**Regla:** Si se añade el comando de tests del proyecto, debe ir **antes** de `validate_harness.py` para que los tests del producto fallen primero. Solo añadir si el proyecto ya tiene tests funcionando; no añadir placeholders.

**Ejemplo para Python (`init.sh`):**
```bash
#!/bin/bash
python -m pytest || exit 1

# [resto del archivo original sin cambios]
```

**Ejemplo para Node.js (`init.ps1`):**
```powershell
npm test
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# [resto del archivo original sin cambios]
```

---

## 9. `CHECKPOINTS.md`

**Estado actual:** Genérico. Los checkpoints A4b mencionan paths de ejemplo (`src/`, `tools/`).

**Qué ajustar:** Solo la sección A4b — Golden Principles:

```markdown
### A4b — Golden Principles (warnings)

- [ ] Ningún archivo de producto excede 300 líneas (Golden #8).
- [ ] <Reemplazar "Routers no importan de tools/ directamente" con la regla de separación de capas real del proyecto, si aplica>
```

**Regla:** Si la arquitectura real no tiene routers ni `tools/`, reemplazar por la regla de capas correspondiente (ej: "Controllers no importan de infrastructure/ directamente"). Si no hay regla equivalente, eliminar ese bullet.

---

## 10. `AGENTS.md`

**Estado actual:** Tiene referencias a `harness-template` en la sección de memoria del sistema (fuera del repo). El archivo en sí no contiene el nombre del proyecto directamente en el cuerpo.

**Regla:** No modificar. El AGENTS.md es estructural y no referencia el nombre del proyecto.

---

## Resumen de prioridades

| Prioridad | Archivo | Impacto en `init` |
|---|---|---|
| **Crítica** | `feature_list.json` | Sí — nombre del proyecto |
| **Crítica** | `docs/architecture/overview.md` | No — pero es el doc más importante para agentes |
| **Alta** | `docs/engineering/verification/shared.md` | No — pero define cómo verificar |
| **Alta** | `docs/harness/lifecycle.md` | No |
| **Alta** | `docs/harness/ticketing.md` | No |
| **Media** | `feature_list.archive.json` | No |
| **Media** | `docs/engineering/conventions/shared.md` | No |
| **Baja** | `init.ps1` / `init.sh` | Solo si hay tests del producto |
| **Baja** | `CHECKPOINTS.md` | No |
