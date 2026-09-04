package ar.edu.utn.turnosquirurgicos.service;

import ar.edu.utn.turnosquirurgicos.config.DatabaseConnection;
import ar.edu.utn.turnosquirurgicos.model.Especialidad;
import ar.edu.utn.turnosquirurgicos.model.EstadoQuirofano;
import ar.edu.utn.turnosquirurgicos.model.EstadoTurno;
import ar.edu.utn.turnosquirurgicos.model.Paciente;
import ar.edu.utn.turnosquirurgicos.model.Profesional;
import ar.edu.utn.turnosquirurgicos.model.Quirofano;
import ar.edu.utn.turnosquirurgicos.model.RolProfesional;
import ar.edu.utn.turnosquirurgicos.model.TipoCirugia;
import ar.edu.utn.turnosquirurgicos.model.TurnoQuirurgico;
import java.sql.Connection;
import java.sql.Date;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.Timestamp;
import java.sql.Types;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

public class TurnoService {
    private static final int MARGEN_PRE_OPERATORIO_MINUTOS = 30;
    private static final int MARGEN_POST_OPERATORIO_MINUTOS = 30;

    private final DatabaseConnection database;

    public TurnoService(DatabaseConnection database) {
        this.database = database;
    }

    public TurnoQuirurgico programarTurno(
            int idPaciente,
            int idTipoCirugia,
            int idQuirofano,
            LocalDateTime inicio,
            List<AsignacionProfesionalRequest> asignaciones,
            String observaciones
    ) {
        validarInicioFuturo(inicio);

        return ejecutarEnTransaccion(connection -> {
            Paciente paciente = buscarPaciente(connection, idPaciente, true);
            TipoCirugia tipoCirugia = buscarTipoCirugia(connection, idTipoCirugia, true);
            Quirofano quirofano = buscarQuirofano(connection, idQuirofano, true);
            Map<Integer, Profesional> profesionales = validarAsignaciones(connection, tipoCirugia, asignaciones, true);

            LocalDateTime fin = tipoCirugia.calcularHoraFin(inicio);
            List<Integer> idsProfesionales = asignaciones.stream()
                    .map(AsignacionProfesionalRequest::getIdProfesional)
                    .toList();
            validarDisponibilidad(
                    connection,
                    paciente.getId(),
                    quirofano.getId(),
                    idsProfesionales,
                    inicio,
                    fin,
                    MARGEN_PRE_OPERATORIO_MINUTOS,
                    MARGEN_POST_OPERATORIO_MINUTOS,
                    null
            );

            TurnoQuirurgico turno = armarTurno(
                    paciente,
                    tipoCirugia,
                    quirofano,
                    inicio,
                    fin,
                    EstadoTurno.PROGRAMADO,
                    observaciones,
                    null,
                    asignaciones,
                    profesionales
            );
            int idTurno = insertarTurno(connection, turno);
            turno.setId(idTurno);
            insertarParticipaciones(connection, idTurno, asignaciones);
            return turno;
        });
    }

    public TurnoQuirurgico reprogramarTurno(int idTurno, LocalDateTime nuevoInicio, int idQuirofano) {
        return reprogramarTurno(idTurno, nuevoInicio, idQuirofano, null);
    }

    public TurnoQuirurgico reprogramarTurno(
            int idTurno,
            LocalDateTime nuevoInicio,
            int idQuirofano,
            List<AsignacionProfesionalRequest> nuevasAsignaciones
    ) {
        validarInicioFuturo(nuevoInicio);

        return ejecutarEnTransaccion(connection -> {
            TurnoQuirurgico turnoActual = buscarTurnoCompleto(connection, idTurno);
            validarTurnoReprogramable(turnoActual);
            validarDatosBaseActivos(turnoActual);

            Quirofano nuevoQuirofano = buscarQuirofano(connection, idQuirofano, true);
            List<AsignacionProfesionalRequest> asignacionesFinales = nuevasAsignaciones == null || nuevasAsignaciones.isEmpty()
                    ? copiarAsignaciones(turnoActual)
                    : nuevasAsignaciones;
            Map<Integer, Profesional> profesionales = validarAsignaciones(
                    connection,
                    turnoActual.getTipoCirugia(),
                    asignacionesFinales,
                    true
            );

            LocalDateTime nuevoFin = turnoActual.getTipoCirugia().calcularHoraFin(nuevoInicio);
            List<Integer> idsProfesionales = asignacionesFinales.stream()
                    .map(AsignacionProfesionalRequest::getIdProfesional)
                    .toList();
            validarDisponibilidad(
                    connection,
                    turnoActual.getPaciente().getId(),
                    nuevoQuirofano.getId(),
                    idsProfesionales,
                    nuevoInicio,
                    nuevoFin,
                    turnoActual.getMargenPreOperatorioMinutos(),
                    turnoActual.getMargenPostOperatorioMinutos(),
                    idTurno
            );

            actualizarReprogramacion(connection, idTurno, nuevoInicio, nuevoFin, nuevoQuirofano.getId());
            if (nuevasAsignaciones != null && !nuevasAsignaciones.isEmpty()) {
                reemplazarParticipaciones(connection, idTurno, asignacionesFinales);
            }

            TurnoQuirurgico turnoReprogramado = armarTurno(
                    turnoActual.getPaciente(),
                    turnoActual.getTipoCirugia(),
                    nuevoQuirofano,
                    nuevoInicio,
                    nuevoFin,
                    EstadoTurno.PROGRAMADO,
                    turnoActual.getObservaciones(),
                    null,
                    asignacionesFinales,
                    profesionales
            );
            turnoReprogramado.setId(idTurno);
            turnoReprogramado.setMargenPreOperatorioMinutos(turnoActual.getMargenPreOperatorioMinutos());
            turnoReprogramado.setMargenPostOperatorioMinutos(turnoActual.getMargenPostOperatorioMinutos());
            return turnoReprogramado;
        });
    }

    public void cancelarTurno(int idTurno, String motivo) {
        ejecutarEnTransaccion(connection -> {
            TurnoQuirurgico turno = buscarTurnoCompleto(connection, idTurno);
            if (turno.getEstado() == EstadoTurno.FINALIZADO) {
                throw new ServiceException("No se puede cancelar un turno finalizado.");
            }
            if (turno.getEstado() == EstadoTurno.CANCELADO) {
                throw new ServiceException("El turno ya esta cancelado.");
            }
            String motivoFinal = motivo == null || motivo.isBlank() ? "Cancelado por usuario" : motivo;
            try (PreparedStatement statement = connection.prepareStatement("""
                    UPDATE turno_quirurgico
                       SET estado = 'CANCELADO', motivo_cancelacion = ?
                     WHERE id_turno = ?
                    """)) {
                statement.setString(1, motivoFinal);
                statement.setInt(2, idTurno);
                statement.executeUpdate();
            }
            return null;
        });
    }

    public TurnoQuirurgico cambiarEstadoTurno(int idTurno, EstadoTurno nuevoEstado) {
        if (nuevoEstado == null) {
            throw new ServiceException("Debe indicar el nuevo estado.");
        }
        if (nuevoEstado == EstadoTurno.CANCELADO) {
            throw new ServiceException("Use la opcion de cancelacion para registrar el motivo.");
        }

        return ejecutarEnTransaccion(connection -> {
            TurnoQuirurgico turno = buscarTurnoCompleto(connection, idTurno);
            if (turno.getEstado() == EstadoTurno.CANCELADO) {
                throw new ServiceException("No se puede cambiar el estado de un turno cancelado.");
            }
            if (turno.getEstado() == EstadoTurno.FINALIZADO && nuevoEstado != EstadoTurno.FINALIZADO) {
                throw new ServiceException("No se puede reabrir un turno finalizado.");
            }
            try (PreparedStatement statement = connection.prepareStatement("""
                    UPDATE turno_quirurgico
                       SET estado = ?, motivo_cancelacion = NULL
                     WHERE id_turno = ?
                    """)) {
                statement.setString(1, nuevoEstado.name());
                statement.setInt(2, idTurno);
                statement.executeUpdate();
            }
            turno.setEstado(nuevoEstado);
            turno.setMotivoCancelacion(null);
            return turno;
        });
    }

    public boolean verificarDisponibilidad(
            int idPaciente,
            int idQuirofano,
            List<Integer> idsProfesionales,
            LocalDateTime inicio,
            LocalDateTime fin
    ) {
        if (inicio == null || fin == null || !fin.isAfter(inicio)) {
            throw new ServiceException("El intervalo indicado es invalido.");
        }

        try (Connection connection = database.open()) {
            return !existeSuperposicionPaciente(connection, idPaciente, inicio, fin, null)
                    && !existeSuperposicionQuirofano(
                    connection,
                    idQuirofano,
                    inicio,
                    fin,
                    MARGEN_PRE_OPERATORIO_MINUTOS,
                    MARGEN_POST_OPERATORIO_MINUTOS,
                    null
            )
                    && buscarProfesionalOcupado(connection, idsProfesionales, inicio, fin, null) == null;
        } catch (SQLException ex) {
            throw new ServiceException("No se pudo verificar la disponibilidad.", ex);
        }
    }

    private void validarDisponibilidad(
            Connection connection,
            int idPaciente,
            int idQuirofano,
            List<Integer> idsProfesionales,
            LocalDateTime inicio,
            LocalDateTime fin,
            int margenPre,
            int margenPost,
            Integer idTurnoExcluido
    ) throws SQLException {
        if (existeSuperposicionPaciente(connection, idPaciente, inicio, fin, idTurnoExcluido)) {
            throw new ServiceException("El paciente ya tiene un turno superpuesto.");
        }
        if (existeSuperposicionQuirofano(connection, idQuirofano, inicio, fin, margenPre, margenPost, idTurnoExcluido)) {
            throw new ServiceException("El quirofano no esta disponible en ese horario.");
        }
        Integer profesionalOcupado = buscarProfesionalOcupado(connection, idsProfesionales, inicio, fin, idTurnoExcluido);
        if (profesionalOcupado != null) {
            throw new ServiceException("El profesional #" + profesionalOcupado + " ya tiene un turno superpuesto.");
        }
    }

    private boolean existeSuperposicionPaciente(
            Connection connection,
            int idPaciente,
            LocalDateTime inicio,
            LocalDateTime fin,
            Integer idTurnoExcluido
    ) throws SQLException {
        String sql = """
                SELECT COUNT(*)
                  FROM turno_quirurgico
                 WHERE id_paciente = ?
                   AND estado IN ('PROGRAMADO', 'CONFIRMADO', 'EN_CURSO')
                   AND ? < fecha_hora_fin
                   AND ? > fecha_hora_inicio
                   AND (? IS NULL OR id_turno <> ?)
                """;
        try (PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setInt(1, idPaciente);
            statement.setTimestamp(2, Timestamp.valueOf(inicio));
            statement.setTimestamp(3, Timestamp.valueOf(fin));
            cargarIdExcluido(statement, 4, idTurnoExcluido);
            return existeResultado(statement);
        }
    }

    private boolean existeSuperposicionQuirofano(
            Connection connection,
            int idQuirofano,
            LocalDateTime inicio,
            LocalDateTime fin,
            int margenPre,
            int margenPost,
            Integer idTurnoExcluido
    ) throws SQLException {
        LocalDateTime inicioConMargen = inicio.minusMinutes(margenPre);
        LocalDateTime finConMargen = fin.plusMinutes(margenPost);
        String sql = """
                SELECT COUNT(*)
                  FROM turno_quirurgico
                 WHERE id_quirofano = ?
                   AND estado IN ('PROGRAMADO', 'CONFIRMADO', 'EN_CURSO')
                   AND ? < DATE_ADD(fecha_hora_fin, INTERVAL margen_post_operatorio_minutos MINUTE)
                   AND ? > DATE_SUB(fecha_hora_inicio, INTERVAL margen_pre_operatorio_minutos MINUTE)
                   AND (? IS NULL OR id_turno <> ?)
                """;
        try (PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setInt(1, idQuirofano);
            statement.setTimestamp(2, Timestamp.valueOf(inicioConMargen));
            statement.setTimestamp(3, Timestamp.valueOf(finConMargen));
            cargarIdExcluido(statement, 4, idTurnoExcluido);
            return existeResultado(statement);
        }
    }

    private Integer buscarProfesionalOcupado(
            Connection connection,
            List<Integer> idsProfesionales,
            LocalDateTime inicio,
            LocalDateTime fin,
            Integer idTurnoExcluido
    ) throws SQLException {
        if (idsProfesionales == null || idsProfesionales.isEmpty()) {
            return null;
        }

        String placeholders = idsProfesionales.stream()
                .map(id -> "?")
                .collect(Collectors.joining(", "));
        String sql = """
                SELECT tp.id_profesional
                  FROM turno_profesional tp
                  JOIN turno_quirurgico t ON t.id_turno = tp.id_turno
                 WHERE tp.id_profesional IN (%s)
                   AND t.estado IN ('PROGRAMADO', 'CONFIRMADO', 'EN_CURSO')
                   AND ? < t.fecha_hora_fin
                   AND ? > t.fecha_hora_inicio
                   AND (? IS NULL OR t.id_turno <> ?)
                 LIMIT 1
                """.formatted(placeholders);

        try (PreparedStatement statement = connection.prepareStatement(sql)) {
            int index = 1;
            for (Integer idProfesional : idsProfesionales) {
                statement.setInt(index++, idProfesional);
            }
            statement.setTimestamp(index++, Timestamp.valueOf(inicio));
            statement.setTimestamp(index++, Timestamp.valueOf(fin));
            cargarIdExcluido(statement, index, idTurnoExcluido);
            try (ResultSet resultSet = statement.executeQuery()) {
                if (resultSet.next()) {
                    return resultSet.getInt("id_profesional");
                }
            }
            return null;
        }
    }

    private Map<Integer, Profesional> validarAsignaciones(
            Connection connection,
            TipoCirugia tipoCirugia,
            List<AsignacionProfesionalRequest> asignaciones,
            boolean requiereActivo
    ) throws SQLException {
        if (asignaciones == null || asignaciones.isEmpty()) {
            throw new ServiceException("Debe asignar al menos un profesional al turno.");
        }

        Set<Integer> idsUnicos = new HashSet<>();
        int cantidadCirujanosPrincipales = 0;
        Profesional cirujanoPrincipal = null;
        Map<Integer, Profesional> profesionales = new HashMap<>();

        for (AsignacionProfesionalRequest asignacion : asignaciones) {
            if (asignacion == null || asignacion.getIdProfesional() <= 0 || asignacion.getRol() == null) {
                throw new ServiceException("Hay una asignacion profesional invalida.");
            }
            if (!idsUnicos.add(asignacion.getIdProfesional())) {
                throw new ServiceException("Un profesional no puede aparecer mas de una vez en el mismo turno.");
            }

            Profesional profesional = buscarProfesional(connection, asignacion.getIdProfesional(), requiereActivo);
            profesionales.put(profesional.getId(), profesional);
            if (asignacion.getRol() == RolProfesional.CIRUJANO_PRINCIPAL) {
                cantidadCirujanosPrincipales++;
                cirujanoPrincipal = profesional;
            }
        }

        if (cantidadCirujanosPrincipales != 1) {
            throw new ServiceException("Cada turno debe tener exactamente un profesional con rol CIRUJANO_PRINCIPAL.");
        }
        if (cirujanoPrincipal.getEspecialidad().getId() != tipoCirugia.getEspecialidad().getId()) {
            throw new ServiceException("El cirujano principal debe pertenecer a la especialidad del tipo de cirugia.");
        }
        return profesionales;
    }

    private TurnoQuirurgico armarTurno(
            Paciente paciente,
            TipoCirugia tipoCirugia,
            Quirofano quirofano,
            LocalDateTime inicio,
            LocalDateTime fin,
            EstadoTurno estado,
            String observaciones,
            String motivoCancelacion,
            List<AsignacionProfesionalRequest> asignaciones,
            Map<Integer, Profesional> profesionales
    ) {
        TurnoQuirurgico turno = new TurnoQuirurgico();
        turno.setPaciente(paciente);
        turno.setTipoCirugia(tipoCirugia);
        turno.setQuirofano(quirofano);
        turno.setFechaHoraInicio(inicio);
        turno.setFechaHoraFin(fin);
        turno.setMargenPreOperatorioMinutos(MARGEN_PRE_OPERATORIO_MINUTOS);
        turno.setMargenPostOperatorioMinutos(MARGEN_POST_OPERATORIO_MINUTOS);
        turno.setEstado(estado);
        turno.setObservaciones(observaciones);
        turno.setMotivoCancelacion(motivoCancelacion);
        for (AsignacionProfesionalRequest asignacion : asignaciones) {
            turno.agregarProfesional(profesionales.get(asignacion.getIdProfesional()), asignacion.getRol());
        }
        return turno;
    }

    private int insertarTurno(Connection connection, TurnoQuirurgico turno) throws SQLException {
        String sql = """
                INSERT INTO turno_quirurgico
                    (fecha_hora_inicio, fecha_hora_fin, margen_pre_operatorio_minutos,
                     margen_post_operatorio_minutos, estado, observaciones, motivo_cancelacion,
                     id_paciente, id_quirofano, id_tipo_cirugia)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """;
        try (PreparedStatement statement = connection.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            statement.setTimestamp(1, Timestamp.valueOf(turno.getFechaHoraInicio()));
            statement.setTimestamp(2, Timestamp.valueOf(turno.getFechaHoraFin()));
            statement.setInt(3, turno.getMargenPreOperatorioMinutos());
            statement.setInt(4, turno.getMargenPostOperatorioMinutos());
            statement.setString(5, turno.getEstado().name());
            statement.setString(6, turno.getObservaciones());
            statement.setString(7, turno.getMotivoCancelacion());
            statement.setInt(8, turno.getPaciente().getId());
            statement.setInt(9, turno.getQuirofano().getId());
            statement.setInt(10, turno.getTipoCirugia().getId());
            statement.executeUpdate();

            try (ResultSet keys = statement.getGeneratedKeys()) {
                if (keys.next()) {
                    return keys.getInt(1);
                }
            }
            throw new ServiceException("No se obtuvo el identificador del turno creado.");
        }
    }

    private void insertarParticipaciones(
            Connection connection,
            int idTurno,
            List<AsignacionProfesionalRequest> asignaciones
    ) throws SQLException {
        String sql = "INSERT INTO turno_profesional (id_turno, id_profesional, rol) VALUES (?, ?, ?)";
        try (PreparedStatement statement = connection.prepareStatement(sql)) {
            for (AsignacionProfesionalRequest asignacion : asignaciones) {
                statement.setInt(1, idTurno);
                statement.setInt(2, asignacion.getIdProfesional());
                statement.setString(3, asignacion.getRol().name());
                statement.addBatch();
            }
            statement.executeBatch();
        }
    }

    private void reemplazarParticipaciones(
            Connection connection,
            int idTurno,
            List<AsignacionProfesionalRequest> asignaciones
    ) throws SQLException {
        try (PreparedStatement delete = connection.prepareStatement(
                "DELETE FROM turno_profesional WHERE id_turno = ?")) {
            delete.setInt(1, idTurno);
            delete.executeUpdate();
        }
        insertarParticipaciones(connection, idTurno, asignaciones);
    }

    private void actualizarReprogramacion(
            Connection connection,
            int idTurno,
            LocalDateTime nuevoInicio,
            LocalDateTime nuevoFin,
            int idQuirofano
    ) throws SQLException {
        try (PreparedStatement statement = connection.prepareStatement("""
                UPDATE turno_quirurgico
                   SET fecha_hora_inicio = ?, fecha_hora_fin = ?,
                       id_quirofano = ?, estado = 'PROGRAMADO',
                       motivo_cancelacion = NULL
                 WHERE id_turno = ?
                """)) {
            statement.setTimestamp(1, Timestamp.valueOf(nuevoInicio));
            statement.setTimestamp(2, Timestamp.valueOf(nuevoFin));
            statement.setInt(3, idQuirofano);
            statement.setInt(4, idTurno);
            statement.executeUpdate();
        }
    }

    private List<AsignacionProfesionalRequest> copiarAsignaciones(TurnoQuirurgico turno) {
        return turno.getParticipaciones().stream()
                .map(participacion -> new AsignacionProfesionalRequest(
                        participacion.getProfesional().getId(),
                        participacion.getRol()
                ))
                .toList();
    }

    private void validarDatosBaseActivos(TurnoQuirurgico turno) {
        if (!turno.getPaciente().isActivo()) {
            throw new ServiceException("No se puede reprogramar: el paciente esta inactivo.");
        }
        if (!turno.getTipoCirugia().isActivo()) {
            throw new ServiceException("No se puede reprogramar: el tipo de cirugia esta inactivo.");
        }
        if (!turno.getTipoCirugia().getEspecialidad().isActivo()) {
            throw new ServiceException("No se puede reprogramar: la especialidad esta inactiva.");
        }
    }

    private void validarTurnoReprogramable(TurnoQuirurgico turno) {
        if (turno.getEstado() == EstadoTurno.CANCELADO) {
            throw new ServiceException("No se puede reprogramar un turno cancelado.");
        }
        if (turno.getEstado() == EstadoTurno.EN_CURSO || turno.getEstado() == EstadoTurno.FINALIZADO) {
            throw new ServiceException("No se puede reprogramar un turno en curso o finalizado.");
        }
    }

    private void validarInicioFuturo(LocalDateTime inicio) {
        if (inicio == null || !inicio.isAfter(LocalDateTime.now())) {
            throw new ServiceException("La fecha y hora de inicio debe ser futura.");
        }
    }

    private TurnoQuirurgico buscarTurnoCompleto(Connection connection, int idTurno) throws SQLException {
        String sql = "SELECT * FROM turno_quirurgico WHERE id_turno = ?";
        try (PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setInt(1, idTurno);
            try (ResultSet resultSet = statement.executeQuery()) {
                if (!resultSet.next()) {
                    throw new ServiceException("No existe el turno indicado.");
                }

                TurnoQuirurgico turno = new TurnoQuirurgico();
                turno.setId(resultSet.getInt("id_turno"));
                turno.setFechaHoraInicio(resultSet.getTimestamp("fecha_hora_inicio").toLocalDateTime());
                turno.setFechaHoraFin(resultSet.getTimestamp("fecha_hora_fin").toLocalDateTime());
                turno.setMargenPreOperatorioMinutos(resultSet.getInt("margen_pre_operatorio_minutos"));
                turno.setMargenPostOperatorioMinutos(resultSet.getInt("margen_post_operatorio_minutos"));
                turno.setEstado(EstadoTurno.valueOf(resultSet.getString("estado")));
                turno.setObservaciones(resultSet.getString("observaciones"));
                turno.setMotivoCancelacion(resultSet.getString("motivo_cancelacion"));
                turno.setPaciente(buscarPaciente(connection, resultSet.getInt("id_paciente"), false));
                turno.setQuirofano(buscarQuirofano(connection, resultSet.getInt("id_quirofano"), false));
                turno.setTipoCirugia(buscarTipoCirugia(connection, resultSet.getInt("id_tipo_cirugia"), false));
                cargarParticipacionesTurno(connection, turno);
                return turno;
            }
        }
    }

    private void cargarParticipacionesTurno(Connection connection, TurnoQuirurgico turno) throws SQLException {
        String sql = "SELECT id_profesional, rol FROM turno_profesional WHERE id_turno = ?";
        try (PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setInt(1, turno.getId());
            try (ResultSet resultSet = statement.executeQuery()) {
                while (resultSet.next()) {
                    Profesional profesional = buscarProfesional(connection, resultSet.getInt("id_profesional"), false);
                    turno.agregarProfesional(profesional, RolProfesional.valueOf(resultSet.getString("rol")));
                }
            }
        }
    }

    private Paciente buscarPaciente(Connection connection, int idPaciente, boolean requiereActivo) throws SQLException {
        String sql = "SELECT * FROM paciente WHERE id_paciente = ?";
        try (PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setInt(1, idPaciente);
            try (ResultSet resultSet = statement.executeQuery()) {
                if (!resultSet.next()) {
                    throw new ServiceException("No existe el paciente indicado.");
                }
                Date fechaNacimiento = resultSet.getDate("fecha_nacimiento");
                Paciente paciente = new Paciente(
                        resultSet.getInt("id_paciente"),
                        resultSet.getString("dni"),
                        resultSet.getString("nombre"),
                        resultSet.getString("apellido"),
                        resultSet.getString("telefono"),
                        resultSet.getString("email"),
                        fechaNacimiento == null ? null : fechaNacimiento.toLocalDate(),
                        resultSet.getBoolean("activo")
                );
                if (requiereActivo && !paciente.isActivo()) {
                    throw new ServiceException("El paciente indicado esta inactivo.");
                }
                return paciente;
            }
        }
    }

    private Quirofano buscarQuirofano(Connection connection, int idQuirofano, boolean requiereHabilitado)
            throws SQLException {
        String sql = "SELECT * FROM quirofano WHERE id_quirofano = ?";
        try (PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setInt(1, idQuirofano);
            try (ResultSet resultSet = statement.executeQuery()) {
                if (!resultSet.next()) {
                    throw new ServiceException("No existe el quirofano indicado.");
                }
                Quirofano quirofano = new Quirofano(
                        resultSet.getInt("id_quirofano"),
                        resultSet.getString("numero"),
                        resultSet.getString("ubicacion"),
                        resultSet.getString("descripcion"),
                        EstadoQuirofano.valueOf(resultSet.getString("estado"))
                );
                if (requiereHabilitado && !quirofano.estaHabilitado()) {
                    throw new ServiceException("El quirofano no esta HABILITADO.");
                }
                return quirofano;
            }
        }
    }

    private TipoCirugia buscarTipoCirugia(Connection connection, int idTipoCirugia, boolean requiereActivo)
            throws SQLException {
        String sql = """
                SELECT tc.id_tipo_cirugia, tc.nombre, tc.descripcion,
                       tc.duracion_estimada_minutos, tc.activo,
                       e.id_especialidad, e.nombre AS especialidad_nombre,
                       e.descripcion AS especialidad_descripcion, e.activo AS especialidad_activo
                  FROM tipo_cirugia tc
                  JOIN especialidad e ON e.id_especialidad = tc.id_especialidad
                 WHERE tc.id_tipo_cirugia = ?
                """;
        try (PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setInt(1, idTipoCirugia);
            try (ResultSet resultSet = statement.executeQuery()) {
                if (!resultSet.next()) {
                    throw new ServiceException("No existe el tipo de cirugia indicado.");
                }
                Especialidad especialidad = new Especialidad(
                        resultSet.getInt("id_especialidad"),
                        resultSet.getString("especialidad_nombre"),
                        resultSet.getString("especialidad_descripcion"),
                        resultSet.getBoolean("especialidad_activo")
                );
                TipoCirugia tipoCirugia = new TipoCirugia(
                        resultSet.getInt("id_tipo_cirugia"),
                        resultSet.getString("nombre"),
                        resultSet.getString("descripcion"),
                        resultSet.getInt("duracion_estimada_minutos"),
                        resultSet.getBoolean("activo"),
                        especialidad
                );
                if (requiereActivo && (!tipoCirugia.isActivo() || !especialidad.isActivo())) {
                    throw new ServiceException("El tipo de cirugia o su especialidad estan inactivos.");
                }
                return tipoCirugia;
            }
        }
    }

    private Profesional buscarProfesional(Connection connection, int idProfesional, boolean requiereActivo)
            throws SQLException {
        String sql = """
                SELECT p.id_profesional, p.matricula, p.dni, p.nombre, p.apellido,
                       p.telefono, p.email, p.activo,
                       e.id_especialidad, e.nombre AS especialidad_nombre,
                       e.descripcion AS especialidad_descripcion, e.activo AS especialidad_activo
                  FROM profesional p
                  JOIN especialidad e ON e.id_especialidad = p.id_especialidad
                 WHERE p.id_profesional = ?
                """;
        try (PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setInt(1, idProfesional);
            try (ResultSet resultSet = statement.executeQuery()) {
                if (!resultSet.next()) {
                    throw new ServiceException("No existe el profesional indicado.");
                }
                Especialidad especialidad = new Especialidad(
                        resultSet.getInt("id_especialidad"),
                        resultSet.getString("especialidad_nombre"),
                        resultSet.getString("especialidad_descripcion"),
                        resultSet.getBoolean("especialidad_activo")
                );
                Profesional profesional = new Profesional(
                        resultSet.getInt("id_profesional"),
                        resultSet.getString("dni"),
                        resultSet.getString("nombre"),
                        resultSet.getString("apellido"),
                        resultSet.getString("telefono"),
                        resultSet.getString("email"),
                        resultSet.getString("matricula"),
                        especialidad,
                        resultSet.getBoolean("activo")
                );
                if (requiereActivo && (!profesional.isActivo() || !especialidad.isActivo())) {
                    throw new ServiceException("El profesional o su especialidad estan inactivos.");
                }
                return profesional;
            }
        }
    }

    private boolean existeResultado(PreparedStatement statement) throws SQLException {
        try (ResultSet resultSet = statement.executeQuery()) {
            return resultSet.next() && resultSet.getInt(1) > 0;
        }
    }

    private void cargarIdExcluido(PreparedStatement statement, int index, Integer idTurnoExcluido)
            throws SQLException {
        if (idTurnoExcluido == null) {
            statement.setNull(index, Types.INTEGER);
            statement.setNull(index + 1, Types.INTEGER);
        } else {
            statement.setInt(index, idTurnoExcluido);
            statement.setInt(index + 1, idTurnoExcluido);
        }
    }

    private <T> T ejecutarEnTransaccion(OperacionTransaccional<T> operacion) {
        try (Connection connection = database.open()) {
            boolean previousAutoCommit = connection.getAutoCommit();
            connection.setAutoCommit(false);
            try {
                T resultado = operacion.ejecutar(connection);
                connection.commit();
                return resultado;
            } catch (SQLException ex) {
                connection.rollback();
                throw new ServiceException("No se pudo completar la operacion sobre turnos.", ex);
            } catch (RuntimeException ex) {
                connection.rollback();
                throw ex;
            } finally {
                connection.setAutoCommit(previousAutoCommit);
            }
        } catch (SQLException ex) {
            throw new ServiceException("No se pudo abrir la conexion con la base de datos.", ex);
        }
    }

    @FunctionalInterface
    private interface OperacionTransaccional<T> {
        T ejecutar(Connection connection) throws SQLException;
    }
}
