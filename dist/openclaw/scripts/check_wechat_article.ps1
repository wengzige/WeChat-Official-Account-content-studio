param(
    [Parameter(Mandatory = $true)]
    [string]$ArticleDir,
    [switch]$Strict
)

$repoRoot = Split-Path -Parent $PSScriptRoot
$workflowRoot = Join-Path $repoRoot 'skill2 paibanyouhua'
$resolvedArticleDir = $ArticleDir

if (-not [System.IO.Path]::IsPathRooted($resolvedArticleDir)) {
    $candidate = Join-Path $workflowRoot $resolvedArticleDir
    if (-not (Test-Path -LiteralPath $candidate)) {
        throw "Template article folder not found: $candidate"
    }
    $resolvedArticleDir = $candidate
}

if (-not (Test-Path -LiteralPath $resolvedArticleDir)) {
    throw "Article folder not found: $resolvedArticleDir"
}

$scriptPath = Join-Path $workflowRoot 'scripts\run-quality-gates.py'
if (-not (Test-Path -LiteralPath $scriptPath)) {
    throw "Quality gate script not found: $scriptPath"
}

$args = @($scriptPath, '--article-dir', $resolvedArticleDir)
if ($Strict) {
    $args += '--strict'
}

& python @args
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
