param(
    [string]$ProjectRoot = (Split-Path -Parent $PSScriptRoot),
    [string]$ArticleDir,
    [switch]$Fix
)

$ErrorActionPreference = 'Stop'

function Write-Utf8NoBom {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,
        [Parameter(Mandatory = $true)]
        [string]$Content
    )

    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Content, $utf8NoBom)
}

function Render-Template {
    param(
        [Parameter(Mandatory = $true)]
        [string]$TemplatePath,
        [Parameter(Mandatory = $true)]
        [hashtable]$Tokens
    )

    $content = Get-Content -LiteralPath $TemplatePath -Raw -Encoding UTF8
    foreach ($key in $Tokens.Keys) {
        $content = $content.Replace($key, $Tokens[$key])
    }

    return $content
}

function Test-SuspiciousQuestionRuns {
    param(
        [AllowEmptyString()]
        [string]$Text
    )

    if ([string]::IsNullOrEmpty($Text)) {
        return $false
    }

    return [regex]::IsMatch($Text, '\?{3,}')
}

function Test-SuspiciousMojibakeText {
    param(
        [AllowEmptyString()]
        [string]$Text
    )

    if ([string]::IsNullOrEmpty($Text)) {
        return $false
    }

    $consecutive = 0
    $total = 0
    foreach ($char in $Text.ToCharArray()) {
        $codepoint = [int][char]$char
        if ($codepoint -ge 0x0080 -and $codepoint -le 0x00FF) {
            $consecutive++
            $total++
            if ($consecutive -ge 3 -or $total -ge 6) {
                return $true
            }
        }
        else {
            $consecutive = 0
        }
    }

    return $false
}

$resolvedRoot = (Resolve-Path -LiteralPath $ProjectRoot).Path
$templatePromptPath = Join-Path $resolvedRoot 'templates\image-prompts.md.template'
$skipNames = @('.agents', '.config', '.local', 'scripts', 'templates')

if (-not (Test-Path -LiteralPath $templatePromptPath)) {
    throw "Prompt template not found: $templatePromptPath"
}

$articleTargets = @()
if ($ArticleDir) {
    if (-not (Test-Path -LiteralPath $ArticleDir)) {
        throw "Article folder not found: $ArticleDir"
    }
    $articleTargets += Get-Item -LiteralPath $ArticleDir
}
else {
    $articleTargets += Get-ChildItem -LiteralPath $resolvedRoot -Directory | Where-Object {
        $skipNames -notcontains $_.Name -and $_.Name -ne 'article_work'
    }
}

$results = New-Object System.Collections.Generic.List[object]

foreach ($article in $articleTargets) {
    $articleRoot = $article.FullName
    $generatedDir = Join-Path $articleRoot 'generated'
    $metadataPath = Join-Path $articleRoot 'draft-metadata.json'
    $articlePath = Join-Path $articleRoot 'article.md'
    $htmlPath = Join-Path $articleRoot 'article-body.template.html'
    $promptPath = Join-Path $generatedDir 'image-prompts.md'
    $bodyVisualPath = Join-Path $articleRoot 'assets\body-visual.png'

    $item = [ordered]@{
        article = $article.Name
        article_dir = $articleRoot
        fixes = New-Object System.Collections.Generic.List[string]
        warnings = New-Object System.Collections.Generic.List[string]
        errors = New-Object System.Collections.Generic.List[string]
        has_native_list = $false
        uses_legacy_body_image = $false
        has_prompt_file = $false
    }

    if (-not (Test-Path -LiteralPath $generatedDir)) {
        if ($Fix) {
            New-Item -ItemType Directory -Force -Path $generatedDir | Out-Null
            $item.fixes.Add('Created missing generated directory.')
        }
        else {
            $item.warnings.Add('generated directory is missing.')
        }
    }

    $metadata = $null
    if (-not (Test-Path -LiteralPath $metadataPath)) {
        $item.errors.Add('draft-metadata.json is missing.')
    }
    else {
        try {
            $metadata = Get-Content -LiteralPath $metadataPath -Raw -Encoding UTF8 | ConvertFrom-Json
        }
        catch {
            $item.errors.Add("draft-metadata.json is not valid UTF-8 JSON: $($_.Exception.Message)")
        }
    }

    if (Test-Path -LiteralPath $articlePath) {
        $articleMarkdown = Get-Content -LiteralPath $articlePath -Raw -Encoding UTF8
        if (Test-SuspiciousQuestionRuns -Text $articleMarkdown) {
            $item.errors.Add('Suspicious question-mark runs found in article.md. This usually means garbled text.')
        }
        if (Test-SuspiciousMojibakeText -Text $articleMarkdown) {
            $item.errors.Add('Suspicious mojibake text found in article.md. This usually means broken encoding.')
        }
    }

    if (-not (Test-Path -LiteralPath $htmlPath)) {
        $item.errors.Add('article-body.template.html is missing.')
    }
    else {
        $html = Get-Content -LiteralPath $htmlPath -Raw -Encoding UTF8
        if (Test-SuspiciousQuestionRuns -Text $html) {
            $item.errors.Add('Suspicious question-mark runs found in article-body.template.html. This usually means garbled text.')
        }
        if (Test-SuspiciousMojibakeText -Text $html) {
            $item.errors.Add('Suspicious mojibake text found in article-body.template.html. This usually means broken encoding.')
        }
        if ([regex]::IsMatch($html, '<\s*(ul|ol|li)\b', 'IgnoreCase')) {
            $item.has_native_list = $true
            $item.warnings.Add('Native list tags found in article-body.template.html.')
        }
        if ($html -match '\{\{BODY_IMAGE_URL\}\}') {
            $item.uses_legacy_body_image = $true
            if ($Fix -and (Test-Path -LiteralPath $bodyVisualPath)) {
                $html = $html.Replace('{{BODY_IMAGE_URL}}', '{{IMAGE:assets/body-visual.png}}')
                Write-Utf8NoBom -Path $htmlPath -Content $html
                $item.uses_legacy_body_image = $false
                $item.fixes.Add('Migrated legacy {{BODY_IMAGE_URL}} placeholder to {{IMAGE:assets/body-visual.png}}.')
            }
            else {
                $item.warnings.Add('Legacy {{BODY_IMAGE_URL}} placeholder detected.')
            }
        }
    }

    $item.has_prompt_file = Test-Path -LiteralPath $promptPath
    if (-not $item.has_prompt_file) {
        if ($Fix -and $metadata) {
            $tokens = @{
                '__TITLE__' = [string]$metadata.title
                '__AUTHOR__' = [string]$metadata.author
                '__SOURCE_URL__' = [string]$metadata.content_source_url
            }
            $promptContent = Render-Template -TemplatePath $templatePromptPath -Tokens $tokens
            Write-Utf8NoBom -Path $promptPath -Content $promptContent
            $item.has_prompt_file = $true
            $item.fixes.Add('Created generated/image-prompts.md from template.')
        }
        else {
            $item.warnings.Add('generated/image-prompts.md is missing.')
        }
    }

    $results.Add([pscustomobject]$item)
}

$articleWorkPath = Join-Path $resolvedRoot 'article_work'
$cleanup = [ordered]@{
    article_work_found = $false
    article_work_removed = $false
}
if (Test-Path -LiteralPath $articleWorkPath) {
    $cleanup.article_work_found = $true
    $item = Get-Item -LiteralPath $articleWorkPath
    if ($Fix -and $item.Attributes.ToString().Contains('ReparsePoint')) {
        Push-Location $resolvedRoot
        try {
            & cmd /c rmdir article_work | Out-Null
        }
        finally {
            Pop-Location
        }
        $cleanup.article_work_removed = -not (Test-Path -LiteralPath $articleWorkPath)
    }
}

[ordered]@{
    project_root = $resolvedRoot
    fix_mode = [bool]$Fix
    cleanup = $cleanup
    articles = $results
} | ConvertTo-Json -Depth 8