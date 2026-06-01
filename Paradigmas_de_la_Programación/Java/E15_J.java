public class E15_J {
    static class DiscoVinilo {
        private final String titulo;
        private final String artista;
        private final String genero;
        private String estado;

        public DiscoVinilo(String titulo, String artista, String genero, String estado){
            this.titulo = titulo;
            this.artista = artista;
            this.genero = genero;
            this.estado = estado;
        }

        public void Reproducir(){
            if ("Legible".equals(this.estado)){
            System.out.println("Reproduciendo " + titulo + " de " + artista + " (" + genero + ").");
            }
            else{
            System.out.println("El disco es irreproducible, arreglelo.");
            }
        }

        public void EvaluarEstado(){
            System.out.println("El disco " + titulo + " tiene un estado " + estado + ".");
        }

        public void Reparar(){
            if ("Ilegible".equals(this.estado)){
            this.estado = "Legible";
            System.out.println("Se ha reparado el disco " + titulo + ".");
            }
            else{
            System.out.println("El disco " + titulo + " no necesita reparaciones.");
            }
        }
    }

    public static void main(String[] args) {
    DiscoVinilo desatormentandonos = new DiscoVinilo("desatormentandonos", "Pescado Rabioso", "Rock", "Ilegible");
    desatormentandonos.Reproducir();
    desatormentandonos.EvaluarEstado();
    desatormentandonos.Reparar();
    desatormentandonos.Reparar();
    desatormentandonos.EvaluarEstado();
    desatormentandonos.Reproducir();
    }
}