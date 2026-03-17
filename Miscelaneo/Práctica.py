import os

class Turno:
    def __init__(self, codigo, nombre, especialidad):
        self.codigo = codigo
        self.nombre = nombre
        self.especialidad = especialidad
        self.estado = "pendiente"

    def __str__(self):
        return f"Código: {self.codigo} | Nombre: {self.nombre} | Especialidad: {self.especialidad} | Estado: {self.estado}"

class SistemaClínica:
    def __init__(self):
        self.cola_pacientes = []
        self.en_atencion = []
        self.atendidos = []
        self.archivo = "pacientes_atendidos.txt"
        
        if os.path.exists(self.archivo):
            self.cargar_archivo()

    # ----------- REGISTRO DE PACIENTES -----------
    def registrar_paciente(self, codigo, nombre, especialidad):
        t = Turno(codigo, nombre, especialidad)
        self.cola_pacientes.append(t)
        print("Paciente registrado correctamente.")

    # ----------- CONSULTAS / VISUALIZACION -----------
    def mostrar_cola(self):
        print(f"\nPacientes en cola: {len(self.cola_pacientes)}")
        for t in self.cola_pacientes:
            print(t)

    def siguiente_paciente(self):
        if len(self.cola_pacientes) == 0:
            print("No hay pacientes pendientes.")
        else:
            print("Siguiente paciente a atender:")
            print(self.cola_pacientes[0])

    def buscar_por_codigo(self, codigo):
        for t in self.cola_pacientes:
            if t.codigo == codigo:
                return t
        for t in self.en_atencion:
            if t.codigo == codigo:
                return t
        for t in self.atendidos:
            if t.codigo == codigo:
                return t
        return None

    # ----------- MANEJO DE ESTADOS -----------
    def pasar_a_atencion(self):
        if len(self.cola_pacientes) == 0:
            print("No hay pacientes para atender.")
            return None
        t = self.cola_pacientes.pop(0)
        t.estado = "en atención"
        self.en_atencion.append(t)
        print(f"Turno {t.codigo} ahora está siendo atendido.")
        return t

    def marcar_atendido(self, turno):
        turno.estado = "atendido"
        self.en_atencion.pop(0)
        self.atendidos.append(turno)
        self.guardar_archivo()
        print(f"Turno {turno.codigo} completado y registrado.")

    # ----------- REPORTES -----------
    def total_atendidos(self):
        print(f"Total atendidos: {len(self.atendidos)}")

    # ----------- ARCHIVOS -----------
    def guardar_archivo(self):
        with open(self.archivo, "w") as f:
            for t in self.atendidos:
                f.write(f"{t.codigo},{t.nombre},{t.especialidad},{t.estado}\n")

    def cargar_archivo(self):
        with open(self.archivo, "r") as f:
            for linea in f:
                codigo, nombre, especialidad, estado = linea.strip().split(",")
                t = Turno(codigo, nombre, especialidad)
                t.estado = estado
                self.atendidos.append(t)

    def listar_pendientes_ordenados(self, asc=True):
        lista = sorted(self.cola_pacientes, key=lambda t: t.nombre, reverse=not asc)
        for t in lista:
            print(t)

# ==============================
#         MENÚ PRINCIPAL
# ==============================
def menu():
    sistema = SistemaClínica()

    while True:
        print("\n--- CLINICA ---")
        print("1. Registrar turno")
        print("2. Ver cola de turnos")
        print("3. Ver siguiente turno")
        print("4. Pasar turno a en atencion")
        print("5. Marcar turno en atencion como atendido")
        print("6. Buscar turno por código")
        print("7. Ver total atendido")
        print("8. Ordenar de A-Z")
        print("9. Ordenar de Z-A")
        print("0. Salir")

        op = input("Opción: ")

        if op == "1":
            c = input("Código: ")
            n = input("Nombre: ")
            e = input("Especialidad: ")
            sistema.registrar_paciente(c, n, e)

        elif op == "2":
            sistema.mostrar_cola()

        elif op == "3":
            sistema.siguiente_paciente()

        elif op == "4":
            sistema.pasar_a_atencion()

        elif op == "5":
            codigo = input("Código del paciente en atencion: ")
            t = sistema.buscar_por_codigo(codigo)
            if t and t.estado == "en atención":
                sistema.marcar_atendido(t)
            else:
                print("Ese paciente no está en atencion.")

        elif op == "6":
            c = input("Código a buscar: ")
            t = sistema.buscar_por_codigo(c)
            if t:
                print(t)
            else:
                print("Paciente no encontrado.")

        elif op == "7":
            sistema.total_atendidos()

        elif op == "8":
            sistema.listar_pendientes_ordenados(True)

        elif op == "9":
            sistema.listar_pendientes_ordenados(False)

        elif op == "0":
            print("Saliendo...")
            break

        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()
