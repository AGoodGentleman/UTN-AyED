package ar.edu.utn.turnosquirurgicos.dao;

import ar.edu.utn.turnosquirurgicos.config.DatabaseConnection;
import ar.edu.utn.turnosquirurgicos.model.Paciente;

import java.sql.Connection;
import java.sql.Date;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

public class PacienteDAO implements CrudDAO<Paciente> {
    private final DatabaseConnection database;

    public PacienteDAO(DatabaseConnection database) {
        this.database = database;
    }

    @Override
    public Paciente crear(Paciente paciente) {
        if (paciente == null || !paciente.validar()) {
            throw new DaoException("Los datos del paciente son invalidos.");
        }

        String sql = """
                INSERT INTO paciente (dni, nombre, apellido, fecha_nacimiento, telefono, email, activo)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """;

        try (Connection connection = database.open();
             PreparedStatement statement = connection.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            statement.setString(1, paciente.getDni());
            statement.setString(2, paciente.getNombre());
            statement.setString(3, paciente.getApellido());
            statement.setDate(4, Date.valueOf(paciente.getFechaNacimiento()));
            statement.setString(5, paciente.getTelefono());
            statement.setString(6, paciente.getEmail());
            statement.setBoolean(7, paciente.isActivo());
            statement.executeUpdate();

            try (ResultSet keys = statement.getGeneratedKeys()) {
                if (keys.next()) {
                    paciente.setId(keys.getInt(1));
                }
            }
            return paciente;
        } catch (SQLException ex) {
            throw new DaoException("No se pudo registrar el paciente.", ex);
        }
    }

    @Override
    public Optional<Paciente> buscarPorId(int id) {
        String sql = "SELECT * FROM paciente WHERE id_paciente = ?";
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
            throw new DaoException("No se pudo buscar el paciente.", ex);
        }
    }

    public Optional<Paciente> buscarPorDni(String dni) {
        String sql = "SELECT * FROM paciente WHERE dni = ?";
        try (Connection connection = database.open();
             PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setString(1, dni);
            try (ResultSet resultSet = statement.executeQuery()) {
                if (resultSet.next()) {
                    return Optional.of(mapear(resultSet));
                }
            }
            return Optional.empty();
        } catch (SQLException ex) {
            throw new DaoException("No se pudo buscar el paciente por DNI.", ex);
        }
    }

    @Override
    public List<Paciente> listar() {
        String sql = "SELECT * FROM paciente ORDER BY apellido, nombre";
        try (Connection connection = database.open();
             PreparedStatement statement = connection.prepareStatement(sql);
             ResultSet resultSet = statement.executeQuery()) {
            List<Paciente> pacientes = new ArrayList<>();
            while (resultSet.next()) {
                pacientes.add(mapear(resultSet));
            }
            return pacientes;
        } catch (SQLException ex) {
            throw new DaoException("No se pudo listar pacientes.", ex);
        }
    }

    @Override
    public boolean actualizar(Paciente paciente) {
        if (paciente == null || paciente.getId() <= 0 || !paciente.validar()) {
            throw new DaoException("Los datos del paciente son invalidos.");
        }

        String sql = """
                UPDATE paciente
                   SET dni = ?, nombre = ?, apellido = ?, fecha_nacimiento = ?,
                       telefono = ?, email = ?, activo = ?
                 WHERE id_paciente = ?
                """;

        try (Connection connection = database.open();
             PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setString(1, paciente.getDni());
            statement.setString(2, paciente.getNombre());
            statement.setString(3, paciente.getApellido());
            statement.setDate(4, Date.valueOf(paciente.getFechaNacimiento()));
            statement.setString(5, paciente.getTelefono());
            statement.setString(6, paciente.getEmail());
            statement.setBoolean(7, paciente.isActivo());
            statement.setInt(8, paciente.getId());
            return statement.executeUpdate() > 0;
        } catch (SQLException ex) {
            throw new DaoException("No se pudo actualizar el paciente.", ex);
        }
    }

    @Override
    public boolean eliminar(int id) {
        String sql = "UPDATE paciente SET activo = FALSE WHERE id_paciente = ?";
        try (Connection connection = database.open();
             PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setInt(1, id);
            return statement.executeUpdate() > 0;
        } catch (SQLException ex) {
            throw new DaoException("No se pudo dar de baja el paciente.", ex);
        }
    }

    private Paciente mapear(ResultSet resultSet) throws SQLException {
        Date fechaNacimiento = resultSet.getDate("fecha_nacimiento");
        return new Paciente(
                resultSet.getInt("id_paciente"),
                resultSet.getString("dni"),
                resultSet.getString("nombre"),
                resultSet.getString("apellido"),
                resultSet.getString("telefono"),
                resultSet.getString("email"),
                fechaNacimiento == null ? null : fechaNacimiento.toLocalDate(),
                resultSet.getBoolean("activo")
        );
    }
}
