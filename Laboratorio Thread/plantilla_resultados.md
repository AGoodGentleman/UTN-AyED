# Laboratorio Thread - Resultados

Completar esta plantilla despues de ejecutar `ejecutar_comparacion.py`.

## Datos de la prueba

- Rango usado: `[10_000_000, 10_100_000)`
- CPU logicos detectados:
- Cantidad de hilos usada:
- Cantidad de procesos usada:

## Tabla comparativa

| Version | Trabajadores | Primos encontrados | Tiempo (s) | Speedup |
|---|---:|---:|---:|---:|
| Secuencial | 1 | | | 1.00x |
| Threading | | | | |
| Multiprocessing | | | | |

## Conclusion

Escribir entre 3 y 5 lineas. Conviene mencionar:

- La tarea es CPU-bound porque casi todo el tiempo se usa en calculo.
- En CPython, los hilos comparten el GIL, por eso threading no suele acelerar este caso.
- Los procesos tienen interpretes separados y GIL separados, por eso multiprocessing puede usar varios nucleos.
- El speedup real puede ser menor que la cantidad de nucleos por el costo de crear procesos y repartir trabajo.
