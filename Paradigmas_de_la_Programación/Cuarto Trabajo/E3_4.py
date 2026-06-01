import tkinter as tk

ventana = tk.Tk()
def add():
    global value
    value+=1
    etiqueta.config(text=f"{value}")
def sub():
    global value
    value-=1
    etiqueta.config(text=f"{value}")
global value
value = 0
etiqueta = tk.Label(ventana, text=f"{value}")
etiqueta.grid(column=1, row=0)
boton1 = tk.Button(ventana, text="Sumar", command=add)
boton1.grid(column=1, row=10)
boton2 = tk.Button(ventana, text="Restar", command=sub)
boton2.grid(column=1, row=20)
ventana.mainloop()