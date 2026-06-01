public class E2_J {
    static class ProductoVending {
        private final String nombre;
        private final int precio;
        private int cantidad;
    
        public ProductoVending(String nombre, int precio, int cantidad){
            this.nombre = nombre;
            this.precio = precio;
            this.cantidad = cantidad;
        }

        public void Comprar(){
            if (this.cantidad>0){
            cantidad -= 1;
            System.out.println("Se compraron unas " + nombre + " a " + precio + " creditos. " + "Quedan " + cantidad + ".");
            }
            else{
            System.out.println("No hay stock de " + nombre + ".");
            }
        }

        public void Reponer(int numero){
            cantidad += numero;
            System.out.println("Se repusieron " + numero + " " + nombre + "." + " Quedan " + cantidad + ".");
        }
    }

    public static void main(String[] args) {
    ProductoVending producto = new ProductoVending("Raciones", 5, 10);
    
    producto.Comprar();
    producto.Reponer(10);
    }
}
