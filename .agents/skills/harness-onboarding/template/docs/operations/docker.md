# Ejemplo de Operaciones con Docker — harness-template

> Este es un documento de ejemplo que muestra el formato y estructura esperado para los archivos de operaciones en `docs/operations/`.

## Contexto

Este ejemplo demuestra cómo documentar operaciones relacionadas con Docker. Cada documento real debe adaptarse a las necesidades específicas del servicio o herramienta que documenta.

## Comandos básicos

### Levantar servicios

```bash
# Ejemplo: levantar todos los servicios
docker compose up -d

# Ejemplo: levantar un servicio específico
docker compose up -d <nombre-servicio>
```

### Detener servicios

```bash
# Ejemplo: detener todos los servicios
docker compose down

# Ejemplo: detener y eliminar volúmenes
docker compose down -v
```

## Escenarios comunes

### Escenario A — Desarrollo con hot reload

```bash
# Comando para levantar con hot reload
# Explicación de qué se espera ver
```

### Escenario B — Debug de un servicio

```bash
# Comando para debug
# Explicación de qué se espera ver
```

### Escenario C — Limpieza de recursos

```bash
# Comando para limpiar
# Explicación de qué se espera ver
```

## Troubleshooting

### Problema X — Descripción del problema

```bash
# Comando para diagnosticar
# Explicación de la solución
```

### Problema Y — Descripción del problema

```bash
# Comando para diagnosticar
# Explicación de la solución
```

## Verificación

```bash
# Comando para verificar que todo funciona correctamente
```

## Variables de entorno

Descripción de las variables de entorno necesarias:

- `VAR_1`: Descripción
- `VAR_2`: Descripción

## Referencias

- [Enlace a documentación oficial](https://example.com)
- [Enlace a recursos internos](https://example.com)
