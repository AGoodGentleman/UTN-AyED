import tkinter as tk
import random as random

ventana = tk.Tk()
def adivinar():
    global target
    global number
    number = int(entrada.get())
    if number == target:
        etiqueta2.config(text=f"¡Acertaste! Mí número era {target}.")
        etiqueta1.config(text=f"¡Felicitaciones!")
    elif number > target:
        etiqueta2.config(text="No no, es menor a ese número.")
        etiqueta1.config(text=f"Ingrese un número menor a {number} y mayor a 1.")
    elif number < target:
        etiqueta2.config(text="No no, es mayor a ese número.")
        etiqueta1.config(text=f"Ingrese un número mayor a {number} y menor a 100.")
global target
global number
target = random.randint(1,100)
number = 0
etiqueta1 = tk.Label(ventana, text="Ingrese un número entre 1 y 100:")
etiqueta1.grid(column=1, row=0)
entrada = tk.Entry(ventana)
entrada.grid(column=1, row=10)
boton = tk.Button(ventana, text="Adivinar", command=adivinar)
boton.grid(column=1, row=20)
etiqueta2 = tk.Label(ventana, text="...")
etiqueta2.grid(column=1, row=30)
ventana.mainloop()