# API-004-cwa-verification — CWA-Verification-Server

Status: **imported_not_runtime_verified**. Source and upstream specification are present;
this project has not been built or exercised over HTTP on this machine.

- Original repository: https://github.com/corona-warn-app/cwa-verification-server
- Pinned WFD commit: `915859080da033fc36feae54bab3ad4a7b04e872`
- [Local source](../../sources/WFD/jdk_11_maven/cs/rest/cwa-verification-server) (58 Java/Kotlin files)
- Declared license: Apache (WFD README). Original notices remain in the source submodule.
- Runtime: JDK 11; build tool: Maven; database: H2.
- Authentication declared by WFD: FALSE.
- Upstream spec: 3.0.1, 5 operations.
- [Raw spec](../../results/API-004-cwa-verification/openapi.upstream.json)
- [Static audit](../../results/API-004-cwa-verification/static-audit.json)
- [Draft smoke plan](../../test_cases/API-004-cwa-verification/http-plan.json)

## Build and run from the Dataset root

Requires Docker Desktop running Linux containers and Docker Compose v2.
Build scripts adapt WFD's commands to this selected module; runtime builds have not yet been verified.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\dataset.ps1 -Action Build -Project API-004-cwa-verification
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\dataset.ps1 -Action Start -Project API-004-cwa-verification
```

Local API base URL: <http://127.0.0.1:8104>. Schema candidates from WFD drivers: see upstream driver/source.
The original spec's public server URL is not used to send requests.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\dataset.ps1 -Action Smoke -Project API-004-cwa-verification
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\dataset.ps1 -Action Stop -Project API-004-cwa-verification
```

Smoke testing does not mark the project as verified Ground Truth. Add full lifecycle and error tests,
compare responses to source, repair/normalize the spec with an audit trail, then review the result.
Do not use live credentials. WFD fixture authentication is under `sources/WFD/auth`.
Stop preserves named volumes; databases declared as tmpfs by WFD are temporary.

## Preserved license/notice files

- [LICENSE](../../sources/WFD/jdk_11_maven/cs/rest/cwa-verification-server/LICENSE)
- [NOTICE](../../sources/WFD/jdk_11_maven/cs/rest/cwa-verification-server/NOTICE)
