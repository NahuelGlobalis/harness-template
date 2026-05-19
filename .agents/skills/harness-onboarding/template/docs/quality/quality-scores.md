# Quality Scores — harness-template

> Escala: **A** (excelente) → **D** (deuda crítica)
>
> El Reviewer actualiza este archivo si detecta degradación o mejora
> significativa durante un review.
>
> **Última actualización:** 2026-05-12 (gardening)

---

| Dominio / Módulo | Score | Notas |
|------------------|-------|-------|

---

## Criterios de scoring

| Score | Significado |
|-------|-------------|
| **A** | Tests completos, typed, docs actualizados, sin deuda conocida |
| **B** | Funcional y mantenible, con mejoras menores identificadas |
| **C** | Funciona pero tiene deuda técnica visible o gaps de testing |
| **D** | Deuda crítica: refactoring urgente antes de seguir construyendo encima |

## Acciones por score

- **A/B:** Seguir construyendo. Mantener calidad.
- **C:** Priorizar refactoring si la próxima feature toca ese módulo.
- **D:** No agregar features nuevas hasta pagar la deuda.
