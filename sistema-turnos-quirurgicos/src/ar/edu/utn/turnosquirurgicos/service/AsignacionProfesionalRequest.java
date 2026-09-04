package ar.edu.utn.turnosquirurgicos.service;

import ar.edu.utn.turnosquirurgicos.model.RolProfesional;

public class AsignacionProfesionalRequest {
    private final int idProfesional;
    private final RolProfesional rol;

    public AsignacionProfesionalRequest(int idProfesional, RolProfesional rol) {
        this.idProfesional = idProfesional;
        this.rol = rol;
    }

    public int getIdProfesional() {
        return idProfesional;
    }

    public RolProfesional getRol() {
        return rol;
    }
}
