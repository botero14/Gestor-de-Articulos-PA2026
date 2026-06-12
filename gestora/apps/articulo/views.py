from django.shortcuts import get_object_or_404, redirect, render

from .forms import ArticuloForm
from .models import Articulo


def listar_articulos(request):
    """
    Consulta los artículos junto con sus relaciones para mostrarlos en tabla.

    ``select_related`` resuelve la llave foránea ``revista`` con un JOIN.
    ``prefetch_related`` obtiene las relaciones de autores en una consulta
    adicional. Así se evita ejecutar una consulta por cada fila del listado.
    """
    articulos = (
        Articulo.objects.select_related("revista")
        .prefetch_related("articulo_autores__autor")
        .all()
    )
    return render(
        request,
        "articulo/lista_articulos.html",
        {"articulos": articulos},
    )


def crear_articulo(request):
    """
    Muestra el formulario y crea un artículo con su PDF y sus autores.

    Los archivos llegan en ``request.FILES`` y los demás campos en
    ``request.POST``. Si el formulario es válido, su método ``save()`` guarda
    el artículo y los registros de la tabla intermedia ``ArticuloAutor``.
    """
    if request.method == "POST":
        form = ArticuloForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("articulo:lista_articulos")
    else:
        form = ArticuloForm()

    contexto = {
        "form": form,
        "titulo": "Crear artículo",
        "texto_boton": "Guardar artículo",
    }
    return render(request, "articulo/crear_articulo.html", contexto)


def editar_articulo(request, id_articulo):
    """
    Actualiza un artículo y reemplaza su selección de autores.

    ``instance=articulo`` carga los valores actuales y hace que el ModelForm
    ejecute un UPDATE. Si no se carga un PDF nuevo, Django conserva el archivo
    existente. ``ArticuloForm.save()`` sincroniza después la tabla intermedia.
    """
    articulo = get_object_or_404(Articulo, pk=id_articulo)

    if request.method == "POST":
        form = ArticuloForm(
            request.POST,
            request.FILES,
            instance=articulo,
        )
        if form.is_valid():
            form.save()
            return redirect("articulo:lista_articulos")
    else:
        form = ArticuloForm(instance=articulo)

    contexto = {
        "form": form,
        "titulo": "Editar artículo",
        "texto_boton": "Actualizar artículo",
    }
    return render(request, "articulo/crear_articulo.html", contexto)


def eliminar_articulo(request, id_articulo):
    """
    Confirma y elimina un artículo.

    El ORM también elimina las filas relacionadas de ``ArticuloAutor`` porque
    sus llaves foráneas usan ``on_delete=models.CASCADE``.
    """
    articulo = get_object_or_404(Articulo, pk=id_articulo)

    if request.method == "POST":
        articulo.delete()
        return redirect("articulo:lista_articulos")

    contexto = {
        "objeto": articulo,
        "tipo_entidad": "artículo",
        "url_lista": "articulo:lista_articulos",
    }
    return render(request, "confirmar_eliminacion.html", contexto)
