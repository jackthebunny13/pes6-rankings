#!/bin/zsh
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
TOOLS_DIR="$ROOT_DIR/tools/pes6-rankings"

cd "$ROOT_DIR"

cp "$TOOLS_DIR/index.html" "$ROOT_DIR/index.html"
cp "$TOOLS_DIR/data.json" "$ROOT_DIR/data.json"

printf 'Synced root site files from tools/pes6-rankings\n'
printf ' - %s\n' "$ROOT_DIR/index.html" "$ROOT_DIR/data.json"
