#!/usr/bin/env python3
"""Validate the OpenAI plugin package against the Agent Plugins schemas and the
OpenAI submission field rules.

The published MCP schema does not allow vendor fields on a server. OpenAI's
packaging guide still requires extensions.com.openai.auth there. This script
validates the portable server fields against the schema, then checks the auth
object against that guide.
"""

from __future__ import annotations

import argparse
import json
import re
import struct
import sys
import urllib.request
import zipfile
from pathlib import Path

PLUGIN_SCHEMA_URL = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_SCHEMA_URL = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
MCP_URL = "https://mysdr.app/api/mcp"
LOGO = "assets/logo-plate.png"

CATEGORIES = {
    "Productivity",
    "Creativity",
    "Developer Tools",
    "Business & Operations",
    "Data & Analytics",
    "Communication",
    "Education & Research",
    "Security",
    "Finance",
    "Healthcare",
    "Travel",
    "Entertainment",
    "Other",
}

FORBIDDEN_KEYS = {
    "test_credentials",
    "reviewer_instructions",
    "clientSecret",
    "client_secret",
    "apps",
}
FORBIDDEN_NAMES = {".app.json", ".mcp.json", "hooks.json"}
SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$"
)
HTTPS = re.compile(r"^https://[^\s]+$")
ASSET_PATH = re.compile(r"^\./[^\s]+$")


class Fail(Exception):
    pass


def fail(message: str) -> None:
    raise Fail(message)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{path.name} is not valid JSON: {exc}")


def fetch_schema(url: str) -> dict:
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            payload = response.read()
    except Exception as exc:  # noqa: BLE001 - report the fetch, then stop
        fail(f"could not fetch schema {url}: {exc}")
    try:
        return json.loads(payload)
    except json.JSONDecodeError as exc:
        fail(f"schema {url} is not valid JSON: {exc}")


def validator_for(schema: dict):
    try:
        from jsonschema import Draft202012Validator
        from jsonschema.exceptions import SchemaError
    except ImportError:
        fail("jsonschema is not installed. Run: python3 -m pip install jsonschema")
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        fail(f"official schema is not a valid Draft 2020-12 schema: {exc}")
    return Draft202012Validator(schema)


def schema_errors(validator, instance) -> list[str]:
    return [
        f"{'/'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in validator.iter_errors(instance)
    ]


def report_mcp_extension_gap(validator, document) -> None:
    """Accept the known gap where the closed MCP schema rejects OpenAI auth.

    A future schema that understands extensions must validate this document
    directly. Any other failure is reported.
    """
    errors = list(validator.iter_errors(document))
    if not errors:
        print("note: published MCP schema accepts server.extensions. Auth object checked against the OpenAI guide.")
        return
    if len(errors) != 1 or errors[0].validator != "oneOf":
        fail("mcp.json failed the Agent Plugins schema:\n" + "\n".join(schema_errors(validator, document)))
    streamable = [child for child in errors[0].context if list(child.schema_path)[:1] == [1]]
    message = streamable[0].message if len(streamable) == 1 else ""
    if (
        len(streamable) == 1
        and streamable[0].validator == "additionalProperties"
        and "extensions" in message
        and "url" not in message
    ):
        print("note: published MCP schema rejects server.extensions; OpenAI's packaging guide requires the auth object. Portable fields passed.")
        return
    details = [f"{list(child.schema_path)}: {child.message}" for child in errors[0].context]
    fail("mcp.json failed the Agent Plugins schema beyond the known extensions gap:\n" + "\n".join(details))


def walk_keys(value, found: set[str]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            found.add(key)
            walk_keys(child, found)
    elif isinstance(value, list):
        for child in value:
            walk_keys(child, found)


def one_line(value: str, label: str, limit: int) -> None:
    if not isinstance(value, str) or not value.strip():
        fail(f"{label} is required")
    if value != value.strip() or "\n" in value or "\r" in value or "\t" in value:
        fail(f"{label} must be a single line without outer whitespace")
    if len(value) > limit:
        fail(f"{label} is {len(value)} characters; final limit is {limit}")


def https_url(value: str, label: str, limit: int) -> None:
    one_line(value, label, limit)
    if not HTTPS.match(value):
        fail(f"{label} must be an HTTPS URL")
    host = value[len("https://") :].split("/")[0]
    if not host or "@" in host:
        fail(f"{label} must be an HTTPS URL without credentials")


def asset_path(value: str, label: str, root: Path) -> None:
    if not isinstance(value, str) or not ASSET_PATH.match(value) or ".." in value.split("/"):
        fail(f"{label} must be a ./ relative path inside the package")
    path = root / value[2:]
    if not path.is_file():
        fail(f"{label} file is missing: {value}")


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if len(data) > 5 * 1024 * 1024:
        fail(f"{path.name} is larger than 5 MiB")
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        fail(f"{path.name} is not a PNG")
    length, kind = struct.unpack(">I4s", data[8:16])
    if kind != b"IHDR" or length < 8:
        fail(f"{path.name} has no PNG IHDR")
    width, height = struct.unpack(">II", data[16:24])
    if width != height:
        fail(f"{path.name} is {width}x{height}; icons must be square")
    if width < 48 or height < 48:
        fail(f"{path.name} is smaller than 48x48")
    if width > 4096 or height > 4096:
        fail(f"{path.name} is larger than 4096 px")
    return width, height


def check_skills(root: Path) -> None:
    skills = root / "skills"
    if not skills.is_dir():
        fail("skills/ is missing")
    found = []
    for skill in sorted(path for path in skills.iterdir() if path.is_dir()):
        if skill.name.startswith("."):
            fail(f"skill directory must not be hidden: {skill.name}")
        manifest = skill / "SKILL.md"
        if not manifest.is_file():
            fail(f"{skill.name} has no SKILL.md")
        text = manifest.read_text(encoding="utf-8")
        if re.search(r"claude", text, re.I):
            fail(f"{skill.name}/SKILL.md contains a Claude-specific instruction")
        match = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
        if not match:
            fail(f"{skill.name}/SKILL.md front matter is missing")
        front, body = match.group(1), match.group(2)
        name = re.search(r"^name: ([a-z0-9-]+)$", front, re.M)
        description = re.search(r"^description: (.+)$", front, re.M)
        if not name or name.group(1) != skill.name:
            fail(f"{skill.name}/SKILL.md name must match the directory")
        if not description or not description.group(1).strip():
            fail(f"{skill.name}/SKILL.md description is missing")
        if len(description.group(1)) > 1024:
            fail(f"{skill.name} description is longer than 1024 characters")
        if not body.strip():
            fail(f"{skill.name}/SKILL.md body is empty")
        if len(f"mysdr:{name.group(1)}") > 64:
            fail(f"{skill.name} identity is longer than 64 characters")
        found.append(skill.name)
    if found != ["mysdr-first-engine", "mysdr-onboarding"]:
        fail(f"unexpected skills: {found}")


def check_auth(server: dict) -> None:
    extra = set(server) - {"type", "url", "headers", "extensions"}
    if extra:
        fail(f"MCP server has fields the package guide does not use: {sorted(extra)}")
    if "headers" in server:
        fail("public submission rejects nonempty MCP headers")
    if server.get("type") != "streamable-http":
        fail("MCP transport must be streamable-http")
    if server.get("url") != MCP_URL:
        fail(f"MCP URL must be {MCP_URL}")
    extensions = server.get("extensions")
    if not isinstance(extensions, dict) or set(extensions) != {"com.openai"}:
        fail("MCP server must declare only extensions.com.openai")
    openai = extensions["com.openai"]
    if not isinstance(openai, dict) or set(openai) != {"auth"}:
        fail("MCP extensions.com.openai must contain only auth")
    auth = openai["auth"]
    if not isinstance(auth, dict) or set(auth) != {"type", "client"}:
        fail("OAuth auth must contain only type and client")
    if auth.get("type") != "oauth":
        fail('auth.type must be "oauth"')
    client = auth.get("client")
    if not isinstance(client, dict) or set(client) != {"mode"} or client.get("mode") != "cimd":
        fail('auth.client must be {"mode": "cimd"} with no client id or secret')


def check_cases(review: dict) -> None:
    cases = review.get("test_cases")
    if not isinstance(cases, dict) or set(cases) != {"positive", "negative"}:
        fail("review.test_cases must contain positive and negative")
    positive = cases["positive"]
    negative = cases["negative"]
    if not isinstance(positive, list) or len(positive) != 5:
        fail("initial MCP review requires exactly five positive test cases")
    if not isinstance(negative, list) or len(negative) != 3:
        fail("initial MCP review requires exactly three negative test cases")
    required = {"description", "prompt", "tools_triggered", "expected_behavior"}
    for label, group in (("positive", positive), ("negative", negative)):
        for index, case in enumerate(group, start=1):
            if not isinstance(case, dict) or set(case) != required:
                fail(f"{label} case {index} must contain {sorted(required)}")
            one_line(case["description"], f"{label} case {index} description", 4000)
            one_line(case["prompt"], f"{label} case {index} prompt", 4000)
            one_line(case["tools_triggered"], f"{label} case {index} tools_triggered", 4000)
            if not case["expected_behavior"].strip():
                fail(f"{label} case {index} expected_behavior is empty")
            if len(case["expected_behavior"]) > 4000:
                fail(f"{label} case {index} expected_behavior is too long")
    if review.get("commerce") is not False:
        fail("review.commerce must be false")
    if not isinstance(review.get("commerce_description"), str) or not review["commerce_description"].strip():
        fail("review.commerce_description is required in this package")
    if "demo_recording_url" in review:
        fail("omit demo_recording_url until a real walkthrough URL exists")


def check_manifest(root: Path, plugin: dict) -> None:
    one_line(plugin["name"], "name", 64)
    if not SEMVER.match(plugin["version"]):
        fail("version must be semantic")
    description = plugin["description"]
    if not isinstance(description, str) or not description.strip():
        fail("description is required")
    # submission-errors rejects package descriptions over 1024.
    # The field table still says 4000. Stay under the stricter code.
    if len(description) > 1024:
        fail(f"description is {len(description)} characters; submission error limit is 1024")
    author = plugin["author"]
    one_line(author["name"], "author.name", 120)
    one_line(author["email"], "author.email", 320)
    https_url(author["url"], "author.url", 2048)
    https_url(plugin["homepage"], "homepage", 2048)

    openai = plugin["extensions"]["com.openai"]
    allowed = {"interface", "onboardingSkill", "review", "publication"}
    if set(openai) != allowed:
        fail(f"extensions.com.openai fields must be {sorted(allowed)}")
    interface = openai["interface"]
    one_line(interface["displayName"], "displayName", 30)
    if interface["displayName"] != "mySDR":
        fail("displayName must be mySDR")
    one_line(interface["shortDescription"], "shortDescription", 30)
    long_description = interface["longDescription"]
    if not isinstance(long_description, str) or not long_description.strip():
        fail("longDescription is required")
    if len(long_description) > 4000:
        fail(f"longDescription is {len(long_description)} characters; limit is 4000")
    one_line(interface["developerName"], "developerName", 80)
    if interface["developerName"] != "LVDP CommV":
        fail("developerName must be LVDP CommV")
    if interface.get("category") not in CATEGORIES:
        fail(f"category {interface.get('category')!r} is not in the published dashboard list")
    capabilities = interface["capabilities"]
    if not isinstance(capabilities, list) or not capabilities or len(capabilities) > 20:
        fail("capabilities must contain 1 to 20 labels")
    for capability in capabilities:
        one_line(capability, "capability", 120)
    for label, key in (
        ("websiteURL", "websiteURL"),
        ("supportURL", "supportURL"),
        ("privacyPolicyURL", "privacyPolicyURL"),
        ("termsOfServiceURL", "termsOfServiceURL"),
    ):
        https_url(interface[key], label, 1024)
    prompts = interface["defaultPrompt"]
    if not isinstance(prompts, list) or len(prompts) != 3:
        fail("defaultPrompt must contain exactly three prompts")
    if len({prompt.strip().casefold() for prompt in prompts}) != 3:
        fail("defaultPrompt entries must be unique")
    for prompt in prompts:
        one_line(prompt, "defaultPrompt", 128)
        if "@" in prompt:
            fail("defaultPrompt must not contain an @ mention")
    for key in ("logo", "composerIcon"):
        asset_path(interface[key], key, root)
        if interface[key] != "./assets/logo-plate.png":
            fail(f"{key} must use ./assets/logo-plate.png")
    for optional in ("brandColor", "brandColorDark", "logoDark", "composerIconDark"):
        if optional in interface:
            fail(f"omit {optional}; no dark asset or brand hex was supplied")
    if openai["onboardingSkill"] != "./skills/mysdr-onboarding/SKILL.md":
        fail("onboardingSkill must point at the packaged onboarding skill")
    onboarding = root / "skills/mysdr-onboarding/SKILL.md"
    if not onboarding.is_file():
        fail("onboarding skill is missing")
    check_cases(openai["review"])
    publication = openai["publication"]
    if set(publication) != {"countries", "release_notes"}:
        fail("publication must contain only countries and release_notes")
    if publication["countries"] != []:
        fail("publication.countries must be an empty list until Louis chooses an allowlist")
    if not publication["release_notes"].strip():
        fail("release_notes is empty")


def check_package(root: Path, plugin_schema: dict, mcp_schema: dict) -> None:
    plugin_path = root / "plugin.json"
    mcp_path = root / "mcp.json"
    if not plugin_path.is_file() or not mcp_path.is_file():
        fail("plugin.json and mcp.json must sit at the package root")
    plugin = load_json(plugin_path)
    mcp = load_json(mcp_path)
    keys: set[str] = set()
    walk_keys(plugin, keys)
    walk_keys(mcp, keys)
    banned = FORBIDDEN_KEYS & keys
    if banned:
        fail(f"package contains forbidden fields: {sorted(banned)}")
    blob = json.dumps({"plugin": plugin, "mcp": mcp}).casefold()
    if "clientsecret" in blob or "reviewer_instructions" in blob or "test_credentials" in blob:
        fail("package contains a secret or reviewer credential field")

    plugin_errors = schema_errors(validator_for(plugin_schema), plugin)
    if plugin_errors:
        fail("plugin.json failed the Agent Plugins schema:\n" + "\n".join(plugin_errors))

    servers = mcp.get("mcpServers")
    if not isinstance(servers, dict) or set(servers) != {"mysdr"}:
        fail("mcp.json must declare exactly one server named mysdr")
    check_auth(servers["mysdr"])
    portable = json.loads(json.dumps(mcp))
    portable["mcpServers"]["mysdr"].pop("extensions", None)
    mcp_validator = validator_for(mcp_schema)
    mcp_errors = schema_errors(mcp_validator, portable)
    if mcp_errors:
        fail("portable mcp.json fields failed the Agent Plugins schema:\n" + "\n".join(mcp_errors))
    # OpenAI requires extensions.com.openai.auth. Agent Plugins 1.0.0 rejects that field.
    report_mcp_extension_gap(mcp_validator, mcp)

    check_manifest(root, plugin)
    check_skills(root)
    width, height = png_size(root / LOGO)
    print(f"logo {width}x{height} PNG")
    interface = plugin["extensions"]["com.openai"]["interface"]
    print(f"description {len(plugin['description'])}/1024")
    print(f"shortDescription {len(interface['shortDescription'])}/30")
    print(f"longDescription {len(interface['longDescription'])}/4000")
    print(f"displayName {len(interface['displayName'])}/30")
    print(f"developerName {len(interface['developerName'])}/80")
    for prompt in interface["defaultPrompt"]:
        print(f"defaultPrompt {len(prompt)}/128 {prompt}")


def check_zip(path: Path, plugin_schema: dict, mcp_schema: dict) -> None:
    if not zipfile.is_zipfile(path):
        fail(f"{path} is not a zip file")
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        bad = [name for name in names if name.startswith("/") or "\\" in name or ".." in name.split("/")]
        if bad:
            fail(f"zip has unsafe paths: {bad}")
        if any(Path(name).name in FORBIDDEN_NAMES or name.endswith(".app.json") for name in names):
            fail("zip contains an app, hook, or compatibility MCP file")
        required = {
            "plugin.json",
            "mcp.json",
            LOGO,
            "skills/mysdr-onboarding/SKILL.md",
            "skills/mysdr-first-engine/SKILL.md",
        }
        files = {name for name in names if not name.endswith("/")}
        if files != required:
            fail(f"zip files differ from the package: {sorted(files)}")
        info = archive.getinfo(LOGO)
        if info.file_size > 5 * 1024 * 1024:
            fail("zip logo is larger than 5 MiB")
    import tempfile

    with tempfile.TemporaryDirectory() as temporary:
        with zipfile.ZipFile(path) as archive:
            archive.extractall(temporary)
        check_package(Path(temporary), plugin_schema, mcp_schema)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("package", nargs="?", help="staged plugin directory")
    parser.add_argument("--zip", dest="zip_path", help="upload zip to validate")
    args = parser.parse_args()
    if bool(args.package) == bool(args.zip_path):
        fail("pass either a package directory or --zip")
    plugin_schema = fetch_schema(PLUGIN_SCHEMA_URL)
    mcp_schema = fetch_schema(MCP_SCHEMA_URL)
    try:
        if args.zip_path:
            check_zip(Path(args.zip_path), plugin_schema, mcp_schema)
        else:
            check_package(Path(args.package), plugin_schema, mcp_schema)
    except Fail as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    print("openai package OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
