# Harness Template — Arnés de Agentes de IA

Plantilla base para instalar un **arnés multi-agente** en cualquier repositorio. Proporciona estructura, roles, ciclo de vida de features y validación automática para que agentes de IA trabajen de forma ordenada, trazable y sin romper el proyecto.

---

## ¿Qué es el Arnés?

Un arnés de agentes es un conjunto de contratos, herramientas y documentación que vive dentro del repositorio del proyecto. Define:

- **Quién hace qué**: roles de agente con responsabilidades claras (arquitecto, implementador, revisor, jardinero).
- **Cómo avanza el trabajo**: ciclo de vida de features con estados explícitos (`pending → in_progress → done`).
- **Qué se valida y cuándo**: checkpoints automáticos (ejecutados por `init`) y checkpoints humanos (ejecutados por el revisor).
- **Dónde está cada cosa**: estructura documental canónica consultable por los agentes sin ambigüedad.

El arnés **no reemplaza tu código**: convive con él en la misma raíz del repositorio y no interfiere con el stack del proyecto.

---

## Estructura de este Repositorio

```
harness-template/
├── .agents/
│   └── skills/
│       ├── copy-files.ps1              # Copia el template al repo destino
│       └── harness-onboarding/
│           ├── SKILL.md                # Instrucciones de onboarding para el agente
│           ├── references/
│           │   ├── detection-guide.md  # Cómo detectar el stack del proyecto destino
│           │   └── file-targets.md     # Qué editar en cada archivo del template
│           └── template/               # Archivos que se instalan en el repo destino
│               ├── AGENTS.md
│               ├── CHECKPOINTS.md
│               ├── feature_list.json
│               ├── init.ps1 / init.sh
│               ├── agents/             # Prompts de roles (architect, implementer, reviewer, gardener)
│               ├── scripts/            # CLI Python: open/block/close/cancel features + validación
│               ├── docs/               # Estructura documental canónica
│               └── progress/           # Sesión activa e historial
└── README.md
```

---

## Instalación en un Proyecto Nuevo

### Prerrequisitos

- Python 3.8+ disponible en el PATH (requerido por los scripts del arnés).
- Acceso de escritura a la raíz del repositorio destino.

### Paso 1 — Copiar los archivos del template

Desde la raíz de **este repositorio** (`harness-template`), ejecuta:

**Windows (PowerShell):**
```powershell
.\.agents\skills\copy-files.ps1
```

El script te pedirá (o infiere automáticamente) el directorio raíz del proyecto destino y copia toda la carpeta `template/` allí, preservando la estructura de subdirectorios. Los archivos ya existentes en el destino **no se sobreescriben**.

**Linux / WSL:**
```bash
# El script es PowerShell; ejecutarlo desde pwsh o copiar manualmente:
pwsh .agents/skills/copy-files.ps1
```

### Paso 2 — Ejecutar el onboarding con tu agente de IA

Con los archivos ya copiados en el repo destino, abre ese repositorio en tu IDE y pide al agente:

```
Instala el harness para este proyecto
```

El agente invocará la skill `harness-onboarding` y completará automáticamente las 4 fases:

| Fase | Qué hace el agente |
|---|---|
| **1 — Análisis** | Detecta nombre, stack, comandos de test/lint y estructura de carpetas |
| **2 — Edición** | Completa `feature_list.json`, `docs/architecture/overview.md`, `docs/engineering/verification/shared.md`, `docs/harness/lifecycle.md` y `docs/harness/ticketing.md` |
| **3 — Validación** | Ejecuta `./init.ps1` o `./init.sh` y corrige hasta obtener exit code 0 |
| **4 — Informe** | Entrega un resumen de lo configurado y las secciones pendientes |

### Paso 3 — Verificar que el init está verde

```powershell
# Windows
./init.ps1

# Linux / WSL
./init.sh
```

La salida debe terminar con **0 errores**. Si hay fallos `[FAIL]`, el agente los corrige antes de finalizar el onboarding.

---

## Uso Diario con el Arnés Instalado

### Abrir una feature

```bash
python scripts/open_feature.py <feature_id>
```

Marca la feature como `in_progress` y actualiza `progress/current.md`.

### Bloquear / desbloquear

```bash
python scripts/block_feature.py <feature_id>
python scripts/unblock_feature.py <feature_id>
```

### Cerrar una feature (solo el Reviewer)

```bash
python scripts/close_feature.py <feature_id>
```

Requiere `progress/review_<feature_name>.md` con `Veredicto: APPROVED` e init verde.

### Cancelar

```bash
python scripts/cancel_feature.py <feature_id>
```

### Consultar estado del backlog

```bash
python scripts/harness_state.py
```

### Cargar documentación contextual

```bash
python scripts/docs_for.py --list all:all         # Ver todas las secciones disponibles
python scripts/docs_for.py architecture:overview  # Leer un paquete concreto
```

---

## Componentes del Arnés Instalado

### `AGENTS.md`
Punto de entrada obligatorio. El agente lo lee primero en cada sesión: ejecuta `init`, lee `progress/current.md` y determina su rol antes de editar cualquier archivo.

### `CHECKPOINTS.md`
Define dos categorías de controles:
- **A (automáticos)**: ejecutados por `init`. Validan integridad del arnés, coherencia del JSON, higiene del código y tests.
- **H (humanos)**: los evalúa el Reviewer. Cubren acceptance real, arquitectura, seguridad y cierre de sesión.

### `feature_list.json`
Backlog estructurado. Cada feature tiene `id`, `name` (snake_case), `title`, `description`, `acceptance` (criterios verificables) y `status`. Las reglas en el bloque `rules` son inmutables.

### `agents/`
Prompts de sistema para cada rol:
- `architect.md` — descubrimiento, diseño técnico y creación de backlog.
- `implementer.md` — código, tests y evidencia de implementación.
- `reviewer.md` — veredicto y cierre de features.
- `gardener.md` — detección y corrección de drift documental/código.

### `scripts/`
CLI Python. Todos los scripts son idempotentes y validan precondiciones antes de mutar estado.

| Script | Acción |
|---|---|
| `open_feature.py` | Activa una feature (`pending → in_progress`) |
| `block_feature.py` | Bloquea una feature activa |
| `unblock_feature.py` | Desbloquea una feature bloqueada |
| `close_feature.py` | Cierra una feature aprobada (`in_progress → done`) |
| `cancel_feature.py` | Cancela una feature |
| `harness_state.py` | Muestra el estado completo del backlog |
| `validate_harness.py` | Validación completa (invocada por `init`) |
| `validate_quality.py` | Validación de calidad de código |
| `docs_for.py` | CLI documental: carga paquetes de contexto para los agentes |

### `docs/`
Estructura documental canónica:

```
docs/
├── README.md                          # Índice y contrato de routing para docs_for.py
├── architecture/overview.md           # Stack, capas y decisiones de diseño
├── engineering/
│   ├── conventions/shared.md          # Convenciones de código del proyecto
│   └── verification/shared.md         # Comandos de test y lint
├── harness/
│   ├── lifecycle.md                   # Protocolo operativo del arnés
│   └── ticketing.md                   # Convenciones de tickets y features
├── exec-plans/                        # Planes de ejecución por feature
├── operations/                        # Runbooks y procedimientos operativos
└── quality/                           # Estándares y métricas de calidad
```

### `progress/`
- `current.md` — sesión activa: feature en curso, estado y notas.
- `history.md` — bitácora append-only de sesiones cerradas.
- `archive/` — documentos de implementación y revisión de features cerradas.

---

## Compatibilidad con IDEs y Agentes de IA

El arnés es agnóstico a la plataforma. Funciona con cualquier agente que pueda leer archivos del repositorio. A continuación se indica cómo activarlo en cada entorno:

### Cursor

Cursor lee automáticamente `AGENTS.md` si está en la raíz del repositorio. Para activar el arnés:

1. Abre el proyecto (con el arnés ya instalado) en Cursor.
2. En el chat del agente, escribe:
   ```
   Lee AGENTS.md y ejecuta init antes de empezar.
   ```
3. Para instalar el arnés en un proyecto nuevo desde Cursor, clona este repositorio como workspace adicional y escribe:
   ```
   Instala el harness para este proyecto
   ```
   Cursor usará la skill `harness-onboarding` automáticamente.

### Windsurf

Windsurf (Cascade) soporta skills declaradas en `.agents/skills/`. El arnés está diseñado nativamente para este entorno:

1. Con este repositorio abierto como workspace, escribe en el chat:
   ```
   Instala el harness para este proyecto
   ```
2. Cascade detecta la skill `harness-onboarding` y ejecuta las 4 fases sin intervención manual.
3. Para uso diario, el agente lee `AGENTS.md` al inicio de cada sesión y sabe qué rol asumir.

### Antigravity

Antigravity respeta archivos de instrucciones en la raíz. Para activar el arnés:

1. Asegúrate de que `AGENTS.md` y `CHECKPOINTS.md` estén en la raíz del proyecto (tras el onboarding).
2. En el system prompt o en el primer mensaje de sesión, incluye:
   ```
   Lee AGENTS.md antes de comenzar cualquier tarea.
   ```
3. Para el onboarding inicial, copia este repositorio junto al proyecto destino y pide al agente que ejecute `.agents/skills/copy-files.ps1` seguido del onboarding.

### Visual Studio Code (con GitHub Copilot / extensiones de agente)

VS Code no tiene una convención estándar de `AGENTS.md`, pero puedes activar el arnés de dos formas:

**Con GitHub Copilot Chat:**
```
@workspace Lee el archivo AGENTS.md y ejecuta ./init.ps1 antes de empezar.
```

**Con `.github/copilot-instructions.md`** (si usas Copilot Workspace):
Crea o agrega al archivo `.github/copilot-instructions.md`:
```markdown
Lee siempre AGENTS.md al inicio de cada sesión y ejecuta init antes de editar código.
```

**Con extensiones MCP (Model Context Protocol):**
Si tu extensión soporta MCP, las skills en `.agents/skills/` pueden registrarse como herramientas disponibles.

### OpenAI Codex / ChatGPT con herramientas

Codex opera vía API o playground. Para usar el arnés:

1. Incluye el contenido de `AGENTS.md` en el system prompt de la sesión.
2. Usa el contexto de `feature_list.json` y `progress/current.md` como parte del prompt de usuario.
3. Las transiciones de estado (abrir/cerrar features) se ejecutan manualmente vía CLI Python en tu terminal local.

```bash
python scripts/open_feature.py 1
# Pega el contenido de progress/current.md en el contexto de Codex
```

### Claude Code (Anthropic)

Claude Code lee `AGENTS.md` y archivos Markdown del repositorio de forma nativa. Para activar el arnés:

1. Inicia Claude Code en la raíz del proyecto (con el arnés instalado).
2. Claude Code detectará `AGENTS.md` automáticamente en el contexto inicial.
3. Para el onboarding desde cero, ejecuta:
   ```
   claude "Instala el harness para este proyecto siguiendo .agents/skills/harness-onboarding/SKILL.md"
   ```
4. Para uso diario, el flujo recomendado es:
   ```
   claude "Lee AGENTS.md, ejecuta init y continúa con la feature en curso"
   ```

---

## Flujo Completo de una Feature (Resumen)

```
1. Arquitecto diseña la feature y la agrega a feature_list.json
2. python scripts/open_feature.py <id>        ← activa la feature
3. Implementador trabaja → código + tests
4. python scripts/validate_harness.py         ← init verde requerido
5. Reviewer evalúa checkpoints H1–H3
6. Reviewer escribe progress/review_<name>.md con Veredicto: APPROVED
7. python scripts/close_feature.py <id>       ← cierre + archivo
```

---

## Reglas del Arnés

- **Una sola feature `in_progress` a la vez.**
- **No se cierra una feature sin init verde** (exit code 0).
- **No se inventan features** en `feature_list.json`: solo lo inferible del código real.
- **No se eliminan archivos del arnés**: solo se edita su contenido.
- **`scripts/` y `progress/history.md` son inmutables** por el agente implementador.
- **`agents/*.md` no llevan el nombre del proyecto**: los roles son genéricos y reutilizables.

---

## Verificación Rápida Post-Instalación

```powershell
# Windows
./init.ps1

# Linux / WSL
./init.sh
```

Salida esperada: `✅ 0 errores` con todos los checkpoints A1–A5 en verde.

---

Este arnés garantiza consistencia, trazabilidad y calidad auditada en cada contribución de agentes autónomos de IA, independientemente del stack tecnológico del proyecto.
