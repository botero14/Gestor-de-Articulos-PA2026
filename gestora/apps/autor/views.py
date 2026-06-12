from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AutorForm
from .models import Autor


def saludo_http(request):
    """Devuelve una respuesta HTTP sencilla sin utilizar una plantilla."""
    return HttpResponse(
        "<a href='https://www.google.com/'>Hola, esta es una respuesta HTTP simple desde la app autor. </a>"
    )


def listar_autores(request):
    """
    Consulta todos los autores y los envía a la plantilla de listado.

    ``Autor.objects`` es el administrador del ORM. ``all()`` construye un
    QuerySet y ``order_by()`` agrega el ordenamiento a la consulta SQL. Django
    ejecuta la consulta cuando la plantilla recorre la variable ``autores``.
    """
    autores = Autor.objects.all().order_by("apellido", "nombre")
    return render(request, "autor/lista_autores.html", {"autores": autores})


def crear_autor(request):
    """
    Muestra el formulario y guarda un autor cuando recibe un POST válido.

    En GET se crea un formulario vacío. En POST, ``request.POST`` llena el
    ``AutorForm``; ``is_valid()`` aplica la validación y ``save()`` ejecuta un
    INSERT mediante el ORM. La redirección evita reenviar el formulario si el
    usuario actualiza la página.
    """
    if request.method == "POST":
        form = AutorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("autor:lista_autores")
    else:
        form = AutorForm()

    contexto = {
        "form": form,
        "titulo": "Crear autor",
        "texto_boton": "Guardar autor",
    }
    return render(request, "autor/crear_autor.html", contexto)


def editar_autor(request, id_autor):
    """
    Actualiza un autor existente utilizando el mismo ``AutorForm``.

    ``get_object_or_404`` busca por llave primaria y responde 404 si no existe.
    El argumento ``instance=autor`` indica al ModelForm que debe ejecutar un
    UPDATE sobre ese registro; sin ``instance`` crearía un autor nuevo.
    """
    autor = get_object_or_404(Autor, pk=id_autor)

    if request.method == "POST":
        form = AutorForm(request.POST, instance=autor)
        if form.is_valid():
            form.save()
            return redirect("autor:lista_autores")
    else:
        form = AutorForm(instance=autor)

    contexto = {
        "form": form,
        "titulo": "Editar autor",
        "texto_boton": "Actualizar autor",
    }
    return render(request, "autor/crear_autor.html", contexto)


def eliminar_autor(request, id_autor):
    """
    Confirma y elimina un autor.

    En GET solo se muestra la confirmación. En POST, ``delete()`` ejecuta el
    DELETE mediante el ORM. Separar ambos métodos evita borrar información por
    visitar accidentalmente un enlace.
    """
    autor = get_object_or_404(Autor, pk=id_autor)

    if request.method == "POST":
        autor.delete()
        return redirect("autor:lista_autores")

    contexto = {
        "objeto": autor,
        "tipo_entidad": "autor",
        "url_lista": "autor:lista_autores",
    }
    return render(request, "confirmar_eliminacion.html", contexto)
