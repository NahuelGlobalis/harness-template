# Harness Template — Arnés de Agentes de IA 🚀

Este repositorio contiene la plantilla base y las herramientas necesarias para instalar y configurar un **arnés multi-agente** en cualquier proyecto. El arnés proporciona una estructura documental, roles de agente predefinidos, un ciclo de vida para las tareas (features) y validaciones automáticas, permitiendo que agentes de IA colaboren de forma ordenada, segura y trazable sin interferir con el stack tecnológico de tu código.

---

## 🗺️ Flujo de Trabajo del Onboarding

El siguiente diagrama ilustra el proceso completo desde la copia inicial del arnés hasta la activación del entorno operativo en el repositorio destino:

```mermaid
graph TD
    A[Repositorio de Destino] -->|Paso 1: Copiar harness-onboarding/ al directorio de skills del IDE| B[Repo Destino con skill instalada]
    B -->|Paso 2: Invocar Agente de IA| C[Ejecución de la Skill: harness-onboarding]
    
    subgraph "Skill de Onboarding (Fases)"
        C --> C1[Fase 1: Análisis del Stack y Estructura]
        C1 --> C2[Fase 2: Personalización de Archivos y Docs]
        C2 --> C3[Fase 3: Validación con ./init.ps1 o ./init.sh]
        C3 --> C4[Fase 4: Generación de Informe de Onboarding]
    end
    
    C4 -->|Init Verde exit code 0| D[Arnés Listo y Operativo]
```

---

## 🛠️ ¿Cómo funciona la Skill `harness-onboarding`?

La skill `harness-onboarding` (definida en [.agents/skills/harness-onboarding/SKILL.md](file:///c:/Dev/GitWSL/Test/harness-template/.agents/skills/harness-onboarding/SKILL.md)) es un conjunto de instrucciones estructuradas para que un agente de IA realice la instalación y personalización del arnés de forma autónoma. El proceso se divide en **4 fases secuenciales**:

| Fase | Tarea del Agente | Archivos Afectados / Comandos |
| :--- | :--- | :--- |
| **Fase 1: Análisis** | Detecta el stack tecnológico, el lenguaje principal, la estructura de carpetas, y los comandos de test/lint. | Lectura de dependencias (`package.json`, `pyproject.toml`, `go.mod`, etc.) |
| **Fase 2: Edición** | Adapta los archivos genéricos del template con la información real descubierta en el análisis. | `feature_list.json`, `docs/architecture/overview.md`, `docs/engineering/verification/shared.md`, `docs/harness/*.md` |
| **Fase 3: Validación** | Ejecuta el script de inicialización y resuelve cualquier error (`[FAIL]`) hasta que esté en verde. | Ejecución de `./init.ps1` (Windows) o `./init.sh` (Linux/WSL) |
| **Fase 4: Informe** | Entrega un informe de cierre al usuario detallando el stack detectado, cambios realizados y tareas pendientes. | Mensaje de finalización en Markdown |

---

## 🚀 Guía de Instalación Paso a Paso

El proceso es simple: **copia la carpeta `harness-onboarding/` al directorio de skills que busca tu IDE** y luego pídele al agente que instale el harness. La skill hará todo el resto de forma autónoma.

### Paso 1 — Copiar la skill al directorio correcto de tu IDE

Cada IDE/agente busca las skills en una ubicación específica. Copia la carpeta `harness-onboarding/` (que contiene `SKILL.md` y sus archivos de soporte) al directorio que corresponda:

| IDE / Agente | Directorio destino (proyecto) |
| :--- | :--- |
| **Windsurf (Cascade)** | `.windsurf/skills/harness-onboarding/` |
| **Cursor** | `.cursor/skills/harness-onboarding/` |
| **VS Code (GitHub Copilot)** | `.github/skills/harness-onboarding/` |
| **Cline** | `.cline/skills/harness-onboarding/` |
| **Roo Code** | `.roo/skills/harness-onboarding/` |
| **Claude Code** | `.claude/skills/harness-onboarding/` |
| **Universal (fallback)** | `.agents/skills/harness-onboarding/` |

> **Nota:** Windsurf, VS Code (Copilot) y Claude Code también descubren skills en `.agents/skills/`, por lo que la carpeta universal sirve como fallback si no conoces la ruta exacta de tu IDE.

### Paso 2 — Iniciar el Onboarding con el Agente de IA

Abre tu proyecto destino en tu IDE y solicita la instalación con una frase como:
```text
Instala el harness para este proyecto
```
El agente detectará automáticamente la skill `harness-onboarding`, la invocará y ejecutará las 4 fases de onboarding de forma autónoma.

---

## 💻 Compatibilidad por IDE

### 1. Windsurf (Cascade)
*   **Directorio de la skill:** `.windsurf/skills/harness-onboarding/`
*   **También detecta:** `.agents/skills/harness-onboarding/`
*   **Cómo invocar:** Cascade detecta la skill automáticamente por su `description` en el frontmatter. Escribe en el chat:
    ```text
    Instala el harness para este proyecto
    ```

### 2. Cursor
*   **Directorio de la skill:** `.cursor/skills/harness-onboarding/`
*   **Cómo invocar:** Cursor detecta la skill por su descripción. En el chat del agente escribe:
    ```text
    Instala el harness para este proyecto
    ```

### 3. VS Code (GitHub Copilot — Agent Mode)
*   **Directorio de la skill:** `.github/skills/harness-onboarding/`
*   **También detecta:** `.agents/skills/harness-onboarding/` y `.claude/skills/harness-onboarding/`
*   **Cómo invocar:** En el chat de Copilot en modo agente, escribe:
    ```text
    Instala el harness para este proyecto
    ```

### 4. Cline
*   **Directorio de la skill:** `.cline/skills/harness-onboarding/`
*   **También detecta:** `.clinerules/skills/` y `.claude/skills/`
*   **Cómo invocar:** En el chat de Cline escribe:
    ```text
    Instala el harness para este proyecto
    ```

### 5. Roo Code
*   **Directorio de la skill:** `.roo/skills/harness-onboarding/`
*   **Cómo invocar:** En el chat de Roo escribe:
    ```text
    Instala el harness para este proyecto
    ```

### 6. Claude Code (CLI)
*   **Directorio de la skill (proyecto):** `.claude/skills/harness-onboarding/`
*   **Directorio global (todas las sesiones):** `~/.claude/skills/harness-onboarding/`
*   **Cómo invocar:** En la sesión de Claude Code escribe:
    ```text
    Instala el harness para este proyecto
    ```

### 7. Otros agentes / IDEs no listados
Si tu IDE o agente no está en la lista, prueba con el directorio universal:
*   **Directorio de la skill:** `.agents/skills/harness-onboarding/`

Si tampoco funciona, consulta la documentación de tu herramienta buscando *"agent skills"* o *"SKILL.md"* para encontrar la ruta correcta. El formato `SKILL.md` es un estándar abierto compatible con la mayoría de los agentes modernos.

---

## 📂 Estructura General del Arnés Desplegado

Una vez finalizado el onboarding, tu repositorio de destino lucirá con la siguiente jerarquía de archivos del arnés conviviendo con tu código fuente:

```text
raiz-del-proyecto/
├── .agents/
│   ├── agents/                     # Prompts de roles del sistema (architect, implementer, reviewer, gardener)
│   └── skills/
│       └── harness-onboarding/     # Archivos de la skill de instalación
├── docs/                           # Documentación técnica del proyecto
│   ├── README.md                   # Índice documental
│   ├── architecture/               # Diagramas, stack y decisiones técnicas
│   ├── engineering/                # Convenciones de código y comandos de verificación
│   └── harness/                    # Manual operativo y flujos del arnés
├── progress/                       # Seguimiento de tareas activas e histórico
│   ├── current.md                  # Feature actualmente bajo desarrollo
│   └── history.md                  # Historial append-only de features terminadas
├── scripts/                        # CLI en Python para la gestión de features
│   ├── open_feature.py             # Abrir feature (pending -> in_progress)
│   ├── close_feature.py            # Cerrar feature (in_progress -> done)
│   ├── block_feature.py            # Bloquear feature por impedimentos
│   ├── harness_state.py            # Ver estado del backlog y features
│   └── validate_harness.py         # Validador de consistencia y formato
├── AGENTS.md                       # Protocolo de entrada para el agente
├── CHECKPOINTS.md                  # Checkpoints de calidad de código y diseño
├── feature_list.json               # Backlog de features del proyecto
├── init.ps1                        # Script de inicialización (Windows)
└── init.sh                         # Script de inicialización (Linux/WSL)
```

---

## ⚠️ Reglas Importantes del Arnés

Para asegurar que el arnés funcione de manera efectiva y no se desvirtúe su propósito, ten en cuenta las siguientes directrices:

> [!IMPORTANT]
> **1. Una sola tarea activa a la vez:** Nunca trabajes en más de una feature en estado `in_progress` simultáneamente.
> 
> **2. Init verde obligatorio:** No se permite realizar fusiones de ramas (merges) ni cerrar una feature en `feature_list.json` si el comando `./init.ps1` o `./init.sh` devuelve algún error (`exit code` distinto de 0).
> 
> **3. Mantén los roles genéricos:** Los prompts en `.agents/agents/` son transversales y no deben modificarse con nombres o rutas específicas de un único proyecto.
> 
> **4. Sin features fantasma:** Todas las features añadidas a `feature_list.json` deben ser reales, realizables y coherentes con la hoja de ruta del proyecto.
