import tkinter as tk

ventana = tk.Tk()
def add():
    global value
    a = int(entrada1.get())
    b = int(entrada2.get())
    etiqueta.config(text=f"Suma = {a+b}")
global value
value = 0
etiqueta = tk.Label(ventana, text=f"Suma = {value}")
etiqueta.grid(column=15, row=0)
boton = tk.Button(ventana, text="Sumar", command=add)
boton.grid(column=15, row=20)
entrada1 = tk.Entry(ventana)
entrada1.grid(column=11, row=10)
entrada2 = tk.Entry(ventana)
entrada2.grid(column=21, row=10)
ventana.mainloop()