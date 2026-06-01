import java.util.Scanner;

public class E8_J {
    static class ModuloCiudad {
        private final String tipo;
        private final int energia;
        private final int habitantes;
        private final String nombre;

        public ModuloCiudad(String tipo, int energia, int habitantes, String nombre) {
            this.tipo = tipo;
            this.energia = energia;
            this.habitantes = habitantes;
            this.nombre = nombre;
        }

        public ModuloCiudad expandir(String tipo, int energia, int habitantes) {
            try (Scanner sc = new Scanner(System.in)) {
                System.out.print("Nombre del nuevo módulo: ");
                String nombreNuevo = sc.nextLine();

                return new ModuloCiudad(
                    tipo,
                    energia,
                    habitantes,
                    nombreNuevo
                );
            }
        }

        public void generarReporte() {
            System.out.println("Nombre: " + nombre);
            System.out.println("Tipo: " + tipo);
            System.out.println("Energía consumida: " + energia + "Kw");
            System.out.println("Habitantes máximos: " + habitantes);
        }
    }

    public static void main(String[] args) {

        ModuloCiudad modulo1 =
            new ModuloCiudad(
                "Residencial",
                100,
                50,
                "Barrio Norte"
            );

        ModuloCiudad modulo2 =
            modulo1.expandir(
                "Comercial",
                150,
                20
            );

        System.out.println("\n--- MÓDULO ORIGINAL ---");
        modulo1.generarReporte();

        System.out.println("\n--- NUEVO MÓDULO ---");
        modulo2.generarReporte();
    }
}