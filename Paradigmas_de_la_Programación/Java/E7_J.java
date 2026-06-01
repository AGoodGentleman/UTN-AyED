public class E7_J {
    static class Gema {
        private final String nombre;
        private final String color;
        private final double quilates;
        private int pureza;
        private boolean tallada;

        public Gema(String nombre, String color, double quilates, int pureza){
            this.nombre = nombre;
            this.color = color;
            this.quilates = quilates;
            this.pureza = pureza;
        }

        public void Tallar(){
            if (tallada == false && pureza<100) {
                tallada = true;
                pureza += ((Math.random()*10)*(Math.random()*10));
                if (pureza >= 100){
                    pureza = 100;
                }
                System.out.println("La gema " + nombre + " color " + color + " con quilates " + quilates + " ha mejorado su pureza a " + pureza);
            }
            else{
            System.out.println("Esta gema ya ha sido tallada.");
            }
        }

        public void Vender(int precio){
            double p_final = (precio*quilates*(pureza/10));
            System.out.println("La gema " + nombre + " color " + color + " con quilates " + quilates + " y pureza " + pureza + " se vendio por " + p_final);
        }
    }

    public static void main(String[] args) {
    Gema gema = new Gema("Amatista", "Lila", 25, 50);
    gema.Tallar();
    gema.Tallar();
    gema.Vender(100);
    }
}