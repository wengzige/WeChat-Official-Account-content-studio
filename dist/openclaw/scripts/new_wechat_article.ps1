param(
    [Parameter(Mandatory = $true)]
    [string]$Title,
    [string]$Author = '',
    [string]$SourceUrl = '',
    [switch]$Force
)

$repoRoot = Split-Path -Parent $PSScriptRoot
$scriptPath = Join-Path $repoRoot 'skill2 paibanyouhua\scripts\new-article.ps1'
if (-not (Test-Path -LiteralPath $scriptPath)) {
    throw "Template article script not found: $scriptPath"
}

& $scriptPath -Title $Title -Author $Author -SourceUrl $SourceUrl -Force:$Force
