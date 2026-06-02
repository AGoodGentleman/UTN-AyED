public class E17_J {

    static class ArtefactoAntiguo {
        private final String nombre;
        private final String eraHistorica;
        private final double valorEstimado;

        public ArtefactoAntiguo(String nombre, String eraHistorica, double valorEstimado) {
            this.nombre = nombre;
            this.eraHistorica = eraHistorica;
            this.valorEstimado = valorEstimado;
        }

        public void examinar() {
            System.out.println(
                "Artefacto: " + nombre +
                ". Era histórica: " + eraHistorica +
                ". Valor estimado: " + valorEstimado + " monedas."
            );
        }
    }

    static class JoyeriaAntigua extends ArtefactoAntiguo {
        private final String materialPrincipal;

        public JoyeriaAntigua(String nombre, String eraHistorica, double valorEstimado, String materialPrincipal) {
            super(nombre, eraHistorica, valorEstimado);
            this.materialPrincipal = materialPrincipal;
        }

        @Override
        public void examinar() {
            System.out.println(
                "Joyería antigua hecha principalmente de " +
                materialPrincipal + "."
            );
        }
    }

    static class HerramientaMisteriosa extends ArtefactoAntiguo {
        private final String funcionDesconocida;

        public HerramientaMisteriosa(String nombre, String eraHistorica, double valorEstimado, String funcionDesconocida) {
            super(nombre, eraHistorica, valorEstimado);
            this.funcionDesconocida = funcionDesconocida;
        }

        @Override
        public void examinar() {
            System.out.println(
                "Herramienta misteriosa. Posible función desconocida: " +
                funcionDesconocida + "."
            );
        }
    }

    public static void main(String[] args) {
        ArtefactoAntiguo artefacto = new ArtefactoAntiguo(
            "Herradura", 
            "Era del Hierro", 
            5000
            );
        
        JoyeriaAntigua joya = new JoyeriaAntigua(
            "Collar del Sol",
            "Imperio Maya",
            8500,
            "Oro"
        );

        HerramientaMisteriosa herramienta = new HerramientaMisteriosa(
            "Llave de Piedra",
            "Civilización Babilónica",
            12000,
            "Abrir mecanismos antiguos"
        );

        artefacto.examinar();
        joya.examinar();
        herramienta.examinar();
    }
}