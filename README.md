# Catálogo de Skills de Agentes de IA — Mercantil Andina 🤖🚀

Este repositorio es el catálogo centralizado de **Skills** de agentes de Inteligencia Artificial de la compañía. Aquí se diseñan, documentan y mantienen los paquetes de instrucciones y herramientas que permiten a los asistentes de desarrollo (como Antigravity, Windsurf's Cascade, Cursor, Cline, VS Code o Claude Code) automatizar flujos de trabajo, configuraciones y tareas recurrentes de forma estandarizada y segura.

---

## 💡 ¿Qué es una Skill?

En el contexto de desarrollo asistido por IA, una **Skill** es un paquete autocontenido de instrucciones, guías, plantillas y scripts que enseña a un agente a realizar un proceso complejo dentro de un repositorio de destino. 

Cada skill consta de:
1. **`SKILL.md`**: El archivo principal que define la skill. Contiene un bloque de metadatos (frontmatter) en formato YAML que los IDEs y agentes leen para entender de qué trata la skill y cuándo invocarla, seguido de instrucciones paso a paso estructuradas en fases.
2. **`README.md`**: Documentación local dirigida a desarrolladores humanos explicando el propósito de la skill, prerrequisitos, uso y arquitectura interna.
3. **Archivos de soporte**: Scripts de automatización (PowerShell, Bash, Python), carpetas de plantillas (`template/`) y guías de referencia rápida (`references/`).

---

## 📂 Estructura del Repositorio

La estructura del repositorio está optimizada para albergar múltiples skills independientes y facilitar su mantenimiento y distribución:

```text
tpml-plataforma-skills/
├── .gitignore
├── CHANGELOG.md             # Historial de cambios y versiones del catálogo
├── README.md                # Este archivo (índice y guía general)
└── skills/                  # Directorio que agrupa todas las skills de la compañía
    └── harness-onboarding/  # Ejemplo: Skill para instalar y configurar el arnés de agentes
        ├── README.md        # Documentación de la skill para humanos
        ├── SKILL.md         # Instrucciones estructuradas para el agente de IA
        ├── copy-files.ps1   # Script de soporte para la copia del arnés
        ├── references/      # Guías de referencia específicas de la skill
        └── template/        # Plantilla del arnés a desplegar en el proyecto destino
```

---

## 🛠️ Catálogo de Skills Disponibles

Actualmente, el repositorio cuenta con las siguientes skills listas para ser utilizadas:

| Skill | Descripción | Directorio |
| :--- | :--- | :--- |
| **`harness-onboarding`** | Automatiza la instalación y personalización del **arnés multi-agente** en repositorios destino, adaptando los archivos y documentación al stack tecnológico del proyecto de forma autónoma. | [`skills/harness-onboarding`](file:///C:/Dev/GitWSL/Gitlab/Nova/tpml-plataforma-harness-skill/skills/harness-onboarding) |

---

## 🚀 ¿Cómo Utilizar una Skill en un Proyecto?

Para que un agente de IA pueda utilizar una de estas skills en un proyecto o repositorio de destino, se debe copiar la carpeta de la skill al directorio específico que tu IDE o agente escanee. 

### Paso 1: Copiar la carpeta al directorio correcto de tu IDE

Copia la carpeta de la skill que deseas utilizar (por ejemplo, `skills/<nombre-de-la-skill>/`) al directorio correspondiente dentro de tu repositorio de destino:

| IDE / Agente de IA | Directorio Destino en el Proyecto |
| :--- | :--- |
| **Windsurf (Cascade)** | `.agents/skills/<nombre-de-la-skill>/` ó `.windsurf/skills/<nombre-de-la-skill>/` |
| **Codex (OpenAI CLI)** | `.agents/skills/<nombre-de-la-skill>/` |
| **OpenCode** | `.agents/skills/<nombre-de-la-skill>/` ó `.opencode/skills/<nombre-de-la-skill>/` |
| **Cursor** | `.agents/skills/<nombre-de-la-skill>/` ó `.cursor/skills/<nombre-de-la-skill>/` |
| **VS Code (GitHub Copilot)** | `.agents/skills/<nombre-de-la-skill>/` ó `.github/skills/<nombre-de-la-skill>/` |
| **Cline** | `.agents/skills/<nombre-de-la-skill>/` ó `.cline/skills/<nombre-de-la-skill>/` |
| **Claude Code (CLI)** | `.agents/skills/<nombre-de-la-skill>/` ó `.claude/skills/<nombre-de-la-skill>/` |
| **Universal** | `.agents/skills/<nombre-de-la-skill>/` |

> [!TIP]
> La ruta `.agents/skills/` es la **opción recomendada para todos los IDEs**, ya que es reconocida de forma estándar por todos los agentes modernos. Las rutas específicas por IDE son alternativas secundarias.

### Paso 2: Invocar la Skill mediante el Chat del Agente

Una vez copiado el directorio, abre el proyecto de destino en tu IDE e interactúa con el agente pidiéndole que ejecute la tarea en lenguaje natural. El agente escaneará los archivos `SKILL.md` disponibles, emparejará la descripción y procederá a ejecutar el flujo estructurado de forma autónoma.

---

## ✍️ Cómo Contribuir o Crear una Nueva Skill

Para expandir el catálogo con nuevas automatizaciones, sigue estos pasos:

### 1. Estructura de la Skill
Crea una carpeta dentro de `skills/` con el nombre de tu skill en minúsculas y separado por guiones (ej. `skills/mi-nueva-skill/`).

Dentro de ella, crea los siguientes componentes esenciales:

#### A. El archivo `SKILL.md`

Este archivo debe comenzar con un bloque frontmatter de YAML que defina el nombre y la descripción para el autodescubrimiento del agente:

```markdown
---
name: mi-nueva-skill
description: >
  Describe de manera concisa y clara qué hace esta skill, qué problemas resuelve
  y con qué palabras clave o peticiones del usuario debe activarse.
---

# mi-nueva-skill

Instrucciones detalladas de ejecución...
```

#### B. La Estructura de Fases
Es una excelente práctica estructurar las instrucciones de `SKILL.md` en 4 fases claras para el agente:
* **Fase 1 — Análisis / Precondiciones**: Qué debe validar o analizar el agente antes de empezar.
* **Fase 2 — Edición / Ejecución**: El paso a paso de los cambios en archivos o la ejecución de comandos.
* **Fase 3 — Validación**: Qué comandos de prueba, compilación, o linters debe correr para asegurar que el cambio es correcto.
* **Fase 4 — Informe**: El formato de reporte de cierre para el usuario.

#### C. El archivo `README.md` local
Documenta para el equipo de desarrollo de manera humana:
* Qué hace la skill.
* Qué stack requiere.
* Variables de entorno o dependencias necesarias.
* Estructura de archivos internos.

### 2. Ciclo de Contribución
1. Crea una rama desde `main` (`feature/nueva-skill-nombre`).
2. Implementa tu skill en `skills/mi-nueva-skill`.
3. Registra tu nueva skill en la sección [Catálogo de Skills Disponibles](#%EF%B8%8F-cat%C3%A1logo-de-skills-disponibles) de este archivo (`README.md` raíz).
4. Actualiza el archivo [`CHANGELOG.md`](file:///C:/Dev/GitWSL/Gitlab/Nova/tpml-plataforma-harness-skill/CHANGELOG.md) siguiendo el estándar bajo la sección `[Unreleased]`.
5. Abre un Merge Request (MR) en GitLab para revisión por parte del equipo de plataforma.
