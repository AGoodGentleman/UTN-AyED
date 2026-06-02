public class E18_J {

    static class MiembroTripulacion {
        private final String nombre;
        private final String rango;
        private final int Experiencia;

        public MiembroTripulacion(String nombre, String rango, int Experiencia) {
            this.nombre = nombre;
            this.rango = rango;
            this.Experiencia = Experiencia;
        }

        public void realizarTarea() {
            System.out.println(
                nombre + ", con rango " + rango +
                " y " + Experiencia +
                " años de experiencia, realiza una tarea general de la tripulación."
            );
        }
    }

    static class CientificoEspacial extends MiembroTripulacion {
        private final String areaEspecializacion;

        public CientificoEspacial(String nombre, String rango, int Experiencia, String areaEspecializacion) {
            super(nombre, rango, Experiencia);
            this.areaEspecializacion = areaEspecializacion;
        }

        @Override
        public void realizarTarea() {
            System.out.println(
                "El científico espacial trabaja en el área de " +
                areaEspecializacion + "."
            );
        }
    }

    static class IngenieroNave extends MiembroTripulacion {
        private final String certificacionMantenimiento;

        public IngenieroNave(String nombre, String rango, int Experiencia, String certificacionMantenimiento) {
            super(nombre, rango, Experiencia);
            this.certificacionMantenimiento = certificacionMantenimiento;
        }

        @Override
        public void realizarTarea() {
            System.out.println(
                "El ingeniero de nave realiza mantenimiento con certificación: " +
                certificacionMantenimiento + "."
            );
        }
    }

    public static void main(String[] args) {
        MiembroTripulacion tripulante = new MiembroTripulacion(
            "Alex", 
            "Sargento", 
            4
        );
        
        CientificoEspacial cientifico = new CientificoEspacial(
            "Elena",
            "Doctora",
            8,
            "Astrobiología"
        );

        IngenieroNave ingeniero = new IngenieroNave(
            "Marco",
            "Jefe Técnico",
            12,
            "Motores Warp"
        );

        tripulante.realizarTarea();
        cientifico.realizarTarea();
        ingeniero.realizarTarea();
    }
}