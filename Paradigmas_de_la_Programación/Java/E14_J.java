public class E14_J {
    static class MascotaVirtual {
        private final String nombre;
        private final String especie;
        private int hambre;
        private int felicidad;

        public MascotaVirtual(String nombre, String especie, int hambre, int felicidad){
            this.nombre = nombre;
            this.especie = especie;
            this.hambre = hambre;
            this.felicidad = felicidad;
        }

        public void Alimentar(){
            if (this.hambre >= 20){
                this.hambre -= 20;
                this.felicidad += 5;
                System.out.println("Se ha alimentado a " + nombre + " (" + especie + ").");
            }
            else {
                System.out.println(nombre + " está muy lleno.");
            }
        }

        public void Jugar(){
            if (this.felicidad <= 80){
                this.hambre += 10;
                this.felicidad += 20;
                System.out.println("Has jugado con " + nombre + " (" + especie + ").");
            }
            else {
                System.out.println(nombre + " está extasiado.");
            }
        }
    }

    public static void main(String[] args) {
    MascotaVirtual jeanluc = new MascotaVirtual("jeanluc", "Pikachu", 30, 80);
    jeanluc.Jugar();
    jeanluc.Jugar();
    jeanluc.Alimentar();
    jeanluc.Alimentar();
    jeanluc.Alimentar();
    }
}