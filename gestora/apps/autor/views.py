from django.http import HttpResponse
from django.shortcuts import render
from .models import Autor


def saludo_http(request):
    return HttpResponse(
        "<a href='https://www.google.com/'>Hola, esta es una respuesta HTTP simple desde la app autor. </a>"
    )


def listar_autores(request):
    autores = Autor.objects.all().order_by("apellido", "nombre")
    return render(request, "autor/lista_autores.html", {"autores": autores})
