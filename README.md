# Gestor de Tareas con Interfaz Gráfica en Python

Esta aplicación de gestión de tareas permite a los usuarios administrar sus tareas diarias con una interfaz gráfica desarrollada en **Tkinter** y una base de datos SQLite utilizando **SQLAlchemy**.

## Características Principales

1. **Agregar Tareas**: Permite agregar nuevas tareas con título y descripción.
2. **Listar Tareas**: Muestra una lista de todas las tareas con su estado (Pendiente o Completada).
3. **Marcar Tareas como Completadas**: Permite marcar una tarea como completada.
4. **Eliminar Tareas Completadas**: Elimina todas las tareas que se han marcado como completadas.
5. **Exportar Tareas**: Exporta las tareas a un archivo `tareas.json` en formato JSON.
6. **Importar Tareas**: Importa tareas desde un archivo `tareas.json`.

## Requisitos Previos

Asegúrete de tener instaladas las siguientes dependencias en tu sistema:

- **Python 3.x**
- **SQLAlchemy**
- **Tkinter**

### Instalación de Dependencias

#### En Ubuntu

1. **Instalar SQLAlchemy**:

   ```bash
   sudo apt update
   sudo apt install python3-sqlalchemy
   ```

2. **Instalar Tkinter**:

   ```bash
   sudo apt install python3-tk
   ```

#### En Windows

1. **Instalar SQLAlchemy** con `pip`:

   ```bash
   pip install SQLAlchemy
   ```

2. **Instalar Tkinter**:

   Tkinter viene preinstalado con las distribuciones de Python para Windows. Si encuentras un error al importar Tkinter, asegúrate de reinstalar Python desde [python.org](https://www.python.org/downloads/) y habilitar la opción "tcl/tk and IDLE" durante la instalación.

## Ejecución del Programa

1. **Clona el repositorio o descarga el archivo `main.py`**.

2. **Ejecuta el script**:

   ```bash
   python3 main.py
   ```

En Windows:

   ```bash
   python main.py
   ```

Esto abrirá una ventana con la interfaz gráfica de la aplicación.

## Uso de la Aplicación

### 1. Agregar Tarea
- Haz clic en el botón **"Agregar Tarea"**.
- Introduce el título y la descripción de la tarea en los cuadros de diálogo.

### 2. Listar Tareas
- Las tareas se muestran automáticamente en la interfaz principal.

### 3. Marcar Tarea como Completada
- Selecciona una tarea de la lista y haz clic en **"Marcar como Completada"**.

### 4. Eliminar Tareas Completadas
- Haz clic en el botón **"Eliminar Tareas Completadas"** para eliminar todas las tareas completadas.

### 5. Exportar Tareas
- Haz clic en el botón **"Exportar Tareas"** para guardar todas las tareas en el archivo `tareas.json`.

### 6. Importar Tareas
- Haz clic en el botón **"Importar Tareas"** para cargar tareas desde el archivo `tareas.json`.

## Casos de Uso

1. **Planificación Diaria**:
   - Los usuarios pueden crear una lista de tareas pendientes para organizar sus actividades diarias.

2. **Gestión de Proyectos Simples**:
   - Ideal para administrar tareas sencillas en pequeños proyectos personales o profesionales.

3. **Seguimiento de Progreso**:
   - Permite marcar tareas completadas y eliminar tareas finalizadas para mantener una lista organizada.

4. **Backup de Tareas**:
   - Los usuarios pueden exportar sus tareas a un archivo JSON y restaurarlas cuando sea necesario.

## Estructura del Proyecto

```
project/
├─ main.py        # Archivo principal con el código de la aplicación
├─ tareas.json    # Archivo de exportación e importación de tareas
```

---

© 2024 - Aplicación de Gestión de Tareas