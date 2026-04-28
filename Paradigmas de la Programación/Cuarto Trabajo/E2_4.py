import tkinter as tk

ventana = tk.Tk()
def funcion():
    nombre = entrada.get()
    etiqueta.config(text=f"Hola, {nombre}.")
etiqueta = tk.Label(ventana, text="...")
etiqueta.grid(column=1, row=0)
boton = tk.Button(ventana, text="Saludar", command=funcion)
boton.grid(column=11, row=10)
entrada = tk.Entry(ventana)
entrada.grid(column=1, row=10)
ventana.mainloop()