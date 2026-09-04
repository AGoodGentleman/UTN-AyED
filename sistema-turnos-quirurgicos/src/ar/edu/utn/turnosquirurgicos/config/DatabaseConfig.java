package ar.edu.utn.turnosquirurgicos.config;

public final class DatabaseConfig {
    private static final String DEFAULT_URL =
            "jdbc:mysql://localhost:3306/turnos_quirurgicos"
                    + "?useSSL=false"
                    + "&allowPublicKeyRetrieval=true"
                    + "&serverTimezone=America/Argentina/Buenos_Aires";

    private DatabaseConfig() {
    }

    public static String url() {
        return envOrDefault("DB_URL", DEFAULT_URL);
    }

    public static String user() {
        return envOrDefault("DB_USER", "root");
    }

    public static String password() {
        return envOrDefault("DB_PASSWORD", "");
    }

    private static String envOrDefault(String name, String defaultValue) {
        String value = System.getenv(name);
        return value == null || value.isBlank() ? defaultValue : value;
    }
}
