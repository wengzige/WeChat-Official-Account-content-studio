param(
    [Parameter(Mandatory = $true)]
    [string]$ArticleDir,
    [string]$Theme = ''
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

$scriptPath = Join-Path $workflowRoot 'scripts\render-article.py'
if (-not (Test-Path -LiteralPath $scriptPath)) {
    throw "Template render script not found: $scriptPath"
}

$args = @($scriptPath, '--article-dir', $resolvedArticleDir)
if (-not [string]::IsNullOrWhiteSpace($Theme)) {
    $args += @('--theme', $Theme)
}

& python @args
if ($LASTEXITCODE -ne 0) {
    throw "Template render step failed for: $resolvedArticleDir"
}

$qualityScriptPath = Join-Path $workflowRoot 'scripts\run-quality-gates.py'
if (-not (Test-Path -LiteralPath $qualityScriptPath)) {
    throw "Quality gate script not found: $qualityScriptPath"
}

& python $qualityScriptPath --article-dir $resolvedArticleDir
if ($LASTEXITCODE -ne 0) {
    throw "Quality gate step failed for: $resolvedArticleDir"
}
