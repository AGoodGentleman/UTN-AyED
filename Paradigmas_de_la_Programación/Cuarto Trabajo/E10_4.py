import tkinter as tk

ventana = tk.Tk()
ventana.title("Calculadora")
expresion = ""

def agregar(valor):
    global expresion
    expresion += valor
    display.config(text=expresion)

def calcular():
    global expresion

    try:
        resultado = eval(expresion)
        display.config(text=str(resultado))
        expresion = str(resultado)
    except:
        display.config(text="Error")
        expresion = ""

def borrar():
    global expresion
    expresion = ""
    display.config(text="0")

display = tk.Label(ventana, text="0", width=25)
display.grid(row=0, column=0, columnspan=4)

tk.Button(ventana, text="7", command=lambda: agregar("7")).grid(row=1, column=0)
tk.Button(ventana, text="8", command=lambda: agregar("8")).grid(row=1, column=1)
tk.Button(ventana, text="9", command=lambda: agregar("9")).grid(row=1, column=2)
tk.Button(ventana, text="/", command=lambda: agregar("/")).grid(row=1, column=3)

tk.Button(ventana, text="4", command=lambda: agregar("4")).grid(row=2, column=0)
tk.Button(ventana, text="5", command=lambda: agregar("5")).grid(row=2, column=1)
tk.Button(ventana, text="6", command=lambda: agregar("6")).grid(row=2, column=2)
tk.Button(ventana, text="x", command=lambda: agregar("*")).grid(row=2, column=3)

tk.Button(ventana, text="1", command=lambda: agregar("1")).grid(row=3, column=0)
tk.Button(ventana, text="2", command=lambda: agregar("2")).grid(row=3, column=1)
tk.Button(ventana, text="3", command=lambda: agregar("3")).grid(row=3, column=2)
tk.Button(ventana, text="-", command=lambda: agregar("-")).grid(row=3, column=3)

tk.Button(ventana, text="0", command=lambda: agregar("0")).grid(row=4, column=0)
tk.Button(ventana, text="C", command=borrar).grid(row=4, column=1)
tk.Button(ventana, text="=", command=calcular).grid(row=4, column=2)
tk.Button(ventana, text="+", command=lambda: agregar("+")).grid(row=4, column=3)

ventana.mainloop()