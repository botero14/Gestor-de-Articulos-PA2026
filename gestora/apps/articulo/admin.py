from django.contrib import admin
from .models import Articulo, ArticuloAutor


class ArticuloAutorInline(admin.TabularInline):
    model = ArticuloAutor
    extra = 1
    autocomplete_fields = ("autor",)
    ordering = ("orden_autor",)


@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ("id_articulo", "titulo", "fecha_publicacion", "revista")
    list_filter = ("revista", "fecha_publicacion")
    search_fields = ("titulo", "resumen", "revista__nombre")
    date_hierarchy = "fecha_publicacion"
    ordering = ("-fecha_publicacion",)

    inlines = [ArticuloAutorInline]


@admin.register(ArticuloAutor)
class ArticuloAutorAdmin(admin.ModelAdmin):
    list_display = ("id_articulo_autor", "articulo", "autor", "orden_autor")
    search_fields = ("articulo__titulo", "autor__nombre", "autor__apellido")
    ordering = ("articulo", "orden_autor")
    autocomplete_fields = ("articulo", "autor")
