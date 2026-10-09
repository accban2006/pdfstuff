$ErrorActionPreference = 'Stop'
$projectRoot = $PSScriptRoot
$destinationRoot = Join-Path $projectRoot '.agents\skills'
$sourceRoots = @(
    'C:\Users\nahsu\.codex\skills',
    'C:\Users\nahsu\.agents\skills',
    'C:\Users\nahsu\.codex\plugins\cache'
)
$skillPaths = @($sourceRoots | ForEach-Object { rg --files --hidden -g SKILL.md $_ })
if ($LASTEXITCODE -ne 0 -or $skillPaths.Count -eq 0) { throw 'Skill discovery failed.' }
$usedNames = @{}
$plan = @($skillPaths | Sort-Object | ForEach-Object {
    $source = Split-Path -Parent $_
    $name = Split-Path -Leaf $source
    $folder = $name
    if ($usedNames.ContainsKey($folder)) {
        $prefix = if ($source -match '\\plugins\\cache\\[^\\]+\\([^\\]+)\\') { $Matches[1] }
                  elseif ($source -match '\\\.system\\') { 'codex-system' }
                  else { 'codex-personal' }
        $folder = "$prefix--$name"
    }
    if ($usedNames.ContainsKey($folder)) { throw "Duplicate destination: $folder" }
    $usedNames[$folder] = $true
    $destination = Join-Path $destinationRoot $folder
    if (Test-Path -LiteralPath $destination) { throw "Destination already exists: $destination" }
    [pscustomobject]@{ Folder = $folder; Source = $source; Destination = $destination }
})
New-Item -ItemType Directory -Path $destinationRoot -Force | Out-Null
$verifiedFiles = 0
foreach ($entry in $plan) {
    Copy-Item -LiteralPath $entry.Source -Destination $entry.Destination -Recurse -Force
    foreach ($sourceFile in Get-ChildItem -LiteralPath $entry.Source -File -Recurse -Force) {
        $relative = $sourceFile.FullName.Substring($entry.Source.Length + 1)
        $copiedFile = Join-Path $entry.Destination $relative
        if (!(Test-Path -LiteralPath $copiedFile)) { throw "Missing copied file: $copiedFile" }
        if ((Get-FileHash -LiteralPath $sourceFile.FullName -Algorithm SHA256).Hash -ne
            (Get-FileHash -LiteralPath $copiedFile -Algorithm SHA256).Hash) {
            throw "Copy verification failed: $copiedFile"
        }
        $verifiedFiles++
    }
}
$manifest = [ordered]@{
    ImportedAt = (Get-Date).ToString('o')
    SkillCount = $plan.Count
    VerifiedFiles = $verifiedFiles
    Skills = @($plan | Select-Object Folder, Source)
}
$manifest | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $projectRoot 'codex-skills-manifest.json') -Encoding UTF8
Write-Output "Imported $($plan.Count) skills; verified $verifiedFiles files with SHA256."
