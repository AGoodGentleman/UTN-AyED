import tkinter as tk

ventana = tk.Tk()
def confirmar():
    nombre = entrada1.get()
    edad_txt = entrada2.get()
    email = entrada3.get()
    password = entrada4.get()

    try:
        if not nombre.isalpha():
            raise ValueError("El nombre debe tener solo letras.")

        edad = int(edad_txt)
        if edad <= 0 or edad >= 150:
            raise ValueError("Edad inválida.")

        if email.count("@") != 1 or "." not in email.split("@")[1]:
            raise ValueError("Email inválido.")

        if len(password) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres.")

        resultado.config(text="Registro exitoso")

    except Exception as e:
        resultado.config(text=str(e))

etiqueta1 = tk.Label(ventana, text="Nombre:")
etiqueta1.grid(column=0, row=0)

etiqueta2 = tk.Label(ventana, text="Edad:")
etiqueta2.grid(column=0, row=1)

etiqueta3 = tk.Label(ventana, text="Email:")
etiqueta3.grid(column=0, row=2)

etiqueta4 = tk.Label(ventana, text="Contraseña:")
etiqueta4.grid(column=0, row=3)

entrada1 = tk.Entry(ventana)
entrada1.grid(column=1, row=0)

entrada2 = tk.Entry(ventana)
entrada2.grid(column=1, row=1)

entrada3 = tk.Entry(ventana)
entrada3.grid(column=1, row=2)

entrada4 = tk.Entry(ventana, show="*")
entrada4.grid(column=1, row=3)

boton = tk.Button(ventana, text="Enviar", command=confirmar)
boton.grid(column=1, row=4)

resultado = tk.Label(ventana, text="")
resultado.grid(column=0, row=5, columnspan=2)

ventana.mainloop()