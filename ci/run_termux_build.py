#!/usr/bin/env python3
import os
import re
import subprocess
import sys

PACKAGES_DIR = "packages"
FAILED = False


def parse_var(path, var):
    pattern = re.compile(rf"^{var}=(.+)$", re.M)
    with open(path) as f:
        content = f.read()
    m = pattern.search(content)
    if not m:
        return None
    return m.group(1).strip().strip('"')


for pkg in sorted(os.listdir(PACKAGES_DIR)):
    pkg_dir = os.path.join(PACKAGES_DIR, pkg)
    build_sh = os.path.join(pkg_dir, "build.sh")

    if not os.path.isdir(pkg_dir):
        continue
    if not os.path.isfile(build_sh):
        continue

    print(f"\n🔍 Validating package: {pkg}")

    try:
        version = parse_var(build_sh, "TERMUX_PKG_VERSION")
        if not version:
            raise ValueError("Missing TERMUX_PKG_VERSION")

        declared_name = parse_var(build_sh, "TERMUX_PKG_NAME")
        if declared_name and declared_name != pkg:
            raise ValueError(f"TERMUX_PKG_NAME mismatch (expected '{pkg}', got '{declared_name}')")

        result = subprocess.run(
            ["./termux-build", "lint", pkg],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        print(f"✅ {pkg} OK (v{version})")

    except subprocess.CalledProcessError as e:
        FAILED = True
        print(f"❌ {pkg} failed (exit code {e.returncode}):")
        output = (e.stdout or "") + (e.stderr or "")
        for line in output.strip().splitlines():
            print(f"    {line}")

    except Exception as e:
        FAILED = True
        print(f"❌ {pkg} failed: {e}")

if FAILED:
    print("\n❌ One or more packages failed validation")
    sys.exit(1)

print("\n✅ All packages validated successfully")
