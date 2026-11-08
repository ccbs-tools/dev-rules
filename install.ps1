# Create two directory junctions in the parent folder (the Cursor workspace root):
#   <root>\.cursor\rules  -> dev-rules\cursor\rules
#   <root>\.cursor\skills -> dev-rules\cursor\skills
# Junctions do not need admin rights. Usage:  cd dev-rules; .\install.ps1
# (ASCII only: Windows PowerShell 5.1 reads BOM-less UTF-8 scripts as ANSI.)

$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $here
$cursorDir = Join-Path $root ".cursor"
New-Item -ItemType Directory -Path $cursorDir -Force | Out-Null

foreach ($name in "rules", "skills") {
    $link = Join-Path $cursorDir $name
    $target = Join-Path $here "cursor\$name"
    if (Test-Path $link) {
        $item = Get-Item $link -Force
        if ($item.LinkType -eq "Junction" -and $item.Target -eq $target) {
            Write-Host "ok      $link -> $target"
            continue
        }
        Write-Warning "$link exists and is not a junction to $target; skipped. Resolve manually and rerun."
        continue
    }
    New-Item -ItemType Junction -Path $link -Target $target | Out-Null
    Write-Host "created $link -> $target"
}
