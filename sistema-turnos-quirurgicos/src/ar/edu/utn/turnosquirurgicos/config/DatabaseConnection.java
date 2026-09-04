package ar.edu.utn.turnosquirurgicos.config;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DatabaseConnection {
    public DatabaseConnection() {
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
        } catch (ClassNotFoundException ex) {
            throw new IllegalStateException(
                    "No se encontro MySQL Connector/J. Configure MYSQL_JDBC_JAR al ejecutar.",
                    ex
            );
        }
    }

    public Connection open() throws SQLException {
        return DriverManager.getConnection(
                DatabaseConfig.url(),
                DatabaseConfig.user(),
                DatabaseConfig.password()
        );
    }
}
