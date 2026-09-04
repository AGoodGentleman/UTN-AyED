package ar.edu.utn.turnosquirurgicos.dao;

import ar.edu.utn.turnosquirurgicos.config.DatabaseConnection;
import ar.edu.utn.turnosquirurgicos.model.Especialidad;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

public class EspecialidadDAO implements CrudDAO<Especialidad> {
    private final DatabaseConnection database;

    public EspecialidadDAO(DatabaseConnection database) {
        this.database = database;
    }

    @Override
    public Especialidad crear(Especialidad especialidad) {
        if (especialidad == null || !especialidad.validar()) {
            throw new DaoException("Los datos de la especialidad son invalidos.");
        }

        String sql = "INSERT INTO especialidad (nombre, descripcion, activo) VALUES (?, ?, ?)";
        try (Connection connection = database.open();
             PreparedStatement statement = connection.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            statement.setString(1, especialidad.getNombre());
            statement.setString(2, especialidad.getDescripcion());
            statement.setBoolean(3, especialidad.isActivo());
            statement.executeUpdate();

            try (ResultSet keys = statement.getGeneratedKeys()) {
                if (keys.next()) {
                    especialidad.setId(keys.getInt(1));
                }
            }
            return especialidad;
        } catch (SQLException ex) {
            throw new DaoException("No se pudo registrar la especialidad.", ex);
        }
    }

    @Override
    public Optional<Especialidad> buscarPorId(int id) {
        String sql = "SELECT * FROM especialidad WHERE id_especialidad = ?";
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
            throw new DaoException("No se pudo buscar la especialidad.", ex);
        }
    }

    @Override
    public List<Especialidad> listar() {
        String sql = "SELECT * FROM especialidad ORDER BY nombre";
        try (Connection connection = database.open();
             PreparedStatement statement = connection.prepareStatement(sql);
             ResultSet resultSet = statement.executeQuery()) {
            List<Especialidad> especialidades = new ArrayList<>();
            while (resultSet.next()) {
                especialidades.add(mapear(resultSet));
            }
            return especialidades;
        } catch (SQLException ex) {
            throw new DaoException("No se pudo listar especialidades.", ex);
        }
    }

    @Override
    public boolean actualizar(Especialidad especialidad) {
        if (especialidad == null || especialidad.getId() <= 0 || !especialidad.validar()) {
            throw new DaoException("Los datos de la especialidad son invalidos.");
        }

        String sql = "UPDATE especialidad SET nombre = ?, descripcion = ?, activo = ? WHERE id_especialidad = ?";
        try (Connection connection = database.open();
             PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setString(1, especialidad.getNombre());
            statement.setString(2, especialidad.getDescripcion());
            statement.setBoolean(3, especialidad.isActivo());
            statement.setInt(4, especialidad.getId());
            return statement.executeUpdate() > 0;
        } catch (SQLException ex) {
            throw new DaoException("No se pudo actualizar la especialidad.", ex);
        }
    }

    @Override
    public boolean eliminar(int id) {
        String sql = "UPDATE especialidad SET activo = FALSE WHERE id_especialidad = ?";
        try (Connection connection = database.open();
             PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setInt(1, id);
            return statement.executeUpdate() > 0;
        } catch (SQLException ex) {
            throw new DaoException("No se pudo dar de baja la especialidad.", ex);
        }
    }

    private Especialidad mapear(ResultSet resultSet) throws SQLException {
        return new Especialidad(
                resultSet.getInt("id_especialidad"),
                resultSet.getString("nombre"),
                resultSet.getString("descripcion"),
                resultSet.getBoolean("activo")
        );
    }
}
