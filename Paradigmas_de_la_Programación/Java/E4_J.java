public class E4_J {
        static class ChatarraEspacial {
        private final String tipo;
        private final double peso;
        private final double valor;

        public ChatarraEspacial(String tipo, double peso, double valor){
            this.tipo = tipo;
            this.peso = peso;
            this.valor = valor;
        }

        public void Recolectar(){
            System.out.println("Se recolectó chatarra de " + tipo + " que pesa " + peso + "kg con un valor de " + valor + " monedas.");
        }
    }

    public static void main(String[] args) {
    ChatarraEspacial chatarra0 = new ChatarraEspacial("Metal", 25, 250);
    ChatarraEspacial chatarra1 = new ChatarraEspacial("Plástico", 12.5, 150);
    ChatarraEspacial chatarra2 = new ChatarraEspacial("Orgánico", 10, 1000);

    chatarra0.Recolectar();
    chatarra1.Recolectar();
    chatarra2.Recolectar();
    }
}