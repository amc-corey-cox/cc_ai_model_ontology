# Agent Instructions for CC AI Model Ontology

This document provides guidance for AI agents working in this repository.

## Purpose

This repository contains a **LinkML ontology** for cataloging AI/ML models, their capabilities, and deployment constraints. It is a **reference resource**, not an application.

## What This Repo Contains

- `schema/ccf_models.yaml` - The LinkML schema definition
- `data/*.yaml` - Instance data (models, families, capabilities, tiers)
- `scripts/` - Validation scripts (schema, provenance, cross-references)
- `Makefile` - Validation and generation targets
- CI validation on PRs to ensure data conforms to schema

## What You Should Do

### When Adding Models

1. Add new entries to `data/models.yaml`
2. Ensure all required fields are populated (including provenance — see below)
3. Use existing entries as templates
4. Run `make validate-all` before committing

### Provenance Requirements

Every model entry **must** include provenance fields:

- `sources` — at least one source with `source_type`, `url` (HTTPS), and `accessed` date
- `curation_type` — one of: `human_curated`, `ai_assisted`, `ai_generated`, `automated`
- `date_added` — ISO date when the entry was created
- `added_by` — `"human"` or agent identifier (e.g., `"agent:claude"`)

Optional provenance:
- `verified_by` — `human`, `automated`, or `unverified`
- `verification_date` — required if `verified_by` is set to `human` or `automated`
- `ai_metadata` — recommended for `ai_assisted` and `ai_generated` entries (model name, generation date)

Use primary source types when possible: `model_card`, `paper`, `official_announcement`.

### When Modifying Schema
- Changes to `schema/ccf_models.yaml` affect all data files
- Ensure backwards compatibility or update all data files
- Update SCHEMA.md documentation if adding new classes/slots

### Validation

Always run full validation locally before creating a PR:

```bash
make validate-all
```

This runs:
- `make validate` — LinkML schema validation for all 4 data files
- `make validate-provenance` — Provenance business rules
- Internal cross-reference checks

Individual targets:
```bash
make validate              # Schema validation only
make validate-provenance   # Provenance rules only
make validate-xrefs ARGS="--internal"   # Internal refs only
make validate-xrefs ARGS="--external"   # External URL checks (slow)
```

### AI Re-Validation Workflow

When adding or updating model entries:
1. Gather data from primary sources (model cards, papers, announcements)
2. Record the source URL and access date in the `sources` field
3. Set `curation_type` appropriately
4. Run `make validate-all` — this catches schema errors, provenance gaps, and broken references
5. CI enforces the same checks on PRs

No human review is required if all automated checks pass. The provenance chain enables programmatic re-validation: any fact can be traced back to its source and re-checked.

## Related Repositories

| Repository | Purpose |
|------------|---------|
| `cc_forge` | Local-first AI coding assistant (main project) |
| `cc_ai_knowledge` | Curated AI/ML educational content |

## Style Guidelines

- Use lowercase with hyphens for IDs: `ccf:model:qwen2.5-coder-7b`
- Keep descriptions concise but informative
- Include cross-references (xref_ollama, xref_huggingface) when available
- Follow existing patterns in the data files
- Source URLs must be HTTPS
- Dates in ISO format (`YYYY-MM-DD`)
