from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


ALGORITMOS = {
    "1": "first",
    "2": "best",
    "3": "next",
    "4": "worst",
    "first": "first",
    "best": "best",
    "next": "next",
    "worst": "worst",
}


@dataclass
class Proceso:
    pid: str
    tamano: int
    paginas: int
    inicio: int
    marcos: List[int]


class SimuladorParticionDinamica:
    def __init__(self, cantidad_marcos: int, tamano_marco: int):
        self.cantidad_marcos = cantidad_marcos
        self.tamano_marco = tamano_marco
        self.marcos = [None] * cantidad_marcos
        self.procesos: Dict[str, Proceso] = {}
        self.algoritmo = "first"
        self.proxima_busqueda = 0

    def calcular_paginas(self, tamano_proceso: int) -> int:
        return (tamano_proceso + self.tamano_marco - 1) // self.tamano_marco

    def cambiar_algoritmo(self, algoritmo: str) -> Tuple[bool, str]:
        algoritmo_normalizado = ALGORITMOS.get(algoritmo.strip().lower())
        if algoritmo_normalizado is None:
            return False, "Algoritmo invalido."
        self.algoritmo = algoritmo_normalizado
        return True, f"Algoritmo activo: {self.nombre_algoritmo()}."

    def nombre_algoritmo(self) -> str:
        nombres = {
            "first": "First Fit",
            "best": "Best Fit",
            "next": "Next Fit",
            "worst": "Worst Fit",
        }
        return nombres[self.algoritmo]

    def bloques_libres(self) -> List[Tuple[int, int]]:
        bloques = []
        inicio = None

        for indice, marco in enumerate(self.marcos):
            if marco is None and inicio is None:
                inicio = indice
            elif marco is not None and inicio is not None:
                bloques.append((inicio, indice - inicio))
                inicio = None

        if inicio is not None:
            bloques.append((inicio, self.cantidad_marcos - inicio))

        return bloques

    def seleccionar_bloque(
        self, paginas_necesarias: int
    ) -> Tuple[Optional[int], Optional[int]]:
        bloques = [
            (inicio, cantidad)
            for inicio, cantidad in self.bloques_libres()
            if cantidad >= paginas_necesarias
        ]

        if not bloques:
            return None, None

        if self.algoritmo == "first":
            return bloques[0]

        if self.algoritmo == "best":
            return min(bloques, key=lambda bloque: (bloque[1], bloque[0]))

        if self.algoritmo == "worst":
            return max(bloques, key=lambda bloque: (bloque[1], -bloque[0]))

        return self.seleccionar_bloque_next_fit(paginas_necesarias)

    def seleccionar_bloque_next_fit(
        self, paginas_necesarias: int
    ) -> Tuple[Optional[int], Optional[int]]:
        candidatos = []

        for inicio, cantidad in self.bloques_libres():
            fin = inicio + cantidad
            if fin <= self.proxima_busqueda:
                continue

            if inicio < self.proxima_busqueda < fin:
                candidatos.append((self.proxima_busqueda, fin - self.proxima_busqueda))
            elif inicio >= self.proxima_busqueda:
                candidatos.append((inicio, cantidad))

        for inicio, cantidad in self.bloques_libres():
            if inicio < self.proxima_busqueda:
                candidatos.append((inicio, cantidad))

        for inicio, cantidad in candidatos:
            if cantidad >= paginas_necesarias:
                return inicio, cantidad

        return None, None

    def crear_proceso(self, pid: str, tamano: int) -> Tuple[bool, str]:
        if pid in self.procesos:
            return False, "Ya existe un proceso con ese nombre."

        paginas_necesarias = self.calcular_paginas(tamano)
        inicio, cantidad_bloque = self.seleccionar_bloque(paginas_necesarias)

        if inicio is None:
            libres_totales = sum(cantidad for _, cantidad in self.bloques_libres())
            if libres_totales >= paginas_necesarias:
                return (
                    False,
                    "Hay memoria libre total suficiente, pero no en un bloque contiguo. "
                    "Eso representa fragmentacion externa.",
                )
            return (
                False,
                "No hay memoria suficiente. "
                f"Necesita {paginas_necesarias} marco(s) y hay {libres_totales}.",
            )

        marcos_asignados = list(range(inicio, inicio + paginas_necesarias))
        for pagina, marco in enumerate(marcos_asignados):
            usado = min(self.tamano_marco, tamano - pagina * self.tamano_marco)
            self.marcos[marco] = {
                "pid": pid,
                "pagina": pagina,
                "usado": usado,
            }

        self.procesos[pid] = Proceso(pid, tamano, paginas_necesarias, inicio, marcos_asignados)
        self.proxima_busqueda = (inicio + paginas_necesarias) % self.cantidad_marcos

        desperdicio = paginas_necesarias * self.tamano_marco - tamano
        sobrante_bloque = cantidad_bloque - paginas_necesarias
        return (
            True,
            f"Proceso {pid} creado con {self.nombre_algoritmo()}: "
            f"{tamano} unidades, {paginas_necesarias} pagina(s), "
            f"marcos {marcos_asignados}. "
            f"Fragmentacion interna: {desperdicio}. "
            f"Marcos libres que quedaron en el bloque elegido: {sobrante_bloque}.",
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
            f"Inicio del bloque asignado: marco {proceso.inicio}",
            "-" * 31,
            f"{'Pagina':>10} -> {'Marco':<10}",
            "-" * 31,
        ]
        for pagina, marco in enumerate(proceso.marcos):
            lineas.append(f"{pagina:>10} -> {marco:<10}")
        return True, "\n".join(lineas)

    def estado_memoria(self) -> str:
        lineas = [
            "Estado de memoria - particion dinamica",
            f"Marcos: {self.cantidad_marcos} | Tamano de marco/pagina: {self.tamano_marco}",
            f"Algoritmo activo: {self.nombre_algoritmo()} | Proxima busqueda Next Fit: {self.proxima_busqueda}",
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

        libres = sum(cantidad for _, cantidad in self.bloques_libres())
        ocupados = self.cantidad_marcos - libres
        lineas.extend(
            [
                "-" * 72,
                f"Marcos ocupados: {ocupados} | Marcos libres: {libres}",
                f"Memoria libre: {libres * self.tamano_marco} unidades",
                "",
                self.estado_bloques(),
            ]
        )
        return "\n".join(lineas)

    def estado_bloques(self) -> str:
        segmentos = []
        inicio = 0

        while inicio < self.cantidad_marcos:
            marco = self.marcos[inicio]
            if marco is None:
                estado = "Libre"
                pid = "-"
                fin = inicio
                while fin < self.cantidad_marcos and self.marcos[fin] is None:
                    fin += 1
            else:
                estado = "Ocupado"
                pid = marco["pid"]
                fin = inicio
                while (
                    fin < self.cantidad_marcos
                    and self.marcos[fin] is not None
                    and self.marcos[fin]["pid"] == pid
                ):
                    fin += 1

            segmentos.append((inicio, fin - 1, fin - inicio, estado, pid))
            inicio = fin

        lineas = [
            "Bloques contiguos",
            "-" * 66,
            f"{'Inicio':>8} | {'Fin':>8} | {'Marcos':>8} | {'Estado':<10} | {'Proceso':<12}",
            "-" * 66,
        ]
        for inicio, fin, cantidad, estado, pid in segmentos:
            lineas.append(f"{inicio:>8} | {fin:>8} | {cantidad:>8} | {estado:<10} | {pid:<12}")
        return "\n".join(lineas)

    def listar_procesos(self) -> str:
        if not self.procesos:
            return "No hay procesos cargados."

        lineas = [
            "Procesos cargados",
            "-" * 82,
            f"{'Proceso':<12} | {'Tamano':>10} | {'Paginas':>8} | {'Inicio':>8} | Marcos",
            "-" * 82,
        ]
        for proceso in self.procesos.values():
            lineas.append(
                f"{proceso.pid:<12} | {proceso.tamano:>10} | {proceso.paginas:>8} | "
                f"{proceso.inicio:>8} | {proceso.marcos}"
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


def configurar_memoria() -> SimuladorParticionDinamica:
    print("\nCONFIGURACION INICIAL - PARTICION DINAMICA")
    cantidad_marcos = leer_entero_positivo("Cantidad de marcos: ")
    tamano_marco = leer_entero_positivo("Tamano de cada marco/pagina: ")
    return SimuladorParticionDinamica(cantidad_marcos, tamano_marco)


def mostrar_menu() -> None:
    print("\n" + "=" * 52)
    print("SIMULADOR DE MEMORIA - PARTICION DINAMICA")
    print("=" * 52)
    print("1. Crear proceso")
    print("2. Liberar proceso")
    print("3. Mostrar tabla de paginas de un proceso")
    print("4. Mostrar estado de memoria")
    print("5. Listar procesos")
    print("6. Cambiar algoritmo de ubicacion")
    print("7. Reiniciar configuracion de memoria")
    print("0. Salir")


def mostrar_menu_algoritmos(simulador: SimuladorParticionDinamica) -> None:
    print("\nALGORITMOS DE UBICACION")
    print(f"Actual: {simulador.nombre_algoritmo()}")
    print("1. First Fit")
    print("2. Best Fit")
    print("3. Next Fit")
    print("4. Worst Fit")


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
            mostrar_menu_algoritmos(simulador)
            algoritmo = input("Seleccione algoritmo: ")
            _, mensaje = simulador.cambiar_algoritmo(algoritmo)
            print("\n" + mensaje)
            pausar()

        elif opcion == "7":
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
