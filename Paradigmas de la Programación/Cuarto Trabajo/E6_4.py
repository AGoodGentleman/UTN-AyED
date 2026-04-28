import tkinter as tk

ventana = tk.Tk()
def convert():
    global value
    value = float(entrada.get()) * 9 / 5 + 32
    etiqueta2.config(text=f"Grados Fahrenheit: {value}")
global value
value = 0.0
etiqueta1 = tk.Label(ventana, text="Grados Celsius:")
etiqueta1.grid(column=15, row=0)
entrada = tk.Entry(ventana)
entrada.grid(column=15, row=10)
boton = tk.Button(ventana, text="Convertir", command=convert)
boton.grid(column=15, row=20)
etiqueta2 = tk.Label(ventana, text=f"Grados Fahrenheit: {value}")
etiqueta2.grid(column=15, row=40)
ventana.mainloop()