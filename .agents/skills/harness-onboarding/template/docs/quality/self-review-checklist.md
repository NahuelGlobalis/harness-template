# Self-Review Checklist — Implementer

> El Implementer ejecuta esta checklist **antes** de entregar al Reviewer.
> Si algún punto falla, corregir antes de escribir `progress/impl_*.md`.

---

## Evidencia automática obligatoria

- [ ] **Init verde.** `./init.ps1` o `./init.sh` termina sin errores.
- [ ] **Acceptance cubierto.** Cada criterio de acceptance del ticket tiene evidencia en tests, comandos o archivos específicos.

## Checks de juicio obligatorios

- [ ] **Imports organizados.** stdlib → external → local. Sin imports en medio del archivo.
- [ ] **Naming correcto.** snake_case (Python), PascalCase componentes (React), camelCase hooks/utils.
- [ ] **Documentación alineada.** Si agregaste un módulo o convención, actualizar `docs/engineering/conventions/`.
- [ ] **No hay helpers duplicados.** Verificar que no existe ya una utilidad similar en el repo.
- [ ] **Shapes validadas en boundaries.** Routers usan Pydantic/schemas, no acceden a dicts crudos.
- [ ] **Dependency direction respetada.** routers/ → services/ → tools/. No al revés.
- [ ] **Secrets seguros.** No hay tokens, passwords ni API keys hardcodeados.

## Checks opcionales (buenas prácticas)

- [ ] **Docstrings en funciones públicas** (Python).
- [ ] **Error messages descriptivos** que ayuden al siguiente agente a debuggear.
- [ ] **Quality score no degradó.** Si tocaste un módulo con score C/D, ¿mejoró?

---

## Si falla algún check

1. Corregir el problema.
2. Re-ejecutar init.
3. Solo cuando todo pase, escribir `progress/impl_<feature_name>.md` con evidencia de `init` y de los checks de juicio.

