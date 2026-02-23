.PHONY: validate validate-provenance validate-xrefs validate-all gen-json-schema

validate:
	uv run python scripts/validate.py

validate-provenance:
	uv run python scripts/validate_provenance.py

validate-xrefs:
	uv run python scripts/validate_xrefs.py $(ARGS)

validate-all: validate validate-provenance
	uv run python scripts/validate_xrefs.py --internal

gen-json-schema:
	uv run gen-json-schema schema/ccf_models.yaml
