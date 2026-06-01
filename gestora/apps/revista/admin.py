from django.contrib import admin
from .models import Revista


@admin.register(Revista)
class RevistaAdmin(admin.ModelAdmin):
    list_display = ("id_revista", "nombre", "issn", "factor_impacto")
    search_fields = ("nombre", "issn")
    ordering = ("nombre",)
