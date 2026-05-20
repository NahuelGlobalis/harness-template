---
name: harness-onboarding
description: >
  Analiza un proyecto arbitrario y adapta los archivos genéricos del harness-template
  al contexto real del proyecto: detecta stack, tecnología, estructura y convenciones,
  luego completa docs/architecture/overview.md, feature_list.json, docs/engineering/verification/shared.md,
  docs/harness/lifecycle.md, docs/harness/ticketing.md y convenciones de ingeniería con información
  real y verificable, dejando el harness operativo (init verde) en el proyecto destino.
  Usar cuando el usuario pida "instalar el harness", "adaptar el template", "configurar el harness
  para este proyecto" o cualquier variante de onboarding de agentes en un repositorio existente.
---

# harness-onboarding

Adapta los archivos genéricos del harness-template al proyecto actual en cuatro fases secuenciales.
Lee [`references/detection-guide.md`](references/detection-guide.md) para la estrategia de análisis
y [`references/file-targets.md`](references/file-targets.md) para saber exactamente qué editar en cada archivo.

---

## Precondición

La carpeta `.agents/` ya fue copiada al proyecto destino.
Como primer paso del onboarding, el agente debe asegurarse de desplegar (o actualizar) los archivos base del arnés ejecutando el script de copia:

- En Windows (PowerShell):
  ```powershell
  .agents/skills/harness-onboarding/copy-files.ps1
  ```
- En Linux / WSL:
  ```bash
  pwsh .agents/skills/harness-onboarding/copy-files.ps1
  ```

*(Si PowerShell no está disponible en Linux, el agente debe copiar de forma recursiva todo el contenido de `.agents/skills/harness-onboarding/template/` directamente en la raíz de destino).*

Verificar la estructura inicial ejecutando:
```
./init.ps1   (Windows)
./init.sh    (Linux / WSL)
```

Si el init falla por archivos faltantes o desactualizados del arnés, resolverlo antes de continuar con la Fase 1.

---

## Fase 1 — Análisis del proyecto

> Lee `references/detection-guide.md` completo antes de empezar esta fase.

Ejecutar en orden:

1. **Nombre del proyecto** — leer `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml` o el nombre del directorio raíz. Convertir a `snake_case` para JSON y mantener legible para docs.

2. **Stack y lenguaje principal** — identificar lenguaje, framework, base de datos e infraestructura leyendo los archivos de dependencias.

3. **Estructura de carpetas** — listar el primer nivel del repo. Clasificar como monorepo / fullstack / backend / frontend.

4. **Comandos de test y lint** — buscar en `package.json scripts`, `pyproject.toml`, `Makefile` y `.github/workflows/*.yml`. Anotar el comando exacto.

5. **Estado del código** — hay código existente o el repo está vacío? Hay `TODO.md`, `ROADMAP.md` o issues que sugieran próximas features?

Documentar internamente los valores encontrados antes de pasar a Fase 2. No editar archivos todavía.

---

## Fase 2 — Edición de archivos (orden de prioridad)

> Lee `references/file-targets.md` para las reglas exactas de cada archivo.

### 2.1 Críticos (siempre)

**`feature_list.json`**
- Reemplazar `project` y `description` con el nombre/descripción real.
- Añadir 1–5 features iniciales derivadas del análisis. Solo features que se puedan inferir del estado real del repo; nunca inventar.
- No tocar el bloque `rules`.

**`docs/architecture/overview.md`**
- Completar con stack, capas, flujo principal y decisiones vigentes.
- Para secciones sin información suficiente, usar `<!-- TODO: completar -->`.

### 2.2 Alta prioridad

**`docs/engineering/verification/shared.md`**
- Simplificar a los comandos reales del proyecto (eliminar secciones de otros ecosistemas).
- Incluir el comando exacto de tests y lint encontrado en Fase 1.

**`docs/harness/lifecycle.md`**
- Reemplazar `harness-template` en el título H1 con el nombre real del proyecto.
- No modificar el cuerpo.

**`docs/harness/ticketing.md`**
- Reemplazar `harness-template` en el título H1 con el nombre real del proyecto.
- No modificar el cuerpo.

### 2.3 Media prioridad

**`feature_list.archive.json`** (si existe)
- Actualizar `project` y `description` con el nombre real.
- No tocar el array `features`.

**`docs/engineering/conventions/shared.md`**
- Ajustar los valores de espaciado, nombres de archivo y herramientas al stack real.
- Mantener la estructura; solo corregir lo que contradice el proyecto real.

### 2.4 Baja prioridad (condicional)

**`init.ps1` / `init.sh`**
- Solo modificar si el proyecto tiene tests propios que deben correr en cada `init`.
- Añadir el comando de tests **antes** de `validate_harness.py`.
- Ver ejemplo en `references/file-targets.md`.

**`CHECKPOINTS.md`** sección A4b
- Ajustar el bullet de separación de capas al patrón de arquitectura real.
- Si no aplica la regla de routers/tools, reemplazar por la regla de capas correspondiente o eliminar ese bullet.

---

## Fase 3 — Validación

Después de todas las ediciones, ejecutar:

```
./init.ps1   (Windows)
./init.sh    (Linux / WSL)
```

**El init debe terminar verde (exit code 0) con 0 errores.**

Si falla:
- Leer los mensajes `[FAIL]` y corregir solo los archivos señalados.
- Volver a ejecutar `init` hasta que pase.
- No continuar a Fase 4 si hay errores.

---

## Fase 4 — Informe de onboarding

Generar un resumen conciso para el usuario con:

```markdown
## Harness adaptado para: <nombre del proyecto>

### Stack detectado
- Lenguaje: ...
- Framework: ...
- Base de datos: ...

### Archivos completados
- `feature_list.json` — proyecto: <nombre>, N features iniciales
- `docs/architecture/overview.md` — stack y capas documentados
- `docs/engineering/verification/shared.md` — comando: `<comando>`
- `docs/harness/lifecycle.md` — título actualizado
- `docs/harness/ticketing.md` — título actualizado
- [otros archivos modificados]

### Secciones pendientes (TODO)
- [listar cualquier sección marcada como TODO en los docs]

### init
✅ 0 errores, N warnings
```

---

## Reglas duras

- **No inventar features** en `feature_list.json`. Solo lo que se puede inferir del código real.
- **No eliminar archivos del harness**. Solo editar contenido.
- **No modificar `scripts/`** ni `progress/history.md`.
- **No modificar `agents/*.md`** — los roles ya son genéricos y no necesitan el nombre del proyecto.
- Si el `init` falla después de las ediciones, corregir antes de entregar.
- Si un archivo no tiene información suficiente para completarse, dejarlo con `<!-- TODO: completar -->` y listarlo en el informe final.
