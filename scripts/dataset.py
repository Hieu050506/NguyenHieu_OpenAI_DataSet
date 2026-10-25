"""Catalog, static audit and Docker lifecycle for the imported WFD APIs."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from urllib.parse import urlparse

import httpx
from openapi_spec_validator import validate_spec
import yaml

ROOT = Path(__file__).resolve().parents[1]
WFD = ROOT / 'sources/WFD'


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def save_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def spec_digest(path):
    return hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest()


def find_docker():
    found = shutil.which('docker')
    candidates = [Path('C:/Program Files/Docker/Docker/resources/bin/docker.exe'), Path(os.environ.get('LOCALAPPDATA', '')) / 'Programs/DockerDesktop/resources/bin/docker.exe']
    return found or next((str(p) for p in candidates if p.is_file()), None)


def require_docker():
    docker = find_docker()
    if not docker:
        raise RuntimeError('Docker is not installed or not in PATH. Install Docker Desktop, start Linux containers, then retry. See documentation/WFD.md.')
    result = subprocess.run([docker, 'info', '--format', '{{.OSType}}'], capture_output=True, text=True)
    if result.returncode or result.stdout.strip() != 'linux':
        raise RuntimeError('Docker must be running in Linux-container mode. Open Docker Desktop, wait until ready, then retry.')
    subprocess.run([docker, 'compose', 'version'], check=True, capture_output=True)
    return docker


def check_pinned_source(project):
    commit = subprocess.check_output(['git', '-C', str(WFD), 'rev-parse', 'HEAD'], text=True).strip()
    if commit != project['collection_commit']:
        raise RuntimeError('WFD source commit differs from the catalog. Restore the pinned submodule before running.')
    return commit


def compose_command(docker, project, kind):
    directory = ROOT / 'api_projects' / project['project_id']
    return [docker, 'compose', '--project-directory', str(directory), '-p', 'dataset-' + project['project_id'].lower(), '-f', str(directory / f'{kind}.compose.yaml')]


def audit(projects):
    reports = []
    for project in projects:
        project_id = project['project_id']
        result_dir = ROOT / 'results' / project_id
        problems = []
        try:
            commit = check_pinned_source(project)
            source = ROOT / project['source_path']
            assert source.is_dir(), 'Source directory missing'
            assert any(source.rglob('*.java')) or any(source.rglob('*.kt')), 'No Java/Kotlin source files'
            raw_path = result_dir / 'openapi.upstream.json'
            assert spec_digest(raw_path) == project['raw_spec_sha256'], 'Imported spec hash changed'
            assert spec_digest(WFD / 'openapi-swagger' / (project['slug'] + '.json')) == project['raw_spec_sha256'], 'Spec differs from pinned WFD'
            for filename in project['license_files']:
                assert (ROOT / filename).is_file(), f'Missing license/notice {filename}'
            for kind in ('build', 'runtime'):
                compose_file = ROOT / 'api_projects' / project_id / f'{kind}.compose.yaml'
                compose = yaml.safe_load(compose_file.read_text(encoding='utf-8'))
                assert compose.get('services'), f'{kind}: missing services'
                for name, service in compose['services'].items():
                    if isinstance(service.get('build'), dict):
                        context = (compose_file.parent / service['build']['context']).resolve()
                        assert context.is_dir(), f'Missing context {context}'
                        assert (context / service['build']['dockerfile']).is_file(), f'Missing Dockerfile for {name}'
                    for volume in service.get('volumes', []):
                        if isinstance(volume, str) and volume.startswith('../'):
                            host = volume.split(':', 1)[0]
                            if not host.endswith('/dist') and not host.endswith('/traffic'):
                                assert (compose_file.parent / host).resolve().exists(), f'Missing bind mount {host}'
            assert read_json(ROOT / 'ground_truth' / project_id / 'verification.json')['status'] == 'not_verified', 'Review runtime verification status before auditing imports'
        except Exception as error:
            problems.append(str(error))
        spec_error = None
        try:
            validate_spec(read_json(result_dir / 'openapi.upstream.json'))
        except Exception as error:
            spec_error = {'type': type(error).__name__, 'message': str(error)[:5000]}
        report = {
            'project_id': project_id, 'checked_at_utc': now(),
            'source_integrity': 'pass' if not problems else 'fail', 'integrity_errors': problems,
            'raw_spec_sha256': project['raw_spec_sha256'],
            'spec_structure': 'valid' if spec_error is None else 'invalid', 'spec_error': spec_error,
            'operation_count': project['operation_count'], 'runtime': 'not_verified',
            'warning': 'Static checks are not HTTP execution or verified Ground Truth.',
        }
        save_json(result_dir / 'static-audit.json', report)
        reports.append(report)
    summary = {'checked_at_utc': now(), 'imported_projects': len(projects), 'source_integrity_passed': sum(r['source_integrity'] == 'pass' for r in reports), 'spec_structure_valid': sum(r['spec_structure'] == 'valid' for r in reports), 'spec_structure_invalid': sum(r['spec_structure'] == 'invalid' for r in reports), 'docker_cli_available': bool(find_docker()), 'runtime_verified_by_this_audit': 0, 'projects': reports}
    save_json(ROOT / 'results/wfd-import-audit.json', summary)
    print(f"Source integrity: {summary['source_integrity_passed']}/{len(projects)}")
    print(f"Spec structure: {summary['spec_structure_valid']} valid, {summary['spec_structure_invalid']} invalid")
    print('Runtime verification: not performed by static audit.')
    return 0 if summary['source_integrity_passed'] == len(projects) else 1


def build(project):
    docker = require_docker()
    check_pinned_source(project)
    dist = WFD / 'dist'
    dist.mkdir(exist_ok=True)
    command = compose_command(docker, project, 'build')
    subprocess.run(command + ['build', 'build'], check=True)
    subprocess.run(command + ['run', '--rm', '-T', 'build'], check=True)
    expected = dist / (project['slug'] + '-sut.jar')
    if not expected.is_file():
        raise RuntimeError('Build did not produce the expected JAR: ' + str(expected))
    for name in ('jacocoagent.jar', 'jacococli.jar'):
        shutil.copyfile(WFD / 'jacoco' / name, dist / name)
    save_json(ROOT / 'results' / project['project_id'] / 'build-status.json', {'status': 'built', 'at_utc': now(), 'jar_sha256': digest(expected), 'collection_commit': project['collection_commit']})
    print('Built ' + str(expected))


def start(project):
    docker = require_docker()
    check_pinned_source(project)
    if not (WFD / 'dist' / (project['slug'] + '-sut.jar')).is_file():
        raise RuntimeError('Build this project first with -Action Build.')
    if not (WFD / 'dist/jacocoagent.jar').is_file():
        raise RuntimeError('JaCoCo agent missing; run -Action Build again.')
    (ROOT / 'results' / project['project_id'] / 'traffic').mkdir(exist_ok=True)
    environment = dict(os.environ)
    environment['AUTH_PORT'] = str(project['auth_port'])
    subprocess.run(compose_command(docker, project, 'runtime') + ['up', '--build', '-d'], check=True, env=environment)
    save_json(ROOT / 'results' / project['project_id'] / 'runtime-status.json', {'status': 'containers_started_not_http_verified', 'at_utc': now(), 'url': f"http://127.0.0.1:{project['http_port']}", 'http_tests_executed': 0})
    print(f"Containers started. API: http://127.0.0.1:{project['http_port']}")
    print('Wait for application startup, then run -Action Smoke. Container start is not runtime verification.')


def stop(project):
    docker = require_docker()
    environment = dict(os.environ)
    environment['AUTH_PORT'] = str(project['auth_port'])
    subprocess.run(compose_command(docker, project, 'runtime') + ['down'], env=environment, check=True)
    print('Stopped project containers; named volumes were preserved.')


def smoke(project):
    plan = read_json(ROOT / 'test_cases' / project['project_id'] / 'http-plan.json')
    base = f"http://127.0.0.1:{project['http_port']}"
    results = []
    with httpx.Client(base_url=base, trust_env=False, timeout=20, follow_redirects=False) as client:
        for case in plan['cases']:
            record = {'case': case, 'at_utc': now(), 'url': base + case['path']}
            if case.get('declared_security'):
                record.update({'status': 'skipped_requires_auth', 'passed': False})
            else:
                # Spec-supplied paths must never redirect this client to another host.
                parts = urlparse(case['path'])
                if parts.scheme or parts.netloc or not case['path'].startswith('/') or case['path'].startswith('//'):
                    raise RuntimeError('Unsafe request path in smoke plan')
                try:
                    response = client.get(case['path'])
                    record.update({'status': 'executed', 'http_status': response.status_code, 'expected_statuses': case['expected_statuses'], 'passed': response.status_code in case['expected_statuses'], 'response_body': response.text[:100000]})
                except httpx.HTTPError as error:
                    record.update({'status': 'connection_error', 'passed': False, 'error': str(error)})
            results.append(record)
    success = bool(results) and all(r['passed'] for r in results)
    save_json(ROOT / 'results' / project['project_id'] / 'smoke-results.json', {'at_utc': now(), 'project_id': project['project_id'], 'scope': 'read_only_smoke_only', 'passed': sum(r['passed'] for r in results), 'total': len(results), 'ground_truth_verified': False, 'cases': results})
    print(f"Smoke: {sum(r['passed'] for r in results)}/{len(results)} passed. Ground Truth remains unverified.")
    return 0 if success else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['list', 'audit', 'build', 'start', 'stop', 'smoke'])
    parser.add_argument('--project')
    args = parser.parse_args()
    projects = read_json(ROOT / 'documentation/wfd-projects.json')
    if args.action == 'list':
        pilot = read_json(ROOT / 'ground_truth/API-001-Bookstore/verification.json')
        print(f"API-001-Bookstore | {pilot['status']} | {pilot['passed']}/{pilot['total']} HTTP tests")
        for project in projects:
            print(f"{project['project_id']} | {project['status']} | port {project['http_port']}")
        print(f'Total source projects: {len(projects)+1}. Imported WFD projects are not runtime verified.')
        return 0
    if args.action == 'audit':
        return audit(projects)
    project = next((p for p in projects if p['project_id'] == args.project), None)
    if project is None:
        parser.error('Use --project with an exact WFD project ID from the list command.')
    if args.action == 'smoke':
        return smoke(project)
    globals()[args.action](project)
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (RuntimeError, subprocess.CalledProcessError) as error:
        print('ERROR: ' + str(error), file=sys.stderr)
        sys.exit(1)
