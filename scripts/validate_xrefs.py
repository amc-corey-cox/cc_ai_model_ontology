#!/usr/bin/env python3
"""Cross-reference validation for the ontology data files.

Checks internal references between data files and optionally validates
external URLs (HuggingFace, Ollama, provenance sources).
"""

import argparse
import sys
from pathlib import Path

import yaml


def load_data(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        return {}
    with open(p) as f:
        return yaml.safe_load(f) or {}


def collect_ids(data: dict, key: str) -> set[str]:
    return {entry["id"] for entry in data.get(key, []) if "id" in entry}


def validate_internal() -> list[str]:
    """Check that all cross-references point to existing IDs."""
    errors = []

    models_data = load_data("data/models.yaml")
    families_data = load_data("data/families.yaml")
    capabilities_data = load_data("data/capabilities.yaml")
    tiers_data = load_data("data/tiers.yaml")

    model_ids = collect_ids(models_data, "models")
    family_ids = collect_ids(families_data, "families")
    capability_ids = collect_ids(capabilities_data, "capabilities")
    tier_ids = collect_ids(tiers_data, "tiers")

    # Validate model references
    for model in models_data.get("models", []):
        mid = model.get("id", "<unknown>")

        family_ref = model.get("member_of_family")
        if family_ref and family_ref not in family_ids:
            errors.append(f"{mid}: member_of_family '{family_ref}' not found in families.yaml")

        derived_ref = model.get("derived_from")
        if derived_ref and derived_ref not in model_ids:
            errors.append(f"{mid}: derived_from '{derived_ref}' not found in models.yaml")

        for cap_ref in model.get("has_capability", []):
            if cap_ref not in capability_ids:
                errors.append(f"{mid}: has_capability '{cap_ref}' not found in capabilities.yaml")

        for tier_ref in model.get("fits_tier", []):
            if tier_ref not in tier_ids:
                errors.append(f"{mid}: fits_tier '{tier_ref}' not found in tiers.yaml")

    # Validate capability parent references
    for cap in capabilities_data.get("capabilities", []):
        cid = cap.get("id", "<unknown>")
        parent_ref = cap.get("parent_capability")
        if parent_ref and parent_ref not in capability_ids:
            errors.append(f"{cid}: parent_capability '{parent_ref}' not found in capabilities.yaml")

    return errors


def validate_external() -> list[str]:
    """HEAD-request external URLs to check they're reachable."""
    import requests

    errors = []
    urls_checked = set()

    models_data = load_data("data/models.yaml")

    for model in models_data.get("models", []):
        mid = model.get("id", "<unknown>")

        # Check HuggingFace xref
        hf = model.get("xref_huggingface")
        if hf:
            url = f"https://huggingface.co/{hf}"
            if url not in urls_checked:
                urls_checked.add(url)
                try:
                    resp = requests.head(url, timeout=10, allow_redirects=True)
                    if resp.status_code >= 400:
                        errors.append(f"{mid}: HuggingFace URL returned {resp.status_code}: {url}")
                    else:
                        print(f"  OK: {url}")
                except requests.RequestException as e:
                    errors.append(f"{mid}: HuggingFace URL unreachable: {url} ({e})")

        # Check Ollama xref
        ollama = model.get("xref_ollama")
        if ollama:
            tag = ollama.split(":")[0]
            url = f"https://ollama.com/library/{tag}"
            if url not in urls_checked:
                urls_checked.add(url)
                try:
                    resp = requests.head(url, timeout=10, allow_redirects=True)
                    if resp.status_code >= 400:
                        errors.append(f"{mid}: Ollama URL returned {resp.status_code}: {url}")
                    else:
                        print(f"  OK: {url}")
                except requests.RequestException as e:
                    errors.append(f"{mid}: Ollama URL unreachable: {url} ({e})")

        # Check provenance source URLs
        for i, source in enumerate(model.get("sources", [])):
            url = source.get("url", "")
            if url and url not in urls_checked:
                urls_checked.add(url)
                try:
                    resp = requests.head(url, timeout=10, allow_redirects=True)
                    if resp.status_code >= 400:
                        errors.append(f"{mid}: source[{i}] URL returned {resp.status_code}: {url}")
                    else:
                        print(f"  OK: {url}")
                except requests.RequestException as e:
                    errors.append(f"{mid}: source[{i}] URL unreachable: {url} ({e})")

    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate cross-references")
    parser.add_argument("--internal", action="store_true", help="Check internal references only")
    parser.add_argument("--external", action="store_true", help="Check external URLs only")
    args = parser.parse_args()

    # Default: run both
    run_internal = args.internal or not (args.internal or args.external)
    run_external = args.external or not (args.internal or args.external)

    all_errors = []

    if run_internal:
        print("Checking internal cross-references...")
        errors = validate_internal()
        all_errors.extend(errors)
        if not errors:
            print("  All internal references valid.")

    if run_external:
        print("Checking external URLs...")
        errors = validate_external()
        all_errors.extend(errors)
        if not errors:
            print("  All external URLs reachable.")

    for error in all_errors:
        print(f"  ERROR: {error}")

    if all_errors:
        print(f"\nXref validation failed: {len(all_errors)} error(s)")
        sys.exit(1)
    else:
        print("\nXref validation passed.")


if __name__ == "__main__":
    main()
