package ar.edu.utn.turnosquirurgicos.model;

public enum EstadoTurno {
    PROGRAMADO,
    CONFIRMADO,
    EN_CURSO,
    FINALIZADO,
    CANCELADO;

    public boolean esActivoParaDisponibilidad() {
        return this == PROGRAMADO || this == CONFIRMADO || this == EN_CURSO;
    }
}
