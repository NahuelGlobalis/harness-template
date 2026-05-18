# Golden Principles — harness-template

> Principios dorados inmutables. Si un agente viola uno de estos, el código
> acumula drift. El init puede reportar violaciones como warnings o errores.
>
> **Actualizado:** 2026-05-11

---

## 1. Parse, don't validate

Validar shapes en boundaries con esquemas de validación de la tecnología elegida.
No acceder a datos estructurados asumiendo propiedades arbitrarias sin un esquema
previo que garantice la forma.

---

## 2. Shared utilities over hand-rolled

Si una utilidad ya existe en el repo, usarla.
No crear helpers duplicados. Antes de escribir un helper, buscar si ya existe.

**Señal de violación:** Dos funciones en módulos distintos haciendo lo mismo.

---

## 3. Boundaries own validation

La responsabilidad de validar input pertenece a la capa de entrada:
- Los controladores o routers validan request/params.
- Los servicios asumen datos válidos y ejecutan lógica de negocio.
- Las herramientas operan sobre datos ya validados.

No mezclar validación dentro de servicios ni herramientas.

---

## 4. Config from env, never hardcoded

Toda configuración vive en variables de entorno y se lee de forma estructurada
según la convención del proyecto.

Nunca hardcodear URLs, puertos, dominios ni feature flags en código.

---

## 5. Tests mirror acceptance

Cada criterio de acceptance del ticket debe tener un test
que lo cubra directamente. Relación 1:1 visible. El naming debe reflejar el criterio.

---

## 6. No opaque dependencies

Preferir:
1. Stdlib cuando cubre el caso.
2. Implementación in-repo cuando la dependencia externa es opaca, inestable o
   tiene API surface demasiado grande para lo que necesitamos.
3. Dependencia externa solo si es estable, bien documentada y el costo de
   reimplementar supera el de adoptarla.

---

## 7. Dependency direction

Las dependencias fluyen siempre hacia adentro o hacia abajo (desde la entrada
hacia el dominio o las herramientas). Nunca al revés. Las capas superiores
no deben ser importadas por las capas inferiores.

---

## 8. Small files over large files

Los archivos de producto deben mantenerse por debajo de 300 líneas.

Si un archivo supera ese límite, extraer módulos, servicios, hooks o componentes.
Las excepciones deben estar documentadas explícitamente al inicio del archivo.

---

## 9. Docs reflect code

Si un cambio agrega, elimina o renombra un módulo, actualizar en el mismo commit:
- El archivo en `docs/engineering/conventions/` correspondiente (árbol de archivos).
- `docs/architecture/overview.md` (si cambia capas o flujo).

Un módulo sin documentar es un módulo invisible para el próximo agente.

