# CC Forge Model Ontology - LinkML Schema

This ontology uses [LinkML](https://linkml.io/) (Linked Data Modeling Language) for schema definition, following OBO Foundry principles.

## Why LinkML?

- **Used by OBO Foundry** - Same framework as MONDO, HPO, etc.
- **YAML-based** - Human-readable schema definitions
- **Multi-format** - Generates JSON Schema, OWL, Python dataclasses
- **Validation** - Runtime data validation
- **Tooling** - Mature ecosystem of generators and validators

## File Organization

```
cc_ai_model_ontology/
├── schema/
│   └── ccf_models.yaml       # LinkML schema definition
├── data/
│   ├── families.yaml         # Model family instances
│   ├── capabilities.yaml     # Capability hierarchy
│   ├── tiers.yaml            # Hardware tier definitions
│   └── models.yaml           # Model instances
└── SCHEMA.md                 # This document
```

## Schema Overview

**Schema file:** `schema/ccf_models.yaml`

### Classes

| Class | Description |
|-------|-------------|
| `ModelFamily` | A lineage of models (Qwen, Llama, etc.) |
| `Capability` | What models can do (code-generation, reasoning) |
| `HardwareTier` | Deployment constraints (GPU, CPU, API) |
| `Model` | Specific model variant |
| `EmbeddingModel` | Specialized embedding model |

**Container Classes** (for data file validation):

| Class | Data File |
|-------|-----------|
| `ModelDatabase` | `data/models.yaml` |
| `FamilyDatabase` | `data/families.yaml` |
| `CapabilityDatabase` | `data/capabilities.yaml` |
| `TierDatabase` | `data/tiers.yaml` |

### Key Relationships

```
Model
  ├── member_of_family → ModelFamily
  ├── derived_from → Model (optional)
  ├── has_capability → Capability (multivalued)
  └── fits_tier → HardwareTier (multivalued)

Capability
  └── parent_capability → Capability (hierarchy)
```

## Identifier Format

```
ccf:<namespace>:<local_id>

Examples:
  ccf:model:qwen2.5-coder-7b
  ccf:family:qwen
  ccf:capability:code-generation
  ccf:tier:gpu-8gb
```

Namespaces:
- `model` - Specific model variants
- `family` - Model families/lineages
- `capability` - What models can do
- `tier` - Hardware deployment tiers

## Using the Schema

### Validation

```bash
# Install LinkML
pip install linkml

# Validate data against schema (specify container class)
linkml-validate -s schema/ccf_models.yaml -C ModelDatabase data/models.yaml
linkml-validate -s schema/ccf_models.yaml -C FamilyDatabase data/families.yaml
linkml-validate -s schema/ccf_models.yaml -C CapabilityDatabase data/capabilities.yaml
linkml-validate -s schema/ccf_models.yaml -C TierDatabase data/tiers.yaml
```

### Generate Artifacts

```bash
# Generate JSON Schema
gen-json-schema schema/ccf_models.yaml > ccf_models.schema.json

# Generate Python dataclasses
gen-python schema/ccf_models.yaml > ccf_models.py

# Generate OWL ontology
gen-owl schema/ccf_models.yaml > ccf_models.owl
```

### Load in Python

```python
from linkml_runtime.loaders import yaml_loader
from ccf_models import Model

# Load a model
model = yaml_loader.load("data/models.yaml", target_class=Model)
```

## Enums

The schema defines controlled vocabularies:

| Enum | Values |
|------|--------|
| `LicenseType` | apache-2.0, mit, llama, cc-by-nc-4.0, proprietary |
| `QuantizationType` | fp16, q8_0, q6_k, q5_k_m, q4_k_m, q3_k_m, q2_k |
| `TierType` | tier1_gpu, tier2_cpu, tier3_api |
| `ModelStatus` | active, deprecated, experimental |

## Cross-References

Models include xrefs to external systems:

| Slot | Description | Example |
|------|-------------|---------|
| `xref_ollama` | Ollama model tag | `qwen2.5-coder:7b-instruct` |
| `xref_huggingface` | HuggingFace ID | `Qwen/Qwen2.5-Coder-7B-Instruct` |
| `xref_github` | GitHub repository | `QwenLM` |

## Versioning

Schema version: `0.1.0`

Follows semantic versioning:
- **Major**: Breaking schema changes
- **Minor**: New classes, slots, or enums
- **Patch**: Description/metadata updates

## References

- [LinkML Documentation](https://linkml.io/linkml/)
- [LinkML Tutorial](https://linkml.io/linkml/intro/tutorial01.html)
- [OBO Foundry Principles](http://obofoundry.org/principles/fp-000-summary.html)
