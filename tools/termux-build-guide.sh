#!/usr/bin/env bash

cat <<'EOF'
📦 Termux App Store – Contributor Guide
======================================

1. termux-build DOES NOT modify files
2. termux-build is NOT a build system
3. termux-build helps you avoid PR rejection

Workflow:
- write build.sh
- run: termux-build lint
- run: termux-build doctor
- fix issues manually
- submit PR

If termux-build passes:
✔ your PR is structurally safe
❌ maintainer may still reject (policy reasons)

This is a pre-flight checklist, not CI.
EOF
