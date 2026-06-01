from django.urls import path
from . import views

app_name = "autor"

urlpatterns = [
    path("saludo/", views.saludo_http, name="saludo"),
    path("lista/", views.listar_autores, name="lista_autores"),
    path("crear/", views.crear_autor, name="crear_autor"),
]
