# CC AI Model Ontology

A [LinkML](https://linkml.io/) ontology for cataloging AI/ML models, their capabilities, and deployment constraints. Designed for local-first AI development.

## Purpose

This ontology provides a structured way to:
- Catalog AI models and their relationships
- Track model capabilities (code generation, reasoning, etc.)
- Define hardware deployment tiers
- Maintain cross-references to Ollama, HuggingFace, etc.

## Structure

```
cc_ai_model_ontology/
├── schema/
│   └── ccf_models.yaml      # LinkML schema definition
├── data/
│   ├── families.yaml        # Model families (Qwen, Llama, etc.)
│   ├── capabilities.yaml    # Capability hierarchy
│   ├── tiers.yaml           # Hardware tier definitions
│   └── models.yaml          # Model instances
└── SCHEMA.md                # Schema documentation
```

## Usage

### Validation

```bash
# Install LinkML
pip install linkml

# Validate data against schema
linkml-validate -s schema/ccf_models.yaml -C ModelDatabase data/models.yaml
linkml-validate -s schema/ccf_models.yaml -C FamilyDatabase data/families.yaml
linkml-validate -s schema/ccf_models.yaml -C CapabilityDatabase data/capabilities.yaml
linkml-validate -s schema/ccf_models.yaml -C TierDatabase data/tiers.yaml
```

### Generate Artifacts

```bash
# JSON Schema
gen-json-schema schema/ccf_models.yaml > ccf_models.schema.json

# Python dataclasses
gen-python schema/ccf_models.yaml > ccf_models.py

# OWL ontology
gen-owl schema/ccf_models.yaml > ccf_models.owl
```

## Related Projects

- [cc_forge](https://github.com/youruser/cc_forge) - Local-first AI coding assistant
- [cc_ai_knowledge](https://github.com/youruser/cc_ai_knowledge) - AI knowledge base

## License

Apache-2.0
