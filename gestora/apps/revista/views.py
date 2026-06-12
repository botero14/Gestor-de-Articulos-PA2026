from django.shortcuts import get_object_or_404, redirect, render

from .forms import RevistaForm
from .models import Revista


def listar_revistas(request):
    """
    Obtiene todas las revistas y renderiza el listado.

    ``Revista.objects.all()`` construye un QuerySet. El orden por nombre no se
    repite aquí porque ya está definido en ``Revista.Meta.ordering``.
    """
    revistas = Revista.objects.all()
    return render(request, "revista/lista_revistas.html", {"revistas": revistas})


def crear_revista(request):
    """
    Muestra el formulario y crea una revista cuando el POST es válido.

    ``is_valid()`` revisa tipos, campos obligatorios y valores únicos definidos
    en el modelo. ``form.save()`` transforma los datos validados en un INSERT.
    """
    if request.method == "POST":
        form = RevistaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("revista:lista_revistas")
    else:
        form = RevistaForm()

    contexto = {
        "form": form,
        "titulo": "Crear revista",
        "texto_boton": "Guardar revista",
    }
    return render(request, "revista/crear_revista.html", contexto)


def editar_revista(request, id_revista):
    """
    Modifica una revista existente con el mismo formulario de creación.

    La búsqueda se realiza con el ORM por llave primaria. Al pasar el registro
    como ``instance``, ``form.save()`` genera un UPDATE y mantiene el mismo ID.
    """
    revista = get_object_or_404(Revista, pk=id_revista)

    if request.method == "POST":
        form = RevistaForm(request.POST, instance=revista)
        if form.is_valid():
            form.save()
            return redirect("revista:lista_revistas")
    else:
        form = RevistaForm(instance=revista)

    contexto = {
        "form": form,
        "titulo": "Editar revista",
        "texto_boton": "Actualizar revista",
    }
    return render(request, "revista/crear_revista.html", contexto)


def eliminar_revista(request, id_revista):
    """
    Confirma y elimina una revista.

    Al ejecutar ``delete()``, el ORM aplica la regla del modelo. Los artículos
    relacionados no se eliminan: su campo ``revista`` queda en NULL porque la
    relación fue configurada con ``on_delete=models.SET_NULL``.
    """
    revista = get_object_or_404(Revista, pk=id_revista)

    if request.method == "POST":
        revista.delete()
        return redirect("revista:lista_revistas")

    contexto = {
        "objeto": revista,
        "tipo_entidad": "revista",
        "url_lista": "revista:lista_revistas",
    }
    return render(request, "confirmar_eliminacion.html", contexto)
