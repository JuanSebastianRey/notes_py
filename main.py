import json
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
        print("\nTarea agregada correctamente!\n")
    except Exception as e:
        session.rollback()
        print(f"Error al agregar tarea: {e}")

def listar_tareas():
    """Listar todas las tareas con su estado."""
    tareas = session.query(Task).all()
    if not tareas:
        print("No hay tareas registradas.")
        return

    for tarea in tareas:
        estado = "Completada" if tarea.completed else "Pendiente"
        print(f"ID: {tarea.id} | Título: {tarea.title} | Descripción: {tarea.description} | Estado: {estado}")

def marcar_completada(task_id):
    """Marcar una tarea como completada."""
    tarea = session.query(Task).get(task_id)
    if tarea:
        tarea.completed = True
        session.commit()
        print("\nTarea marcada como completada!\n")
    else:
        print("\nTarea no encontrada.\n")

def eliminar_tarea_completada():
    """Eliminar todas las tareas completadas."""
    try:
        tareas_completadas = session.query(Task).filter_by(completed=True).all()
        for tarea in tareas_completadas:
            session.delete(tarea)
        session.commit()
        print("\nTareas completadas eliminadas correctamente!\n")
    except Exception as e:
        session.rollback()
        print(f"Error al eliminar tareas: {e}")

def exportar_tareas():
    """Exportar todas las tareas a un archivo JSON."""
    tareas = session.query(Task).all()
    datos = [{"id": t.id, "title": t.title, "description": t.description, "completed": t.completed} for t in tareas]
    with open("tareas.json", "w") as f:
        json.dump(datos, f, indent=4)
    print("\nTareas exportadas a 'tareas.json'.\n")

def importar_tareas():
    """Importar tareas desde un archivo JSON."""
    try:
        with open("tareas.json", "r") as f:
            datos = json.load(f)
            for tarea in datos:
                nueva_tarea = Task(id=tarea['id'], title=tarea['title'], description=tarea['description'], completed=tarea['completed'])
                session.merge(nueva_tarea)
            session.commit()
        print("\nTareas importadas correctamente!\n")
    except Exception as e:
        session.rollback()
        print(f"Error al importar tareas: {e}")

# --- Menú de la aplicación ---
def menu():
    while True:
        print("\n--- Aplicación de Gestión de Tareas ---")
        print("1. Agregar Tarea")
        print("2. Listar Tareas")
        print("3. Marcar Tarea como Completada")
        print("4. Eliminar Tareas Completadas")
        print("5. Exportar Tareas")
        print("6. Importar Tareas")
        print("7. Salir")

        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            title = input("Ingrese el título de la tarea: ")
            description = input("Ingrese la descripción de la tarea: ")
            agregar_tarea(title, description)
        elif opcion == "2":
            listar_tareas()
        elif opcion == "3":
            task_id = int(input("Ingrese el ID de la tarea a marcar como completada: "))
            marcar_completada(task_id)
        elif opcion == "4":
            eliminar_tarea_completada()
        elif opcion == "5":
            exportar_tareas()
        elif opcion == "6":
            importar_tareas()
        elif opcion == "7":
            print("\nSaliendo de la aplicación.\n")
            break
        else:
            print("\nOpción no válida. Intente nuevamente.\n")

if __name__ == "__main__":
    menu()
