# Detection Guide — Análisis del proyecto destino

## Objetivo

Antes de editar cualquier archivo del harness, recolectar suficiente contexto del proyecto destino para completar los genéricos con información real y verificable.

---

## Fase 1 — Nombre y descripción del proyecto

Leer en orden, tomar el primer valor encontrado:

| Archivo | Campo |
|---|---|
| `package.json` | `.name` |
| `pyproject.toml` | `[project] name` o `[tool.poetry] name` |
| `go.mod` | primera línea `module <nombre>` |
| `Cargo.toml` | `[package] name` |
| `pom.xml` | `<artifactId>` |
| `build.gradle` / `build.gradle.kts` | `rootProject.name` en `settings.gradle` |
| `.git/config` | `url = ...` → último segmento sin `.git` |
| Nombre del directorio raíz | fallback final |

El nombre debe convertirse a `snake_case` para `feature_list.json` y mantenerse legible para los agentes y documentos.

---

## Fase 2 — Stack tecnológico

### Archivos que revelan el lenguaje principal

| Archivo presente | Lenguaje / runtime |
|---|---|
| `package.json` | Node.js / JavaScript / TypeScript |
| `tsconfig.json` | TypeScript |
| `pyproject.toml` / `setup.py` / `requirements.txt` | Python |
| `go.mod` | Go |
| `Cargo.toml` | Rust |
| `pom.xml` / `build.gradle` | Java / Kotlin |
| `Gemfile` | Ruby |
| `mix.exs` | Elixir |
| `composer.json` | PHP |
| `*.csproj` / `*.sln` | C# / .NET |

### Framework / librería principal

Leer el archivo de dependencias correspondiente y buscar:

**Node.js** — leer `dependencies` + `devDependencies` en `package.json`:
- `react` / `next` → React / Next.js
- `vue` / `nuxt` → Vue / Nuxt
- `svelte` / `sveltekit` → Svelte
- `express` / `fastify` / `hono` → API backend
- `nest` → NestJS

**Python** — leer `[project].dependencies` en `pyproject.toml` o `requirements.txt`:
- `fastapi` / `flask` / `django` / `starlette` → web framework
- `sqlalchemy` / `tortoise-orm` → ORM
- `pydantic` → validación de modelos

**Go** — leer `go.mod` `require` block:
- `gin-gonic/gin` / `labstack/echo` / `gofiber/fiber` → web framework

### Base de datos

Buscar en dependencias o en archivos de configuración:
- `pg` / `postgres` / `psycopg2` / `asyncpg` → PostgreSQL
- `mysql` / `mysqlclient` / `pymysql` → MySQL / MariaDB
- `mongodb` / `motor` / `pymongo` → MongoDB
- `redis` / `aioredis` / `ioredis` → Redis
- `sqlite3` / `better-sqlite3` → SQLite
- `prisma` / `drizzle-orm` / `typeorm` / `sequelize` → ORM (inferir DB de config)

---

## Fase 3 — Estructura de carpetas

Listar el primer nivel del repo. Inferir:

| Carpeta presente | Significado |
|---|---|
| `src/` | código fuente principal |
| `app/` | aplicación (Next.js App Router, Django, etc.) |
| `packages/` / `apps/` | monorepo |
| `cmd/` | binarios Go |
| `lib/` / `core/` | lógica compartida |
| `tests/` / `test/` / `__tests__/` / `spec/` | tests |
| `docs/` | documentación (ya existe en harness) |
| `infra/` / `terraform/` / `k8s/` / `helm/` | infraestructura |
| `scripts/` | scripts utilitarios (ya existe en harness) |
| `migrations/` | migraciones de base de datos |
| `public/` / `static/` / `assets/` | archivos estáticos |

Identificar si es:
- **Monorepo**: hay `packages/`, `apps/` o `workspaces` en `package.json`
- **Fullstack**: hay tanto carpetas de frontend como de backend en el mismo repo
- **Backend puro**: solo API / workers / servicios
- **Frontend puro**: solo UI

---

## Fase 4 — Comandos de test y lint

### Python
Buscar en orden:
1. `pyproject.toml` sección `[tool.pytest.ini_options]` → confirma pytest
2. `Makefile` targets `test`, `lint`, `check`
3. Presencia de `pytest.ini` o `setup.cfg` con `[tool:pytest]`
4. Default: `python -m pytest`

Para linting:
- `ruff` en deps → `ruff check .`
- `flake8` → `flake8 .`
- `mypy` → `mypy .`
- `black` → `black --check .`

### Node.js
Buscar en `package.json` → `scripts`:
- `"test"` → usar ese comando exacto
- `"lint"` → usar ese comando exacto
- `"typecheck"` / `"type-check"` → añadir

### Go
- `go test ./...` (siempre aplica)
- `golangci-lint run` si hay `.golangci.yml`

### Otros
- Presencia de `Makefile` → listar targets relevantes (`make test`, `make lint`)
- `.github/workflows/*.yml` → buscar jobs con `run:` que contengan test/lint para copiar el comando exacto

---

## Fase 5 — Capas y flujo de datos

Con la información anterior, armar mentalmente el diagrama de capas para `docs/architecture/overview.md`:

1. **Entrada** (HTTP, CLI, mensaje, evento)
2. **Capa de routing / controladores**
3. **Lógica de negocio / servicios**
4. **Persistencia / external services**
5. **Infraestructura** (Docker, cloud, CI/CD)

Si el proyecto es pequeño o la estructura no está clara, documentar solo lo que se puede inferir con certeza y marcar las secciones desconocidas con `<!-- TODO: completar -->`.

---

## Fase 6 — Features iniciales del backlog

Analizar el estado actual del código para proponer un backlog inicial realista:

- Si el repo está vacío → proponer features de bootstrapping (estructura base, CI, modelo de datos inicial)
- Si ya hay código → proponer features de las próximas mejoras o deudas técnicas evidentes
- Si hay un `TODO.md`, `ROADMAP.md`, issues o PR abiertos → tomarlos como input

Regla: **nunca inventar features**. Solo proponer lo que se puede inferir del estado real del repo.
