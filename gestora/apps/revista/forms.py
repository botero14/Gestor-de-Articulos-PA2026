from django import forms

from .models import Revista


class RevistaForm(forms.ModelForm):
    """
    Formulario basado en el modelo ``Revista``.

    Django obtiene del modelo los tipos, campos obligatorios y restricciones
    de unicidad. Los widgets agregan las clases de Bootstrap y ayudas visuales.
    """

    class Meta:
        model = Revista
        fields = ["nombre", "issn", "factor_impacto"]
        labels = {
            "nombre": "Nombre",
            "issn": "ISSN",
            "factor_impacto": "Factor de impacto",
        }
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Escriba el nombre de la revista",
                }
            ),
            "issn": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ejemplo: 1234-5678"}
            ),
            "factor_impacto": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01", "min": "0"}
            ),
        }
