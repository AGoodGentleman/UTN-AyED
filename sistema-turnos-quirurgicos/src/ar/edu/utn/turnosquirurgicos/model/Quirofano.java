package ar.edu.utn.turnosquirurgicos.model;

public class Quirofano implements Validable {
    private int id;
    private String numero;
    private String ubicacion;
    private String descripcion;
    private EstadoQuirofano estado = EstadoQuirofano.HABILITADO;

    public Quirofano() {
    }

    public Quirofano(int id, String numero, String ubicacion, String descripcion, EstadoQuirofano estado) {
        this.id = id;
        this.numero = numero;
        this.ubicacion = ubicacion;
        this.descripcion = descripcion;
        this.estado = estado;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getNumero() {
        return numero;
    }

    public void setNumero(String numero) {
        this.numero = numero;
    }

    public String getUbicacion() {
        return ubicacion;
    }

    public void setUbicacion(String ubicacion) {
        this.ubicacion = ubicacion;
    }

    public String getDescripcion() {
        return descripcion;
    }

    public void setDescripcion(String descripcion) {
        this.descripcion = descripcion;
    }

    public EstadoQuirofano getEstado() {
        return estado;
    }

    public void cambiarEstado(EstadoQuirofano estado) {
        this.estado = estado;
    }

    public boolean estaHabilitado() {
        return estado == EstadoQuirofano.HABILITADO;
    }

    @Override
    public boolean validar() {
        return numero != null && !numero.isBlank()
                && ubicacion != null && !ubicacion.isBlank()
                && estado != null;
    }

    @Override
    public String toString() {
        return "#" + id + " - Quirofano " + numero + " - " + ubicacion + " (" + estado + ")";
    }
}
