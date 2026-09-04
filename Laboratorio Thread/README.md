# Laboratorio Thread

Codigos para comparar concurrencia y paralelismo en Python:

- `secuencial.py`: linea base, un solo flujo de ejecucion.
- `threading_primos.py`: divide el rango entre varios hilos.
- `multiprocessing_primos.py`: divide el rango entre varios procesos.
- `ejecutar_comparacion.py`: corre las tres versiones y calcula speedup.
- `comunes.py`: funciones compartidas por todas las versiones.
- `plantilla_resultados.md`: tabla para completar el informe.

## Como ejecutar

Abrir una terminal dentro de esta carpeta:

```powershell
cd "C:\Users\lvbla\OneDrive\Escritorio\Universidad - 1er Año\Trabajos\UTN-AyED\Laboratorio Thread"
```

Prueba rapida con un rango chico:

```powershell
python ejecutar_comparacion.py --inicio 100000 --fin 105000 --hilos 4 --procesos 4
```

Ejecucion del laboratorio con el rango propuesto:

```powershell
python ejecutar_comparacion.py
```

Si los tiempos salen muy chicos y las diferencias no se notan, aumentar el
rango manteniendo el mismo inicio aproximado:

```powershell
python ejecutar_comparacion.py --inicio 10000000 --fin 11000000 --hilos 4 --procesos 4
```

En Windows, crear procesos suele tener mas costo que en Linux porque se usa
`spawn`. Por eso, si el trabajo total es pequeno, `multiprocessing` puede no
mostrar mejora aunque tecnicamente permita paralelismo real.

Tambien se puede ejecutar cada version por separado:

```powershell
python secuencial.py
python threading_primos.py --hilos 4
python multiprocessing_primos.py
```

## Que mide cada version

### Secuencial

Recorre todo el rango `[RANGO_INICIO, RANGO_FIN)` y llama a `es_primo(n)`
para cada numero. Es la referencia contra la cual se calculan los speedups.

### Threading

Parte el rango en sub-rangos y crea un `threading.Thread` por cada parte.
Cada hilo guarda su resultado parcial en una posicion propia de una lista
compartida. No se usa `Lock` porque no hay dos hilos escribiendo la misma
posicion.

En CPython, este caso no deberia acelerar demasiado porque la tarea es
CPU-bound y los hilos comparten el GIL: aunque existan varios hilos, solo
uno puede ejecutar bytecode Python a la vez.

### Multiprocessing

Parte el rango de la misma forma, pero crea procesos con
`multiprocessing.Process`. Como los procesos no comparten memoria, cada hijo
manda su resultado parcial al proceso principal usando una `Queue`.

Esta version si puede mejorar en tareas CPU-bound porque cada proceso tiene
su propio interprete de Python y su propio GIL. La mejora se nota mas cuando
el trabajo por proceso es suficientemente grande como para compensar el costo
de crear procesos y comunicar resultados.

## Formula de speedup

```text
speedup = T_secuencial / T_version
```

Ejemplo: si la version secuencial tarda 20 s y multiprocessing tarda 6 s:

```text
speedup = 20 / 6 = 3.33x
```

## Nota para Windows

En Windows, `multiprocessing` usa el metodo `spawn`. Por eso el codigo que
crea procesos esta protegido con:

```python
if __name__ == "__main__":
    main()
```

Sin esa proteccion, cada proceso hijo podria volver a importar el archivo y
crear mas procesos de manera recursiva.
