from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class Proceso:
    pid: str
    tamano: int
    paginas: int
    marcos: List[int]


class SimuladorParticionFija:
    def __init__(self, cantidad_marcos: int, tamano_marco: int):
        self.cantidad_marcos = cantidad_marcos
        self.tamano_marco = tamano_marco
        self.marcos = [None] * cantidad_marcos
        self.procesos: Dict[str, Proceso] = {}

    def calcular_paginas(self, tamano_proceso: int) -> int:
        return (tamano_proceso + self.tamano_marco - 1) // self.tamano_marco

    def marcos_libres(self) -> List[int]:
        return [indice for indice, marco in enumerate(self.marcos) if marco is None]

    def crear_proceso(self, pid: str, tamano: int) -> Tuple[bool, str]:
        if pid in self.procesos:
            return False, "Ya existe un proceso con ese nombre."

        paginas_necesarias = self.calcular_paginas(tamano)
        libres = self.marcos_libres()

        if paginas_necesarias > len(libres):
            return (
                False,
                "No hay suficientes marcos libres. "
                f"Necesita {paginas_necesarias} y hay {len(libres)}.",
            )

        marcos_asignados = libres[:paginas_necesarias]
        for pagina, marco in enumerate(marcos_asignados):
            usado = min(self.tamano_marco, tamano - pagina * self.tamano_marco)
            self.marcos[marco] = {
                "pid": pid,
                "pagina": pagina,
                "usado": usado,
            }

        self.procesos[pid] = Proceso(pid, tamano, paginas_necesarias, marcos_asignados)
        desperdicio = paginas_necesarias * self.tamano_marco - tamano
        return (
            True,
            f"Proceso {pid} creado: {tamano} unidades, "
            f"{paginas_necesarias} pagina(s), marcos {marcos_asignados}. "
            f"Fragmentacion interna: {desperdicio}.",
        )

    def liberar_proceso(self, pid: str) -> Tuple[bool, str]:
        proceso = self.procesos.get(pid)
        if proceso is None:
            return False, "No existe un proceso con ese nombre."

        for marco in proceso.marcos:
            self.marcos[marco] = None
        del self.procesos[pid]
        return True, f"Proceso {pid} liberado. Se recuperaron {proceso.paginas} marco(s)."

    def tabla_paginas(self, pid: str) -> Tuple[bool, str]:
        proceso = self.procesos.get(pid)
        if proceso is None:
            return False, "No existe un proceso con ese nombre."

        lineas = [
            f"Tabla de paginas del proceso {pid}",
            f"Tamano: {proceso.tamano} | Paginas: {proceso.paginas}",
            "-" * 31,
            f"{'Pagina':>10} -> {'Marco':<10}",
            "-" * 31,
        ]
        for pagina, marco in enumerate(proceso.marcos):
            lineas.append(f"{pagina:>10} -> {marco:<10}")
        return True, "\n".join(lineas)

    def estado_memoria(self) -> str:
        lineas = [
            "Estado de memoria - particion fija",
            f"Marcos: {self.cantidad_marcos} | Tamano de marco/pagina: {self.tamano_marco}",
            "-" * 72,
            f"{'Marco':>6} | {'Estado':<12} | {'Proceso':<12} | {'Pagina':<8} | {'Usado':<8}",
            "-" * 72,
        ]

        for indice, marco in enumerate(self.marcos):
            if marco is None:
                lineas.append(f"{indice:>6} | {'Libre':<12} | {'-':<12} | {'-':<8} | {'0':<8}")
            else:
                lineas.append(
                    f"{indice:>6} | {'Ocupado':<12} | {marco['pid']:<12} | "
                    f"{marco['pagina']:<8} | {marco['usado']:<8}"
                )

        libres = len(self.marcos_libres())
        ocupados = self.cantidad_marcos - libres
        lineas.extend(
            [
                "-" * 72,
                f"Marcos ocupados: {ocupados} | Marcos libres: {libres}",
                f"Memoria libre: {libres * self.tamano_marco} unidades",
            ]
        )
        return "\n".join(lineas)

    def listar_procesos(self) -> str:
        if not self.procesos:
            return "No hay procesos cargados."

        lineas = [
            "Procesos cargados",
            "-" * 70,
            f"{'Proceso':<12} | {'Tamano':>10} | {'Paginas':>8} | Marcos",
            "-" * 70,
        ]
        for proceso in self.procesos.values():
            lineas.append(
                f"{proceso.pid:<12} | {proceso.tamano:>10} | "
                f"{proceso.paginas:>8} | {proceso.marcos}"
            )
        return "\n".join(lineas)


def leer_entero_positivo(mensaje: str) -> int:
    while True:
        valor = input(mensaje).strip()
        try:
            numero = int(valor)
            if numero > 0:
                return numero
            print("Ingrese un numero entero mayor que cero.")
        except ValueError:
            print("Entrada invalida. Ingrese un numero entero.")


def leer_texto_no_vacio(mensaje: str) -> str:
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("El dato no puede estar vacio.")


def pausar() -> None:
    input("\nPresione Enter para continuar...")


def configurar_memoria() -> SimuladorParticionFija:
    print("\nCONFIGURACION INICIAL - PARTICION FIJA")
    cantidad_marcos = leer_entero_positivo("Cantidad de marcos: ")
    tamano_marco = leer_entero_positivo("Tamano de cada marco/pagina: ")
    return SimuladorParticionFija(cantidad_marcos, tamano_marco)


def mostrar_menu() -> None:
    print("\n" + "=" * 48)
    print("SIMULADOR DE MEMORIA - PARTICION FIJA")
    print("=" * 48)
    print("1. Crear proceso")
    print("2. Liberar proceso")
    print("3. Mostrar tabla de paginas de un proceso")
    print("4. Mostrar estado de memoria")
    print("5. Listar procesos")
    print("6. Reiniciar configuracion de memoria")
    print("0. Salir")


def main() -> None:
    simulador = configurar_memoria()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            pid = leer_texto_no_vacio("Nombre/ID del proceso: ")
            tamano = leer_entero_positivo("Tamano del proceso: ")
            _, mensaje = simulador.crear_proceso(pid, tamano)
            print("\n" + mensaje)
            pausar()

        elif opcion == "2":
            if not simulador.procesos:
                print("\nNo hay procesos para liberar.")
            else:
                print("\n" + simulador.listar_procesos())
                pid = leer_texto_no_vacio("Proceso a liberar: ")
                _, mensaje = simulador.liberar_proceso(pid)
                print("\n" + mensaje)
            pausar()

        elif opcion == "3":
            if not simulador.procesos:
                print("\nNo hay procesos cargados.")
            else:
                print("\n" + simulador.listar_procesos())
                pid = leer_texto_no_vacio("Proceso a consultar: ")
                _, mensaje = simulador.tabla_paginas(pid)
                print("\n" + mensaje)
            pausar()

        elif opcion == "4":
            print("\n" + simulador.estado_memoria())
            pausar()

        elif opcion == "5":
            print("\n" + simulador.listar_procesos())
            pausar()

        elif opcion == "6":
            simulador = configurar_memoria()
            print("\nConfiguracion reiniciada. La memoria quedo vacia.")
            pausar()

        elif opcion == "0":
            print("\nFin del simulador.")
            break

        else:
            print("\nOpcion invalida.")
            pausar()


if __name__ == "__main__":
    main()
