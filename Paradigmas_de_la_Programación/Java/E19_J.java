public class E19_J {

    static class EnemigoJuego {
        protected String nombre;
        protected int salud;
        protected int dmgAtaque;

        public EnemigoJuego(String nombre, int salud, int dmgAtaque) {
            this.nombre = nombre;
            this.salud = salud;
            this.dmgAtaque = dmgAtaque;
        }

        public void recibirDanio(int cantidad) {
            salud -= cantidad;

            if (salud < 0) {
                salud = 0;
            }

            System.out.println(
                nombre +
                " recibió " +
                cantidad +
                " puntos de daño. Salud restante: " +
                salud
            );
        }

        public void atacar(String objetivo) {
            System.out.println(
                nombre +
                " ataca a " +
                objetivo +
                " causando " +
                dmgAtaque +
                " puntos de daño."
            );
        }
    }

    static class Goblin extends EnemigoJuego {
        private final String tipoArma;

        public Goblin(String nombre, int salud, int dmgAtaque, String tipoArma) {
            super(nombre, salud, dmgAtaque);
            this.tipoArma = tipoArma;
        }

        @Override
        public void atacar(String objetivo) {
            System.out.println(
                nombre +
                " ataca a " +
                objetivo +
                " con su " +
                tipoArma +
                ", causando " +
                dmgAtaque +
                " puntos de daño."
            );
        }
    }

    static class Dragon extends EnemigoJuego {
        private final String alientoElemento;

        public Dragon(String nombre, int salud, int dmgAtaque, String alientoElemento) {
            super(nombre, salud, dmgAtaque);
            this.alientoElemento = alientoElemento;
        }

        @Override
        public void atacar(String objetivo) {
            System.out.println(
                nombre +
                " lanza un aliento de " +
                alientoElemento +
                " sobre " +
                objetivo +
                ", causando " +
                dmgAtaque +
                " puntos de daño."
            );
        }
    }

    public static void main(String[] args) {

        Goblin goblin = new Goblin(
            "Gruk",
            50,
            10,
            "Espada Oxidada"
        );

        Dragon dragon = new Dragon(
            "Smaug",
            300,
            50,
            "Fuego"
        );

        goblin.atacar("Héroe");
        dragon.atacar("Caballero");

        goblin.recibirDanio(15);
        dragon.recibirDanio(40);
    }
}