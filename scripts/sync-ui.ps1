# Sync shared UI files from cursor-sites-shared into consuming projects.

$ErrorActionPreference = 'Stop'
$sharedRoot = Split-Path -Parent $PSScriptRoot
$uiSource = Join-Path $sharedRoot 'ui'
$sitesRoot = Split-Path -Parent $sharedRoot

# Copy a text file as UTF-8 without a BOM. Refuses UTF-16 or other non-UTF-8 sources,
# because GitHub Pages serves everything as UTF-8 and a UTF-16 .js file fails to parse.
function Copy-Utf8File {
    param([string]$Source, [string]$Dest)
    $bytes = [IO.File]::ReadAllBytes($Source)
    if ($bytes -contains 0) {
        throw "Refusing to sync ${Source}: it contains NUL bytes (probably UTF-16). Convert it to UTF-8 first."
    }
    $start = 0
    if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) { $start = 3 }
    $strict = New-Object Text.UTF8Encoding($false, $true)
    try {
        $text = $strict.GetString($bytes, $start, $bytes.Length - $start)
    } catch {
        throw "Refusing to sync ${Source}: it is not valid UTF-8."
    }
    [IO.File]::WriteAllText($Dest, $text, (New-Object Text.UTF8Encoding $false))
}

function Sync-Pair {
    param(
        [string]$ProjectName,
        [string]$JsName,
        [string]$CssName
    )
    $project = Join-Path $sitesRoot $ProjectName
    if (-not (Test-Path $project)) {
        Write-Warning "Skipping missing project: $ProjectName"
        return
    }
    $jsDest = Join-Path $project "assets\js\utils\$JsName"
    $cssDest = Join-Path $project "assets\css\$CssName"
    $jsDir = Split-Path -Parent $jsDest
    $cssDir = Split-Path -Parent $cssDest
    if (-not (Test-Path $jsDir)) { New-Item -ItemType Directory -Path $jsDir -Force | Out-Null }
    if (-not (Test-Path $cssDir)) { New-Item -ItemType Directory -Path $cssDir -Force | Out-Null }
    Copy-Utf8File (Join-Path $uiSource $JsName) $jsDest
    Copy-Utf8File (Join-Path $uiSource $CssName) $cssDest
    Write-Host "Synced $JsName -> $ProjectName"
}

# Brief message
$briefTargets = @(
    'theGolfApp', 'BGS', 'Splitify', 'theConfessional', 'Edison', 'FamilyTree',
    'Scrabble', 'ierne-snooker', 'PubliiCrossguns', 'ierne-tennis'
)
foreach ($name in $briefTargets) {
    Sync-Pair -ProjectName $name -JsName 'brief-message.js' -CssName 'brief-message.css'
}

# Confirm dialog — BGS only for now (FamilyTree still uses sheet-based ConfirmDialog.show(title, message, label, onYes))
$confirmTargets = @('BGS', 'ierne-tennis')
foreach ($name in $confirmTargets) {
    Sync-Pair -ProjectName $name -JsName 'confirm-dialog.js' -CssName 'confirm-dialog.css'
}

# Working indicator — Splitify (keeps SplitifyWorking alias in shared JS)
$workingTargets = @('Splitify', 'ierne-tennis', 'Edison')
foreach ($name in $workingTargets) {
    Sync-Pair -ProjectName $name -JsName 'working-indicator.js' -CssName 'working-indicator.css'
}

Write-Host 'Done.'
