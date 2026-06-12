from django.urls import path
from . import views

app_name = "autor"

urlpatterns = [
    path("saludo/", views.saludo_http, name="saludo"),
    path("lista/", views.listar_autores, name="lista_autores"),
    path("crear/", views.crear_autor, name="crear_autor"),
    path("editar/<int:id_autor>/", views.editar_autor, name="editar_autor"),
    path("eliminar/<int:id_autor>/", views.eliminar_autor, name="eliminar_autor"),
]
