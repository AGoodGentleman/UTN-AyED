import tkinter as tk

ventana = tk.Tk()
ventana.title("Mini Paint")
color_actual = "black"
x_anterior = None
y_anterior = None

def cambiar_color(nuevo_color):
    global color_actual
    color_actual = nuevo_color

def empezar_dibujo(evento):
    global x_anterior, y_anterior
    x_anterior = evento.x
    y_anterior = evento.y

def dibujar(evento):
    global x_anterior, y_anterior

    canvas.create_line(
        x_anterior,
        y_anterior,
        evento.x,
        evento.y,
        fill=color_actual,
        width=3
    )

    x_anterior = evento.x
    y_anterior = evento.y

def limpiar():
    canvas.delete("all")

canvas = tk.Canvas(ventana, width=600, height=400, bg="white")
canvas.grid(row=0, column=0, columnspan=5)

boton_negro = tk.Button(ventana, text="Negro", command=lambda: cambiar_color("black"))
boton_negro.grid(row=1, column=0)

boton_rojo = tk.Button(ventana, text="Rojo", command=lambda: cambiar_color("red"))
boton_rojo.grid(row=1, column=1)

boton_verde = tk.Button(ventana, text="Verde", command=lambda: cambiar_color("green"))
boton_verde.grid(row=1, column=2)

boton_azul = tk.Button(ventana, text="Azul", command=lambda: cambiar_color("blue"))
boton_azul.grid(row=1, column=3)

boton_limpiar = tk.Button(ventana, text="Limpiar", command=limpiar)
boton_limpiar.grid(row=1, column=4)

canvas.bind("<Button-1>", empezar_dibujo)
canvas.bind("<B1-Motion>", dibujar)

ventana.mainloop()