from django.urls import path

from . import views

app_name = "articulo"

urlpatterns = [
    path("lista/", views.listar_articulos, name="lista_articulos"),
    path("crear/", views.crear_articulo, name="crear_articulo"),
    path(
        "editar/<int:id_articulo>/",
        views.editar_articulo,
        name="editar_articulo",
    ),
    path(
        "eliminar/<int:id_articulo>/",
        views.eliminar_articulo,
        name="eliminar_articulo",
    ),
]
