# Sistema de Gestion de Turnos Quirurgicos

Proyecto Java + MySQL para el trabajo especial de Paradigmas de Programacion.

## Que incluye

- Modelo OOP con herencia: `Persona`, `Paciente`, `Profesional`.
- Interfaces: `Validable` y `CrudDAO<T>`.
- Enumeraciones: `EstadoTurno`, `EstadoQuirofano`, `RolProfesional`.
- DAO JDBC para pacientes, especialidades, profesionales, quirofanos, tipos de cirugia y turnos.
- Servicio de negocio para programar, reprogramar, cancelar y consultar turnos.
- Validaciones de superposicion de paciente, quirofano y profesionales.
- Validacion de exactamente un `CIRUJANO_PRINCIPAL` por turno.
- Script MySQL con tablas, claves, restricciones, indices y datos de prueba.
- Consola interactiva simple para cargar datos y operar el sistema.

## Crear la base de datos

Opcion recomendada desde PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\sistema-turnos-quirurgicos\scripts\init-db.ps1
```

El script busca automaticamente `mysql.exe` dentro de MySQL Workbench. Si tu usuario no es `root`, podes ejecutar:

```powershell
powershell -ExecutionPolicy Bypass -File .\sistema-turnos-quirurgicos\scripts\init-db.ps1 -User tu_usuario
```

Tambien podes hacerlo manualmente en MySQL Workbench:

```sql
SOURCE C:/Users/lvbla/OneDrive/Escritorio/Universidad - 1er Año/Trabajos/UTN-AyED/sistema-turnos-quirurgicos/database/schema.sql;
```

Tambien podes cargarlo desde PowerShell con:

```powershell
mysql -u root -p < .\sistema-turnos-quirurgicos\database\schema.sql
```

O copiar el contenido de `database/schema.sql` y ejecutarlo desde MySQL Workbench.

## Compilar

```powershell
powershell -ExecutionPolicy Bypass -File .\sistema-turnos-quirurgicos\scripts\compile.ps1
```

## Ejecutar

El proyecto ya busca MySQL Connector/J en la carpeta `lib`. Si alguna vez falta, ejecuta:

```powershell
powershell -ExecutionPolicy Bypass -File .\sistema-turnos-quirurgicos\scripts\download-connector.ps1
```

Para ejecutar el programa:

```powershell
$env:DB_USER="root"
$env:DB_PASSWORD="tu_password"
powershell -ExecutionPolicy Bypass -File .\sistema-turnos-quirurgicos\scripts\run.ps1
```

Si tu MySQL no tiene password, podes omitir `DB_PASSWORD`.

Para cargar o verificar la base con un usuario sin password:

```powershell
powershell -ExecutionPolicy Bypass -File .\sistema-turnos-quirurgicos\scripts\init-db.ps1 -NoPassword
powershell -ExecutionPolicy Bypass -File .\sistema-turnos-quirurgicos\scripts\verify-db.ps1 -NoPassword
```

Variables opcionales:

- `DB_URL`: por defecto `jdbc:mysql://localhost:3306/turnos_quirurgicos?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=America/Argentina/Buenos_Aires`
- `DB_USER`: por defecto `root`
- `DB_PASSWORD`: por defecto vacio
- `MYSQL_JDBC_JAR`: ruta manual al `.jar` de MySQL Connector/J, solo si no queres usar el de `lib`
- `MYSQL_EXE`: ruta manual a `mysql.exe`, solo si `init-db.ps1` no lo encuentra

## Notas de diseno

La disponibilidad del quirofano no se guarda como estado fijo. El estado `HABILITADO` indica que puede usarse si no hay superposicion horaria. Las superposiciones se calculan contra turnos activos.

La tabla `turno_profesional` usa clave primaria compuesta por `id_turno` e `id_profesional`. El rol es atributo. La regla de exactamente un `CIRUJANO_PRINCIPAL` por turno esta implementada en `TurnoService`.
