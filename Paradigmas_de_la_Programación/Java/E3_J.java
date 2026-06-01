public class E3_J {
    static class NaveEspacial {
        private final String nombre;
        private final int capacidad;
        private final double velocidad_max;
        private double combustible;

        public NaveEspacial(String nombre, int capacidad, double velocidad_max, double combustible){
            this.nombre = nombre;
            this.capacidad = capacidad;
            this.velocidad_max = velocidad_max;
            this.combustible = combustible;
        }

        public void Despegar(){
            System.out.println("La nave " + nombre + " esta despegando." + " Tiene capacidad para " + capacidad + " pasajeros y una Vel Max de " + velocidad_max + " m/s.");

        }

        public void Reabastecer(double cantidad){
            System.out.println("Había " + combustible + " litros de combustible.");
            combustible += cantidad;
            System.out.println("Ahora hay " + combustible + " litros de combustible.");
        }
    }

    public static void main(String[] args) {
    NaveEspacial nave = new NaveEspacial("El Argos", 500, 100000, 1000.5);
    
    nave.Despegar();
    nave.Reabastecer(100.5);
    }
}
