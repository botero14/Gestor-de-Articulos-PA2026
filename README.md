# Gestor de Artículos Científicos - PA2026

Este proyecto es un sistema de gestión de artículos científicos y autores desarrollado como parte de las asignaturas de Programación de la Universidad de La Guajira. Permite administrar la información de publicaciones académicas, perfiles de autores y el orden de autoría mediante una arquitectura relacional en Django.

---

## Tecnologías y Versiones

![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![Uniguajira](https://img.shields.io/badge/Universidad-de%20La%20Guajira-00875A?style=for-the-badge)

El entorno de desarrollo está configurado y garantizado para funcionar bajo las siguientes versiones de software:

- **Python:** `3.14.x` (o superior)
- **Django:** `5.2.x`
- **Base de Datos:** SQLite 3 (Entorno de desarrollo local) / Compatible con MySQL.

### Librerías del Entorno (`requirements.txt`)

- `django>=5.2,<5.3`
- `django-countries>=7.5` _(Para la gestión de nacionalidades en el modelo Author)_

---

## Funcionalidades CRUD

El sistema implementa las operaciones **Create, Read, Update y Delete (CRUD)**
para las siguientes entidades:

- **Autores:** registrar, listar, editar y eliminar autores.
- **Artículos:** registrar, listar, editar y eliminar artículos científicos.
- **Revistas:** registrar, listar, editar y eliminar revistas.

Los artículos permiten seleccionar una revista, cargar un archivo PDF y
relacionar varios autores conservando su orden de autoría.

También se incluye:

- Navegación mediante URLs nombradas de Django.
- Formularios de confirmación antes de eliminar registros.
- Página personalizada para rutas no encontradas con respuesta HTTP 404.
- Servicio de archivos PDF desde la carpeta `media` durante el desarrollo.
- Pruebas automatizadas para los principales flujos CRUD.

---

## Estructura de Django

Cada entidad está organizada en los archivos principales de una aplicación
Django:

- `models.py`: define las entidades, campos y relaciones de la base de datos.
- `forms.py`: representa y valida los datos enviados por el usuario.
- `views.py`: procesa las peticiones HTTP y coordina formularios y consultas.
- `urls.py`: relaciona cada ruta con una función de la vista.
- `templates/`: contiene los formularios, listados y páginas de confirmación.

El flujo general de una petición es:

```text
URL -> View -> Form -> ORM/Modelo -> Base de datos
                         |
                     Template
```

### Django Forms

`AutorForm`, `ArticuloForm` y `RevistaForm` heredan de `forms.ModelForm`.
La clase interna `Meta` define:

- `model`: modelo que será creado o actualizado.
- `fields`: campos permitidos en el formulario.
- `labels`: nombres visibles para el usuario.
- `widgets`: elementos HTML y clases de Bootstrap.

Los tres formularios utilizan la misma estructura en sus plantillas:

```django
{% for field in form %}
  {{ field.label }}
  {{ field }}
  {{ field.errors }}
{% endfor %}
```

### Listar Registros

Las vistas consultan los registros por medio del ORM de Django:

```python
autores = Autor.objects.all().order_by("apellido", "nombre")
```

`all()` construye una consulta `SELECT` y `order_by()` define su orden. La vista
entrega el `QuerySet` a la plantilla con `render()`.

En el listado de artículos se utilizan:

- `select_related("revista")` para obtener la revista mediante un JOIN.
- `prefetch_related("articulo_autores__autor")` para cargar los autores
  relacionados eficientemente.

### Guardar Registros

Una petición GET muestra un formulario vacío. Cuando se recibe una petición
POST, la vista valida y guarda los datos:

```python
form = AutorForm(request.POST)

if form.is_valid():
    form.save()
```

`is_valid()` aplica las validaciones del formulario y del modelo. Si los datos
son válidos, `save()` utiliza el ORM para ejecutar un `INSERT`.

Los artículos también reciben `request.FILES` para procesar el PDF.
`ArticuloForm.save()` guarda primero el artículo y después sincroniza la tabla
intermedia `ArticuloAutor` dentro de `transaction.atomic`.

### Editar Registros

La vista obtiene el objeto solicitado con `get_object_or_404()` y lo entrega al
formulario mediante `instance`:

```python
autor = get_object_or_404(Autor, pk=id_autor)
form = AutorForm(request.POST, instance=autor)
```

- Sin `instance`, `form.save()` crea un registro mediante `INSERT`.
- Con `instance`, `form.save()` conserva el ID y ejecuta un `UPDATE`.

Las vistas de creación y edición reutilizan el mismo formulario y la misma
plantilla.

### Eliminar Registros

La eliminación se realiza en dos pasos:

1. Una petición GET muestra la página de confirmación.
2. Una petición POST ejecuta `objeto.delete()` mediante el ORM.

Las relaciones respetan las reglas `on_delete` de los modelos. Al eliminar un
artículo también se eliminan sus relaciones de autoría; al eliminar una revista,
los artículos permanecen y su campo `revista` queda vacío.

### Resumen CRUD

| Operación | Acción | ORM principal |
| --- | --- | --- |
| Create | Crear | `form.save()` sin `instance` |
| Read | Listar | `Model.objects.all()` |
| Update | Editar | `form.save()` con `instance` |
| Delete | Eliminar | `objeto.delete()` |

---

## Instrucciones para Levantar el Servidor

Sigue estos pasos en la terminal de tu sistema (PowerShell, CMD o Terminal de Linux/WSL) para ejecutar el proyecto localmente.

```bash
python -m venv entorno
source entorno/bin/activate|
```

### 1. Clonar el repositorio y navegar al proyecto

```bash
git clone [https://github.com/botero14/Gestor-de-Articulos-PA2026.git](https://github.com/botero14/Gestor-de-Articulos-PA2026.git)
cd Gestor-de-Articulos-PA2026/gestora
```

## 2. Instalar las dependencias

```bash
pip install -r requirements.txt
```
