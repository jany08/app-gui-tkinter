"""
Gestor de Información - Aplicación GUI (Tkinter)

INSTRUCCIONES RÁPIDAS (LEE ANTES DE EJECUTAR)
1) Esta es una aplicación de ejemplo que cumple con la tarea: ventana principal, labels,
   campo de texto, botones (Agregar, Limpiar entrada, Eliminar seleccionado, Limpiar todo)
   y una lista (Listbox) para mostrar los datos.

2) Requisitos: Python 3.x. Tkinter suele venir con Python en Windows y macOS. En Linux
   (Debian/Ubuntu) puede que necesites: sudo apt-get install python3-tk

3) Entorno virtual (recomendado): el enunciado menciona un entorno llamado 'CURSO PYTHON'.
   Puedes crear/activar uno así:

   Windows (PowerShell/CMD):
       python -m venv CURSO_PYTHON
       .\CURSO_PYTHON\Scripts\activate
       python --version

   macOS / Linux:
       python3 -m venv CURSO_PYTHON
       source CURSO_PYTHON/bin/activate

4) Ejecutar:
       python app_gui_tkinter.py
   (o Run -> en tu IDE como PyCharm con el intérprete del entorno virtual 'CURSO PYTHON')

5) Subir a GitHub:
   - Si ya tienes el repositorio local (Repositorio_Jany-UEA):
       cd ruta/al/Repositorio_Jany-UEA
       cp /ruta/al/archivo/app_gui_tkinter.py .
       git add app_gui_tkinter.py
       git commit -m "Tarea GUI: app Tkinter - gestor de información"
       git push origin main

   - Si no tienes el repo local:
       git clone https://github.com/<tu_usuario>/Repositorio_Jany-UEA.git
       cd Repositorio_Jany-UEA
       (pega o crea app_gui_tkinter.py aquí)
       git add app_gui_tkinter.py
       git commit -m "Tarea GUI: app Tkinter"
       git push -u origin main

------------------------------------------------------------------
NOTAS DE DISEÑO (por qué lo hice así):
- Uso una clase App para separar la lógica de la interfaz (mejor mantenibilidad).
- Botones claros con funciones separadas: agregar, limpiar entrada, eliminar seleccionado,
  limpiar todo.
- Mensajes al usuario con messagebox y una etiqueta de estado para feedback corto.
- Atajo: Enter en el campo de texto agrega un elemento; tecla Supr (Delete) elimina
  el elemento seleccionado.

PRUEBAS SUGERIDAS (CHECKLIST):
- Agregar un texto válido -> aparece en la lista.
- Intentar agregar texto vacío -> aparece advertencia.
- Seleccionar un elemento y pulsar "Eliminar seleccionado" -> desaparece.
- Pulsar "Limpiar todo" -> lista vacía.
- Pulsar Enter después de escribir -> agrega.
- Probar comportamiento al cerrar la ventana.

------------------------------------------------------------------
"""

import tkinter as tk
from tkinter import messagebox


class App(tk.Tk):
    """Aplicación principal - Gestor de Información"""

    def __init__(self):
        super().__init__()
        self.title("Gestor de Información - Tarea GUI")
        self.geometry("480x420")
        self.resizable(False, False)
        self.configure(padx=12, pady=12)

        # --- Widgets ---
        # Etiqueta instructiva
        self.label_instruccion = tk.Label(self, text="Ingrese información:", font=("Arial", 12))
        self.label_instruccion.pack(anchor="w")

        # Campo de texto para la entrada
        self.entrada_texto = tk.Entry(self, width=50)
        self.entrada_texto.pack(pady=(6, 8), anchor="w")
        self.entrada_texto.focus()

        # Asociar la tecla Enter para agregar
        self.entrada_texto.bind("<Return>", lambda event: self.agregar_dato())

        # Frame para botones
        botones_frame = tk.Frame(self)
        botones_frame.pack(fill="x", pady=(0, 8))

        # Botón Agregar
        self.boton_agregar = tk.Button(botones_frame, text="Agregar", width=12, command=self.agregar_dato)
        self.boton_agregar.grid(row=0, column=0, padx=(0, 6))

        # Botón Limpiar Entrada (solo limpia el Entry)
        self.boton_limpiar_entrada = tk.Button(botones_frame, text="Limpiar entrada", width=14, command=self.limpiar_entrada)
        self.boton_limpiar_entrada.grid(row=0, column=1, padx=(0, 6))

        # Botón Eliminar seleccionado
        self.boton_eliminar = tk.Button(botones_frame, text="Eliminar seleccionado", width=16, command=self.eliminar_seleccionado)
        self.boton_eliminar.grid(row=0, column=2, padx=(0, 6))

        # Botón Limpiar todo
        self.boton_limpiar_todo = tk.Button(botones_frame, text="Limpiar todo", width=12, command=self.limpiar_todo)
        self.boton_limpiar_todo.grid(row=0, column=3)

        # Listbox con scrollbar para mostrar los datos ingresados
        lista_frame = tk.Frame(self)
        lista_frame.pack(fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(lista_frame, orient=tk.VERTICAL)
        self.lista_datos = tk.Listbox(lista_frame, width=60, height=12, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lista_datos.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.lista_datos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Bind doble click para editar (opcional) o mostrar info
        self.lista_datos.bind("<Double-1>", lambda event: self.mostrar_seleccion())
        # Bind tecla Supr (Delete) para eliminar la selección
        self.bind('<Delete>', lambda event: self.eliminar_seleccionado())

        # Etiqueta de estado (pequeños mensajes al usuario)
        self.label_estado = tk.Label(self, text="Listo.", anchor='w')
        self.label_estado.pack(fill="x", pady=(8, 0))

    # ----------------- Funciones -----------------
    def agregar_dato(self):
        """Agrega el texto del Entry a la lista si no está vacío."""
        dato = self.entrada_texto.get().strip()
        if not dato:
            messagebox.showwarning("Advertencia", "No puedes agregar un campo vacío.")
            self.label_estado.config(text="Error: intento de agregar vacío.")
            return

        self.lista_datos.insert(tk.END, dato)
        self.entrada_texto.delete(0, tk.END)
        self.label_estado.config(text=f"Agregado: {dato}")

    def limpiar_entrada(self):
        """Limpia únicamente el campo de texto (Entry)."""
        self.entrada_texto.delete(0, tk.END)
        self.label_estado.config(text="Campo de entrada limpio.")

    def eliminar_seleccionado(self):
        """Elimina el elemento seleccionado en la Listbox."""
        seleccion = self.lista_datos.curselection()
        if not seleccion:
            messagebox.showinfo("Información", "No hay ningún elemento seleccionado para eliminar.")
            self.label_estado.config(text="No se eliminó nada (ninguna selección).")
            return

        # eliminar desde el último índice seleccionado (para ser seguro con múltiples selecciones)
        for index in reversed(seleccion):
            texto = self.lista_datos.get(index)
            self.lista_datos.delete(index)
            self.label_estado.config(text=f"Eliminado: {texto}")

    def limpiar_todo(self):
        """Elimina todos los elementos de la Listbox con confirmación."""
        if self.lista_datos.size() == 0:
            messagebox.showinfo("Información", "La lista ya está vacía.")
            self.label_estado.config(text="La lista ya estaba vacía.")
            return

        if messagebox.askyesno("Confirmar", "¿Deseas eliminar todos los elementos?"):
            self.lista_datos.delete(0, tk.END)
            self.label_estado.config(text="Todos los elementos han sido eliminados.")
        else:
            self.label_estado.config(text="Operación cancelada.")

    def mostrar_seleccion(self):
        """Muestra el elemento seleccionado en un messagebox (doble click)."""
        seleccion = self.lista_datos.curselection()
        if not seleccion:
            return
        index = seleccion[0]
        texto = self.lista_datos.get(index)
        messagebox.showinfo("Elemento seleccionado", texto)


if __name__ == "__main__":
    app = App()
    app.mainloop()
