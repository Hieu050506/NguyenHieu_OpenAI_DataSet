param([string]$PythonExe = '')
$ErrorActionPreference = 'Stop'
$datasetRoot = Split-Path -Parent $PSScriptRoot
$projectRoot = Join-Path $datasetRoot 'api_projects\API-001-Bookstore'
if (-not (Test-Path -LiteralPath (Join-Path $projectRoot 'src\app.py'))) {
    & git -C $datasetRoot submodule update --init --recursive
    if ($LASTEXITCODE -ne 0) { throw 'Khong tai duoc source. Kiem tra ket noi GitHub.' }
}
if (-not $PythonExe) {
    $PythonExe = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python312\python.exe'
}
if (-not (Test-Path -LiteralPath $PythonExe)) {
    throw 'Can Python 3.12. Truyen duong dan: .\scripts\setup.ps1 -PythonExe C:\path\python.exe'
}
$venvPython = Join-Path $projectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $venvPython)) {
    & $PythonExe -m venv (Join-Path $projectRoot '.venv')
    if ($LASTEXITCODE -ne 0) { throw 'Khong tao duoc venv.' }
}
& $venvPython -m pip install --disable-pip-version-check -r (Join-Path $datasetRoot 'documentation\requirements.windows-py312.lock.txt')
if ($LASTEXITCODE -ne 0) { throw 'Cai dependencies that bai.' }
Write-Host 'Da cai xong. Chay .\scripts\start-api.ps1 hoac .\scripts\verify.ps1.'
