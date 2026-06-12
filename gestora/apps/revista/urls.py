from django.urls import path

from . import views

app_name = "revista"

urlpatterns = [
    path("lista/", views.listar_revistas, name="lista_revistas"),
    path("crear/", views.crear_revista, name="crear_revista"),
    path(
        "editar/<int:id_revista>/",
        views.editar_revista,
        name="editar_revista",
    ),
    path(
        "eliminar/<int:id_revista>/",
        views.eliminar_revista,
        name="eliminar_revista",
    ),
]
