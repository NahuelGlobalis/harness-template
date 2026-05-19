from __future__ import annotations

import pytest
from pathlib import Path
import docs_for


@pytest.fixture(autouse=True)
def mock_docs_env(tmp_path, monkeypatch):
    # 1. Create a mock docs directory in tmp_path
    tmp_docs_dir = tmp_path / "docs"
    tmp_docs_dir.mkdir()
    
    # 2. Create a mock README.md
    readme_content = """# Documentacion - test-project

## Organizacion

<!-- sections:begin -->
| Key | Contenido |
|---|---|
| `harness` | Ciclo de vida |
| `engineering` | Convenciones |
| `quality` | Principios |
| `architecture` | Diseno |
| `operations` | Runbooks |
| `exec-plans` | Planes |
<!-- sections:end -->

## Keys

<!-- keys:begin -->
| Key | Contenido |
|---|---|
| `shared` | Transversal |
| `api` | Backend |
| `web` | Frontend |
| `design` | Transversal |
| `delivery` | Transversal |
| `gardening` | Transversal |
| `client-agents` | Frontend |
| `system-agents` | Backend |
<!-- keys:end -->

## Mapa documental

### Harness

<!-- harness:begin -->
| Documento | Contenido | key |
|---|---|---|
| `harness/lifecycle.md` | Ciclo | shared,delivery,gardening |
| `harness/ticketing.md` | Tickets | shared,design,delivery,gardening |
| `harness/templates/progress/brief.md` | Briefs | shared,design,gardening |
| `harness/templates/progress/current.empty.md` | Vacio | shared,delivery,gardening |
| `harness/templates/progress/current.active.md` | Activo | shared,delivery,gardening |
| `harness/templates/progress/impl.md` | Impl | shared,delivery |
| `harness/templates/progress/review.md` | Review | shared,delivery |
<!-- harness:end -->

### Architecture

<!-- architecture:begin -->
| Documento | Contenido | key |
|---|---|---|
| `architecture/overview.md` | Overview | shared,design,delivery,gardening |
| `architecture/adr/` | ADRs | shared,design,gardening |
<!-- architecture:end -->

### Engineering

<!-- engineering:begin -->
| Documento | Contenido | key |
|---|---|---|
| `engineering/conventions/shared.md` | Convenciones | shared |
| `engineering/conventions/api.md` | Convenciones backend | api |
| `engineering/verification/api.md` | Backend verif | api |
| `engineering/conventions/client-agents.md` | client agents | client-agents |
| `engineering/verification/system-agents.md` | system agents | system-agents |
<!-- engineering:end -->

### Operations

<!-- operations:begin -->
| Documento | Contenido | key |
|---|---|---|
| `operations/docker.md` | Docker | shared,design,delivery,gardening |
<!-- operations:end -->

### Quality

<!-- quality:begin -->
| Documento | Contenido | key |
|---|---|---|
| `quality/golden-principles.md` | Principios | shared,design,delivery,gardening |
| `quality/gardening.md` | Gardening | shared,gardening,design |
| `quality/quality-scores.md` | Scores | shared,gardening,design,delivery |
| `quality/self-review-checklist.md` | Self-review | shared,delivery |
<!-- quality:end -->

### Exec Plans

<!-- exec-plans:begin -->
| Documento | Contenido | key |
|---|---|---|
| `exec-plans/template.md` | Plantilla | shared,design |
| `exec-plans/completed/` | Completados | shared,design,gardening |
<!-- exec-plans:end -->
"""
    tmp_readme_path = tmp_docs_dir / "README.md"
    tmp_readme_path.write_text(readme_content, encoding="utf-8")
    
    # 3. Create all mock files in the tmp_docs_dir so they "exist" during tests
    mock_files = [
        "harness/lifecycle.md",
        "harness/ticketing.md",
        "harness/templates/progress/brief.md",
        "harness/templates/progress/current.empty.md",
        "harness/templates/progress/current.active.md",
        "harness/templates/progress/impl.md",
        "harness/templates/progress/review.md",
        "architecture/overview.md",
        "engineering/conventions/shared.md",
        "engineering/conventions/api.md",
        "engineering/verification/api.md",
        "engineering/conventions/client-agents.md",
        "engineering/verification/system-agents.md",
        "operations/docker.md",
        "quality/golden-principles.md",
        "quality/gardening.md",
        "quality/quality-scores.md",
        "quality/self-review-checklist.md",
        "exec-plans/template.md",
    ]
    for rel_file in mock_files:
        p = tmp_docs_dir / rel_file
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(f"content of {rel_file}", encoding="utf-8")
        
    mock_dirs = [
        "architecture/adr",
        "exec-plans/completed",
    ]
    for rel_dir in mock_dirs:
        p = tmp_docs_dir / rel_dir
        p.mkdir(parents=True, exist_ok=True)
        
    # Apply monkeypatch to override module constants in docs_for
    monkeypatch.setattr(docs_for, "DOCS_DIR", tmp_docs_dir)
    monkeypatch.setattr(docs_for, "README_PATH", tmp_readme_path)
    monkeypatch.setattr(docs_for, "ROOT", tmp_path)


def test_parse_implementation_routing_has_api_docs() -> None:
    routing = docs_for.parse_routing_table("engineering")
    assert "api" in routing
    assert "engineering/conventions/api.md" in routing["api"]["paths"]
    assert "engineering/verification/api.md" in routing["api"]["paths"]


def test_engineering_uses_only_technical_keys() -> None:
    routing = docs_for.parse_routing_table("engineering")
    assert "design" not in routing
    assert "delivery" not in routing
    assert "gardening" not in routing
    assert "client-agents" in routing
    assert "system-agents" in routing
    assert "engineering/conventions/client-agents.md" in routing["client-agents"]["paths"]
    assert "engineering/verification/system-agents.md" in routing["system-agents"]["paths"]


def test_section_and_item_aliases_are_supported() -> None:
    # normalize_section just lowercases and strips
    assert docs_for.normalize_section("ENGINEERING") == "engineering"
    assert docs_for.normalize_section("Quality") == "quality"
    # normalize_item just lowercases and strips
    assert docs_for.normalize_item("BACKEND") == "backend"
    assert docs_for.normalize_item("FULL-STACK") == "full-stack"


def test_resolve_paths_deduplicates() -> None:
    paths = docs_for.resolve_paths(
        ["quality/golden-principles.md", "quality/golden-principles.md"]
    )
    assert paths == [docs_for.DOCS_DIR / "quality/golden-principles.md"]


def test_all_canonical_routes_exist() -> None:
    sections = [
        "harness",
        "engineering",
        "quality",
        "architecture",
        "operations",
        "exec-plans",
    ]

    for section in sections:
        routing = docs_for.parse_routing_table(section)
        all_paths: list[str] = []
        # Skip special keys like _path_descriptions
        for key, info in routing.items():
            if key != "_path_descriptions" and "paths" in info:
                all_paths.extend(info["paths"])
        # Filter out directories (they're not files)
        resolved = [p for p in docs_for.resolve_paths(all_paths) if p.is_file()]
        missing = docs_for.missing_paths(resolved)
        assert missing == []


def test_directory_routes_count_as_existing_for_strict_checks() -> None:
    paths = docs_for.resolve_paths(["architecture/adr/", "exec-plans/completed/"])
    assert docs_for.missing_paths(paths) == []


def test_json_payload_shape_for_api_route() -> None:
    _, payloads = docs_for.resolve_pairs([("engineering", "api")])
    payload = payloads[0]

    assert payload["section"] == "engineering"
    assert payload["item"] == "api"
    # Description is the actual description from docs/README.md
    assert "Convenciones" in payload["description"]
    assert payload["paths"][0]["path"] == "docs/engineering/conventions/api.md"
    assert payload["paths"][0]["status"] == "OK"


def test_quality_delivery_route_contains_review_material() -> None:
    _, payloads = docs_for.resolve_pairs([("quality", "delivery")])
    payload = payloads[0]
    paths = [entry["path"] for entry in payload["paths"]]

    assert payload["section"] == "quality"
    assert payload["item"] == "delivery"
    assert "docs/quality/golden-principles.md" in paths
    assert "docs/quality/quality-scores.md" in paths
    assert "docs/quality/self-review-checklist.md" in paths


def test_harness_design_route_contains_ticketing_and_brief() -> None:
    _, payloads = docs_for.resolve_pairs([("harness", "design")])
    payload = payloads[0]
    paths = [entry["path"] for entry in payload["paths"]]

    assert payload["section"] == "harness"
    assert payload["item"] == "design"
    assert "docs/harness/ticketing.md" in paths
    assert "docs/harness/templates/progress/brief.md" in paths


def test_harness_delivery_route_contains_execution_templates() -> None:
    _, payloads = docs_for.resolve_pairs([("harness", "delivery")])
    payload = payloads[0]
    paths = [entry["path"] for entry in payload["paths"]]

    assert payload["section"] == "harness"
    assert payload["item"] == "delivery"
    assert "docs/harness/lifecycle.md" in paths
    assert "docs/harness/templates/progress/impl.md" in paths
    assert "docs/harness/templates/progress/review.md" in paths


def test_quality_gardening_route_contains_drift_material() -> None:
    _, payloads = docs_for.resolve_pairs([("quality", "gardening")])
    payload = payloads[0]
    paths = [entry["path"] for entry in payload["paths"]]

    assert payload["section"] == "quality"
    assert payload["item"] == "gardening"
    assert "docs/quality/golden-principles.md" in paths
    assert "docs/quality/gardening.md" in paths
    assert "docs/quality/quality-scores.md" in paths
