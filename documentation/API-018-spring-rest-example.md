# API-018-spring-rest-example — Spring Boot Restful API Example

Status: **imported_not_runtime_verified**. Source and upstream specification are present;
this project has not been built or exercised over HTTP on this machine.

- Original repository: https://github.com/phantasmicmeans/spring-boot-restful-api-example
- Pinned WFD commit: `915859080da033fc36feae54bab3ad4a7b04e872`
- [Local source](../sources/WFD/jdk_17_maven/cs/rest/spring-rest-example) (32 Java/Kotlin files)
- Declared license: MIT (WFD README). Original notices remain in the source submodule.
- Runtime: JDK 17; build tool: Maven; database: MySQL.
- Authentication declared by WFD: FALSE.
- Upstream spec: 3.0.1, 9 operations.
- [Raw spec](../results/API-018-spring-rest-example/openapi.upstream.json)
- [Static audit](../results/API-018-spring-rest-example/static-audit.json)
- [Draft smoke plan](../test_cases/API-018-spring-rest-example/http-plan.json)

## Build and run from the Dataset root

Requires Docker Desktop running Linux containers and Docker Compose v2.
Build scripts adapt WFD's commands to this selected module; runtime builds have not yet been verified.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\dataset.ps1 -Action Build -Project API-018-spring-rest-example
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\dataset.ps1 -Action Start -Project API-018-spring-rest-example
```

Local API base URL: <http://127.0.0.1:8118>. Schema candidates from WFD drivers: /v3/api-docs.
The original spec's public server URL is not used to send requests.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\dataset.ps1 -Action Smoke -Project API-018-spring-rest-example
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\dataset.ps1 -Action Stop -Project API-018-spring-rest-example
```

Smoke testing does not mark the project as verified Ground Truth. Add full lifecycle and error tests,
compare responses to source, repair/normalize the spec with an audit trail, then review the result.
Do not use live credentials. WFD fixture authentication is under `sources/WFD/auth`.
Stop preserves named volumes; databases declared as tmpfs by WFD are temporary.

## Preserved license/notice files

- [LICENSE](../sources/WFD/jdk_17_maven/cs/rest/spring-rest-example/LICENSE)
