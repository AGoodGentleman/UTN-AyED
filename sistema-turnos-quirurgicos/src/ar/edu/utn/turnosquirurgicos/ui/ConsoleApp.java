package ar.edu.utn.turnosquirurgicos.ui;

import ar.edu.utn.turnosquirurgicos.dao.DaoException;
import ar.edu.utn.turnosquirurgicos.dao.EspecialidadDAO;
import ar.edu.utn.turnosquirurgicos.dao.PacienteDAO;
import ar.edu.utn.turnosquirurgicos.dao.ProfesionalDAO;
import ar.edu.utn.turnosquirurgicos.dao.QuirofanoDAO;
import ar.edu.utn.turnosquirurgicos.dao.TipoCirugiaDAO;
import ar.edu.utn.turnosquirurgicos.dao.TurnoDAO;
import ar.edu.utn.turnosquirurgicos.model.Especialidad;
import ar.edu.utn.turnosquirurgicos.model.EstadoQuirofano;
import ar.edu.utn.turnosquirurgicos.model.EstadoTurno;
import ar.edu.utn.turnosquirurgicos.model.Paciente;
import ar.edu.utn.turnosquirurgicos.model.Profesional;
import ar.edu.utn.turnosquirurgicos.model.Quirofano;
import ar.edu.utn.turnosquirurgicos.model.RolProfesional;
import ar.edu.utn.turnosquirurgicos.model.TipoCirugia;
import ar.edu.utn.turnosquirurgicos.model.TurnoQuirurgico;
import ar.edu.utn.turnosquirurgicos.service.AsignacionProfesionalRequest;
import ar.edu.utn.turnosquirurgicos.service.ServiceException;
import ar.edu.utn.turnosquirurgicos.service.TurnoService;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

public class ConsoleApp {
    private final PacienteDAO pacienteDAO;
    private final EspecialidadDAO especialidadDAO;
    private final ProfesionalDAO profesionalDAO;
    private final QuirofanoDAO quirofanoDAO;
    private final TipoCirugiaDAO tipoCirugiaDAO;
    private final TurnoDAO turnoDAO;
    private final TurnoService turnoService;
    private final ConsoleInput input = new ConsoleInput();

    public ConsoleApp(
            PacienteDAO pacienteDAO,
            EspecialidadDAO especialidadDAO,
            ProfesionalDAO profesionalDAO,
            QuirofanoDAO quirofanoDAO,
            TipoCirugiaDAO tipoCirugiaDAO,
            TurnoDAO turnoDAO,
            TurnoService turnoService
    ) {
        this.pacienteDAO = pacienteDAO;
        this.especialidadDAO = especialidadDAO;
        this.profesionalDAO = profesionalDAO;
        this.quirofanoDAO = quirofanoDAO;
        this.tipoCirugiaDAO = tipoCirugiaDAO;
        this.turnoDAO = turnoDAO;
        this.turnoService = turnoService;
    }

    public void run() {
        boolean salir = false;
        while (!salir) {
            mostrarMenuPrincipal();
            int opcion = input.readInt("Opcion: ");
            try {
                switch (opcion) {
                    case 1 -> gestionarPacientes();
                    case 2 -> gestionarEspecialidades();
                    case 3 -> gestionarProfesionales();
                    case 4 -> gestionarQuirofanos();
                    case 5 -> gestionarTiposCirugia();
                    case 6 -> programarTurno();
                    case 7 -> reprogramarTurno();
                    case 8 -> cancelarTurno();
                    case 9 -> cambiarEstadoTurno();
                    case 10 -> listarTurnosPorFecha();
                    case 11 -> consultarAgendaProfesional();
                    case 12 -> listarTurnosPaciente();
                    case 13 -> limpiarPantalla();
                    case 0 -> salir = true;
                    default -> System.out.println("Opcion invalida.");
                }
            } catch (DaoException | ServiceException | IllegalArgumentException ex) {
                System.out.println("Error: " + ex.getMessage());
            }
        }
        System.out.println("Programa finalizado.");
    }

    private void mostrarMenuPrincipal() {
        System.out.println();
        System.out.println("=== Sistema de Gestion de Turnos Quirurgicos ===");
        System.out.println("1. Gestionar pacientes");
        System.out.println("2. Gestionar especialidades");
        System.out.println("3. Gestionar profesionales");
        System.out.println("4. Gestionar quirofanos");
        System.out.println("5. Gestionar tipos de cirugia");
        System.out.println("6. Programar turno quirurgico");
        System.out.println("7. Reprogramar turno quirurgico");
        System.out.println("8. Cancelar turno quirurgico");
        System.out.println("9. Cambiar estado de turno");
        System.out.println("10. Consultar turnos por fecha");
        System.out.println("11. Consultar agenda profesional");
        System.out.println("12. Consultar turnos por paciente");
        System.out.println("13. Limpiar pantalla");
        System.out.println("0. Salir");
    }

    private void gestionarPacientes() {
        boolean volver = false;
        while (!volver) {
            mostrarSubmenu("pacientes");
            int opcion = input.readInt("Opcion: ");
            switch (opcion) {
                case 1 -> imprimirListado("Pacientes", pacienteDAO.listar());
                case 2 -> registrarPaciente();
                case 3 -> actualizarPaciente();
                case 4 -> darDeBajaPaciente();
                case 9 -> limpiarPantalla();
                case 0 -> volver = true;
                default -> System.out.println("Opcion invalida.");
            }
        }
    }

    private void registrarPaciente() {
        Paciente paciente = new Paciente();
        paciente.setDni(input.readRequiredString("DNI: "));
        paciente.setNombre(input.readRequiredString("Nombre: "));
        paciente.setApellido(input.readRequiredString("Apellido: "));
        paciente.setFechaNacimiento(input.readDate("Fecha de nacimiento"));
        paciente.setTelefono(input.readOptionalString("Telefono: "));
        paciente.setEmail(input.readOptionalString("Email: "));
        pacienteDAO.crear(paciente);
        System.out.println("Paciente registrado: " + paciente);
    }

    private void actualizarPaciente() {
        Paciente paciente = pacienteDAO.buscarPorId(input.readPositiveInt("ID paciente: "))
                .orElseThrow(() -> new IllegalArgumentException("No existe el paciente."));
        paciente.setDni(input.readStringDefault("DNI", paciente.getDni()));
        paciente.setNombre(input.readStringDefault("Nombre", paciente.getNombre()));
        paciente.setApellido(input.readStringDefault("Apellido", paciente.getApellido()));
        paciente.setFechaNacimiento(input.readDateDefault("Fecha de nacimiento", paciente.getFechaNacimiento()));
        paciente.setTelefono(input.readStringDefault("Telefono", paciente.getTelefono()));
        paciente.setEmail(input.readStringDefault("Email", paciente.getEmail()));
        pacienteDAO.actualizar(paciente);
        System.out.println("Paciente actualizado.");
    }

    private void darDeBajaPaciente() {
        int id = input.readPositiveInt("ID paciente: ");
        if (pacienteDAO.eliminar(id)) {
            System.out.println("Paciente dado de baja.");
        } else {
            System.out.println("No se encontro el paciente.");
        }
    }

    private void gestionarEspecialidades() {
        boolean volver = false;
        while (!volver) {
            mostrarSubmenu("especialidades");
            int opcion = input.readInt("Opcion: ");
            switch (opcion) {
                case 1 -> imprimirListado("Especialidades", especialidadDAO.listar());
                case 2 -> registrarEspecialidad();
                case 3 -> actualizarEspecialidad();
                case 4 -> darDeBajaEspecialidad();
                case 9 -> limpiarPantalla();
                case 0 -> volver = true;
                default -> System.out.println("Opcion invalida.");
            }
        }
    }

    private void registrarEspecialidad() {
        Especialidad especialidad = new Especialidad();
        especialidad.setNombre(input.readRequiredString("Nombre: "));
        especialidad.setDescripcion(input.readOptionalString("Descripcion: "));
        especialidadDAO.crear(especialidad);
        System.out.println("Especialidad registrada: " + especialidad);
    }

    private void actualizarEspecialidad() {
        Especialidad especialidad = especialidadDAO.buscarPorId(input.readPositiveInt("ID especialidad: "))
                .orElseThrow(() -> new IllegalArgumentException("No existe la especialidad."));
        especialidad.setNombre(input.readStringDefault("Nombre", especialidad.getNombre()));
        especialidad.setDescripcion(input.readStringDefault("Descripcion", especialidad.getDescripcion()));
        especialidadDAO.actualizar(especialidad);
        System.out.println("Especialidad actualizada.");
    }

    private void darDeBajaEspecialidad() {
        int id = input.readPositiveInt("ID especialidad: ");
        if (especialidadDAO.eliminar(id)) {
            System.out.println("Especialidad dada de baja.");
        } else {
            System.out.println("No se encontro la especialidad.");
        }
    }

    private void gestionarProfesionales() {
        boolean volver = false;
        while (!volver) {
            mostrarSubmenu("profesionales");
            int opcion = input.readInt("Opcion: ");
            switch (opcion) {
                case 1 -> imprimirListado("Profesionales", profesionalDAO.listar());
                case 2 -> registrarProfesional();
                case 3 -> actualizarProfesional();
                case 4 -> darDeBajaProfesional();
                case 9 -> limpiarPantalla();
                case 0 -> volver = true;
                default -> System.out.println("Opcion invalida.");
            }
        }
    }

    private void registrarProfesional() {
        imprimirListado("Especialidades", especialidadDAO.listar());
        Especialidad especialidad = especialidadDAO.buscarPorId(input.readPositiveInt("ID especialidad principal: "))
                .orElseThrow(() -> new IllegalArgumentException("No existe la especialidad."));
        Profesional profesional = new Profesional();
        profesional.setMatricula(input.readRequiredString("Matricula: "));
        profesional.setDni(input.readRequiredString("DNI: "));
        profesional.setNombre(input.readRequiredString("Nombre: "));
        profesional.setApellido(input.readRequiredString("Apellido: "));
        profesional.setTelefono(input.readOptionalString("Telefono: "));
        profesional.setEmail(input.readOptionalString("Email: "));
        profesional.setEspecialidad(especialidad);
        profesionalDAO.crear(profesional);
        System.out.println("Profesional registrado: " + profesional);
    }

    private void actualizarProfesional() {
        Profesional profesional = profesionalDAO.buscarPorId(input.readPositiveInt("ID profesional: "))
                .orElseThrow(() -> new IllegalArgumentException("No existe el profesional."));
        imprimirListado("Especialidades", especialidadDAO.listar());
        Especialidad especialidad = especialidadDAO.buscarPorId(input.readIntDefault(
                "ID especialidad principal",
                profesional.getEspecialidad().getId()
        )).orElseThrow(() -> new IllegalArgumentException("No existe la especialidad."));
        profesional.setMatricula(input.readStringDefault("Matricula", profesional.getMatricula()));
        profesional.setDni(input.readStringDefault("DNI", profesional.getDni()));
        profesional.setNombre(input.readStringDefault("Nombre", profesional.getNombre()));
        profesional.setApellido(input.readStringDefault("Apellido", profesional.getApellido()));
        profesional.setTelefono(input.readStringDefault("Telefono", profesional.getTelefono()));
        profesional.setEmail(input.readStringDefault("Email", profesional.getEmail()));
        profesional.setEspecialidad(especialidad);
        profesionalDAO.actualizar(profesional);
        System.out.println("Profesional actualizado.");
    }

    private void darDeBajaProfesional() {
        int id = input.readPositiveInt("ID profesional: ");
        if (profesionalDAO.eliminar(id)) {
            System.out.println("Profesional dado de baja.");
        } else {
            System.out.println("No se encontro el profesional.");
        }
    }

    private void gestionarQuirofanos() {
        boolean volver = false;
        while (!volver) {
            mostrarSubmenu("quirofanos");
            int opcion = input.readInt("Opcion: ");
            switch (opcion) {
                case 1 -> imprimirListado("Quirofanos", quirofanoDAO.listar());
                case 2 -> registrarQuirofano();
                case 3 -> actualizarQuirofano();
                case 4 -> sacarQuirofanoDeServicio();
                case 9 -> limpiarPantalla();
                case 0 -> volver = true;
                default -> System.out.println("Opcion invalida.");
            }
        }
    }

    private void registrarQuirofano() {
        Quirofano quirofano = new Quirofano();
        quirofano.setNumero(input.readRequiredString("Numero: "));
        quirofano.setUbicacion(input.readRequiredString("Ubicacion: "));
        quirofano.setDescripcion(input.readOptionalString("Descripcion: "));
        quirofano.cambiarEstado(seleccionarEstadoQuirofano());
        quirofanoDAO.crear(quirofano);
        System.out.println("Quirofano registrado: " + quirofano);
    }

    private void actualizarQuirofano() {
        Quirofano quirofano = quirofanoDAO.buscarPorId(input.readPositiveInt("ID quirofano: "))
                .orElseThrow(() -> new IllegalArgumentException("No existe el quirofano."));
        quirofano.setNumero(input.readStringDefault("Numero", quirofano.getNumero()));
        quirofano.setUbicacion(input.readStringDefault("Ubicacion", quirofano.getUbicacion()));
        quirofano.setDescripcion(input.readStringDefault("Descripcion", quirofano.getDescripcion()));
        if (input.readYesNo("Cambiar estado")) {
            quirofano.cambiarEstado(seleccionarEstadoQuirofano());
        }
        quirofanoDAO.actualizar(quirofano);
        System.out.println("Quirofano actualizado.");
    }

    private void sacarQuirofanoDeServicio() {
        int id = input.readPositiveInt("ID quirofano: ");
        if (quirofanoDAO.eliminar(id)) {
            System.out.println("Quirofano marcado como FUERA_DE_SERVICIO.");
        } else {
            System.out.println("No se encontro el quirofano.");
        }
    }

    private void gestionarTiposCirugia() {
        boolean volver = false;
        while (!volver) {
            mostrarSubmenu("tipos de cirugia");
            int opcion = input.readInt("Opcion: ");
            switch (opcion) {
                case 1 -> imprimirListado("Tipos de cirugia", tipoCirugiaDAO.listar());
                case 2 -> registrarTipoCirugia();
                case 3 -> actualizarTipoCirugia();
                case 4 -> darDeBajaTipoCirugia();
                case 9 -> limpiarPantalla();
                case 0 -> volver = true;
                default -> System.out.println("Opcion invalida.");
            }
        }
    }

    private void registrarTipoCirugia() {
        imprimirListado("Especialidades", especialidadDAO.listar());
        Especialidad especialidad = especialidadDAO.buscarPorId(input.readPositiveInt("ID especialidad: "))
                .orElseThrow(() -> new IllegalArgumentException("No existe la especialidad."));
        TipoCirugia tipoCirugia = new TipoCirugia();
        tipoCirugia.setNombre(input.readRequiredString("Nombre: "));
        tipoCirugia.setDescripcion(input.readOptionalString("Descripcion: "));
        tipoCirugia.setDuracionEstimadaMinutos(input.readPositiveInt("Duracion estimada en minutos: "));
        tipoCirugia.setEspecialidad(especialidad);
        tipoCirugiaDAO.crear(tipoCirugia);
        System.out.println("Tipo de cirugia registrado: " + tipoCirugia);
    }

    private void actualizarTipoCirugia() {
        TipoCirugia tipoCirugia = tipoCirugiaDAO.buscarPorId(input.readPositiveInt("ID tipo de cirugia: "))
                .orElseThrow(() -> new IllegalArgumentException("No existe el tipo de cirugia."));
        imprimirListado("Especialidades", especialidadDAO.listar());
        Especialidad especialidad = especialidadDAO.buscarPorId(input.readIntDefault(
                "ID especialidad",
                tipoCirugia.getEspecialidad().getId()
        )).orElseThrow(() -> new IllegalArgumentException("No existe la especialidad."));
        tipoCirugia.setNombre(input.readStringDefault("Nombre", tipoCirugia.getNombre()));
        tipoCirugia.setDescripcion(input.readStringDefault("Descripcion", tipoCirugia.getDescripcion()));
        tipoCirugia.setDuracionEstimadaMinutos(input.readIntDefault(
                "Duracion estimada en minutos",
                tipoCirugia.getDuracionEstimadaMinutos()
        ));
        tipoCirugia.setEspecialidad(especialidad);
        tipoCirugiaDAO.actualizar(tipoCirugia);
        System.out.println("Tipo de cirugia actualizado.");
    }

    private void darDeBajaTipoCirugia() {
        int id = input.readPositiveInt("ID tipo de cirugia: ");
        if (tipoCirugiaDAO.eliminar(id)) {
            System.out.println("Tipo de cirugia dado de baja.");
        } else {
            System.out.println("No se encontro el tipo de cirugia.");
        }
    }

    private void programarTurno() {
        imprimirListado("Pacientes", pacienteDAO.listar());
        int idPaciente = input.readPositiveInt("ID paciente: ");
        imprimirListado("Tipos de cirugia", tipoCirugiaDAO.listar());
        int idTipoCirugia = input.readPositiveInt("ID tipo de cirugia: ");
        imprimirListado("Quirofanos", quirofanoDAO.listar());
        int idQuirofano = leerIdQuirofanoHabilitado("ID quirofano: ");
        LocalDateTime inicio = input.readDateTime("Inicio del turno");
        imprimirListado("Profesionales", profesionalDAO.listar());
        List<AsignacionProfesionalRequest> asignaciones = leerAsignacionesProfesionales();
        String observaciones = input.readOptionalString("Observaciones: ");

        TurnoQuirurgico turno = turnoService.programarTurno(
                idPaciente,
                idTipoCirugia,
                idQuirofano,
                inicio,
                asignaciones,
                observaciones
        );
        System.out.println("Turno programado:");
        imprimirTurno(turno);
    }

    private void reprogramarTurno() {
        int idTurno = input.readPositiveInt("ID turno: ");
        LocalDateTime nuevoInicio = input.readDateTime("Nuevo inicio");
        imprimirListado("Quirofanos", quirofanoDAO.listar());
        int idQuirofano = leerIdQuirofanoHabilitado("ID nuevo quirofano: ");
        List<AsignacionProfesionalRequest> asignaciones = null;
        if (input.readYesNo("Modificar equipo medico")) {
            imprimirListado("Profesionales", profesionalDAO.listar());
            asignaciones = leerAsignacionesProfesionales();
        }

        TurnoQuirurgico turno = turnoService.reprogramarTurno(idTurno, nuevoInicio, idQuirofano, asignaciones);
        System.out.println("Turno reprogramado:");
        imprimirTurno(turno);
    }

    private void cancelarTurno() {
        int idTurno = input.readPositiveInt("ID turno: ");
        String motivo = input.readOptionalString("Motivo: ");
        turnoService.cancelarTurno(idTurno, motivo);
        System.out.println("Turno cancelado.");
    }

    private void cambiarEstadoTurno() {
        int idTurno = input.readPositiveInt("ID turno: ");
        EstadoTurno estado = seleccionarEstadoTurno();
        TurnoQuirurgico turno = turnoService.cambiarEstadoTurno(idTurno, estado);
        System.out.println("Estado actualizado:");
        imprimirTurno(turno);
    }

    private void listarTurnosPorFecha() {
        LocalDate fecha = input.readDate("Fecha");
        imprimirTurnos(turnoDAO.listarPorFecha(fecha));
    }

    private void consultarAgendaProfesional() {
        imprimirListado("Profesionales", profesionalDAO.listar());
        int idProfesional = input.readPositiveInt("ID profesional: ");
        imprimirTurnos(turnoDAO.listarPorProfesional(idProfesional));
    }

    private void listarTurnosPaciente() {
        imprimirListado("Pacientes", pacienteDAO.listar());
        int idPaciente = input.readPositiveInt("ID paciente: ");
        imprimirTurnos(turnoDAO.listarPorPaciente(idPaciente));
    }

    private int leerIdQuirofanoHabilitado(String prompt) {
        int idQuirofano = input.readPositiveInt(prompt);
        Quirofano quirofano = quirofanoDAO.buscarPorId(idQuirofano)
                .orElseThrow(() -> new IllegalArgumentException("No existe el quirofano indicado."));
        if (!quirofano.estaHabilitado()) {
            throw new IllegalArgumentException(
                    "No se puede usar el quirofano " + quirofano.getNumero()
                            + " porque su estado actual es " + quirofano.getEstado()
                            + ". Debe estar HABILITADO."
            );
        }
        return idQuirofano;
    }

    private List<AsignacionProfesionalRequest> leerAsignacionesProfesionales() {
        int cantidad = input.readPositiveInt("Cantidad de profesionales del equipo: ");
        List<AsignacionProfesionalRequest> asignaciones = new ArrayList<>();
        for (int i = 1; i <= cantidad; i++) {
            System.out.println("Profesional " + i);
            int idProfesional = input.readPositiveInt("ID profesional: ");
            RolProfesional rol = seleccionarRolProfesional();
            asignaciones.add(new AsignacionProfesionalRequest(idProfesional, rol));
        }
        return asignaciones;
    }

    private RolProfesional seleccionarRolProfesional() {
        RolProfesional[] roles = RolProfesional.values();
        for (int i = 0; i < roles.length; i++) {
            System.out.println((i + 1) + ". " + roles[i]);
        }
        while (true) {
            int opcion = input.readPositiveInt("Rol: ");
            if (opcion >= 1 && opcion <= roles.length) {
                return roles[opcion - 1];
            }
            System.out.println("Rol invalido.");
        }
    }

    private EstadoQuirofano seleccionarEstadoQuirofano() {
        EstadoQuirofano[] estados = EstadoQuirofano.values();
        for (int i = 0; i < estados.length; i++) {
            System.out.println((i + 1) + ". " + estados[i]);
        }
        while (true) {
            int opcion = input.readPositiveInt("Estado: ");
            if (opcion >= 1 && opcion <= estados.length) {
                return estados[opcion - 1];
            }
            System.out.println("Estado invalido.");
        }
    }

    private EstadoTurno seleccionarEstadoTurno() {
        EstadoTurno[] estados = {
                EstadoTurno.PROGRAMADO,
                EstadoTurno.CONFIRMADO,
                EstadoTurno.EN_CURSO,
                EstadoTurno.FINALIZADO
        };
        for (int i = 0; i < estados.length; i++) {
            System.out.println((i + 1) + ". " + estados[i]);
        }
        while (true) {
            int opcion = input.readPositiveInt("Estado: ");
            if (opcion >= 1 && opcion <= estados.length) {
                return estados[opcion - 1];
            }
            System.out.println("Estado invalido.");
        }
    }

    private void mostrarSubmenu(String nombre) {
        System.out.println();
        System.out.println("=== Gestion de " + nombre + " ===");
        System.out.println("1. Listar");
        System.out.println("2. Registrar");
        System.out.println("3. Actualizar");
        System.out.println("4. Dar de baja");
        System.out.println("9. Limpiar pantalla");
        System.out.println("0. Volver");
    }

    private void limpiarPantalla() {
        System.out.print("\033[H\033[2J");
        System.out.flush();
    }

    private void imprimirTurnos(List<TurnoQuirurgico> turnos) {
        if (turnos.isEmpty()) {
            System.out.println("No hay turnos para mostrar.");
            return;
        }
        for (TurnoQuirurgico turno : turnos) {
            imprimirTurno(turno);
            System.out.println();
        }
    }

    private void imprimirTurno(TurnoQuirurgico turno) {
        System.out.println(turno);
        if (!turno.getParticipaciones().isEmpty()) {
            System.out.println("Equipo medico:");
            turno.getParticipaciones().forEach(participacion -> System.out.println("  - " + participacion));
        }
        if (turno.getMotivoCancelacion() != null && !turno.getMotivoCancelacion().isBlank()) {
            System.out.println("Motivo de cancelacion: " + turno.getMotivoCancelacion());
        }
    }

    private void imprimirListado(String titulo, List<?> elementos) {
        System.out.println();
        System.out.println("--- " + titulo + " ---");
        if (elementos.isEmpty()) {
            System.out.println("Sin datos.");
            return;
        }
        elementos.forEach(System.out::println);
    }
}
