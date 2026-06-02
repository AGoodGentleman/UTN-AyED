public class E16_J {

    static class GlitchDigital {
        private final String tipo;
        private final int gravedad;

        public GlitchDigital(String tipo, int gravedad) {
            this.tipo = tipo;
            this.gravedad = gravedad;
        }

        public void manifestarse() {
            System.out.println("El glitch de tipo " + tipo + " se manifiesta con gravedad " + gravedad + ".");
        }
    }

    static class GlitchGrafico extends GlitchDigital {
        private final String colorDominante;

        public GlitchGrafico(String tipo, int gravedad, String colorDominante) {
            super(tipo, gravedad);
            this.colorDominante = colorDominante;
        }

        @Override
        public void manifestarse() {
            System.out.println("El glitch gráfico distorsiona la pantalla con color dominante " + colorDominante + ".");
        }
    }

    static class GlitchSonoro extends GlitchDigital {
        private final int frecuenciaHz;

        public GlitchSonoro(String tipo, int gravedad, int frecuenciaHz) {
            super(tipo, gravedad);
            this.frecuenciaHz = frecuenciaHz;
        }

        @Override
        public void manifestarse() {
            System.out.println("El glitch sonoro emite una frecuencia de " + frecuenciaHz + " Hz.");
        }
    }

    public static void main(String[] args) {
        GlitchDigital glitchDigital = 
            new GlitchDigital("Comun", 4);
        
        GlitchGrafico glitchGrafico =
            new GlitchGrafico("Visual", 8, "Rojo");

        GlitchSonoro glitchSonoro =
            new GlitchSonoro("Sonoro", 6, 440);

        glitchDigital.manifestarse();
        glitchGrafico.manifestarse();
        glitchSonoro.manifestarse();
    }
}