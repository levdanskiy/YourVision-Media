#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [ "$#" -eq 3 ]; then
  python3 tools/preflight_day.py "$1" "$2" "$3"
else
  python3 tools/validate_almanac.py
  python3 tools/audit_service_specials.py
  python3 tools/audit_system_docs.py
fi
