public class E13_J {
    static class ElementoZen {
        private final String tipo;
        private int posicionX;
        private int posicionY;

        public ElementoZen(String tipo, int posicionX, int posicionY) {
            this.tipo = tipo;
            this.posicionX = posicionX;
            this.posicionY = posicionY;
        }

        public void mover(int nuevaX, int nuevaY) {
            this.posicionX = nuevaX;
            this.posicionY = nuevaY;

            System.out.println("El elemento fue movido.");
        }

        public void observar() {
            System.out.println("Tipo: " + tipo);
            System.out.println("Posición X: " + posicionX);
            System.out.println("Posición Y: " + posicionY);
        }
    }

    public static void main(String[] args) {
        ElementoZen piedra = new ElementoZen("Piedra", 1, 2);

        System.out.println("--- POSICIÓN INICIAL ---");
        piedra.observar();

        piedra.mover(3, 4);

        System.out.println("--- NUEVA POSICIÓN ---");
        piedra.observar();
    }
}