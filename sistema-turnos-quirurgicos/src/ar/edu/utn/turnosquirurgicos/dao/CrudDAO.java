package ar.edu.utn.turnosquirurgicos.dao;

import java.util.List;
import java.util.Optional;

public interface CrudDAO<T> {
    T crear(T objeto);

    Optional<T> buscarPorId(int id);

    List<T> listar();

    boolean actualizar(T objeto);

    boolean eliminar(int id);
}
