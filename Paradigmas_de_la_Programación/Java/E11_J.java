public class E11_J {
    static class ItemInventario {
        private final String nombre;
        private final String tipo;
        private final int peso;
        private final int valor;

        public ItemInventario(String nombre, String tipo, int peso, int valor){
            this.nombre = nombre;
            this.tipo = tipo;
            this.peso = peso;
            this.valor = valor;
        }

        public void Usar(){
            if (null != this.tipo)switch (this.tipo) {
                case "Arma" -> System.out.println("Atacas con el arma (" + nombre + ").");
                case "Armadura" -> System.out.println("Te equipas con la armadura (" + nombre + ").");
                case "Consumible" -> System.out.println("Usas el consumible (" + nombre + ").");
                default -> {
                }
            }
        }

        public void Descartar(){
            System.out.println("Descartas el ítem " + nombre + ". Tu mochila se siente mas ligera... y tu cartera tambien... (-" + peso + "kg y -" + valor + " de oro).");
        }
    }

    public static void main(String[] args) {
    ItemInventario espada = new ItemInventario("Espada Larga", "Arma", 10, 100);
    ItemInventario pechera = new ItemInventario("Pechera de Hierro", "Armadura", 50, 500);
    ItemInventario pocion = new ItemInventario("Poción Curativa", "Consumible", 1, 250);

    espada.Usar();
    pechera.Usar();
    pocion.Usar();
    espada.Descartar();
    pechera.Descartar();
    pocion.Descartar();
    }
}