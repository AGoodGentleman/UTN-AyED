import tkinter as tk
from tkinter import filedialog

ventana = tk.Tk()
ventana.title("Mini Bloc")
ventana.geometry("600x400")

def guardar_archivo():
    archivo = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Archivos de texto", "*.txt")]
    )

    if archivo:
        contenido = texto.get("1.0", tk.END)

        with open(archivo, "w", encoding="utf-8") as f:
            f.write(contenido)

def abrir_archivo():
    archivo = filedialog.askopenfilename(
        filetypes=[("Archivos de texto", "*.txt")]
    )

    if archivo:
        with open(archivo, "r", encoding="utf-8") as f:
            contenido = f.read()

        texto.delete("1.0", tk.END)
        texto.insert("1.0", contenido)

texto = tk.Text(ventana, width=70, height=20)
texto.grid(row=0, column=0, columnspan=2)

boton_guardar = tk.Button(ventana, text="Guardar", command=guardar_archivo)
boton_guardar.grid(row=1, column=0)

boton_abrir = tk.Button(ventana, text="Abrir", command=abrir_archivo)
boton_abrir.grid(row=1, column=1)

ventana.mainloop()