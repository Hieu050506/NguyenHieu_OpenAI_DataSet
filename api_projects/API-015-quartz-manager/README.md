# API-015-quartz-manager — Quartz Manager

Status: **imported_not_runtime_verified**. Source and upstream specification are present;
this project has not been built or exercised over HTTP on this machine.

- Original repository: https://github.com/fabioformosa/quartz-manager
- Pinned WFD commit: `915859080da033fc36feae54bab3ad4a7b04e872`
- [Local source](../../sources/WFD/jdk_11_maven/cs/rest-gui/quartz-manager) (129 Java/Kotlin files)
- Declared license: Apache (WFD README). Original notices remain in the source submodule.
- Runtime: JDK 11; build tool: Maven; database: .
- Authentication declared by WFD: TRUE.
- Upstream spec: 3.0.1, 11 operations.
- [Raw spec](../../results/API-015-quartz-manager/openapi.upstream.json)
- [Static audit](../../results/API-015-quartz-manager/static-audit.json)
- [Draft smoke plan](../../test_cases/API-015-quartz-manager/http-plan.json)

## Build and run from the Dataset root

Requires Docker Desktop running Linux containers and Docker Compose v2.
Build scripts adapt WFD's commands to this selected module; runtime builds have not yet been verified.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\dataset.ps1 -Action Build -Project API-015-quartz-manager
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\dataset.ps1 -Action Start -Project API-015-quartz-manager
```

Local API base URL: <http://127.0.0.1:8115>. Schema candidates from WFD drivers: /v3/api-docs.
The original spec's public server URL is not used to send requests.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\dataset.ps1 -Action Smoke -Project API-015-quartz-manager
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\dataset.ps1 -Action Stop -Project API-015-quartz-manager
```

Smoke testing does not mark the project as verified Ground Truth. Add full lifecycle and error tests,
compare responses to source, repair/normalize the spec with an audit trail, then review the result.
Do not use live credentials. WFD fixture authentication is under `sources/WFD/auth`.
Stop preserves named volumes; databases declared as tmpfs by WFD are temporary.

## Preserved license/notice files

- [LICENSE](../../sources/WFD/jdk_11_maven/cs/rest-gui/quartz-manager/LICENSE)
