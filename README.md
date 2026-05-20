# Harness Template — Arnés de Agentes de IA 🚀

Este repositorio contiene la plantilla base y las herramientas necesarias para instalar y configurar un **arnés multi-agente** en cualquier proyecto. El arnés proporciona una estructura documental, roles de agente predefinidos, un ciclo de vida para las tareas (features) y validaciones automáticas, permitiendo que agentes de IA colaboren de forma ordenada, segura y trazable sin interferir con el stack tecnológico de tu código.

---

## 🗺️ Flujo de Trabajo del Onboarding

El siguiente diagrama ilustra el proceso completo desde la copia inicial del arnés hasta la activación del entorno operativo en el repositorio destino:

```mermaid
graph TD
    A[Repositorio de Destino] -->|Paso 1: Copiar .agents/| B[Repo Destino con .agents/]
    B -->|Paso 2: Ejecutar copy-files.ps1| C[Despliegue de Estructura Base]
    C -->|Paso 3: Invocar Agente de IA| D[Ejecución de la Skill: harness-onboarding]
    
    subgraph Skill de Onboarding (Fases)
        D --> D1[Fase 1: Análisis del Stack y Estructura]
        D1 --> D2[Fase 2: Personalización de Archivos y Docs]
        D2 --> D3[Fase 3: Validación con ./init.ps1 o ./init.sh]
        D3 --> D4[Fase 4: Generación de Informe de Onboarding]
    end
    
    D4 -->|Init Verde exit code 0| E[Arnés Listo y Operativo]
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

Sigue estos pasos para instalar el arnés en tu proyecto:

### Paso 1 — Copiar la carpeta `.agents/`
Copia la carpeta `.agents` (que contiene las skills, los prompts de roles de agentes y los scripts de copia) desde este repositorio a la raíz de tu proyecto destino.

### Paso 2 — Desplegar la estructura base (Template)
Desde la raíz de tu proyecto destino, ejecuta el script de PowerShell para copiar todos los archivos del arnés (como `AGENTS.md`, `CHECKPOINTS.md`, los scripts de CLI Python y las plantillas de documentación) a su ubicación final en la raíz del repositorio:

*   **En Windows (PowerShell):**
    ```powershell
    .\.agents\skills\harness-onboarding\copy-files.ps1
    ```
*   **En Linux / WSL / macOS:**
    ```bash
    pwsh .agents/skills/harness-onboarding/copy-files.ps1
    ```
    > [!NOTE]
    > Si no dispones de PowerShell en Linux/macOS, puedes copiar el contenido de la carpeta `.agents/skills/harness-onboarding/template/` directamente a la raíz de tu repositorio manteniendo la misma estructura de directorios.

### Paso 3 — Iniciar el Onboarding con el Agente de IA
Abre tu proyecto destino en tu IDE favorito y solicita al agente de IA la instalación del arnés usando una frase clave similar a esta:
```text
Instala el harness para este proyecto
```
El agente detectará la skill `harness-onboarding`, ejecutará las fases correspondientes y configurará todo de forma automática.

---

## 💻 Compatibilidad y Configuración según tu IDE o Agente de IA

El arnés y sus skills están diseñados para ser agnósticos y compatibles con las principales herramientas de desarrollo asistido por IA. A continuación se detalla cómo invocarlos y configurarlos en cada entorno:

### 1. Antigravity (Google DeepMind)
Antigravity es un entorno altamente estructurado que detecta y ejecuta automáticamente las skills de desarrollo.
*   **Cómo copiar:** Copia la carpeta `.agents/` a la raíz del repositorio de trabajo.
*   **Cómo invocar:** Escribe en el chat:
    ```text
    Instala el harness para este proyecto
    ```
    Antigravity detectará la skill `harness-onboarding` en el directorio de skills, abrirá [SKILL.md](file:///c:/Dev/GitWSL/Test/harness-template/.agents/skills/harness-onboarding/SKILL.md) con su herramienta de visualización de archivos, y ejecutará el análisis y la edición guiada de forma autónoma.
*   **Uso diario:** El agente lee el archivo `AGENTS.md` al iniciar cada turno de trabajo para identificar el rol solicitado (Arquitecto, Implementador, Revisor o Jardinero) y actualizar el archivo de progreso `progress/current.md`.

### 2. Windsurf (Codeium)
Windsurf soporta de manera nativa la definición de habilidades personalizadas a través de la carpeta `.agents/skills/`.
*   **Cómo copiar:** Coloca la carpeta `.agents/` en el raíz de tu espacio de trabajo.
*   **Cómo invocar:** En el chat de Cascade (el agente interactivo de Windsurf), ingresa:
    ```text
    Instala el harness para este proyecto
    ```
    Cascade leerá la sección frontmatter de `SKILL.md` (donde se define el nombre y descripción del trigger de la skill) e iniciará el plan de ejecución en 4 fases, solicitando tus aprobaciones previas en cada paso.

### 3. Cursor
Cursor utiliza configuraciones personalizadas y reglas de contexto específicas.
*   **Configuración recomendada:** Crea o edita el archivo `.cursorrules` en la raíz de tu proyecto destino agregando la siguiente referencia:
    ```markdown
    Lee siempre el archivo AGENTS.md en la raíz antes de realizar cualquier tarea.
    Para el onboarding inicial, sigue las instrucciones de la skill en: .agents/skills/harness-onboarding/SKILL.md
    ```
*   **Cómo invocar:** En el chat de Cursor Composer (o Cmd+K), escribe:
    ```text
    @SKILL.md Instala el harness para este proyecto
    ```
    Al utilizar el símbolo `@` y apuntar a `SKILL.md`, obligas a Cursor a incluir el archivo de instrucciones completo de la skill en su ventana de contexto activo.

### 4. Cline / Roo Code (Roo Clinic)
Cline y Roo Code son extensiones open-source potentes basadas en directivas de sistema.
*   **Configuración recomendada:** Agrega al archivo `.clinerules` o `.instructions.md` la regla:
    ```markdown
    Antes de cualquier tarea de código, ejecuta init.ps1 (o init.sh) y lee AGENTS.md para conocer tu rol actual.
    ```
*   **Cómo invocar:** Ejecuta la siguiente orden en el chat de la extensión:
    ```text
    Lee las instrucciones en .agents/skills/harness-onboarding/SKILL.md y ejecuta el onboarding de este repositorio
    ```
    Cline tiene la capacidad de leer archivos locales, por lo que cargará la skill y ejecutará las tareas de edición y testing de forma secuencial.

### 5. Visual Studio Code (GitHub Copilot Chat)
GitHub Copilot en VS Code permite referenciar archivos y el espacio de trabajo actual.
*   **Configuración recomendada:** Crea un archivo en la ruta `.github/copilot-instructions.md` con el siguiente contenido:
    ```markdown
    Lee siempre AGENTS.md antes de comenzar a trabajar en cualquier feature y valida tus cambios con ./init.ps1 o ./init.sh.
    ```
*   **Cómo invocar:** En la barra de chat de Copilot, ingresa:
    ```text
    @workspace Lee el archivo .agents/skills/harness-onboarding/SKILL.md e instala el harness en este proyecto
    ```
    Copilot analizará el espacio de trabajo, localizará la guía y te asistirá escribiendo el código de configuración de los archivos.

### 6. OpenAI Codex / ChatGPT (Custom GPTs / API)
En entornos sin acceso nativo al sistema de archivos local, debes actuar como puente de ejecución.
*   **Cómo utilizar:**
    1.  Crea un **Custom GPT** y sube el contenido de `SKILL.md`, `detection-guide.md` y `file-targets.md` como parte de sus archivos de conocimiento (Knowledge).
    2.  Alternativamente, puedes copiar y pegar el contenido de [SKILL.md](file:///c:/Dev/GitWSL/Test/harness-template/.agents/skills/harness-onboarding/SKILL.md) directamente al inicio de la sesión del chat.
    3.  Pídele al modelo que analice tu stack y edite los archivos necesarios.
    4.  Copia las salidas sugeridas del modelo a tus archivos locales y ejecuta los scripts del CLI o `./init.sh` en tu terminal local, retroalimentando al chat con los resultados o errores obtenidos.

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
