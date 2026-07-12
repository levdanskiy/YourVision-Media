#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [ "$#" -eq 3 ]; then
  python3 tools/almanac publish "$1-$2-$3"
else
  python3 tools/validate_almanac.py
  python3 tools/audit_service_specials.py
  python3 tools/audit_system_docs.py
  python3 tools/audit_continuity.py
  python3 tools/audit_series.py "$(date +%F)"
  python3 tools/publication_status.py audit
  python3 tools/visual_assets.py audit
  python3 tools/evidence_registry.py audit
  python3 tools/experiment_registry.py audit "$(date +%F)"
  python3 tools/incident_manager.py audit
fi
