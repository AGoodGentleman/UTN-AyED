package ar.edu.utn.turnosquirurgicos.dao;

import ar.edu.utn.turnosquirurgicos.config.DatabaseConnection;
import ar.edu.utn.turnosquirurgicos.model.Especialidad;
import ar.edu.utn.turnosquirurgicos.model.TipoCirugia;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

public class TipoCirugiaDAO implements CrudDAO<TipoCirugia> {
    private static final String SELECT_BASE = """
            SELECT tc.id_tipo_cirugia, tc.nombre, tc.descripcion,
                   tc.duracion_estimada_minutos, tc.activo,
                   e.id_especialidad, e.nombre AS especialidad_nombre,
                   e.descripcion AS especialidad_descripcion, e.activo AS especialidad_activo
              FROM tipo_cirugia tc
              JOIN especialidad e ON e.id_especialidad = tc.id_especialidad
            """;

    private final DatabaseConnection database;

    public TipoCirugiaDAO(DatabaseConnection database) {
        this.database = database;
    }

    @Override
    public TipoCirugia crear(TipoCirugia tipoCirugia) {
        if (tipoCirugia == null || !tipoCirugia.validar()) {
            throw new DaoException("Los datos del tipo de cirugia son invalidos.");
        }

        String sql = """
                INSERT INTO tipo_cirugia (nombre, descripcion, duracion_estimada_minutos, activo, id_especialidad)
                VALUES (?, ?, ?, ?, ?)
                """;

        try (Connection connection = database.open();
             PreparedStatement statement = connection.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            statement.setString(1, tipoCirugia.getNombre());
            statement.setString(2, tipoCirugia.getDescripcion());
            statement.setInt(3, tipoCirugia.getDuracionEstimadaMinutos());
            statement.setBoolean(4, tipoCirugia.isActivo());
            statement.setInt(5, tipoCirugia.getEspecialidad().getId());
            statement.executeUpdate();

            try (ResultSet keys = statement.getGeneratedKeys()) {
                if (keys.next()) {
                    tipoCirugia.setId(keys.getInt(1));
                }
            }
            return tipoCirugia;
        } catch (SQLException ex) {
            throw new DaoException("No se pudo registrar el tipo de cirugia.", ex);
        }
    }

    @Override
    public Optional<TipoCirugia> buscarPorId(int id) {
        String sql = SELECT_BASE + " WHERE tc.id_tipo_cirugia = ?";
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
            throw new DaoException("No se pudo buscar el tipo de cirugia.", ex);
        }
    }

    @Override
    public List<TipoCirugia> listar() {
        String sql = SELECT_BASE + " ORDER BY tc.nombre";
        try (Connection connection = database.open();
             PreparedStatement statement = connection.prepareStatement(sql);
             ResultSet resultSet = statement.executeQuery()) {
            List<TipoCirugia> tipos = new ArrayList<>();
            while (resultSet.next()) {
                tipos.add(mapear(resultSet));
            }
            return tipos;
        } catch (SQLException ex) {
            throw new DaoException("No se pudo listar tipos de cirugia.", ex);
        }
    }

    public List<TipoCirugia> listarPorEspecialidad(int idEspecialidad) {
        String sql = SELECT_BASE + """
                 WHERE tc.id_especialidad = ?
                 ORDER BY tc.nombre
                """;
        try (Connection connection = database.open();
             PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setInt(1, idEspecialidad);
            try (ResultSet resultSet = statement.executeQuery()) {
                List<TipoCirugia> tipos = new ArrayList<>();
                while (resultSet.next()) {
                    tipos.add(mapear(resultSet));
                }
                return tipos;
            }
        } catch (SQLException ex) {
            throw new DaoException("No se pudo listar tipos de cirugia por especialidad.", ex);
        }
    }

    @Override
    public boolean actualizar(TipoCirugia tipoCirugia) {
        if (tipoCirugia == null || tipoCirugia.getId() <= 0 || !tipoCirugia.validar()) {
            throw new DaoException("Los datos del tipo de cirugia son invalidos.");
        }

        String sql = """
                UPDATE tipo_cirugia
                   SET nombre = ?, descripcion = ?, duracion_estimada_minutos = ?,
                       activo = ?, id_especialidad = ?
                 WHERE id_tipo_cirugia = ?
                """;

        try (Connection connection = database.open();
             PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setString(1, tipoCirugia.getNombre());
            statement.setString(2, tipoCirugia.getDescripcion());
            statement.setInt(3, tipoCirugia.getDuracionEstimadaMinutos());
            statement.setBoolean(4, tipoCirugia.isActivo());
            statement.setInt(5, tipoCirugia.getEspecialidad().getId());
            statement.setInt(6, tipoCirugia.getId());
            return statement.executeUpdate() > 0;
        } catch (SQLException ex) {
            throw new DaoException("No se pudo actualizar el tipo de cirugia.", ex);
        }
    }

    @Override
    public boolean eliminar(int id) {
        String sql = "UPDATE tipo_cirugia SET activo = FALSE WHERE id_tipo_cirugia = ?";
        try (Connection connection = database.open();
             PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setInt(1, id);
            return statement.executeUpdate() > 0;
        } catch (SQLException ex) {
            throw new DaoException("No se pudo dar de baja el tipo de cirugia.", ex);
        }
    }

    private TipoCirugia mapear(ResultSet resultSet) throws SQLException {
        Especialidad especialidad = new Especialidad(
                resultSet.getInt("id_especialidad"),
                resultSet.getString("especialidad_nombre"),
                resultSet.getString("especialidad_descripcion"),
                resultSet.getBoolean("especialidad_activo")
        );

        return new TipoCirugia(
                resultSet.getInt("id_tipo_cirugia"),
                resultSet.getString("nombre"),
                resultSet.getString("descripcion"),
                resultSet.getInt("duracion_estimada_minutos"),
                resultSet.getBoolean("activo"),
                especialidad
        );
    }
}
