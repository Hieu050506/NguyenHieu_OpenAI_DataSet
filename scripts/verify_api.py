"""Verify the pinned upstream API over HTTP, using a disposable SQLite database."""
import copy
import hashlib
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone

import httpx
from jsonschema import Draft4Validator
from openapi_spec_validator import validate_spec

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ID = "API-001-Bookstore"
PROJECT = ROOT / "api_projects" / PROJECT_ID
RESULTS = ROOT / "results" / PROJECT_ID
TRUTH = ROOT / "ground_truth" / PROJECT_ID


def save_json(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def reference(name):
    return {"$ref": f"#/components/schemas/{name}"}


def build_contract(raw):
    """Curate an OAS 3.0.3 contract from source + explicitly tested behavior."""
    spec = copy.deepcopy(raw)
    spec["openapi"] = "3.0.3"
    spec["info"] = {
        "title": "Book Management API - verified pilot",
        "version": "1.0.0",
        "description": "Contract for upstream commit 6888542d376057a82d954d31ec4a962d6f8e1839. "
        "Verified against source and recorded HTTP cases. This is not an exhaustive proof. "
        "PUT returns data={} on this pinned runtime; GET verifies the persisted update.",
        "license": {"name": "MIT", "url": "https://github.com/martcpp/crud-api-fastapi/blob/main/LICENSE"},
    }
    spec["servers"] = [{"url": "http://127.0.0.1:8000"}]
    schemas = spec["components"]["schemas"]
    schemas["Book"] = {
        "type": "object",
        "required": ["id", "title", "author", "year", "isbn"],
        "properties": {"id": {"type": "integer"}, **copy.deepcopy(schemas["bookbase"]["properties"])},
    }
    schemas["NotFound"] = {
        "type": "object", "required": ["detail"],
        "properties": {"detail": {"type": "string", "enum": ["Book not found"]}},
    }

    def response(description, schema):
        return {"description": description, "content": {"application/json": {"schema": schema}}}

    def message(text, data=None):
        properties = {"message": {"type": "string", "enum": [text]}}
        if data is not None:
            properties["data"] = data
        return {"type": "object", "required": list(properties), "properties": properties}

    paths = spec["paths"]
    paths["/books/"]["get"]["responses"]["200"] = response("All books; empty list when none exist", {"type": "array", "items": reference("Book")})
    paths["/books/"]["post"]["responses"]["201"] = response("Book created", message("Book created successfully", reference("Book")))
    by_id = paths["/books/{book_id}"]
    by_id["get"]["responses"]["200"] = response("Book found", reference("Book"))
    by_id["put"]["responses"]["200"] = response("Book updated; data is an empty object in the pinned implementation", message("Book updated successfully", {"type": "object", "maxProperties": 0}))
    by_id["delete"]["responses"]["200"] = response("Book deleted", message("Book deleted successfully"))
    for method in ("get", "put", "delete"):
        by_id[method]["responses"]["404"] = response("Book does not exist", reference("NotFound"))
    return spec


def expand_refs(value, spec):
    if isinstance(value, dict):
        if "$ref" in value:
            target = spec
            for part in value["$ref"].removeprefix("#/").split("/"):
                target = target[part]
            return expand_refs(target, spec)
        return {k: expand_refs(v, spec) for k, v in value.items()}
    if isinstance(value, list):
        return [expand_refs(v, spec) for v in value]
    return value


def substitute(value, variables):
    if isinstance(value, str):
        for key, replacement in variables.items():
            value = value.replace("$" + key, str(replacement))
    elif isinstance(value, list):
        return [substitute(v, variables) for v in value]
    elif isinstance(value, dict):
        return {k: substitute(v, variables) for k, v in value.items()}
    return value


def value_at(body, dotted):
    for key in dotted.split("."):
        body = body[int(key)] if isinstance(body, list) else body[key]
    return body


def run_case(client, case, variables, spec):
    case = substitute(case, variables)
    method, path = case["method"], case["path"]
    kwargs = {}
    for key in ("json", "content", "headers"):
        if key in case:
            kwargs[key] = case[key]
    response = client.request(method, path, **kwargs)
    try:
        body = response.json()
    except ValueError:
        body = response.text
    record = {
        "id": case["id"], "description": case["description"],
        "request": {"method": method, "path": path, **kwargs},
        "expected_status": case["status"],
        "response": {"status": response.status_code, "headers": dict(response.headers), "body": body},
    }
    try:
        assert response.status_code == case["status"], f"expected {case['status']}, got {response.status_code}"
        if "body" in case:
            assert body == case["body"], f"unexpected body: {body!r}"
        for key, expected in case.get("equals", {}).items():
            assert value_at(body, key) == expected, f"unexpected {key}: {value_at(body, key)!r}"
        if "length" in case:
            assert len(body) == case["length"], f"unexpected length: {len(body)}"
        if "contains" in case:
            assert case["contains"] in body
        if "location" in case:
            assert response.headers["location"].endswith(case["location"])
        if "save_id" in case:
            variables[case["save_id"]] = body["data"]["id"]
            assert isinstance(body["data"]["id"], int)
        route = "/books/{book_id}" if path.startswith("/books/") and path != "/books/" else path
        operation = spec["paths"].get(route, {}).get(method.lower(), {})
        declared = operation.get("responses", {}).get(str(response.status_code))
        if declared and "content" in declared:
            schema = declared["content"]["application/json"]["schema"]
            Draft4Validator(expand_refs(schema, spec)).validate(body)
            record["response_schema_valid"] = True
        record["passed"] = True
    except Exception as error:
        record["passed"] = False
        record["error"] = str(error)
    return record


def main():
    started = datetime.now(timezone.utc).isoformat()
    cases = json.loads((ROOT / "test_cases" / PROJECT_ID / "cases.json").read_text(encoding="utf-8"))
    for directory in (RESULTS, TRUTH):
        directory.mkdir(parents=True, exist_ok=True)
    commit = subprocess.check_output(["git", "-C", str(PROJECT), "rev-parse", "HEAD"], text=True).strip()
    assert commit == "6888542d376057a82d954d31ec4a962d6f8e1839", "Upstream commit changed; review before verifying."
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    env = dict(os.environ)
    env["PYTHONPATH"] = str(PROJECT / "src")
    env["PYTHONUTF8"] = "1"
    records = []
    with tempfile.TemporaryDirectory(prefix="bookstore-test-") as temporary:
        with (RESULTS / "server.log").open("w", encoding="utf-8") as log:
            process = subprocess.Popen(
                [sys.executable, "-m", "uvicorn", "app:app", "--host", "127.0.0.1", "--port", str(port)],
                cwd=temporary, env=env, stdout=log, stderr=subprocess.STDOUT,
            )
            try:
                with httpx.Client(base_url=f"http://127.0.0.1:{port}", trust_env=False, timeout=10, follow_redirects=False) as client:
                    deadline = time.monotonic() + 30
                    while True:
                        if process.poll() is not None:
                            raise RuntimeError("API failed to start. See results/API-001-Bookstore/server.log")
                        try:
                            if client.get("/openapi.json").status_code == 200:
                                break
                        except httpx.TransportError:
                            pass
                        if time.monotonic() > deadline:
                            raise RuntimeError("API startup timed out")
                        time.sleep(0.2)
                    raw = client.get("/openapi.json").json()
                    save_json(RESULTS / "openapi.generated.json", raw)
                    validate_spec(raw)
                    contract = build_contract(raw)
                    validate_spec(contract)
                    variables = {}
                    for case in cases:
                        records.append(run_case(client, case, variables, contract))
            finally:
                # Windows venv launchers can spawn a Python child; stop our tree.
                if os.name == "nt":
                    subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
                else:
                    process.terminate()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
    passed = sum(record["passed"] for record in records)
    success = passed == len(cases)
    # A failed re-verification must not leave an older contract marked verified.
    save_json(TRUTH / "verification.json", {"status": "verified_with_known_limitations" if success else "failed", "commit": commit, "verified_at_utc": started, "passed": passed, "total": len(cases), "limitations": ["PUT returns an empty data object", "No exhaustive or security verification", "Pinned upstream dependency versions are not a production recommendation"]})
    if success:
        save_json(TRUTH / "openapi.3.0.3.json", contract)
    hashes = {name: hashlib.sha256((PROJECT / name).read_bytes()).hexdigest() for name in ("src/app.py", "src/database.py", "src/models.py", "src/schema.py", "requirements.txt", "LICENSE")}
    save_json(RESULTS / "http-results.json", {"started_at_utc": started, "upstream_commit": commit, "source_sha256": hashes, "total": len(cases), "passed": passed, "failed": len(cases) - passed, "generated_openapi_version": raw["openapi"], "curated_openapi_version": contract["openapi"], "cases": records})
    summary = [f"# {PROJECT_ID}: HTTP verification", "", f"UTC: {started}", f"Upstream commit: `{commit}`", f"Result: {passed}/{len(cases)} passed.", "", "| Case | Description | Status | Result |", "|---|---|---|---|"]
    for record in records:
        summary.append(f"| {record['id']} | {record['description']} | {record['response']['status']} | {'PASS' if record['passed'] else 'FAIL'} |")
    (RESULTS / "summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print(f"{PROJECT_ID}: {passed}/{len(cases)} HTTP cases passed.")
    for record in records:
        if not record["passed"]:
            print(f"FAIL {record['id']}: {record['error']}")
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
