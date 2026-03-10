import os

# ==============================
#        CLASE PEDIDO
# ==============================
class Pedido:
    def __init__(self, codigo, cliente, monto):
        self.codigo = codigo
        self.cliente = cliente
        self.monto = monto
        self.estado = "pendiente"

    def __str__(self):
        return f"Código: {self.codigo} | Cliente: {self.cliente} | Monto: ${self.monto} | Estado: {self.estado}"


# ==============================
#    CLASE SISTEMA CAFETERIA
# ==============================
class SistemaCafeteria:
    def __init__(self):
        self.cola_pedidos = []        # cola de pendientes (FIFO)
        self.entregados = []          # historial de pedidos entregados
        self.archivo = "pedidos_entregados.txt"

        # si existe archivo, lo carga
        if os.path.exists(self.archivo):
            self.cargar_archivo()

    # ----------- REGISTRO DE PEDIDOS -----------
    def registrar_pedido(self, codigo, cliente, monto):
        p = Pedido(codigo, cliente, monto)
        self.cola_pedidos.append(p)
        print("Pedido registrado correctamente.")

    # ----------- CONSULTAS / VISUALIZACION -----------
    def mostrar_cola(self):
        print(f"\nPedidos en cola: {len(self.cola_pedidos)}")
        for p in self.cola_pedidos:
            print(p)

    def siguiente_pedido(self):
        if len(self.cola_pedidos) == 0:
            print("No hay pedidos pendientes.")
        else:
            print("Siguiente pedido a preparar:")
            print(self.cola_pedidos[0])

    def buscar_por_codigo(self, codigo):
        # buscar en cola
        for p in self.cola_pedidos:
            if p.codigo == codigo:
                return p
        # buscar en entregados
        for p in self.entregados:
            if p.codigo == codigo:
                return p
        return None

    # ----------- MANEJO DE ESTADOS -----------
    def pasar_a_preparacion(self):
        if len(self.cola_pedidos) == 0:
            print("No hay pedidos para preparar.")
            return None
        p = self.cola_pedidos.pop(0)
        p.estado = "en preparación"
        print(f"Pedido {p.codigo} ahora está en preparación.")
        return p

    def marcar_entregado(self, pedido):
        pedido.estado = "entregado"
        self.entregados.append(pedido)
        self.guardar_archivo()
        print(f"Pedido {pedido.codigo} entregado y registrado.")

    # ----------- REPORTES -----------
    def total_entregados(self):
        print(f"Total entregados: {len(self.entregados)}")

    def total_recaudado(self):
        total = sum(p.monto for p in self.entregados)
        print(f"Total recaudado: ${total}")

    def listar_pendientes_ordenados(self, asc=True):
        lista = sorted(self.cola_pedidos, key=lambda x: x.monto, reverse=not asc)
        for p in lista:
            print(p)

    # ----------- ARCHIVOS -----------
    def guardar_archivo(self):
        with open(self.archivo, "w") as f:
            for p in self.entregados:
                f.write(f"{p.codigo},{p.cliente},{p.monto},{p.estado}\n")

    def cargar_archivo(self):
        with open(self.archivo, "r") as f:
            for linea in f:
                codigo, cliente, monto, estado = linea.strip().split(",")
                p = Pedido(codigo, cliente, float(monto))
                p.estado = estado
                self.entregados.append(p)


# ==============================
#         MENÚ PRINCIPAL
# ==============================
def menu():
    sistema = SistemaCafeteria()

    while True:
        print("\n--- MENÚ CAFETERÍA ---")
        print("1. Registrar pedido")
        print("2. Ver cola de pedidos")
        print("3. Ver siguiente pedido")
        print("4. Pasar pedido a preparación")
        print("5. Marcar pedido en preparación como entregado")
        print("6. Buscar pedido por código")
        print("7. Ver total entregados")
        print("8. Ver total recaudado")
        print("9. Ordenar pendientes por monto (ascendente)")
        print("10. Ordenar pendientes por monto (descendente)")
        print("0. Salir")

        op = input("Opción: ")

        if op == "1":
            c = input("Código: ")
            cl = input("Cliente: ")
            try:
                m = float(input("Monto: "))
            except:
                print("Monto inválido.")
                continue
            sistema.registrar_pedido(c, cl, m)

        elif op == "2":
            sistema.mostrar_cola()

        elif op == "3":
            sistema.siguiente_pedido()

        elif op == "4":
            sistema.pasar_a_preparacion()

        elif op == "5":
            codigo = input("Código del pedido en preparación: ")
            p = sistema.buscar_por_codigo(codigo)
            if p and p.estado == "en preparación":
                sistema.marcar_entregado(p)
            else:
                print("Ese pedido no está en preparación.")

        elif op == "6":
            c = input("Código a buscar: ")
            p = sistema.buscar_por_codigo(c)
            if p:
                print(p)
            else:
                print("Pedido no encontrado.")

        elif op == "7":
            sistema.total_entregados()

        elif op == "8":
            sistema.total_recaudado()

        elif op == "9":
            sistema.listar_pendientes_ordenados(asc=True)

        elif op == "10":
            sistema.listar_pendientes_ordenados(asc=False)

        elif op == "0":
            print("Saliendo...")
            break

        else:
            print("Opción no válida.")


# ==============================
#      EJECUCIÓN DEL PROGRAMA
# ==============================
if __name__ == "__main__":
    menu()
