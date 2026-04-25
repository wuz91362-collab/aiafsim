param(
    [string]$Python = "python",
    [string]$Wheelhouse = "wheelhouse"
)

$ErrorActionPreference = "Stop"

if (!(Test-Path $Wheelhouse)) {
    New-Item -ItemType Directory -Path $Wheelhouse | Out-Null
}

Write-Host "Downloading python wheels into $Wheelhouse ..."
& $Python -m pip download -r requirements.txt -d $Wheelhouse

Write-Host "Offline wheel bundle is ready."
