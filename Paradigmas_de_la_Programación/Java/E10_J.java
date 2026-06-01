public class E10_J {
    static class Conjuro {
        private final String nombre;
        private final String efecto;
        private final int costo;
        private final int dificultad;

        public Conjuro(String nombre, String efecto, int costo, int dificultad){
            this.nombre = nombre;
            this.efecto = efecto;
            this.costo = costo;
            this.dificultad = dificultad;
        }

        public void Lanzar(){
            System.out.println("Se ha lanzado el conjuro " + nombre + ". Produce " + efecto + ". (-" + costo + ")");
        }
        public void Aprender(){
            if (this.dificultad >= 0 && this.dificultad < 5){
                System.out.println("El hechizo " + nombre + " se aprendio sencillamente.");
            }
            else if (this.dificultad >= 5 && this.dificultad < 10){
                System.out.println("El hechizo " + nombre + " se aprendio con esfuerzo moderado.");
            }
            else if (this.dificultad >=10){
                System.out.println("El hechizo " + nombre + " se aprendio a duras penas.");
            }
        }
    }

    public static void main(String[] args) {
    Conjuro descarga_de_fuego = new Conjuro("descarga", "una pequeña llamarada", 10, 3);
    Conjuro bola_de_fuego = new Conjuro("fireball", "una mediana bola de fuego", 50, 6);
    Conjuro meteorito = new Conjuro("meteorito", "una masiva esfera de metal fundido", 100, 12);

    descarga_de_fuego.Aprender();
    bola_de_fuego.Aprender();
    meteorito.Aprender();
    descarga_de_fuego.Lanzar();
    bola_de_fuego.Lanzar();
    meteorito.Lanzar();
    }
}