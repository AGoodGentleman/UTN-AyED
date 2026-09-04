$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Lib = Join-Path $ProjectRoot "lib"
$Version = "9.7.0"
$Jar = Join-Path $Lib "mysql-connector-j-$Version.jar"
$Url = "https://repo1.maven.org/maven2/com/mysql/mysql-connector-j/$Version/mysql-connector-j-$Version.jar"

New-Item -ItemType Directory -Force -Path $Lib | Out-Null

if (Test-Path $Jar) {
    Write-Host "MySQL Connector/J ya existe: $Jar"
    exit 0
}

Invoke-WebRequest -Uri $Url -OutFile $Jar
Write-Host "MySQL Connector/J descargado: $Jar"
