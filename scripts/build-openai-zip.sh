#!/usr/bin/env bash
# Build the OpenAI upload ZIP. The archive root is the plugin root.
# dist/ is gitignored. This script does not submit anything.
set -euo pipefail

cd "$(dirname "$0")/.."
root=$(pwd)
stage=$(mktemp -d)
trap 'rm -rf "$stage"' EXIT

mkdir -p "$stage/assets" "$stage/skills" "$root/dist"
cp openai/plugin.json "$stage/plugin.json"
cp openai/mcp.json "$stage/mcp.json"
cp -R openai/skills/. "$stage/skills/"
cp assets/logo-plate.png "$stage/assets/logo-plate.png"

python3 scripts/validate-openai-package.py "$stage"

archive="$root/dist/mysdr-openai-plugin.zip"
tmp=$(mktemp --suffix=.zip)
rm -f "$tmp"
(
  cd "$stage"
  zip -q -r -X "$tmp" plugin.json mcp.json skills assets
)
python3 scripts/validate-openai-package.py --zip "$tmp"
mv "$tmp" "$archive"
echo "wrote $archive"
