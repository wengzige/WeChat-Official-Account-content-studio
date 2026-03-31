param(
    [switch]$Json
)

$repoRoot = Split-Path -Parent $PSScriptRoot
$scriptPath = Join-Path $repoRoot 'scripts\git_privacy_guard.py'

if (-not (Test-Path -LiteralPath $scriptPath)) {
    throw "Privacy guard script not found: $scriptPath"
}

$args = @($scriptPath)
if ($Json) {
    $args += '--json'
}

& python @args
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
