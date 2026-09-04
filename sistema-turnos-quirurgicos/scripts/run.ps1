$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Out = Join-Path $ProjectRoot "out\classes"
$Lib = Join-Path $ProjectRoot "lib"

if (-not (Test-Path $Out)) {
    & (Join-Path $PSScriptRoot "compile.ps1")
}

$ConnectorJar = $env:MYSQL_JDBC_JAR
if ($ConnectorJar -and -not (Test-Path $ConnectorJar)) {
    throw "No existe el jar indicado en MYSQL_JDBC_JAR: $ConnectorJar"
}

if (-not $ConnectorJar) {
    $ConnectorJar = Get-ChildItem -Path $Lib -Filter "mysql-connector-j-*.jar" -ErrorAction SilentlyContinue |
        Sort-Object Name -Descending |
        Select-Object -First 1 -ExpandProperty FullName
}

if (-not $ConnectorJar) {
    throw "No se encontro MySQL Connector/J. Ejecuta scripts\download-connector.ps1 o defini MYSQL_JDBC_JAR."
}

$Classpath = "$Out;$ConnectorJar"
java -cp $Classpath ar.edu.utn.turnosquirurgicos.App
