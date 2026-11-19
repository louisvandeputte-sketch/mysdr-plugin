#!/usr/bin/env bash
# Validates the plugin package and checks the unauthenticated MCP discovery it relies on.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 - <<'PY'
import json, os, re, sys
ok = True
def fail(m):
    global ok; ok = False; print("FAIL", m)
m = json.load(open(".cursor-plugin/plugin.json"))
if not re.fullmatch(r"[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?", m.get("name", "")): fail("name not kebab-case")
for k in ("logo",):
    p = m.get(k)
    if p and (p.startswith("/") or ".." in p or not os.path.exists(p)): fail(f"{k} path invalid: {p}")
for f in ("mcp.json", ".mcp.json"):
    d = json.load(open(f))
    for name, s in d["mcpServers"].items():
        if "headers" in s or "env" in s: fail(f"{f}:{name} carries headers/env")
        if not s.get("url", "").startswith("https://"): fail(f"{f}:{name} url not https")
for root, dirs, files in os.walk("skills"):
    if "SKILL.md" in files:
        t = open(os.path.join(root, "SKILL.md")).read()
        fm = re.match(r"---\n(.*?)\n---\n", t, re.S)
        if not fm or not re.search(r"^name: [a-z0-9-]+$", fm.group(1), re.M) or "description:" not in fm.group(1):
            fail(f"{root}/SKILL.md frontmatter")
        elif re.search(r"^name: (.+)$", fm.group(1), re.M).group(1) != os.path.basename(root):
            fail(f"{root}: skill name differs from folder")
for root, dirs, files in os.walk("."):
    if ".git" in root: continue
    for f in files:
        p = os.path.join(root, f)
        if p.endswith((".png", ".zip")) or p.endswith("validate.sh"): continue
        t = open(p, errors="ignore").read()
        if re.search(r"(sk_live|sk_test|rk_live|whsec_|ejk_[A-Za-z0-9]{8}|fmo_[A-Za-z0-9]{8}|ghp_|BEGIN [A-Z ]*PRIVATE KEY)", t): fail(f"possible secret in {p}")
print("package OK" if ok else "package has problems"); sys.exit(0 if ok else 1)
PY
URL=$(python3 -c 'import json;print(json.load(open("mcp.json"))["mcpServers"]["mysdr"]["url"])')
ORIGIN=$(python3 -c "from urllib.parse import urlparse;u=urlparse('$URL');print(f'{u.scheme}://{u.netloc}')")
hdr=$(curl -s -o /dev/null -D - -X POST "$URL" -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}')
echo "$hdr" | grep -qi '^HTTP/[0-9.]* 401' && echo "401 OK" || { echo "FAIL: expected 401"; exit 1; }
prm=$(echo "$hdr" | grep -io 'resource_metadata="[^"]*"' | cut -d'"' -f2)
[ -n "$prm" ] && echo "WWW-Authenticate resource_metadata OK: $prm" || { echo "FAIL: no resource_metadata"; exit 1; }
curl -sf "$prm" | python3 -c 'import json,sys;d=json.load(sys.stdin);assert d["resource"]=="'"$URL"'";assert d["authorization_servers"];print("PRM OK")'
curl -sf "$ORIGIN/.well-known/oauth-authorization-server" | python3 -c 'import json,sys;d=json.load(sys.stdin);assert "S256" in d["code_challenge_methods_supported"];assert d.get("registration_endpoint");assert "none" in d["token_endpoint_auth_methods_supported"];assert {"authorization_code","refresh_token"}<=set(d["grant_types_supported"]);print("AS metadata OK (S256, DCR, none, code+refresh)")'
echo "all checks passed"
