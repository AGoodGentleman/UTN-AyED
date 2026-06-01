import tkinter as tk

ventana = tk.Tk()
def agregar():
    texto = entrada.get()
    lista.insert(tk.END, texto)
    entrada.delete(0, tk.END)
entrada = tk.Entry(ventana)
entrada.pack()
boton = tk.Button(ventana, text="Agregar", command=agregar)
boton.pack()
lista = tk.Listbox(ventana)
lista.pack()
ventana.mainloop()