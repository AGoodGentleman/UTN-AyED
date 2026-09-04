param(
    [string]$User = $env:DB_USER,
    [string]$Password = $env:DB_PASSWORD,
    [string]$MysqlExe = $env:MYSQL_EXE,
    [switch]$NoPassword
)

$ErrorActionPreference = "Stop"

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
    throw "No se encontro mysql.exe. Configura MYSQL_EXE o instala MySQL Server/Workbench."
}

if (-not $NoPassword -and -not $PSBoundParameters.ContainsKey("Password") -and -not $env:DB_PASSWORD) {
    $Password = Read-Host "Password de MySQL para $User (Enter si no tiene)"
}

$MysqlArgs = @("-u", $User, "--default-character-set=utf8mb4")
if (-not $NoPassword -and $Password) {
    $MysqlArgs += "-p$Password"
}

$Query = @"
SELECT 'especialidad' AS tabla, COUNT(*) AS registros FROM turnos_quirurgicos.especialidad
UNION ALL SELECT 'paciente', COUNT(*) FROM turnos_quirurgicos.paciente
UNION ALL SELECT 'profesional', COUNT(*) FROM turnos_quirurgicos.profesional
UNION ALL SELECT 'quirofano', COUNT(*) FROM turnos_quirurgicos.quirofano
UNION ALL SELECT 'tipo_cirugia', COUNT(*) FROM turnos_quirurgicos.tipo_cirugia
UNION ALL SELECT 'turno_quirurgico', COUNT(*) FROM turnos_quirurgicos.turno_quirurgico
UNION ALL SELECT 'turno_profesional', COUNT(*) FROM turnos_quirurgicos.turno_profesional;
"@

& $MysqlExe @MysqlArgs "--execute=$Query"
if ($LASTEXITCODE -ne 0) {
    throw "No se pudo verificar la base turnos_quirurgicos. Revisa usuario, password y si el schema se cargo."
}
