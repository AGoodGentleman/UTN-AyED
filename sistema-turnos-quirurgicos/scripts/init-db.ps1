param(
    [string]$User = $env:DB_USER,
    [string]$Password = $env:DB_PASSWORD,
    [string]$MysqlExe = $env:MYSQL_EXE,
    [switch]$NoPassword
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Schema = Join-Path $ProjectRoot "database\schema.sql"

if (-not $User) {
    $User = "root"
}

if (-not $MysqlExe) {
    $Candidates = @(
        (Get-Command mysql -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty Source),
        "C:\Program Files\MySQL\MySQL Workbench 8.0 CE\mysql.exe",
        "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe",
        "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.exe"
    ) | Where-Object { $_ -and (Test-Path $_) }

    $MysqlExe = $Candidates | Select-Object -First 1
}

if (-not $MysqlExe -or -not (Test-Path $MysqlExe)) {
    throw "No se encontro mysql.exe. Abri MySQL Workbench y ejecuta manualmente database\schema.sql, o configura MYSQL_EXE."
}

if (-not (Test-Path $Schema)) {
    throw "No se encontro el schema SQL: $Schema"
}

if (-not $NoPassword -and -not $PSBoundParameters.ContainsKey("Password") -and -not $env:DB_PASSWORD) {
    $Password = Read-Host "Password de MySQL para $User (Enter si no tiene)"
}

$MysqlArgs = @("-u", $User)
if (-not $NoPassword -and $Password) {
    $MysqlArgs += "-p$Password"
}
$MysqlArgs += "--default-character-set=utf8mb4"

Write-Host "Cargando base con: $MysqlExe"
Get-Content -Raw -Encoding UTF8 $Schema | & $MysqlExe @MysqlArgs
if ($LASTEXITCODE -ne 0) {
    throw "MySQL devolvio un error al cargar schema.sql. Revisa el mensaje anterior."
}
Write-Host "Base turnos_quirurgicos creada/actualizada correctamente."

if ($NoPassword) {
    & (Join-Path $PSScriptRoot "verify-db.ps1") -User $User -MysqlExe $MysqlExe -NoPassword
} else {
    & (Join-Path $PSScriptRoot "verify-db.ps1") -User $User -Password $Password -MysqlExe $MysqlExe
}
