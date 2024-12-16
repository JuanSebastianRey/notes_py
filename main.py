import json
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

# --- Base de datos con SQLAlchemy ---
Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    completed = Column(Boolean, default=False)

# Crear conexión con SQLite
try:
    db_engine = create_engine('sqlite:///tasks.db')
    Base.metadata.create_all(db_engine)
    Session = sessionmaker(bind=db_engine)
    session = Session()
except SQLAlchemyError as e:
    messagebox.showerror("Error", f"No se pudo conectar a la base de datos: {e}")
    exit()

# --- Funciones de la aplicación ---
def agregar_tarea(title, description):
    if not title or not description:
        messagebox.showwarning("Advertencia", "El título y la descripción no pueden estar vacíos.")
        return
    try:
        nueva_tarea = Task(title=title, description=description)
        session.add(nueva_tarea)
        session.commit()
        messagebox.showinfo("Éxito", "Tarea agregada correctamente!")
        listar_tareas()
    except SQLAlchemyError as e:
        session.rollback()
        messagebox.showerror("Error", f"Error al agregar tarea: {e}")

def listar_tareas():
    try:
        for item in tree.get_children():
            tree.delete(item)
        tareas = session.query(Task).all()
        for tarea in tareas:
            estado = "Completada" if tarea.completed else "Pendiente"
            tree.insert("", "end", values=(tarea.id, tarea.title, tarea.description, estado))
    except SQLAlchemyError as e:
        messagebox.showerror("Error", f"Error al listar tareas: {e}")

def marcar_completada():
    try:
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
                messagebox.showerror("Error", "No se encontró la tarea seleccionada.")
        else:
            messagebox.showwarning("Advertencia", "Seleccione una tarea para marcar como completada.")
    except SQLAlchemyError as e:
        messagebox.showerror("Error", f"Error al marcar la tarea como completada: {e}")

def eliminar_tarea_completada():
    try:
        tareas_completadas = session.query(Task).filter_by(completed=True).all()
        if not tareas_completadas:
            messagebox.showinfo("Información", "No hay tareas completadas para eliminar.")
            return
        for tarea in tareas_completadas:
            session.delete(tarea)
        session.commit()
        messagebox.showinfo("Éxito", "Tareas completadas eliminadas correctamente!")
        listar_tareas()
    except SQLAlchemyError as e:
        session.rollback()
        messagebox.showerror("Error", f"Error al eliminar tareas: {e}")

def exportar_tareas():
    try:
        tareas = session.query(Task).all()
        datos = [{"id": t.id, "title": t.title, "description": t.description, "completed": t.completed} for t in tareas]
        with open("tareas.json", "w") as f:
            json.dump(datos, f, indent=4)
        messagebox.showinfo("Éxito", "Tareas exportadas a 'tareas.json'.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al exportar tareas: {e}")

def importar_tareas():
    try:
        with open("tareas.json", "r") as f:
            datos = json.load(f)
            for tarea in datos:
                nueva_tarea = Task(id=tarea['id'], title=tarea['title'], description=tarea['description'], completed=tarea['completed'])
                session.merge(nueva_tarea)
            session.commit()
        messagebox.showinfo("Éxito", "Tareas importadas correctamente!")
        listar_tareas()
    except FileNotFoundError:
        messagebox.showerror("Error", "El archivo 'tareas.json' no existe.")
    except json.JSONDecodeError:
        messagebox.showerror("Error", "El archivo 'tareas.json' no es válido.")
    except SQLAlchemyError as e:
        session.rollback()
        messagebox.showerror("Error", f"Error al importar tareas: {e}")

def agregar_tarea_dialogo():
    try:
        title = simpledialog.askstring("Agregar Tarea", "Ingrese el título de la tarea:")
        if title:
            description = simpledialog.askstring("Agregar Tarea", "Ingrese la descripción de la tarea:")
            if description:
                agregar_tarea(title, description)
    except Exception as e:
        messagebox.showerror("Error", f"Error al agregar tarea: {e}")

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
