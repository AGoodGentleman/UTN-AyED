public class E9_J {
    static class FenomenoNatural {
        private final String tipo;
        private final int intensidad;
        private final int duracion;
    
        public FenomenoNatural(String tipo, int intensidad, int duracion){
        this.tipo = tipo;
        this.intensidad = intensidad;
        this.duracion = duracion;
        }

        public void Desencadenar(){
            System.out.println("¡Un " + tipo + " está arrasando con una intensidad de " + intensidad + " por " + duracion + " horas!");
        }

        public void EvaluarImpacto(){
            double impacto = intensidad * duracion;
            System.out.println("Se estima que el impacto de " + tipo + " sea de " + impacto + " unidades.");
        }
    }

    public static void main(String[] args) {
    FenomenoNatural tornado = new FenomenoNatural("tornado", 5, 2);
    FenomenoNatural terremoto = new FenomenoNatural("terremoto", 7, 1);
    tornado.Desencadenar();
    terremoto.Desencadenar();
    tornado.EvaluarImpacto();
    terremoto.EvaluarImpacto();
    }
}