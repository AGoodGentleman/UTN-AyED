package ar.edu.utn.turnosquirurgicos;

import ar.edu.utn.turnosquirurgicos.config.DatabaseConnection;
import ar.edu.utn.turnosquirurgicos.dao.EspecialidadDAO;
import ar.edu.utn.turnosquirurgicos.dao.PacienteDAO;
import ar.edu.utn.turnosquirurgicos.dao.ProfesionalDAO;
import ar.edu.utn.turnosquirurgicos.dao.QuirofanoDAO;
import ar.edu.utn.turnosquirurgicos.dao.TipoCirugiaDAO;
import ar.edu.utn.turnosquirurgicos.dao.TurnoDAO;
import ar.edu.utn.turnosquirurgicos.service.TurnoService;
import ar.edu.utn.turnosquirurgicos.ui.ConsoleApp;

public class App {
    public static void main(String[] args) {
        DatabaseConnection database = new DatabaseConnection();
        PacienteDAO pacienteDAO = new PacienteDAO(database);
        EspecialidadDAO especialidadDAO = new EspecialidadDAO(database);
        ProfesionalDAO profesionalDAO = new ProfesionalDAO(database);
        QuirofanoDAO quirofanoDAO = new QuirofanoDAO(database);
        TipoCirugiaDAO tipoCirugiaDAO = new TipoCirugiaDAO(database);
        TurnoDAO turnoDAO = new TurnoDAO(database);

        TurnoService turnoService = new TurnoService(database);
        ConsoleApp consoleApp = new ConsoleApp(
                pacienteDAO,
                especialidadDAO,
                profesionalDAO,
                quirofanoDAO,
                tipoCirugiaDAO,
                turnoDAO,
                turnoService
        );
        consoleApp.run();
    }
}
