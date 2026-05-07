import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

ventana = tk.Tk()
ventana.title("Liquidación de Sueldos")
ventana.geometry("450x600")

def calcular():

    try:
        antiguedad = int(entrada_antiguedad.get())

        categoria = combo_categoria.get()

        horas = float(entrada_horas.get())
        valor_hora = float(entrada_valor_hora.get())

        horas_extra = float(entrada_horas_extra.get())
        valor_extra = float(entrada_valor_extra.get())

        beneficios = float(entrada_beneficios.get())

        if categoria == "A":
            base_categoria = 5000
        elif categoria == "B":
            base_categoria = 7000
        elif categoria == "C":
            base_categoria = 9000
        else:
            messagebox.showerror("Error", "Seleccione una categoría")
            return

        sueldo_base = base_categoria + (antiguedad * 200)

        sueldo_normal = horas * valor_hora

        sueldo_extra = horas_extra * valor_extra

        sueldo_bruto = (
            sueldo_base +
            sueldo_normal +
            sueldo_extra +
            beneficios
        )

        jubilacion = sueldo_bruto * 0.11
        obra_social = sueldo_bruto * 0.03
        sindicato = sueldo_bruto * 0.02

        descuentos_totales = (
            jubilacion +
            obra_social +
            sindicato
        )

        sueldo_neto = sueldo_bruto - descuentos_totales

        resultado.config(
            text=
            f"Sueldo Bruto: ARS ${sueldo_bruto:.2f}\n\n"
            f"Aporte Jubilatorio (11%): ARS ${jubilacion:.2f}\n"
            f"Obra Social (3%): ARS ${obra_social:.2f}\n"
            f"Aporte Sindicato (2%): ARS ${sindicato:.2f}\n\n"
            f"Descuentos Totales: ARS ${descuentos_totales:.2f}\n\n"
            f"Sueldo Neto: ARS ${sueldo_neto:.2f}"
        )

    except ValueError:
        messagebox.showerror(
            "Error",
            "Ingrese solamente números válidos"
        )

tk.Label(ventana, text="Antigüedad (años)").pack()

entrada_antiguedad = tk.Entry(ventana)
entrada_antiguedad.pack()

tk.Label(ventana, text="Categoría").pack()

combo_categoria = ttk.Combobox(
    ventana,
    values=["A", "B", "C"]
)

combo_categoria.pack()

tk.Label(ventana, text="Horas trabajadas").pack()

entrada_horas = tk.Entry(ventana)
entrada_horas.pack()

tk.Label(ventana, text="Valor por hora").pack()

entrada_valor_hora = tk.Entry(ventana)
entrada_valor_hora.pack()

tk.Label(ventana, text="Horas extra").pack()

entrada_horas_extra = tk.Entry(ventana)
entrada_horas_extra.pack()

tk.Label(ventana, text="Valor por hora extra").pack()

entrada_valor_extra = tk.Entry(ventana)
entrada_valor_extra.pack()

tk.Label(ventana, text="Otros beneficios").pack()

entrada_beneficios = tk.Entry(ventana)
entrada_beneficios.pack()

boton = tk.Button(
    ventana,
    text="Calcular Sueldo",
    command=calcular
)

boton.pack(pady=10)

resultado = tk.Label(
    ventana,
    text="",
    justify="left",
    font=("Arial", 10)
)

resultado.pack(pady=20)

ventana.mainloop()