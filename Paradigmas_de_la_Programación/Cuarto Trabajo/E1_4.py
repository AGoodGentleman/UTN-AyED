import tkinter as tk

ventana = tk.Tk()
def funcion():
    etiqueta.config(text="¡Hola Mundo!")
    pass
etiqueta = tk.Label(ventana, text="...")
etiqueta.grid(column=1, row=0)
boton = tk.Button(ventana, text="Saludar", command=funcion)
boton.grid(column=11, row=0)
ventana.mainloop()