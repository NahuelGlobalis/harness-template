# Convenciones de Ejemplo — harness-template

> Este archivo es un ejemplo/template para nuevas convenciones.
>
> **Este archivo lo completa el Arquitecto (rol 1).**

## Propósito

Este archivo demuestra el formato y estructura estándar para las convenciones de ingeniería del proyecto.

## Convenciones de ejemplo

- **Nombres:** usar `snake_case` para archivos y variables, `PascalCase` para clases.
- **Constantes:** definidas en mayúsculas con guiones bajos (`MAX_RETRIES`).
- **Funciones:** verbos que describen la acción (`fetch_user_data`, `validate_input`).
- **Módulos:** un módulo por responsabilidad única.

## Formato de archivos

- **Encabezados:** usar `#` para título principal, `##` para secciones.
- **Listas:** usar guiones `-` para items simples.
- **Código:** bloques de código con triple backticks y lenguaje especificado.
- **Notas:** usar `>` para notas importantes o advertencias.

## Documentación

- **Docstrings:** explicar qué hace, parámetros y retorno.
- **Comentarios:** solo para explicar "por qué", no "qué".
- **Changelog:** registrar cambios mayores en `CHANGELOG.md`.

## Validación

- Todo código nuevo debe pasar tests unitarios.
- Revisión de código requerida para cambios mayores.
- Linting antes de commit.

## Ejemplo de bloque de código

```python
def process_data(data: dict) -> dict:
    """Procesa los datos de entrada aplicando transformaciones estándar."""
    # Validar entrada
    if not data:
        raise ValueError("Datos vacíos")
    
    # Transformar
    result = {k: v.upper() for k, v in data.items()}
    return result
```
