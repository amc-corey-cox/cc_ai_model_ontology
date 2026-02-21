#!/usr/bin/env python3
"""Provenance business rule validation beyond schema checks."""

import sys
from datetime import date, timedelta
from pathlib import Path

import yaml

STALENESS_THRESHOLD = timedelta(days=180)
PRIMARY_SOURCE_TYPES = {"model_card", "paper", "official_announcement"}


def convert_dates(obj):
    """Ensure dates are datetime.date objects for comparison."""
    if isinstance(obj, date):
        return obj
    if isinstance(obj, str):
        try:
            return date.fromisoformat(obj)
        except ValueError:
            return obj
    if isinstance(obj, dict):
        return {k: convert_dates(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [convert_dates(item) for item in obj]
    return obj


def validate_model_provenance(model: dict, today: date) -> tuple[list[str], list[str]]:
    """Validate provenance rules for a single model entry.

    Returns (errors, warnings).
    """
    errors = []
    warnings = []
    model_id = model.get("id", "<unknown>")

    curation_type = model.get("curation_type")
    ai_metadata = model.get("ai_metadata")
    verified_by = model.get("verified_by")
    verification_date = model.get("verification_date")
    sources = model.get("sources", [])

    # AI curation types require ai_metadata
    if curation_type in ("ai_generated", "ai_assisted") and not ai_metadata:
        warnings.append(
            f"{model_id}: curation_type={curation_type} but no ai_metadata"
        )

    # verified_by != unverified requires verification_date
    if verified_by and verified_by != "unverified" and not verification_date:
        errors.append(
            f"{model_id}: verified_by={verified_by} but no verification_date"
        )

    # Source URL checks
    for i, source in enumerate(sources):
        url = source.get("url", "")
        if url and not url.startswith("https://"):
            errors.append(f"{model_id}: source[{i}] URL is not HTTPS: {url}")

        accessed = source.get("accessed")
        if isinstance(accessed, date):
            if accessed > today:
                errors.append(
                    f"{model_id}: source[{i}] accessed date is in the future: {accessed}"
                )
            elif today - accessed > STALENESS_THRESHOLD:
                warnings.append(
                    f"{model_id}: source[{i}] accessed {accessed} is older than 6 months"
                )

    # Date checks
    date_added = model.get("date_added")
    if isinstance(date_added, date) and date_added > today:
        errors.append(f"{model_id}: date_added is in the future: {date_added}")

    if isinstance(verification_date, date) and verification_date > today:
        errors.append(
            f"{model_id}: verification_date is in the future: {verification_date}"
        )

    # Warn if no primary source type
    if sources:
        source_types = {s.get("source_type") for s in sources}
        if not source_types & PRIMARY_SOURCE_TYPES:
            warnings.append(
                f"{model_id}: no primary source type (model_card/paper/announcement)"
            )

    return errors, warnings


def validate_all() -> bool:
    today = date.today()
    all_errors = []
    all_warnings = []

    models_path = Path("data/models.yaml")
    if not models_path.exists():
        print("MISSING: data/models.yaml")
        return False

    with open(models_path) as f:
        data = yaml.safe_load(f)

    data = convert_dates(data)

    for model in data.get("models", []):
        errors, warnings = validate_model_provenance(model, today)
        all_errors.extend(errors)
        all_warnings.extend(warnings)

    for warning in all_warnings:
        print(f"  WARNING: {warning}")

    for error in all_errors:
        print(f"  ERROR: {error}")

    if all_errors:
        print(f"\nProvenance validation failed: {len(all_errors)} error(s), {len(all_warnings)} warning(s)")
        return False

    print(f"\nProvenance validation passed ({len(all_warnings)} warning(s))")
    return True


if __name__ == "__main__":
    success = validate_all()
    if not success:
        sys.exit(1)
