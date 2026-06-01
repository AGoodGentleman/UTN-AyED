import tkinter as tk

ventana = tk.Tk()
def calcular():
    global result
    cm = float(entrada2.get()) / 100
    sqr = cm ** 2
    result = float(entrada1.get()) / sqr
    etiqueta3.config(text=f"Su IMC es {result:.2f}.")
    if result >= 25:
        etiqueta4.config(text="Usted tiene sobrepeso.")
    elif result <= 18.4:
        etiqueta4.config(text="Usted tiene delgadez.")
    else:
        etiqueta4.config(text="Usted tiene un peso saludable.")
global result
result = 0.0
etiqueta1 = tk.Label(ventana, text="Peso (kg):")
etiqueta1.grid(column=1, row=0)
etiqueta2 = tk.Label(ventana, text="Altura (cm):")
etiqueta2.grid(column=1, row=10)
entrada1 = tk.Entry(ventana)
entrada1.grid(column=11, row=0)
entrada2 = tk.Entry(ventana)
entrada2.grid(column=11, row=10)
etiqueta3 = tk.Label(ventana, text="")
etiqueta3.grid(column=1, row=30)
etiqueta4 = tk.Label(ventana, text="")
etiqueta4.grid(column=1, row=40)
boton = tk.Button(ventana, text="Calcular", command=calcular)
boton.grid(column=11, row=20)
ventana.mainloop()