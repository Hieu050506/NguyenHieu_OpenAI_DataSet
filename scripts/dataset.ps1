param(
    [ValidateSet('List', 'Audit', 'Build', 'Start', 'Stop', 'Smoke')]
    [string]$Action = 'List',
    [string]$Project = ''
)
$ErrorActionPreference = 'Stop'
$datasetRoot = Split-Path -Parent $PSScriptRoot
$pythonExe = Join-Path $datasetRoot 'api_projects\API-001-Bookstore\.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonExe)) {
    throw 'Chay scripts\setup.ps1 truoc de cai Python dependencies.'
}
$datasetArgs = @('-X', 'utf8', (Join-Path $PSScriptRoot 'dataset.py'), $Action.ToLowerInvariant())
if ($Project) { $datasetArgs += @('--project', $Project) }
& $pythonExe @datasetArgs
if ($LASTEXITCODE -ne 0) { throw 'Lenh khong hoan tat. Xem thong bao ERROR phia tren.' }
