import tkinter as tk

ventana = tk.Tk()
ventana.title("Lista de tareas")
tareas = []

def agregar_tarea():
    texto = entrada.get()

    if texto == "":
        return

    variable = tk.IntVar()

    check = tk.Checkbutton(
        ventana,
        text=texto,
        variable=variable
    )

    check.grid(row=len(tareas) + 2, column=0, sticky="w")

    tareas.append((check, variable))

    entrada.delete(0, tk.END)

def eliminar_tareas_completadas():
    nuevas_tareas = []

    for check, variable in tareas:
        if variable.get() == 1:
            check.destroy()
        else:
            nuevas_tareas.append((check, variable))

    tareas.clear()
    tareas.extend(nuevas_tareas)

    for i, (check, variable) in enumerate(tareas):
        check.grid(row=i + 2, column=0, sticky="w")

etiqueta = tk.Label(ventana, text="Ingrese una tarea:")
etiqueta.grid(row=0, column=0)

entrada = tk.Entry(ventana)
entrada.grid(row=0, column=1)

boton_agregar = tk.Button(ventana, text="Agregar", command=agregar_tarea)
boton_agregar.grid(row=0, column=2)

boton_eliminar = tk.Button(
    ventana,
    text="Eliminar completadas",
    command=eliminar_tareas_completadas
)
boton_eliminar.grid(row=1, column=0, columnspan=3)

ventana.mainloop()