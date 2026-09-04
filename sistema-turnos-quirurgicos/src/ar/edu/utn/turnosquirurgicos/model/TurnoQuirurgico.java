package ar.edu.utn.turnosquirurgicos.model;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

public class TurnoQuirurgico implements Validable {
    private int id;
    private LocalDateTime fechaHoraInicio;
    private LocalDateTime fechaHoraFin;
    private int margenPreOperatorioMinutos = 30;
    private int margenPostOperatorioMinutos = 30;
    private EstadoTurno estado = EstadoTurno.PROGRAMADO;
    private String observaciones;
    private String motivoCancelacion;
    private Paciente paciente;
    private Quirofano quirofano;
    private TipoCirugia tipoCirugia;
    private final List<ParticipacionProfesional> participaciones = new ArrayList<>();

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public LocalDateTime getFechaHoraInicio() {
        return fechaHoraInicio;
    }

    public void setFechaHoraInicio(LocalDateTime fechaHoraInicio) {
        this.fechaHoraInicio = fechaHoraInicio;
    }

    public LocalDateTime getFechaHoraFin() {
        return fechaHoraFin;
    }

    public void setFechaHoraFin(LocalDateTime fechaHoraFin) {
        this.fechaHoraFin = fechaHoraFin;
    }

    public int getMargenPreOperatorioMinutos() {
        return margenPreOperatorioMinutos;
    }

    public void setMargenPreOperatorioMinutos(int margenPreOperatorioMinutos) {
        this.margenPreOperatorioMinutos = margenPreOperatorioMinutos;
    }

    public int getMargenPostOperatorioMinutos() {
        return margenPostOperatorioMinutos;
    }

    public void setMargenPostOperatorioMinutos(int margenPostOperatorioMinutos) {
        this.margenPostOperatorioMinutos = margenPostOperatorioMinutos;
    }

    public EstadoTurno getEstado() {
        return estado;
    }

    public void setEstado(EstadoTurno estado) {
        this.estado = estado;
    }

    public String getObservaciones() {
        return observaciones;
    }

    public void setObservaciones(String observaciones) {
        this.observaciones = observaciones;
    }

    public String getMotivoCancelacion() {
        return motivoCancelacion;
    }

    public void setMotivoCancelacion(String motivoCancelacion) {
        this.motivoCancelacion = motivoCancelacion;
    }

    public Paciente getPaciente() {
        return paciente;
    }

    public void setPaciente(Paciente paciente) {
        this.paciente = paciente;
    }

    public Quirofano getQuirofano() {
        return quirofano;
    }

    public void setQuirofano(Quirofano quirofano) {
        this.quirofano = quirofano;
    }

    public TipoCirugia getTipoCirugia() {
        return tipoCirugia;
    }

    public void setTipoCirugia(TipoCirugia tipoCirugia) {
        this.tipoCirugia = tipoCirugia;
    }

    public List<ParticipacionProfesional> getParticipaciones() {
        return participaciones;
    }

    public void agregarProfesional(Profesional profesional, RolProfesional rol) {
        participaciones.add(new ParticipacionProfesional(profesional, rol));
    }

    public void cancelar(String motivo) {
        this.estado = EstadoTurno.CANCELADO;
        this.motivoCancelacion = motivo;
    }

    public void reprogramar(LocalDateTime inicio, LocalDateTime fin, Quirofano quirofano) {
        this.fechaHoraInicio = inicio;
        this.fechaHoraFin = fin;
        this.quirofano = quirofano;
    }

    public boolean seSuperpone(LocalDateTime inicio, LocalDateTime fin) {
        return fechaHoraInicio != null
                && fechaHoraFin != null
                && inicio.isBefore(fechaHoraFin)
                && fin.isAfter(fechaHoraInicio);
    }

    @Override
    public boolean validar() {
        return fechaHoraInicio != null
                && fechaHoraFin != null
                && fechaHoraFin.isAfter(fechaHoraInicio)
                && paciente != null
                && quirofano != null
                && tipoCirugia != null
                && estado != null
                && !participaciones.isEmpty();
    }

    @Override
    public String toString() {
        String pacienteTxt = paciente == null ? "sin paciente" : paciente.getNombreCompleto();
        String quirofanoTxt = quirofano == null ? "sin quirofano" : quirofano.getNumero();
        String tipoTxt = tipoCirugia == null ? "sin tipo" : tipoCirugia.getNombre();
        return "#" + id + " - " + fechaHoraInicio + " a " + fechaHoraFin
                + " - " + estado
                + " - Paciente: " + pacienteTxt
                + " - Quirofano: " + quirofanoTxt
                + " - Tipo: " + tipoTxt;
    }
}
