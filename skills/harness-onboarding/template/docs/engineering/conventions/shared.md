# Convenciones de Ingeniería Compartidas

Este documento establece las convenciones transversales de codificación, estilo y organización de código aplicables a todos los proyectos derivados de esta plantilla.

## Convenciones de Archivos y Formato

- **Nombres de Archivo**: Utilizar `snake_case` para scripts de backend (Python) y `kebab-case` o `camelCase` para componentes y módulos de frontend (Node.js/TypeScript) según las mejores prácticas del ecosistema.
- **Codificación**: Todos los archivos de texto y código fuente deben guardarse en formato **UTF-8** sin BOM.
- **Fin de Línea (EOL)**: Configurar los editores para utilizar saltos de línea estilo Unix (**LF** / `\n`).
- **Espaciado**: Utilizar espacios en lugar de tabulaciones para la indentación (por defecto, 4 espacios para Python y 2 espacios para JavaScript/TypeScript/JSON).

## Calidad del Código y Comentarios

- **Evitar Comentarios Redundantes**: El código debe auto-explicarse mediante nombres de variables, funciones y clases claros y descriptivos. Los comentarios deben limitarse a explicar el "por qué" de decisiones no obvias, no el "cómo".
- **Docstrings y Documentación de API**: Proveer documentación en los puntos de entrada públicos (funciones exportadas, módulos principales, clases públicas).
- **Código Muerto**: Eliminar código comentado, importaciones no utilizadas y funciones obsoletas antes de solicitar un review.

## Control de Versiones

- **Commits Descriptivos**: Los mensajes de commit deben seguir la especificación de *Conventional Commits* (ej. `feat:`, `fix:`, `docs:`, `test:`, `refactor:`).
- **Atomicidad**: Cada commit debe representar un cambio lógico y autocontenido.

## Adaptabilidad por Tecnología

Estas convenciones representan el estándar mínimo común del repositorio. Cada sub-proyecto o componente tecnológico (Python, Node.js, Go, etc.) debe extender estas directrices mediante su propia especificación en archivos dedicados (por ejemplo, `docs/engineering/conventions/python.md` o `docs/engineering/conventions/node.md`) para definir formateadores (como Black, Prettier), linters (como Flake8, ESLint) y reglas estilísticas específicas del lenguaje.
