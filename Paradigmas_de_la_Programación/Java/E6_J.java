public class E6_J {
        static class RobotLimpiador {
        private final String nombre;
        private int bateria;
        private String area;
        private boolean limpiando;

        public RobotLimpiador(String nombre, int bateria, String area, boolean limpiando){
            this.nombre = nombre;
            this.bateria = bateria;
            this.area = area;
            this.limpiando = limpiando;
        }

        public void CargarBateria(){
            if (bateria <= 90){
                bateria += 10;
                System.out.println("El Robot ha cargado y ahora tiene " + bateria + " de bateria.");
            }
            else{
                System.out.println("El Robot está al máximo o casi al máximo de batería.");
            }
        }

        public void LimpiarHabitacion(String habitacion){
            area = habitacion;
            limpiando = true;
            System.out.println("El Robot " + nombre + " limpiará " + area + ".");
        }

        public void DetenerLimpieza(){
            if (limpiando == true){
            limpiando = false;
            System.out.println("El Robot ha parado de limpiar.");
            }
        }
    }

    public static void main(String[] args) {
    RobotLimpiador roomba = new RobotLimpiador("Roomba01", 90, "Nada", false);

    roomba.CargarBateria();
    roomba.CargarBateria();
    roomba.LimpiarHabitacion("Sala");
    roomba.DetenerLimpieza();
    }
}