param([ValidateRange(1024, 65535)][int]$Port = 8000)
$ErrorActionPreference = 'Stop'
$datasetRoot = Split-Path -Parent $PSScriptRoot
$projectRoot = Join-Path $datasetRoot 'api_projects\API-001-Bookstore'
$pythonExe = Join-Path $projectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonExe)) {
    throw 'Chua co moi truong Python. Chay scripts\setup.ps1 truoc.'
}
# An absolute --app-dir plus a fixed working directory keeps SQLite in src.
Push-Location (Join-Path $projectRoot 'src')
try {
    Write-Host "Swagger UI: http://127.0.0.1:$Port/docs"
    Write-Host "OpenAPI:    http://127.0.0.1:$Port/openapi.json"
    Write-Host 'Nhan Ctrl+C de dung API.'
    & $pythonExe -X utf8 -m uvicorn app:app --host 127.0.0.1 --port $Port
    if ($LASTEXITCODE -ne 0) { throw "API exited with code $LASTEXITCODE" }
} finally {
    Pop-Location
}
