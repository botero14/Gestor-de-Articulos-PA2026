from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Autor
from .forms import AutorForm


def saludo_http(request):
    return HttpResponse(
        "<a href='https://www.google.com/'>Hola, esta es una respuesta HTTP simple desde la app autor. </a>"
    )


def listar_autores(request):
    autores = Autor.objects.all().order_by("apellido", "nombre")
    return render(request, "autor/lista_autores.html", {"autores": autores})


def crear_autor(request):
    if request.method == "POST":
        form = AutorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/autor/lista/")
    else:
        form = AutorForm()

    return render(request, "autor/crear_autor.html", {"form": form})
