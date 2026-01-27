# Agent Instructions for CC AI Model Ontology

This document provides guidance for AI agents working in this repository.

## Purpose

This repository contains a **LinkML ontology** for cataloging AI/ML models, their capabilities, and deployment constraints. It is a **reference resource**, not an application.

## What This Repo Contains

- `schema/ccf_models.yaml` - The LinkML schema definition
- `data/*.yaml` - Instance data (models, families, capabilities, tiers)
- CI validation to ensure data conforms to schema

## What You Should Do

### When Adding Models
- Add new entries to `data/models.yaml`
- Ensure all required fields are populated
- Use existing patterns as templates
- Run validation before committing: `linkml-validate -s schema/ccf_models.yaml -C ModelDatabase data/models.yaml`

### When Modifying Schema
- Changes to `schema/ccf_models.yaml` affect all data files
- Ensure backwards compatibility or update all data files
- Update SCHEMA.md documentation if adding new classes/slots

### Validation
Always validate changes locally before committing:
```bash
pip install linkml
linkml-validate -s schema/ccf_models.yaml -C ModelDatabase data/models.yaml
linkml-validate -s schema/ccf_models.yaml -C FamilyDatabase data/families.yaml
linkml-validate -s schema/ccf_models.yaml -C CapabilityDatabase data/capabilities.yaml
linkml-validate -s schema/ccf_models.yaml -C TierDatabase data/tiers.yaml
```

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
