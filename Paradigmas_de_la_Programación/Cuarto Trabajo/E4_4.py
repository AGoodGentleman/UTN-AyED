import tkinter as tk

ventana = tk.Tk()
def color(pick):
    if pick == "red":
        ventana.config(background="red")
    elif pick == "green":
        ventana.config(background="green")
    elif pick == "blue":
        ventana.config(background="blue")
boton1 = tk.Button(ventana, text="Rojo", command=lambda: color("red"))
boton1.grid(column=1, row=10)
boton2 = tk.Button(ventana, text="Verde", command=lambda: color("green"))
boton2.grid(column=1, row=20)
boton3 = tk.Button(ventana, text="Azul", command=lambda: color("blue"))
boton3.grid(column=1, row=30)
ventana.mainloop()