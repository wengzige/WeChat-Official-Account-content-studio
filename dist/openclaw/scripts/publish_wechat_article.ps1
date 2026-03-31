param(
    [Parameter(Mandatory = $true)]
    [string]$ArticleDir,
    [switch]$AllowNativeLists
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

$scriptPath = Join-Path $workflowRoot 'scripts\publish-article.ps1'
if (-not (Test-Path -LiteralPath $scriptPath)) {
    throw "Template publish script not found: $scriptPath"
}

& $scriptPath -ArticleDir $resolvedArticleDir -AllowNativeLists:$AllowNativeLists
