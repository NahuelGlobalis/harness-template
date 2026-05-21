# AGENTS.md — Mapa de navegación para agentes de IA

Este archivo es el punto de entrada. No es la fuente canónica de reglas: enruta al documento correcto según el tipo de trabajo.

## Inicio obligatorio

1. Ejecuta el init de tu plataforma:
   - Windows PowerShell: `./init.ps1`
   - WSL/Linux: `./init.sh`
2. Lee `progress/current.md`.
3. Lee `docs/README.md` y usa `python scripts/docs_for.py --list <seccion>:<capa>` para descubrir primero el paquete documental correspondiente.
4. Identifica el modo de trabajo antes de editar archivos:
   - Diseño de arquitectura → `agents/architect.md`
   - Descubrimiento, decisiones de diseño, SDD y creación de backlog → `agents/architect.md`
   - Implementación de feature → `agents/implementer.md`
   - Revisión/cierre → `agents/reviewer.md`
   - Gardening/documentación drift → `agents/gardener.md`
   - Consulta o análisis → no abras feature salvo pedido explícito.
5. Para Docker o infraestructura, usa WSL.

## Documentación

`docs/README.md` es el índice documental canónico y el contrato de routing para `scripts/docs_for.py`.

Usa la CLI documental para cargar el contexto necesario:

```bash
python scripts/docs_for.py --list <seccion>:<key>
```

Flujo recomendado:

1. Usa `--list` para ver qué archivos incluye una key.
2. Abre o lee solo los archivos puntuales que necesites consultar o modificar.
3. Usa `python scripts/docs_for.py <seccion>:<key>` sin `--list` solo cuando te convenga leer el paquete concatenado como contexto amplio.

Para ver las secciones y keys disponibles, consulta directamente `docs/README.md` (tablas `seccions` y `keys`) o usa:

```bash
python scripts/docs_for.py --list all:all
```
## Mapa rápido del repositorio

| Archivo / carpeta | Qué contiene |
|---|---|
| `docs/README.md` | Índice documental canónico |
| `feature_list.json` | Backlog activo |
| `feature_list.archive.json` | Features cerradas |
| `progress/current.md` | Sesión activa |
| `progress/history.md` | Bitácora append-only |
| `agents/` | Prompts de roles de desarrollo |

## Roles

| Rol | Archivo | Responsabilidad |
|---|---|---|
| Arquitecto | `agents/architect.md` | Descubrimiento con el usuario, diseño técnico, SDD y backlog |
| Implementer | `agents/implementer.md` | Código, tests y evidencia |
| Reviewer | `agents/reviewer.md` | Veredicto y cierre |
| Gardener | `agents/gardener.md` | Drift docs/código y tickets de corrección |

## Si te bloqueas

- Relee la sección canónica correspondiente.
- Si una herramienta falla inesperadamente, documenta el bloqueo en `progress/current.md` y detén la sesión.
