#!/usr/bin/env python3
"""
add-dependency.sh <group> <artifact> <version>
Adds a dependency to gradle/libs.versions.toml

Usage:
    python add-dependency.py androidx.core core-ktx 1.13.1
"""

import sys
import re
from pathlib import Path

def add_dependency(group, artifact, version):
    toml_path = Path(__file__).parent.parent.parent.parent / "gradle" / "libs.versions.toml"

    if not toml_path.exists():
        print(f"[ERROR] {toml_path} not found")
        return False

    content = toml_path.read_text(encoding='utf-8')

    lib_name = artifact.replace("-", "").replace("_", "").lower()

    new_lib = f'{lib_name} = {{ group = "{group}", name = "{artifact}", version = "{version}" }}\n'

    if f'name = "{artifact}"' in content:
        print(f"[INFO] Dependency {group}:{artifact} already exists")
        return True

    if '[libraries]' in content:
        content = content.replace('[libraries]', f'[libraries]\n{new_lib}')
    else:
        content += f'\n[libraries]\n{new_lib}'

    toml_path.write_text(content, encoding='utf-8')
    print(f"[OK] Added {group}:{artifact}:{version} to libs.versions.toml")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python add-dependency.py <group> <artifact> <version>")
        sys.exit(1)

    group, artifact, version = sys.argv[1], sys.argv[2], sys.argv[3]
    success = add_dependency(group, artifact, version)
    sys.exit(0 if success else 1)