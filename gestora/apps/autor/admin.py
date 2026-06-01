from django.contrib import admin
from .models import Autor, PerfilAutor


class PerfilAutorInline(admin.StackedInline):
    model = PerfilAutor
    extra = 0


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ("id_autor", "nombre", "apellido", "sexo", "nacionalidad")
    list_filter = ("sexo", "nacionalidad")
    search_fields = ("nombre", "apellido")
    ordering = ("apellido", "nombre")
    inlines = [PerfilAutorInline]


@admin.register(PerfilAutor)
class PerfilAutorAdmin(admin.ModelAdmin):
    list_display = ("id_perfil", "autor", "orcid", "afiliacion")
    search_fields = ("autor__nombre", "autor__apellido", "orcid", "afiliacion")
