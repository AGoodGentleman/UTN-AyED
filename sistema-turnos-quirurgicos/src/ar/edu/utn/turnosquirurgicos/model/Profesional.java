package ar.edu.utn.turnosquirurgicos.model;

public class Profesional extends Persona {
    private String matricula;
    private Especialidad especialidad;
    private boolean activo = true;

    public Profesional() {
    }

    public Profesional(int id, String dni, String nombre, String apellido, String telefono, String email,
                       String matricula, Especialidad especialidad, boolean activo) {
        super(id, dni, nombre, apellido, telefono, email);
        this.matricula = matricula;
        this.especialidad = especialidad;
        this.activo = activo;
    }

    public String getMatricula() {
        return matricula;
    }

    public void setMatricula(String matricula) {
        this.matricula = matricula;
    }

    public Especialidad getEspecialidad() {
        return especialidad;
    }

    public void setEspecialidad(Especialidad especialidad) {
        this.especialidad = especialidad;
    }

    public boolean isActivo() {
        return activo;
    }

    public void activar() {
        this.activo = true;
    }

    public void desactivar() {
        this.activo = false;
    }

    @Override
    public boolean validar() {
        return super.validar()
                && matricula != null
                && !matricula.isBlank()
                && especialidad != null
                && especialidad.getId() > 0;
    }

    @Override
    public String toString() {
        String esp = especialidad == null ? "sin especialidad" : especialidad.getNombre();
        return "#" + getId() + " - " + getApellido() + ", " + getNombre()
                + " Mat. " + matricula + " - " + esp
                + " (" + (activo ? "activo" : "inactivo") + ")";
    }
}
