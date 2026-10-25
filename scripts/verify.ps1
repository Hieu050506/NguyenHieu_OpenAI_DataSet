$ErrorActionPreference = 'Stop'
$datasetRoot = Split-Path -Parent $PSScriptRoot
$pythonExe = Join-Path $datasetRoot 'api_projects\API-001-Bookstore\.venv\Scripts\python.exe'
& $pythonExe -X utf8 (Join-Path $PSScriptRoot 'verify_api.py')
if ($LASTEXITCODE -ne 0) { throw 'Kiem thu that bai. Xem results\API-001-Bookstore.' }
