package ar.edu.utn.turnosquirurgicos.model;

import java.time.LocalDate;
import java.time.Period;

public class Paciente extends Persona {
    private LocalDate fechaNacimiento;
    private boolean activo = true;

    public Paciente() {
    }

    public Paciente(int id, String dni, String nombre, String apellido, String telefono, String email,
                    LocalDate fechaNacimiento, boolean activo) {
        super(id, dni, nombre, apellido, telefono, email);
        this.fechaNacimiento = fechaNacimiento;
        this.activo = activo;
    }

    public LocalDate getFechaNacimiento() {
        return fechaNacimiento;
    }

    public void setFechaNacimiento(LocalDate fechaNacimiento) {
        this.fechaNacimiento = fechaNacimiento;
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

    public int calcularEdad() {
        if (fechaNacimiento == null) {
            return 0;
        }
        return Period.between(fechaNacimiento, LocalDate.now()).getYears();
    }

    @Override
    public boolean validar() {
        return super.validar()
                && fechaNacimiento != null
                && fechaNacimiento.isBefore(LocalDate.now());
    }

    @Override
    public String toString() {
        return "#" + getId() + " - " + getApellido() + ", " + getNombre()
                + " DNI " + getDni() + " (" + (activo ? "activo" : "inactivo") + ")";
    }
}
