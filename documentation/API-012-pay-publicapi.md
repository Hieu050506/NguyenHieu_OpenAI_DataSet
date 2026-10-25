# API-012-pay-publicapi — Payments Public API

Status: **imported_not_runtime_verified**. Source and upstream specification are present;
this project has not been built or exercised over HTTP on this machine.

- Original repository: https://github.com/alphagov/pay-publicapi
- Pinned WFD commit: `915859080da033fc36feae54bab3ad4a7b04e872`
- [Local source](../sources/WFD/jdk_11_maven/cs/rest/pay-publicapi) (377 Java/Kotlin files)
- Declared license: MIT (WFD README). Original notices remain in the source submodule.
- Runtime: JDK 11; build tool: Maven; database: Redis.
- Authentication declared by WFD: TRUE.
- Upstream spec: 3.0.1, 16 operations.
- [Raw spec](../results/API-012-pay-publicapi/openapi.upstream.json)
- [Static audit](../results/API-012-pay-publicapi/static-audit.json)
- [Draft smoke plan](../test_cases/API-012-pay-publicapi/http-plan.json)

## Build and run from the Dataset root

Requires Docker Desktop running Linux containers and Docker Compose v2.
Build scripts adapt WFD's commands to this selected module; runtime builds have not yet been verified.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\dataset.ps1 -Action Build -Project API-012-pay-publicapi
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\dataset.ps1 -Action Start -Project API-012-pay-publicapi
```

Local API base URL: <http://127.0.0.1:8112>. Schema candidates from WFD drivers: /assets/swagger.json.
The original spec's public server URL is not used to send requests.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\dataset.ps1 -Action Smoke -Project API-012-pay-publicapi
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\dataset.ps1 -Action Stop -Project API-012-pay-publicapi
```

Smoke testing does not mark the project as verified Ground Truth. Add full lifecycle and error tests,
compare responses to source, repair/normalize the spec with an audit trail, then review the result.
Do not use live credentials. WFD fixture authentication is under `sources/WFD/auth`.
Stop preserves named volumes; databases declared as tmpfs by WFD are temporary.

## Preserved license/notice files

- [LICENSE](../sources/WFD/jdk_11_maven/cs/rest/pay-publicapi/LICENSE)
