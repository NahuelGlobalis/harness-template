# Verificación de Ejemplo — harness-template

> Este es un documento de ejemplo que muestra el formato y estructura esperado para los archivos de verificación por capa.

## Contexto

Este ejemplo demuestra cómo documentar verificación para una capa hipotética. Cada capa real (api, web, infra, etc.) debe tener su propio archivo de verificación específico.

## Nivel 1 — Tests unitarios (obligatorio)

Toda función pública tiene al menos un test que:
1. Cubre el camino feliz.
2. Cubre al menos un camino de error.

Comandos:

```bash
# Ejemplo: ejecutar tests unitarios de la capa
cd <directorio-de-la-capa>
python3 -m pytest tests/unit/ -v
```

## Nivel 2 — Tests de integración (obligatorio para features de UI/API)

Las features que exponen interfaces se verifican ejecutando la interfaz real contra datos temporales.

```bash
# Ejemplo: tests de integración con datos temporales
cd <directorio-de-la-capa>
python3 -m pytest tests/integration/ -v -m "not live"
```

## Nivel 3 — Smoke test manual (recomendado)

Antes de cerrar sesión, ejecutar un flujo end-to-end con datos temporales.

```bash
# Ejemplo: levantar el servicio y verificar respuesta
cd <directorio-de-la-capa>
docker compose up -d

# Verificar que el servicio responde
curl http://localhost:<puerto>/health
```

## Casos específicos de la capa

### Escenario A — Verificación de funcionalidad X

```bash
# Comando para verificar la funcionalidad X
# Explicación de qué se espera ver
```

### Escenario B — Verificación de funcionalidad Y

```bash
# Comando para verificar la funcionalidad Y
# Explicación de qué se espera ver
```

## Verificación final

Después de verificar la capa específica, ejecutar el init de la plataforma desde la raíz del repositorio:

```bash
# Windows PowerShell
./init.ps1

# WSL/Linux
./init.sh
```

Si está rojo, **no** marques nada como `done`.

## Anti-patrones específicos de esta capa

- Anti-patrón 1 → descripción y solución
- Anti-patrón 2 → descripción y solución
- Anti-patrón 3 → descripción y solución
