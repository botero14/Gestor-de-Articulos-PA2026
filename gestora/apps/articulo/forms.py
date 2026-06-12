from django import forms
from django.db import transaction

from apps.autor.models import Autor

from .models import Articulo, ArticuloAutor


class ArticuloForm(forms.ModelForm):
    """
    Formulario para crear y editar artículos.

    El campo ``autores`` se declara manualmente porque el modelo usa la tabla
    intermedia ``ArticuloAutor``. Esa tabla, además de relacionar registros,
    guarda el orden de autoría.
    """

    autores = forms.ModelMultipleChoiceField(
        queryset=Autor.objects.all(),
        label="Autores",
        help_text=(
            "Mantenga presionada la tecla Ctrl para seleccionar varios autores. "
            "Se guardarán siguiendo el orden mostrado en la lista."
        ),
        widget=forms.SelectMultiple(attrs={"class": "form-select", "size": 5}),
    )

    class Meta:
        model = Articulo
        fields = [
            "titulo",
            "resumen",
            "fecha_publicacion",
            "archivo_pdf",
            "revista",
            "autores",
        ]
        labels = {
            "titulo": "Título",
            "resumen": "Resumen",
            "fecha_publicacion": "Fecha de publicación",
            "archivo_pdf": "Archivo PDF",
            "revista": "Revista",
        }
        widgets = {
            "titulo": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Escriba el título del artículo",
                }
            ),
            "resumen": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "fecha_publicacion": forms.DateInput(
                format="%Y-%m-%d",
                attrs={"class": "form-control", "type": "date"}
            ),
            "archivo_pdf": forms.ClearableFileInput(
                attrs={"class": "form-control", "accept": "application/pdf"}
            ),
            "revista": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        """
        Prepara el formulario y carga los autores actuales durante una edición.

        Cuando ``instance`` contiene un artículo ya guardado, el ORM consulta
        ``ArticuloAutor`` y marca como seleccionados sus autores en el campo
        múltiple. En un POST se respetan los valores enviados por el usuario.
        """
        super().__init__(*args, **kwargs)

        if self.instance.pk and not self.is_bound:
            self.initial["autores"] = list(
                self.instance.articulo_autores.order_by("orden_autor").values_list(
                    "autor_id", flat=True
                )
            )

    @transaction.atomic
    def save(self, commit=True):
        """
        Guarda el artículo y sus autores como una sola operación atómica.

        Primero ``ModelForm.save(commit=False)`` construye el objeto sin
        escribirlo todavía. Después se guarda el artículo con el ORM, se
        eliminan sus relaciones anteriores y se crean las nuevas relaciones
        con ``bulk_create``. ``transaction.atomic`` revierte todo si alguna
        operación falla, evitando que el artículo quede actualizado a medias.
        """
        articulo = super().save(commit=False)

        if commit:
            articulo.save()
            ArticuloAutor.objects.filter(articulo=articulo).delete()
            ArticuloAutor.objects.bulk_create(
                [
                    ArticuloAutor(
                        articulo=articulo,
                        autor=autor,
                        orden_autor=orden,
                    )
                    for orden, autor in enumerate(
                        self.cleaned_data["autores"], start=1
                    )
                ]
            )

        return articulo
