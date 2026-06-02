public class E20_J {

    static class SerMagico {
        protected String nombre;
        protected int longevidad;

        public SerMagico(String nombre, int longevidad) {
            this.nombre = nombre;
            this.longevidad = longevidad;
        }

        public void emitirLuz() {
            System.out.println(
                nombre +
                " emite una tenue luz mágica."
            );
        }

        public void interactuar() {
            System.out.println(
                nombre +
                " interactúa de forma amistosa."
            );
        }
    }

    static class Hada extends SerMagico {
        private final String colorAlas;

        public Hada(String nombre, int longevidad, String colorAlas) {
            super(nombre, longevidad);
            this.colorAlas = colorAlas;
        }

        @Override
        public void emitirLuz() {
            System.out.println(
                nombre +
                " brilla con una luz proveniente de sus alas " +
                colorAlas +
                "."
            );
        }
    }

    static class Ent extends SerMagico {
        private final String especieArbol;

        public Ent(String nombre, int longevidad, String especieArbol) {
            super(nombre, longevidad);
            this.especieArbol = especieArbol;
        }

        @Override
        public void interactuar() {
            System.out.println(
                nombre +
                ", un antiguo " +
                especieArbol +
                ", comparte su sabiduría lentamente."
            );
        }
    }

    public static void main(String[] args) {

        Hada hada = new Hada(
            "Lunaria",
            250,
            "Plateadas"
        );

        Ent ent = new Ent(
            "Roblebarba",
            3000,
            "Roble"
        );

        hada.emitirLuz();
        hada.interactuar();

        System.out.println();

        ent.emitirLuz();
        ent.interactuar();
    }
}