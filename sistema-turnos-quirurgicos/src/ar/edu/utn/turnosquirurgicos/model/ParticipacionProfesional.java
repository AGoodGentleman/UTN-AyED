package ar.edu.utn.turnosquirurgicos.model;

public class ParticipacionProfesional implements Validable {
    private Profesional profesional;
    private RolProfesional rol;

    public ParticipacionProfesional() {
    }

    public ParticipacionProfesional(Profesional profesional, RolProfesional rol) {
        this.profesional = profesional;
        this.rol = rol;
    }

    public Profesional getProfesional() {
        return profesional;
    }

    public void setProfesional(Profesional profesional) {
        this.profesional = profesional;
    }

    public RolProfesional getRol() {
        return rol;
    }

    public void setRol(RolProfesional rol) {
        this.rol = rol;
    }

    @Override
    public boolean validar() {
        return profesional != null && profesional.getId() > 0 && rol != null;
    }

    @Override
    public String toString() {
        String nombre = profesional == null ? "Profesional no asignado" : profesional.getNombreCompleto();
        return nombre + " - " + rol;
    }
}
