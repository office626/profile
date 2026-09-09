param([Parameter(Mandatory=$true)][string]$Config)
$ErrorActionPreference='Stop'
$siteRoot = Split-Path $PSScriptRoot -Parent
Set-Location -LiteralPath $siteRoot
$settings = Get-Content -LiteralPath $Config -Raw | ConvertFrom-Json
$repoRoot = (& git rev-parse --show-toplevel).Trim()
if ($LASTEXITCODE -ne 0) { throw 'Repository is not initialized' }
$remote = (& git remote get-url origin).Trim()
if ($remote -notmatch '^https://github.com/office626/profile(?:\.git)?$') { throw 'Unexpected GitHub destination' }
$branch = (& git branch --show-current).Trim()
if ($branch -ne $settings.publishBranch) { throw 'Unexpected publication branch' }
if (& git status --porcelain) { throw 'Working tree has changes; review before automatic update' }
& git pull --ff-only origin $branch
if ($LASTEXITCODE -ne 0) { throw 'Update could not be applied safely' }
& node scripts/collect.mjs $Config
if ($LASTEXITCODE -ne 0) { throw 'Collection failed' }
& node scripts/publish-content.mjs $Config
if ($LASTEXITCODE -ne 0) { throw 'Approval validation failed; nothing was uploaded' }
& node --test scripts/collection.test.mjs
if ($LASTEXITCODE -ne 0) { throw 'Validation failed' }
& git add -- content/collected-cases.json content/activities.json public/files
& git diff --cached --quiet
if ($LASTEXITCODE -eq 0) { Write-Output 'No published changes'; exit 0 }
& git -c user.name='office626 portfolio updater' -c user.email='office626@users.noreply.github.com' commit -m 'Update reviewed portfolio content'
if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }
& git push origin $branch
if ($LASTEXITCODE -ne 0) { throw 'GitHub update failed; local commit retained' }
