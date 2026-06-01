public class E12_J {
    static class Juguete {
        private final String nombre;
        private final String material;
        private boolean defectuoso;
        private double precio;

        public Juguete(String nombre, String material, boolean defectuoso, double precio){
            this.nombre = nombre;
            this.material = material;
            this.defectuoso = defectuoso;
            this.precio = precio;
        }

        public void Inspeccionar(){
            if ("Plastico A+".equals(this.material)){
                System.out.println("No se han encontrado defectos en el juguete " + nombre + ".");
            }
            else{
                this.defectuoso = true;
                System.out.println("Se han encontrado defectos en el juguete " + nombre + ". Buen ojo.");
            }
        }

        public void Reparar(){
            if (this.defectuoso){
                this.defectuoso = false;
                this.precio /= 2;
                System.out.println("El juguete " + nombre + " ha sido arreglado y ahora cuesta " + precio + ".");
            }
            else{
                System.out.println("El juguete " + nombre + " no estaba defectuoso.");
            }
        }
    }

    public static void main(String[] args) {
    Juguete barbie = new Juguete("Barbie", "Plastico A+", false, 1000);
    Juguete ken = new Juguete("Ken", "Plastico B+", false, 500);

    barbie.Reparar();
    ken.Reparar();
    barbie.Inspeccionar();
    ken.Inspeccionar();
    barbie.Reparar();
    ken.Reparar();
    }
}