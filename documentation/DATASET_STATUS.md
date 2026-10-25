# Danh muc va trang thai Dataset

**20 project co source; 1 project da kiem thu HTTP, 19 project WFD chua runtime verified.**

Kiem tra tinh toan ven source/spec: 19/19. Dac ta WFD: 8 hop le ve cau truc, 11 co loi.
Cau truc spec hop le khong co nghia la da doi chieu hanh vi API.

| Project | Source | Operations | Spec | Runtime |
|---|---|---:|---|---|
| API-001-Bookstore | [Source](../api_projects/API-001-Bookstore) | 5 | OAS 3.0.3, verified with limitations | 28/28 HTTP cases |
| [API-002-bibliothek](../api_projects/API-002-bibliothek/README.md) | [Source](../sources/WFD/jdk_17_gradle/cs/rest/bibliothek) | 8 | 3.0.1 — invalid | Not run |
| [API-003-catwatch](../api_projects/API-003-catwatch/README.md) | [Source](../sources/WFD/jdk_8_maven/cs/rest/original/catwatch) | 23 | 2.0 — invalid | Not run |
| [API-004-cwa-verification](../api_projects/API-004-cwa-verification/README.md) | [Source](../sources/WFD/jdk_11_maven/cs/rest/cwa-verification-server) | 5 | 3.0.1 — invalid | Not run |
| [API-005-familie-ba-sak](../api_projects/API-005-familie-ba-sak/README.md) | [Source](../sources/WFD/jdk_17_maven/cs/rest/familie-ba-sak) | 183 | 3.0.1 — valid | Not run |
| [API-006-features-service](../api_projects/API-006-features-service/README.md) | [Source](../sources/WFD/jdk_8_maven/cs/rest/original/features-service) | 18 | 2.0 — invalid | Not run |
| [API-007-genome-nexus](../api_projects/API-007-genome-nexus/README.md) | [Source](../sources/WFD/jdk_8_maven/cs/rest-gui/genome-nexus) | 23 | 2.0 — invalid | Not run |
| [API-008-http-patch-spring](../api_projects/API-008-http-patch-spring/README.md) | [Source](../sources/WFD/jdk_11_maven/cs/rest/http-patch-spring) | 6 | 3.0.1 — valid | Not run |
| [API-009-market](../api_projects/API-009-market/README.md) | [Source](../sources/WFD/jdk_11_maven/cs/rest-gui/market) | 13 | 2.0 — valid | Not run |
| [API-010-microcks](../api_projects/API-010-microcks/README.md) | [Source](../sources/WFD/jdk_21_maven/cs/rest-gui/microcks) | 88 | 3.0.1 — invalid | Not run |
| [API-011-ocvn](../api_projects/API-011-ocvn/README.md) | [Source](../sources/WFD/jdk_8_maven/cs/rest-gui/ocvn) | 192 | 2.0 — invalid | Not run |
| [API-012-pay-publicapi](../api_projects/API-012-pay-publicapi/README.md) | [Source](../sources/WFD/jdk_11_maven/cs/rest/pay-publicapi) | 16 | 3.0.1 — valid | Not run |
| [API-013-person-controller](../api_projects/API-013-person-controller/README.md) | [Source](../sources/WFD/jdk_21_maven/cs/rest/person-controller) | 12 | 3.0.1 — invalid | Not run |
| [API-014-proxyprint](../api_projects/API-014-proxyprint/README.md) | [Source](../sources/WFD/jdk_8_maven/cs/rest/original/proxyprint) | 115 | 2.0 — invalid | Not run |
| [API-015-quartz-manager](../api_projects/API-015-quartz-manager/README.md) | [Source](../sources/WFD/jdk_11_maven/cs/rest-gui/quartz-manager) | 11 | 3.0.1 — invalid | Not run |
| [API-016-scout-api](../api_projects/API-016-scout-api/README.md) | [Source](../sources/WFD/jdk_8_maven/cs/rest/original/scout-api) | 49 | 2.0 — invalid | Not run |
| [API-017-spring-batch-rest](../api_projects/API-017-spring-batch-rest/README.md) | [Source](../sources/WFD/jdk_8_maven/cs/rest/original/spring-batch-rest) | 5 | 3.0.1 — valid | Not run |
| [API-018-spring-rest-example](../api_projects/API-018-spring-rest-example/README.md) | [Source](../sources/WFD/jdk_17_maven/cs/rest/spring-rest-example) | 9 | 3.0.1 — valid | Not run |
| [API-019-swagger-petstore](../api_projects/API-019-swagger-petstore/README.md) | [Source](../sources/WFD/jdk_8_maven/cs/rest/original/swagger-petstore) | 19 | 3.0.4 — valid | Not run |
| [API-020-user-management](../api_projects/API-020-user-management/README.md) | [Source](../sources/WFD/jdk_8_maven/cs/rest/original/user-management) | 21 | 2.0 — valid | Not run |

## Tiep tuc

Xem [huong dan WFD](WFD.md). Can Docker Desktop voi Linux containers de build/chay.
Moi project co `project.json`, build/run compose, raw spec, operation inventory, draft smoke plan va static audit.
Source that duoc giu trong submodule WFD ghim commit, khong sao chep code vao 19 thu muc ho so.
11 dac ta loi duoc giu nguyen de xu ly co bang chung; khong tao Ground Truth da verified tu chung.
