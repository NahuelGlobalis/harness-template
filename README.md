# Harness Template (Arnés de Agentes de IA)

Este repositorio contiene la plantilla base y las herramientas necesarias para incorporar de forma estructurada un **Arnés de Agentes de IA** en cualquier proyecto existente o nuevo. El arnés permite organizar, guiar y auditar el trabajo de agentes de inteligencia artificial en las distintas fases del desarrollo de software (diseño, implementación, revisión y mantenimiento).

---

## 🚀 ¿Qué es el Arnés de Agentes?

El arnés proporciona un marco de trabajo (framework) operativo para que agentes de desarrollo autónomos interactúen de forma segura con un repositorio. Establece:
1. **Reglas Claras**: Definición de roles y comportamientos específicos para los agentes en [AGENTS.md](file:///c:/Dev/GitWSL/Test/harness-template/.agents/skills/harness-onboarding/template/AGENTS.md).
2. **Ciclo de Vida de Features**: Transición estructurada mediante comandos CLI para abrir, bloquear, desbloquear, y cerrar features.
3. **Métricas de Calidad y Checkpoints**: Validación automática de la integridad del repositorio y el código mediante [CHECKPOINTS.md](file:///c:/Dev/GitWSL/Test/harness-template/.agents/skills/harness-onboarding/template/CHECKPOINTS.md).
4. **Documentación Autocontenida**: Una estructura estándar para almacenar requerimientos, especificaciones, bitácoras e historial de cambios.

---

## 📂 Estructura del Repositorio

A continuación se detalla la estructura principal de este repositorio de plantilla:

*   **[.agents/](file:///c:/Dev/GitWSL/Test/harness-template/.agents/)**: Directorio que centraliza las capacidades y scripts de automatización de los agentes.
    *   **[skills/](file:///c:/Dev/GitWSL/Test/harness-template/.agents/skills/)**:
        *   **[copy-files.ps1](file:///c:/Dev/GitWSL/Test/harness-template/.agents/skills/copy-files.ps1)**: Script en PowerShell diseñado para copiar todos los archivos del arnés base a la raíz de un repositorio de destino.
        *   **[harness-onboarding/](file:///c:/Dev/GitWSL/Test/harness-template/.agents/skills/harness-onboarding/)**: Skill especializada en la adaptación e instalación del arnés en un proyecto real.
            *   **[SKILL.md](file:///c:/Dev/GitWSL/Test/harness-template/.agents/skills/harness-onboarding/SKILL.md)**: Manual de ejecución paso a paso (en 4 fases) para inicializar y adaptar la plantilla al stack del repositorio objetivo.
            *   **[references/](file:///c:/Dev/GitWSL/Test/harness-template/.agents/skills/harness-onboarding/references/)**: Guías de referencia para la detección del stack tecnológico y edición de archivos críticos.
                *   **[detection-guide.md](file:///c:/Dev/GitWSL/Test/harness-template/.agents/skills/harness-onboarding/references/detection-guide.md)**: Guía para analizar el stack y configuración del proyecto objetivo.
                *   **[file-targets.md](file:///c:/Dev/GitWSL/Test/harness-template/.agents/skills/harness-onboarding/references/file-targets.md)**: Reglas precisas y ejemplos de cómo rellenar los archivos editables.
            *   **[template/](file:///c:/Dev/GitWSL/Test/harness-template/.agents/skills/harness-onboarding/template/)**: Los archivos reales del arnés que serán instalados en el repositorio de destino (ej. `AGENTS.md`, `CHECKPOINTS.md`, scripts de features, plantillas documentales).

---

## 🛠️ ¿Cómo usar esta Plantilla?

Para instalar y configurar el arnés en un nuevo proyecto objetivo, se deben seguir los siguientes pasos:

### Paso 1: Copiar los Archivos de la Plantilla
Ejecuta el script de copia desde PowerShell en la raíz de este repositorio:
```powershell
powershell -File .agents/skills/copy-files.ps1
```
*Este script copiará todo el contenido de la carpeta `template` al directorio del proyecto destino.*

### Paso 2: Ejecutar el Onboarding de Agentes
Utiliza la skill **[harness-onboarding](file:///c:/Dev/GitWSL/Test/harness-template/.agents/skills/harness-onboarding/SKILL.md)** para adaptar la configuración general al stack real del proyecto objetivo. El proceso consta de cuatro fases secuenciales:

1.  **Fase 1: Análisis del Proyecto**: Detección del nombre, lenguaje principal, frameworks, comandos de test/lint y estructura de carpetas.
2.  **Fase 2: Edición de Archivos**: Configuración de archivos clave como:
    *   `feature_list.json`
    *   `docs/architecture/overview.md`
    *   `docs/engineering/verification/shared.md`
    *   `docs/harness/lifecycle.md` y `docs/harness/ticketing.md`
3.  **Fase 3: Validación**: Ejecución de `./init.ps1` o `./init.sh` para verificar que el arnés esté verde (exit code 0).
4.  **Fase 4: Informe**: Creación del informe de onboarding para el usuario.

---

## 🧩 Componentes del Arnés Instalado

Una vez inicializado en el repositorio de destino, el arnés consta de:

*   **`init.ps1` / `init.sh`**: Scripts de arranque y validación continua. Se ejecutan automáticamente al iniciar tareas para comprobar la coherencia de los datos.
*   **`AGENTS.md`**: Punto de entrada obligatorio y mapa de navegación para los agentes de IA.
*   **`CHECKPOINTS.md`**: Listado de checkpoints automáticos y de revisión humana que deben cumplirse antes de dar una tarea por terminada.
*   **`feature_list.json`**: El backlog estructurado que almacena el estado de las tareas y sus criterios de aceptación.
*   **`agents/`**: Configuración de roles y prompts del sistema para los distintos perfiles de IA:
    *   `architect.md` (Arquitecto de Software y Backlog)
    *   `implementer.md` (Implementador de Código y Tests)
    *   `reviewer.md` (Revisor de Calidad y Cierre de Features)
    *   `gardener.md` (Jardinero / Prevención de Drift Documental)
*   **`scripts/`**: Módulos CLI en Python para gestionar transiciones de estados de las features (abrir, bloquear, cerrar).
*   **`docs/`**: Estructura canónica de la documentación del proyecto (arquitectura, convenciones, verificación, operaciones).

---

Este arnés asegura consistencia, trazabilidad y alta calidad en cada contribución realizada por agentes autónomos de IA.
