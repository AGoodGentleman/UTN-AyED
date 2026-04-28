import tkinter as tk
import random

ventana = tk.Tk()
ventana.title("Busca Letras")
letras = ["A", "A", "B", "B", "C", "C", "D", "D", "E", "E", "F", "F"]
random.shuffle(letras)
botones = []
seleccionados = []
encontrados = []

def presionar(indice):
    if indice in encontrados:
        return

    if indice in seleccionados:
        return

    if len(seleccionados) == 2:
        return

    botones[indice].config(text=letras[indice])
    seleccionados.append(indice)

    if len(seleccionados) == 2:
        ventana.after(1000, verificar)

def verificar():
    global seleccionados

    indice1 = seleccionados[0]
    indice2 = seleccionados[1]

    if letras[indice1] == letras[indice2]:
        encontrados.append(indice1)
        encontrados.append(indice2)

        botones[indice1].config(state="disabled")
        botones[indice2].config(state="disabled")
    else:
        botones[indice1].config(text="?")
        botones[indice2].config(text="?")

    seleccionados = []

    if len(encontrados) == len(letras):
        etiqueta.config(text="¡Ganaste!")

for i in range(len(letras)):
    boton = tk.Button(
        ventana,
        text="?",
        width=6,
        height=3,
        command=lambda i=i: presionar(i)
    )

    fila = i // 4
    columna = i % 4

    boton.grid(row=fila, column=columna)

    botones.append(boton)

etiqueta = tk.Label(ventana, text="")
etiqueta.grid(row=4, column=0, columnspan=4)

ventana.mainloop()