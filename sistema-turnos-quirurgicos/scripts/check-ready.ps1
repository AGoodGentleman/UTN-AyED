$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Workbench = "C:\Program Files\MySQL\MySQL Workbench 8.0 CE\MySQLWorkbench.exe"
$MysqlExe = "C:\Program Files\MySQL\MySQL Workbench 8.0 CE\mysql.exe"
$Connector = Get-ChildItem -Path (Join-Path $ProjectRoot "lib") -Filter "mysql-connector-j-*.jar" -ErrorAction SilentlyContinue |
    Sort-Object Name -Descending |
    Select-Object -First 1 -ExpandProperty FullName

Write-Host "Java:" ((Get-Command java -ErrorAction SilentlyContinue).Source)
Write-Host "Javac:" ((Get-Command javac -ErrorAction SilentlyContinue).Source)
Write-Host "Workbench:" ($(if (Test-Path $Workbench) { $Workbench } else { "No encontrado" }))
Write-Host "mysql.exe:" ($(if (Test-Path $MysqlExe) { $MysqlExe } else { "No encontrado" }))
Write-Host "Connector/J:" ($(if ($Connector) { $Connector } else { "No encontrado" }))
Write-Host "Schema:" (Join-Path $ProjectRoot "database\schema.sql")
