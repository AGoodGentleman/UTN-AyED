package ar.edu.utn.turnosquirurgicos.model;

public abstract class Persona implements Validable {
    private int id;
    private String dni;
    private String nombre;
    private String apellido;
    private String telefono;
    private String email;

    protected Persona() {
    }

    protected Persona(int id, String dni, String nombre, String apellido, String telefono, String email) {
        this.id = id;
        this.dni = dni;
        this.nombre = nombre;
        this.apellido = apellido;
        this.telefono = telefono;
        this.email = email;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getDni() {
        return dni;
    }

    public void setDni(String dni) {
        this.dni = dni;
    }

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public String getApellido() {
        return apellido;
    }

    public void setApellido(String apellido) {
        this.apellido = apellido;
    }

    public String getTelefono() {
        return telefono;
    }

    public void setTelefono(String telefono) {
        this.telefono = telefono;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getNombreCompleto() {
        return nombre + " " + apellido;
    }

    @Override
    public boolean validar() {
        return notBlank(dni) && notBlank(nombre) && notBlank(apellido);
    }

    protected boolean notBlank(String value) {
        return value != null && !value.isBlank();
    }
}
