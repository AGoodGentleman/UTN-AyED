public class E5_J {
        static class Pocion {
        private final String nombre;
        private final String color;
        private final String efecto;
        private final int duracion;

        public Pocion(String nombre, String color, String efecto, int duracion){
            this.nombre = nombre;
            this.color = color;
            this.efecto = efecto;
            this.duracion = duracion;
        }

        public void MezclarIngredientes(){
            System.out.println("Mezclando ingredientes para la poción " + nombre + "." + " El líquido se torna " + color + ".");

        }

        public void BeberPocion(){
            System.out.println("Se bebió la poción " + nombre + ", lo que le proporciona " + efecto + " por " + duracion + " minutos.");
        }
    }

    public static void main(String[] args) {
    Pocion curativa = new Pocion("Curativa", "Rojo", "Sanación", 10);
    
    curativa.MezclarIngredientes();
    curativa.BeberPocion();
    }
}