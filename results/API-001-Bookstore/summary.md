# API-001-Bookstore: HTTP verification

UTC: 2026-10-25T16:53:04.376015+00:00
Upstream commit: `6888542d376057a82d954d31ec4a962d6f8e1839`
Result: 28/28 passed.

| Case | Description | Status | Result |
|---|---|---|---|
| TC01 | Swagger UI is available | 200 | PASS |
| TC02 | Empty database returns [] | 200 | PASS |
| TC03 | Read missing book | 404 | PASS |
| TC04 | Update missing book | 404 | PASS |
| TC05 | Delete missing book | 404 | PASS |
| TC06 | Reject empty request body object | 422 | PASS |
| TC07 | Reject nonnumeric year | 422 | PASS |
| TC08 | Reject missing title | 422 | PASS |
| TC09 | Reject null title | 422 | PASS |
| TC10 | Reject noninteger path ID | 422 | PASS |
| TC11 | Reject malformed JSON | 422 | PASS |
| TC12 | Create book with nested returned ID | 201 | PASS |
| TC13 | Created book appears in list | 200 | PASS |
| TC14 | Read created book | 200 | PASS |
| TC15 | Update returns empty data object (known upstream defect) | 200 | PASS |
| TC16 | Read confirms update was persisted | 200 | PASS |
| TC17 | Duplicate ISBN accepted (not unique in source) | 201 | PASS |
| TC18 | List contains two books | 200 | PASS |
| TC19 | Delete second book | 200 | PASS |
| TC20 | Delete first book | 200 | PASS |
| TC21 | Read deleted book returns 404 | 404 | PASS |
| TC22 | Update deleted book returns 404 | 404 | PASS |
| TC23 | Delete deleted book returns 404 | 404 | PASS |
| TC24 | CRUD cleanup leaves empty list | 200 | PASS |
| TC25 | Missing trailing slash redirects | 307 | PASS |
| TC26 | PATCH is not implemented | 405 | PASS |
| TC27 | Unknown route returns 404 | 404 | PASS |
| TC28 | Negative ID is accepted as integer then not found | 404 | PASS |
