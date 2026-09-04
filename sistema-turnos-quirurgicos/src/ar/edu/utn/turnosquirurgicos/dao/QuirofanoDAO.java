package ar.edu.utn.turnosquirurgicos.dao;

import ar.edu.utn.turnosquirurgicos.config.DatabaseConnection;
import ar.edu.utn.turnosquirurgicos.model.EstadoQuirofano;
import ar.edu.utn.turnosquirurgicos.model.Quirofano;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

public class QuirofanoDAO implements CrudDAO<Quirofano> {
    private final DatabaseConnection database;

    public QuirofanoDAO(DatabaseConnection database) {
        this.database = database;
    }

    @Override
    public Quirofano crear(Quirofano quirofano) {
        if (quirofano == null || !quirofano.validar()) {
            throw new DaoException("Los datos del quirofano son invalidos.");
        }

        String sql = "INSERT INTO quirofano (numero, ubicacion, descripcion, estado) VALUES (?, ?, ?, ?)";
        try (Connection connection = database.open();
             PreparedStatement statement = connection.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            statement.setString(1, quirofano.getNumero());
            statement.setString(2, quirofano.getUbicacion());
            statement.setString(3, quirofano.getDescripcion());
            statement.setString(4, quirofano.getEstado().name());
            statement.executeUpdate();

            try (ResultSet keys = statement.getGeneratedKeys()) {
                if (keys.next()) {
                    quirofano.setId(keys.getInt(1));
                }
            }
            return quirofano;
        } catch (SQLException ex) {
            throw new DaoException("No se pudo registrar el quirofano.", ex);
        }
    }

    @Override
    public Optional<Quirofano> buscarPorId(int id) {
        String sql = "SELECT * FROM quirofano WHERE id_quirofano = ?";
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
            throw new DaoException("No se pudo buscar el quirofano.", ex);
        }
    }

    @Override
    public List<Quirofano> listar() {
        String sql = "SELECT * FROM quirofano ORDER BY numero";
        try (Connection connection = database.open();
             PreparedStatement statement = connection.prepareStatement(sql);
             ResultSet resultSet = statement.executeQuery()) {
            List<Quirofano> quirofanos = new ArrayList<>();
            while (resultSet.next()) {
                quirofanos.add(mapear(resultSet));
            }
            return quirofanos;
        } catch (SQLException ex) {
            throw new DaoException("No se pudo listar quirofanos.", ex);
        }
    }

    @Override
    public boolean actualizar(Quirofano quirofano) {
        if (quirofano == null || quirofano.getId() <= 0 || !quirofano.validar()) {
            throw new DaoException("Los datos del quirofano son invalidos.");
        }

        String sql = """
                UPDATE quirofano
                   SET numero = ?, ubicacion = ?, descripcion = ?, estado = ?
                 WHERE id_quirofano = ?
                """;

        try (Connection connection = database.open();
             PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setString(1, quirofano.getNumero());
            statement.setString(2, quirofano.getUbicacion());
            statement.setString(3, quirofano.getDescripcion());
            statement.setString(4, quirofano.getEstado().name());
            statement.setInt(5, quirofano.getId());
            return statement.executeUpdate() > 0;
        } catch (SQLException ex) {
            throw new DaoException("No se pudo actualizar el quirofano.", ex);
        }
    }

    @Override
    public boolean eliminar(int id) {
        String sql = "UPDATE quirofano SET estado = 'FUERA_DE_SERVICIO' WHERE id_quirofano = ?";
        try (Connection connection = database.open();
             PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setInt(1, id);
            return statement.executeUpdate() > 0;
        } catch (SQLException ex) {
            throw new DaoException("No se pudo sacar de servicio el quirofano.", ex);
        }
    }

    private Quirofano mapear(ResultSet resultSet) throws SQLException {
        return new Quirofano(
                resultSet.getInt("id_quirofano"),
                resultSet.getString("numero"),
                resultSet.getString("ubicacion"),
                resultSet.getString("descripcion"),
                EstadoQuirofano.valueOf(resultSet.getString("estado"))
        );
    }
}
