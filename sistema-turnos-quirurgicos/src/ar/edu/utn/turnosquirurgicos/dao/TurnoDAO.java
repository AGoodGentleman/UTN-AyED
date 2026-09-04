package ar.edu.utn.turnosquirurgicos.dao;

import ar.edu.utn.turnosquirurgicos.config.DatabaseConnection;
import ar.edu.utn.turnosquirurgicos.model.Especialidad;
import ar.edu.utn.turnosquirurgicos.model.EstadoQuirofano;
import ar.edu.utn.turnosquirurgicos.model.EstadoTurno;
import ar.edu.utn.turnosquirurgicos.model.Paciente;
import ar.edu.utn.turnosquirurgicos.model.ParticipacionProfesional;
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
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

public class TurnoDAO implements CrudDAO<TurnoQuirurgico> {
    private static final String SELECT_BASE = """
            SELECT t.id_turno, t.fecha_hora_inicio, t.fecha_hora_fin,
                   t.margen_pre_operatorio_minutos, t.margen_post_operatorio_minutos,
                   t.estado, t.observaciones, t.motivo_cancelacion,
                   p.id_paciente, p.dni AS paciente_dni, p.nombre AS paciente_nombre,
                   p.apellido AS paciente_apellido, p.fecha_nacimiento,
                   p.telefono AS paciente_telefono, p.email AS paciente_email,
                   p.activo AS paciente_activo,
                   q.id_quirofano, q.numero AS quirofano_numero,
                   q.ubicacion AS quirofano_ubicacion,
                   q.descripcion AS quirofano_descripcion,
                   q.estado AS quirofano_estado,
                   tc.id_tipo_cirugia, tc.nombre AS tipo_nombre,
                   tc.descripcion AS tipo_descripcion,
                   tc.duracion_estimada_minutos, tc.activo AS tipo_activo,
                   e.id_especialidad, e.nombre AS especialidad_nombre,
                   e.descripcion AS especialidad_descripcion,
                   e.activo AS especialidad_activo
              FROM turno_quirurgico t
              JOIN paciente p ON p.id_paciente = t.id_paciente
              JOIN quirofano q ON q.id_quirofano = t.id_quirofano
              JOIN tipo_cirugia tc ON tc.id_tipo_cirugia = t.id_tipo_cirugia
              JOIN especialidad e ON e.id_especialidad = tc.id_especialidad
            """;

    private final DatabaseConnection database;

    public TurnoDAO(DatabaseConnection database) {
        this.database = database;
    }

    @Override
    public TurnoQuirurgico crear(TurnoQuirurgico turno) {
        if (turno == null || !turno.validar()) {
            throw new DaoException("Los datos del turno son invalidos.");
        }
        validarCirujanoPrincipal(turno);

        String sql = """
                INSERT INTO turno_quirurgico
                    (fecha_hora_inicio, fecha_hora_fin, margen_pre_operatorio_minutos,
                     margen_post_operatorio_minutos, estado, observaciones,
                     motivo_cancelacion, id_paciente, id_quirofano, id_tipo_cirugia)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """;

        try (Connection connection = database.open()) {
            boolean previousAutoCommit = connection.getAutoCommit();
            connection.setAutoCommit(false);
            try (PreparedStatement statement = connection.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
                cargarTurno(statement, turno);
                statement.executeUpdate();

                try (ResultSet keys = statement.getGeneratedKeys()) {
                    if (keys.next()) {
                        turno.setId(keys.getInt(1));
                    }
                }
                insertarParticipaciones(connection, turno);
                connection.commit();
                return turno;
            } catch (SQLException | RuntimeException ex) {
                connection.rollback();
                throw ex;
            } finally {
                connection.setAutoCommit(previousAutoCommit);
            }
        } catch (SQLException ex) {
            throw new DaoException("No se pudo registrar el turno quirurgico.", ex);
        }
    }

    @Override
    public Optional<TurnoQuirurgico> buscarPorId(int id) {
        String sql = SELECT_BASE + " WHERE t.id_turno = ?";
        try (Connection connection = database.open();
             PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setInt(1, id);
            try (ResultSet resultSet = statement.executeQuery()) {
                if (resultSet.next()) {
                    TurnoQuirurgico turno = mapearTurno(resultSet);
                    cargarParticipaciones(connection, turno);
                    return Optional.of(turno);
                }
            }
            return Optional.empty();
        } catch (SQLException ex) {
            throw new DaoException("No se pudo buscar el turno quirurgico.", ex);
        }
    }

    @Override
    public List<TurnoQuirurgico> listar() {
        String sql = SELECT_BASE + " ORDER BY t.fecha_hora_inicio DESC";
        try (Connection connection = database.open();
             PreparedStatement statement = connection.prepareStatement(sql);
             ResultSet resultSet = statement.executeQuery()) {
            return mapearListado(connection, resultSet);
        } catch (SQLException ex) {
            throw new DaoException("No se pudieron listar turnos quirurgicos.", ex);
        }
    }

    public List<TurnoQuirurgico> listarPorFecha(LocalDate fecha) {
        String sql = SELECT_BASE + """
                 WHERE DATE(t.fecha_hora_inicio) = ?
                 ORDER BY t.fecha_hora_inicio
                """;
        try (Connection connection = database.open();
             PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setDate(1, Date.valueOf(fecha));
            try (ResultSet resultSet = statement.executeQuery()) {
                return mapearListado(connection, resultSet);
            }
        } catch (SQLException ex) {
            throw new DaoException("No se pudieron listar turnos por fecha.", ex);
        }
    }

    public List<TurnoQuirurgico> listarPorProfesional(int idProfesional) {
        String sql = SELECT_BASE + """
              JOIN turno_profesional tp_filtro ON tp_filtro.id_turno = t.id_turno
             WHERE tp_filtro.id_profesional = ?
             ORDER BY t.fecha_hora_inicio
            """;
        try (Connection connection = database.open();
             PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setInt(1, idProfesional);
            try (ResultSet resultSet = statement.executeQuery()) {
                return mapearListado(connection, resultSet);
            }
        } catch (SQLException ex) {
            throw new DaoException("No se pudo consultar la agenda del profesional.", ex);
        }
    }

    public List<TurnoQuirurgico> listarPorPaciente(int idPaciente) {
        String sql = SELECT_BASE + """
             WHERE t.id_paciente = ?
             ORDER BY t.fecha_hora_inicio
            """;
        try (Connection connection = database.open();
             PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setInt(1, idPaciente);
            try (ResultSet resultSet = statement.executeQuery()) {
                return mapearListado(connection, resultSet);
            }
        } catch (SQLException ex) {
            throw new DaoException("No se pudieron listar turnos del paciente.", ex);
        }
    }

    @Override
    public boolean actualizar(TurnoQuirurgico turno) {
        if (turno == null || turno.getId() <= 0 || !turno.validar()) {
            throw new DaoException("Los datos del turno son invalidos.");
        }
        validarCirujanoPrincipal(turno);

        String sql = """
                UPDATE turno_quirurgico
                   SET fecha_hora_inicio = ?, fecha_hora_fin = ?,
                       margen_pre_operatorio_minutos = ?,
                       margen_post_operatorio_minutos = ?, estado = ?,
                       observaciones = ?, motivo_cancelacion = ?,
                       id_paciente = ?, id_quirofano = ?, id_tipo_cirugia = ?
                 WHERE id_turno = ?
                """;

        try (Connection connection = database.open()) {
            boolean previousAutoCommit = connection.getAutoCommit();
            connection.setAutoCommit(false);
            try (PreparedStatement statement = connection.prepareStatement(sql);
                 PreparedStatement deleteParticipaciones = connection.prepareStatement(
                         "DELETE FROM turno_profesional WHERE id_turno = ?")) {
                cargarTurno(statement, turno);
                statement.setInt(11, turno.getId());
                boolean actualizado = statement.executeUpdate() > 0;

                deleteParticipaciones.setInt(1, turno.getId());
                deleteParticipaciones.executeUpdate();
                insertarParticipaciones(connection, turno);
                connection.commit();
                return actualizado;
            } catch (SQLException | RuntimeException ex) {
                connection.rollback();
                throw ex;
            } finally {
                connection.setAutoCommit(previousAutoCommit);
            }
        } catch (SQLException ex) {
            throw new DaoException("No se pudo actualizar el turno quirurgico.", ex);
        }
    }

    @Override
    public boolean eliminar(int id) {
        return cancelar(id, "Cancelado por baja logica");
    }

    public boolean cancelar(int id, String motivo) {
        String sql = """
                UPDATE turno_quirurgico
                   SET estado = 'CANCELADO', motivo_cancelacion = ?
                 WHERE id_turno = ?
                """;
        try (Connection connection = database.open();
             PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setString(1, motivo);
            statement.setInt(2, id);
            return statement.executeUpdate() > 0;
        } catch (SQLException ex) {
            throw new DaoException("No se pudo cancelar el turno quirurgico.", ex);
        }
    }

    private void cargarTurno(PreparedStatement statement, TurnoQuirurgico turno) throws SQLException {
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
    }

    private void insertarParticipaciones(Connection connection, TurnoQuirurgico turno) throws SQLException {
        String sql = "INSERT INTO turno_profesional (id_turno, id_profesional, rol) VALUES (?, ?, ?)";
        try (PreparedStatement statement = connection.prepareStatement(sql)) {
            for (ParticipacionProfesional participacion : turno.getParticipaciones()) {
                statement.setInt(1, turno.getId());
                statement.setInt(2, participacion.getProfesional().getId());
                statement.setString(3, participacion.getRol().name());
                statement.addBatch();
            }
            statement.executeBatch();
        }
    }

    private List<TurnoQuirurgico> mapearListado(Connection connection, ResultSet resultSet) throws SQLException {
        List<TurnoQuirurgico> turnos = new ArrayList<>();
        while (resultSet.next()) {
            TurnoQuirurgico turno = mapearTurno(resultSet);
            cargarParticipaciones(connection, turno);
            turnos.add(turno);
        }
        return turnos;
    }

    private TurnoQuirurgico mapearTurno(ResultSet resultSet) throws SQLException {
        TurnoQuirurgico turno = new TurnoQuirurgico();
        turno.setId(resultSet.getInt("id_turno"));
        turno.setFechaHoraInicio(resultSet.getTimestamp("fecha_hora_inicio").toLocalDateTime());
        turno.setFechaHoraFin(resultSet.getTimestamp("fecha_hora_fin").toLocalDateTime());
        turno.setMargenPreOperatorioMinutos(resultSet.getInt("margen_pre_operatorio_minutos"));
        turno.setMargenPostOperatorioMinutos(resultSet.getInt("margen_post_operatorio_minutos"));
        turno.setEstado(EstadoTurno.valueOf(resultSet.getString("estado")));
        turno.setObservaciones(resultSet.getString("observaciones"));
        turno.setMotivoCancelacion(resultSet.getString("motivo_cancelacion"));

        Date fechaNacimiento = resultSet.getDate("fecha_nacimiento");
        turno.setPaciente(new Paciente(
                resultSet.getInt("id_paciente"),
                resultSet.getString("paciente_dni"),
                resultSet.getString("paciente_nombre"),
                resultSet.getString("paciente_apellido"),
                resultSet.getString("paciente_telefono"),
                resultSet.getString("paciente_email"),
                fechaNacimiento == null ? null : fechaNacimiento.toLocalDate(),
                resultSet.getBoolean("paciente_activo")
        ));

        turno.setQuirofano(new Quirofano(
                resultSet.getInt("id_quirofano"),
                resultSet.getString("quirofano_numero"),
                resultSet.getString("quirofano_ubicacion"),
                resultSet.getString("quirofano_descripcion"),
                EstadoQuirofano.valueOf(resultSet.getString("quirofano_estado"))
        ));

        Especialidad especialidad = new Especialidad(
                resultSet.getInt("id_especialidad"),
                resultSet.getString("especialidad_nombre"),
                resultSet.getString("especialidad_descripcion"),
                resultSet.getBoolean("especialidad_activo")
        );
        turno.setTipoCirugia(new TipoCirugia(
                resultSet.getInt("id_tipo_cirugia"),
                resultSet.getString("tipo_nombre"),
                resultSet.getString("tipo_descripcion"),
                resultSet.getInt("duracion_estimada_minutos"),
                resultSet.getBoolean("tipo_activo"),
                especialidad
        ));
        return turno;
    }

    private void cargarParticipaciones(Connection connection, TurnoQuirurgico turno) throws SQLException {
        String sql = """
                SELECT tp.rol,
                       p.id_profesional, p.matricula, p.dni, p.nombre, p.apellido,
                       p.telefono, p.email, p.activo,
                       e.id_especialidad, e.nombre AS especialidad_nombre,
                       e.descripcion AS especialidad_descripcion, e.activo AS especialidad_activo
                  FROM turno_profesional tp
                  JOIN profesional p ON p.id_profesional = tp.id_profesional
                  JOIN especialidad e ON e.id_especialidad = p.id_especialidad
                 WHERE tp.id_turno = ?
                 ORDER BY tp.rol, p.apellido, p.nombre
                """;
        try (PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setInt(1, turno.getId());
            try (ResultSet resultSet = statement.executeQuery()) {
                while (resultSet.next()) {
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
                    turno.getParticipaciones().add(new ParticipacionProfesional(
                            profesional,
                            RolProfesional.valueOf(resultSet.getString("rol"))
                    ));
                }
            }
        }
    }

    private void validarCirujanoPrincipal(TurnoQuirurgico turno) {
        long cantidad = turno.getParticipaciones().stream()
                .filter(participacion -> participacion.getRol() == RolProfesional.CIRUJANO_PRINCIPAL)
                .count();
        if (cantidad != 1) {
            throw new DaoException("Cada turno debe tener exactamente un cirujano principal.");
        }
    }
}
