import tkinter as tk

ventana = tk.Tk()
def confirmar():
    global name
    global surname
    global email
    global pword
    name = entrada1.get()
    surname = entrada2.get()
    email = entrada3.get()
    pword = entrada4.get()
    mensaje(name, surname, email, pword)
def mensaje(name, surname, email, pword):
    etiqueta5 = tk.Label(ventana, text=f"Su nombre es {name}.")
    etiqueta5.grid(column=50, row=0)
    etiqueta6 = tk.Label(ventana, text=f"Su apellido es {surname}.")
    etiqueta6.grid(column=50, row=10)
    etiqueta7 = tk.Label(ventana, text=f"Su email es {email}.")
    etiqueta7.grid(column=50, row=20)
    etiqueta8 = tk.Label(ventana, text=f"Su contraseña es {pword}.")
    etiqueta8.grid(column=50, row=30)
global name
global surname
global email
global pword
name = ""
surname = ""
email = ""
pword = ""
etiqueta1 = tk.Label(ventana, text="Nombre:")
etiqueta1.grid(column=1, row=0)
etiqueta2 = tk.Label(ventana, text="Apellido:")
etiqueta2.grid(column=1, row=10)
etiqueta3 = tk.Label(ventana, text="Email:")
etiqueta3.grid(column=1, row=20)
etiqueta4 = tk.Label(ventana, text="Contraseña:")
etiqueta4.grid(column=1, row=30)
etiqueta5 = None
etiqueta6 = None
etiqueta7 = None
etiqueta8 = None
entrada1 = tk.Entry(ventana)
entrada1.grid(column=15, row=0)
entrada2 = tk.Entry(ventana)
entrada2.grid(column=15, row=10)
entrada3 = tk.Entry(ventana)
entrada3.grid(column=15, row=20)
entrada4 = tk.Entry(ventana, show="*")
entrada4.grid(column=15, row=30)
boton = tk.Button(ventana, text="Enviar", command=confirmar)
boton.grid(column=15, row=40)
ventana.mainloop()