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
├── scripts/
│   ├── validate.py           # Schema validation
│   ├── validate_provenance.py # Provenance business rules
│   └── validate_xrefs.py     # Cross-reference validation
├── Makefile                   # Validation targets
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
| `Source` | A source of information for a data entry |
| `AIMetadata` | Metadata about AI-assisted curation |

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
  ├── fits_tier → HardwareTier (multivalued)
  ├── sources → Source[] (provenance)
  └── ai_metadata → AIMetadata (optional)

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
# Run all validation
make validate-all

# Individual checks
make validate              # LinkML schema validation
make validate-provenance   # Provenance business rules
make validate-xrefs ARGS="--internal"  # Internal cross-references
make validate-xrefs ARGS="--external"  # External URL checks
```

### Generate Artifacts

```bash
# Generate JSON Schema
make gen-json-schema

# Generate Python dataclasses
uv run gen-python schema/ccf_models.yaml > ccf_models.py

# Generate OWL ontology
uv run gen-owl schema/ccf_models.yaml > ccf_models.owl
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
| `CurationType` | human_curated, ai_assisted, ai_generated, automated |
| `VerifiedByType` | human, automated, unverified |
| `SourceType` | model_card, paper, official_announcement, repository, api_verified, community |

## Provenance

### Source Class

Tracks where information came from:

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `source_type` | SourceType | Yes | Type of source |
| `url` | uri | Yes | URL of the source |
| `accessed` | date | Yes | When the source was accessed |
| `title` | string | No | Title of the source |

### AIMetadata Class

Records AI involvement in curation:

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `model` | string | Yes | AI model used (e.g., "claude-opus-4-6") |
| `generation_date` | date | Yes | When the AI generated the data |
| `confidence_notes` | string | No | Notes about uncertainty |

### Provenance Slots on Model

| Slot | Type | Required | Description |
|------|------|----------|-------------|
| `sources` | Source[] | Yes | At least one source |
| `curation_type` | CurationType | Yes | How data was gathered |
| `date_added` | date | Yes | When entry was created |
| `added_by` | string | Yes | Who added it |
| `verified_by` | VerifiedByType | No | What verified it |
| `verification_date` | date | No | When verified |
| `ai_metadata` | AIMetadata | No | AI curation details |

ModelFamily has the same slots, all optional.

Capability and HardwareTier do **not** have provenance (they are definitional taxonomy, not factual claims).

## Cross-References

Models include xrefs to external systems:

| Slot | Description | Example |
|------|-------------|---------|
| `xref_ollama` | Ollama model tag | `qwen2.5-coder:7b-instruct` |
| `xref_huggingface` | HuggingFace ID | `Qwen/Qwen2.5-Coder-7B-Instruct` |
| `xref_github` | GitHub repository | `QwenLM` |

## Versioning

Schema version: `0.2.0`

Follows semantic versioning:
- **Major**: Breaking schema changes
- **Minor**: New classes, slots, or enums
- **Patch**: Description/metadata updates

## References

- [LinkML Documentation](https://linkml.io/linkml/)
- [LinkML Tutorial](https://linkml.io/linkml/intro/tutorial01.html)
- [OBO Foundry Principles](http://obofoundry.org/principles/fp-000-summary.html)
