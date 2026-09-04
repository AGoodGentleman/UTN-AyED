package ar.edu.utn.turnosquirurgicos.ui;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.Scanner;

public class ConsoleInput {
    private static final DateTimeFormatter DATE_TIME_FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm");
    private final Scanner scanner = new Scanner(System.in);

    public String readRequiredString(String prompt) {
        while (true) {
            System.out.print(prompt);
            String value = scanner.nextLine().trim();
            if (!value.isBlank()) {
                return value;
            }
            System.out.println("El valor es obligatorio.");
        }
    }

    public String readOptionalString(String prompt) {
        System.out.print(prompt);
        String value = scanner.nextLine().trim();
        return value.isBlank() ? null : value;
    }

    public String readStringDefault(String prompt, String currentValue) {
        String current = currentValue == null ? "" : currentValue;
        System.out.print(prompt + " [" + current + "]: ");
        String value = scanner.nextLine().trim();
        return value.isBlank() ? currentValue : value;
    }

    public int readInt(String prompt) {
        while (true) {
            System.out.print(prompt);
            String value = scanner.nextLine().trim();
            try {
                return Integer.parseInt(value);
            } catch (NumberFormatException ex) {
                System.out.println("Ingrese un numero entero valido.");
            }
        }
    }

    public int readPositiveInt(String prompt) {
        while (true) {
            int value = readInt(prompt);
            if (value > 0) {
                return value;
            }
            System.out.println("El numero debe ser mayor que cero.");
        }
    }

    public int readIntDefault(String prompt, int currentValue) {
        while (true) {
            System.out.print(prompt + " [" + currentValue + "]: ");
            String value = scanner.nextLine().trim();
            if (value.isBlank()) {
                return currentValue;
            }
            try {
                return Integer.parseInt(value);
            } catch (NumberFormatException ex) {
                System.out.println("Ingrese un numero entero valido.");
            }
        }
    }

    public LocalDate readDate(String prompt) {
        while (true) {
            System.out.print(prompt + " (yyyy-MM-dd): ");
            String value = scanner.nextLine().trim();
            try {
                return LocalDate.parse(value);
            } catch (DateTimeParseException ex) {
                System.out.println("Ingrese una fecha valida.");
            }
        }
    }

    public LocalDate readDateDefault(String prompt, LocalDate currentValue) {
        while (true) {
            System.out.print(prompt + " [" + currentValue + "] (yyyy-MM-dd): ");
            String value = scanner.nextLine().trim();
            if (value.isBlank()) {
                return currentValue;
            }
            try {
                return LocalDate.parse(value);
            } catch (DateTimeParseException ex) {
                System.out.println("Ingrese una fecha valida.");
            }
        }
    }

    public LocalDateTime readDateTime(String prompt) {
        while (true) {
            System.out.print(prompt + " (yyyy-MM-dd HH:mm): ");
            String value = scanner.nextLine().trim();
            try {
                return LocalDateTime.parse(value, DATE_TIME_FORMATTER);
            } catch (DateTimeParseException ex) {
                System.out.println("Ingrese fecha y hora validas.");
            }
        }
    }

    public boolean readYesNo(String prompt) {
        while (true) {
            System.out.print(prompt + " (s/n): ");
            String value = scanner.nextLine().trim().toLowerCase();
            if (value.equals("s") || value.equals("si")) {
                return true;
            }
            if (value.equals("n") || value.equals("no")) {
                return false;
            }
            System.out.println("Responda con s o n.");
        }
    }
}
