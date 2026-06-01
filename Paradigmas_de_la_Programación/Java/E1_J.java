public class E1_J {
    static class CreaturaMagica {
        private final String nombre;
        private final String tipo_elemento;
        private final int nivel_poder;
        private boolean esta_domesticada;

        public CreaturaMagica(String nombre, String tipo_elemento, int nivel_poder, boolean esta_domesticada){
            this.nombre = nombre;
            this.tipo_elemento = tipo_elemento;
            this.nivel_poder = nivel_poder;
            this.esta_domesticada = esta_domesticada;
        }

        public void LanzarHechizo() {
            System.out.println(nombre + " lanza un hechizo de " + tipo_elemento + " nivel " + nivel_poder + ".");
        }

        public void IntentarDomesticar() {
            if (esta_domesticada == false) {
                esta_domesticada = true;
            }
            System.out.println(nombre + " fue domesticada.");
        }
    }
    
    public static void main(String[] args) {
    CreaturaMagica creatura = new CreaturaMagica("Pikachu", "Electrico", 10, false);
    
    creatura.LanzarHechizo();
    creatura.IntentarDomesticar();
    }
}
