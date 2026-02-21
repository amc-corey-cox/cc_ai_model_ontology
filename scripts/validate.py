#!/usr/bin/env python3
"""Schema validation for all data files using LinkML."""

import subprocess
import sys
from pathlib import Path

SCHEMA_PATH = Path("schema/ccf_models.yaml")

DATA_FILES = {
    "data/models.yaml": "ModelDatabase",
    "data/families.yaml": "FamilyDatabase",
    "data/capabilities.yaml": "CapabilityDatabase",
    "data/tiers.yaml": "TierDatabase",
}


def validate_all() -> bool:
    errors_found = False

    for data_file, target_class in DATA_FILES.items():
        path = Path(data_file)
        if not path.exists():
            print(f"MISSING: {data_file}")
            errors_found = True
            continue

        print(f"Validating {data_file} as {target_class}...")

        result = subprocess.run(
            [
                "linkml-validate",
                "-s", str(SCHEMA_PATH),
                "-C", target_class,
                str(path),
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            errors_found = True
            if result.stderr:
                for line in result.stderr.strip().splitlines():
                    print(f"  ERROR: {line}")
            if result.stdout:
                for line in result.stdout.strip().splitlines():
                    print(f"  {line}")
        else:
            print(f"  OK")

    return not errors_found


if __name__ == "__main__":
    success = validate_all()
    if success:
        print("\nAll data files are valid.")
    else:
        print("\nValidation failed.")
        sys.exit(1)
