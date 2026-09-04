package ar.edu.utn.turnosquirurgicos.model;

import java.time.LocalDateTime;

public class TipoCirugia implements Validable {
    private int id;
    private String nombre;
    private String descripcion;
    private int duracionEstimadaMinutos;
    private boolean activo = true;
    private Especialidad especialidad;

    public TipoCirugia() {
    }

    public TipoCirugia(int id, String nombre, String descripcion, int duracionEstimadaMinutos,
                       boolean activo, Especialidad especialidad) {
        this.id = id;
        this.nombre = nombre;
        this.descripcion = descripcion;
        this.duracionEstimadaMinutos = duracionEstimadaMinutos;
        this.activo = activo;
        this.especialidad = especialidad;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public String getDescripcion() {
        return descripcion;
    }

    public void setDescripcion(String descripcion) {
        this.descripcion = descripcion;
    }

    public int getDuracionEstimadaMinutos() {
        return duracionEstimadaMinutos;
    }

    public void setDuracionEstimadaMinutos(int duracionEstimadaMinutos) {
        this.duracionEstimadaMinutos = duracionEstimadaMinutos;
    }

    public boolean isActivo() {
        return activo;
    }

    public void setActivo(boolean activo) {
        this.activo = activo;
    }

    public Especialidad getEspecialidad() {
        return especialidad;
    }

    public void setEspecialidad(Especialidad especialidad) {
        this.especialidad = especialidad;
    }

    public LocalDateTime calcularHoraFin(LocalDateTime inicio) {
        return inicio.plusMinutes(duracionEstimadaMinutos);
    }

    @Override
    public boolean validar() {
        return nombre != null && !nombre.isBlank()
                && duracionEstimadaMinutos > 0
                && especialidad != null
                && especialidad.getId() > 0;
    }

    @Override
    public String toString() {
        String esp = especialidad == null ? "sin especialidad" : especialidad.getNombre();
        return "#" + id + " - " + nombre + " (" + duracionEstimadaMinutos + " min, " + esp + ")";
    }
}
