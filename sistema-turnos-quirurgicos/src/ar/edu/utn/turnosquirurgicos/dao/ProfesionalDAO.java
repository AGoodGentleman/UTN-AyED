package ar.edu.utn.turnosquirurgicos.dao;

import ar.edu.utn.turnosquirurgicos.config.DatabaseConnection;
import ar.edu.utn.turnosquirurgicos.model.Especialidad;
import ar.edu.utn.turnosquirurgicos.model.Profesional;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

public class ProfesionalDAO implements CrudDAO<Profesional> {
    private static final String SELECT_BASE = """
            SELECT p.id_profesional, p.matricula, p.dni, p.nombre, p.apellido,
                   p.telefono, p.email, p.activo,
                   e.id_especialidad, e.nombre AS especialidad_nombre,
                   e.descripcion AS especialidad_descripcion, e.activo AS especialidad_activo
              FROM profesional p
              JOIN especialidad e ON e.id_especialidad = p.id_especialidad
            """;

    private final DatabaseConnection database;

    public ProfesionalDAO(DatabaseConnection database) {
        this.database = database;
    }

    @Override
    public Profesional crear(Profesional profesional) {
        if (profesional == null || !profesional.validar()) {
            throw new DaoException("Los datos del profesional son invalidos.");
        }

        String sql = """
                INSERT INTO profesional (matricula, dni, nombre, apellido, telefono, email, activo, id_especialidad)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """;

        try (Connection connection = database.open();
             PreparedStatement statement = connection.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            statement.setString(1, profesional.getMatricula());
            statement.setString(2, profesional.getDni());
            statement.setString(3, profesional.getNombre());
            statement.setString(4, profesional.getApellido());
            statement.setString(5, profesional.getTelefono());
            statement.setString(6, profesional.getEmail());
            statement.setBoolean(7, profesional.isActivo());
            statement.setInt(8, profesional.getEspecialidad().getId());
            statement.executeUpdate();

            try (ResultSet keys = statement.getGeneratedKeys()) {
                if (keys.next()) {
                    profesional.setId(keys.getInt(1));
                }
            }
            return profesional;
        } catch (SQLException ex) {
            throw new DaoException("No se pudo registrar el profesional.", ex);
        }
    }

    @Override
    public Optional<Profesional> buscarPorId(int id) {
        String sql = SELECT_BASE + " WHERE p.id_profesional = ?";
        try (Connection connection = database.open();
             PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setInt(1, id);
            try (ResultSet resultSet = statement.executeQuery()) {
                if (resultSet.next()) {
                    return Optional.of(mapear(resultSet));
                }
            }
            return Optional.empty();
        } catch (SQLException ex) {
            throw new DaoException("No se pudo buscar el profesional.", ex);
        }
    }

    public Optional<Profesional> buscarPorMatricula(String matricula) {
        String sql = SELECT_BASE + " WHERE p.matricula = ?";
        try (Connection connection = database.open();
             PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setString(1, matricula);
            try (ResultSet resultSet = statement.executeQuery()) {
                if (resultSet.next()) {
                    return Optional.of(mapear(resultSet));
                }
            }
            return Optional.empty();
        } catch (SQLException ex) {
            throw new DaoException("No se pudo buscar el profesional por matricula.", ex);
        }
    }

    @Override
    public List<Profesional> listar() {
        String sql = SELECT_BASE + " ORDER BY p.apellido, p.nombre";
        try (Connection connection = database.open();
             PreparedStatement statement = connection.prepareStatement(sql);
             ResultSet resultSet = statement.executeQuery()) {
            List<Profesional> profesionales = new ArrayList<>();
            while (resultSet.next()) {
                profesionales.add(mapear(resultSet));
            }
            return profesionales;
        } catch (SQLException ex) {
            throw new DaoException("No se pudo listar profesionales.", ex);
        }
    }

    public List<Profesional> listarPorEspecialidad(int idEspecialidad) {
        String sql = SELECT_BASE + """
                 WHERE p.id_especialidad = ?
                 ORDER BY p.apellido, p.nombre
                """;
        try (Connection connection = database.open();
             PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setInt(1, idEspecialidad);
            try (ResultSet resultSet = statement.executeQuery()) {
                List<Profesional> profesionales = new ArrayList<>();
                while (resultSet.next()) {
                    profesionales.add(mapear(resultSet));
                }
                return profesionales;
            }
        } catch (SQLException ex) {
            throw new DaoException("No se pudo listar profesionales por especialidad.", ex);
        }
    }

    @Override
    public boolean actualizar(Profesional profesional) {
        if (profesional == null || profesional.getId() <= 0 || !profesional.validar()) {
            throw new DaoException("Los datos del profesional son invalidos.");
        }

        String sql = """
                UPDATE profesional
                   SET matricula = ?, dni = ?, nombre = ?, apellido = ?, telefono = ?,
                       email = ?, activo = ?, id_especialidad = ?
                 WHERE id_profesional = ?
                """;

        try (Connection connection = database.open();
             PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setString(1, profesional.getMatricula());
            statement.setString(2, profesional.getDni());
            statement.setString(3, profesional.getNombre());
            statement.setString(4, profesional.getApellido());
            statement.setString(5, profesional.getTelefono());
            statement.setString(6, profesional.getEmail());
            statement.setBoolean(7, profesional.isActivo());
            statement.setInt(8, profesional.getEspecialidad().getId());
            statement.setInt(9, profesional.getId());
            return statement.executeUpdate() > 0;
        } catch (SQLException ex) {
            throw new DaoException("No se pudo actualizar el profesional.", ex);
        }
    }

    @Override
    public boolean eliminar(int id) {
        String sql = "UPDATE profesional SET activo = FALSE WHERE id_profesional = ?";
        try (Connection connection = database.open();
             PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setInt(1, id);
            return statement.executeUpdate() > 0;
        } catch (SQLException ex) {
            throw new DaoException("No se pudo dar de baja el profesional.", ex);
        }
    }

    private Profesional mapear(ResultSet resultSet) throws SQLException {
        Especialidad especialidad = new Especialidad(
                resultSet.getInt("id_especialidad"),
                resultSet.getString("especialidad_nombre"),
                resultSet.getString("especialidad_descripcion"),
                resultSet.getBoolean("especialidad_activo")
        );

        return new Profesional(
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
    }
}
