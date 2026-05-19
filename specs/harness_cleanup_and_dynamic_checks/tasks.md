# Tasks - harness_cleanup_and_dynamic_checks

Este documento contiene la lista de tareas para implementar la limpieza y flexibilización del arnés, asociadas a los requisitos correspondientes.

- [ ] T1 — Renombrar `docs/operations/example.md` a `docs/operations/docker.md` y actualizar `docs/README.md`. Cubre: R1, R2.
- [ ] T2 — Limpiar claves de grupo y referencias de proyectos específicos en `docs/README.md`. Cubre: R3.
- [ ] T3 — Modificar `scripts/validate_quality.py` para escaneo dinámico de carpetas de código de producto y soporte multi-tecnología. Cubre: R4, R5, R6, R7, R8, R9, R10.
- [ ] T4 — Modificar `scripts/validate_quality.py` para que la validación de dirección de dependencias de `routers` sea condicional. Cubre: R11.
- [ ] T5 — Implementar fixture de mock y monkeypatch en `scripts/tests/test_docs_for.py` para desacoplar los tests del README real. Cubre: R12.
- [ ] T6 — Reemplazar las referencias hardcodeadas de `deepagents-api` en los documentos de soporte (`docs/harness/lifecycle.md`, `docs/quality/gardening.md`, `docs/harness/ticketing.md`). Cubre: R13.
- [ ] T7 — Ejecutar `python scripts/validate_harness.py` y `python -m pytest` para verificar la corrección completa. Cubre: R1 al R13.
