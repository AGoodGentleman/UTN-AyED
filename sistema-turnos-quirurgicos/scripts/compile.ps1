$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Src = Join-Path $ProjectRoot "src"
$Out = Join-Path $ProjectRoot "out\classes"

if (Test-Path $Out) {
    Remove-Item -Recurse -Force $Out
}
New-Item -ItemType Directory -Force -Path $Out | Out-Null

$Sources = Get-ChildItem -Path $Src -Recurse -Filter "*.java" | ForEach-Object { $_.FullName }
if (-not $Sources) {
    throw "No se encontraron archivos .java en $Src"
}

javac -encoding UTF-8 -d $Out $Sources
Write-Host "Compilacion OK: $Out"
