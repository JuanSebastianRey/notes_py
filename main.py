import json
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

# --- Base de datos con SQLAlchemy ---
Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    completed = Column(Boolean, default=False)

# Crear conexión con SQLite
db_engine = create_engine('sqlite:///tasks.db')
Base.metadata.create_all(db_engine)
Session = sessionmaker(bind=db_engine)
session = Session()

# --- Funciones de la aplicación ---
def agregar_tarea(title, description):
    """Agregar una nueva tarea a la base de datos."""
    try:
        nueva_tarea = Task(title=title, description=description)
        session.add(nueva_tarea)
        session.commit()
        messagebox.showinfo("Éxito", "Tarea agregada correctamente!")
        listar_tareas()
    except Exception as e:
        session.rollback()
        messagebox.showerror("Error", f"Error al agregar tarea: {e}")

def listar_tareas():
    """Listar todas las tareas en el Treeview."""
    for item in tree.get_children():
        tree.delete(item)
    tareas = session.query(Task).all()
    for tarea in tareas:
        estado = "Completada" if tarea.completed else "Pendiente"
        tree.insert("", "end", values=(tarea.id, tarea.title, tarea.description, estado))

def marcar_completada():
    """Marcar una tarea seleccionada como completada."""
    selected_item = tree.selection()
    if selected_item:
        task_id = tree.item(selected_item)['values'][0]
        tarea = session.query(Task).get(task_id)
        if tarea:
            tarea.completed = True
            session.commit()
            messagebox.showinfo("Éxito", "Tarea marcada como completada!")
            listar_tareas()
    else:
        messagebox.showwarning("Advertencia", "Seleccione una tarea para marcar como completada.")

def eliminar_tarea_completada():
    """Eliminar todas las tareas completadas."""
    try:
        tareas_completadas = session.query(Task).filter_by(completed=True).all()
        for tarea in tareas_completadas:
            session.delete(tarea)
        session.commit()
        messagebox.showinfo("Éxito", "Tareas completadas eliminadas correctamente!")
        listar_tareas()
    except Exception as e:
        session.rollback()
        messagebox.showerror("Error", f"Error al eliminar tareas: {e}")

def exportar_tareas():
    """Exportar todas las tareas a un archivo JSON."""
    tareas = session.query(Task).all()
    datos = [{"id": t.id, "title": t.title, "description": t.description, "completed": t.completed} for t in tareas]
    with open("tareas.json", "w") as f:
        json.dump(datos, f, indent=4)
    messagebox.showinfo("Éxito", "Tareas exportadas a 'tareas.json'.")

def importar_tareas():
    """Importar tareas desde un archivo JSON."""
    try:
        with open("tareas.json", "r") as f:
            datos = json.load(f)
            for tarea in datos:
                nueva_tarea = Task(id=tarea['id'], title=tarea['title'], description=tarea['description'], completed=tarea['completed'])
                session.merge(nueva_tarea)
            session.commit()
        messagebox.showinfo("Éxito", "Tareas importadas correctamente!")
        listar_tareas()
    except Exception as e:
        session.rollback()
        messagebox.showerror("Error", f"Error al importar tareas: {e}")

def agregar_tarea_dialogo():
    title = simpledialog.askstring("Agregar Tarea", "Ingrese el título de la tarea:")
    if title:
        description = simpledialog.askstring("Agregar Tarea", "Ingrese la descripción de la tarea:")
        if description:
            agregar_tarea(title, description)

# --- Interfaz Gráfica con Tkinter ---
root = tk.Tk()
root.title("Gestión de Tareas")

frame = tk.Frame(root)
frame.pack(pady=20)

columns = ("ID", "Título", "Descripción", "Estado")
tree = ttk.Treeview(frame, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.pack()

# Botones de control
btn_agregar = tk.Button(root, text="Agregar Tarea", command=agregar_tarea_dialogo)
btn_agregar.pack(pady=5)

btn_completar = tk.Button(root, text="Marcar como Completada", command=marcar_completada)
btn_completar.pack(pady=5)

btn_eliminar = tk.Button(root, text="Eliminar Tareas Completadas", command=eliminar_tarea_completada)
btn_eliminar.pack(pady=5)

btn_exportar = tk.Button(root, text="Exportar Tareas", command=exportar_tareas)
btn_exportar.pack(pady=5)

btn_importar = tk.Button(root, text="Importar Tareas", command=importar_tareas)
btn_importar.pack(pady=5)

listar_tareas()

root.mainloop()
