# Guía Transversal de Verificación

Este documento establece las directrices y comandos estándar para verificar y validar la calidad del software antes de considerar una feature completada.

## Proceso de Verificación

Toda feature implementada debe cumplir con el siguiente flujo de verificación antes del cierre:

1. **Pruebas Automatizadas**: Ejecución de las suites de pruebas unitarias, de integración y extremo a extremo pertinentes.
2. **Análisis Estático (Linting)**: Verificación de formato y reglas de código.
3. **Autoevaluación (Self-Review)**: Validación manual utilizando los checklists de calidad del proyecto.
4. **Smoke Testing**: Ejecución rápida del sistema en un entorno de desarrollo local para asegurar que las rutas críticas funcionan.

## Comandos de Pruebas por Ecosistema

### Python

Para ejecutar pruebas unitarias en proyectos de Python, se utiliza `pytest`.

```bash
# Ejecutar todas las pruebas con pytest
python -m pytest

# Ejecutar con cobertura de código
python -m pytest --cov=src
```

### Node.js

Para proyectos basados en Node.js (JavaScript / TypeScript), los comandos varían según el gestor de paquetes.

```bash
# Usando npm
npm test

# Usando yarn
yarn test

# Usando pnpm
pnpm test
```

### Monorepos y Workspaces

En arquitecturas monorepo que contienen múltiples paquetes/aplicaciones independientes:

```bash
# Ejecutar pruebas en todos los workspaces de npm
npm run test --workspaces

# Ejecutar pruebas en un paquete específico
npm run test --workspace=apps/api
yarn workspace api test
pnpm --filter api test
```

## Aseguramiento del Arnés

Independientemente de la tecnología del producto, el arnés de agentes siempre debe estar verificado:
- **Windows**: Ejecutar `./init.ps1`
- **Linux/WSL**: Ejecutar `./init.sh`
- Ninguno de los scripts debe reportar errores o alertas antes de la entrega al Reviewer.
