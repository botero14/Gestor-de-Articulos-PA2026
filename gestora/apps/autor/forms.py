from django import forms

from .models import Autor


class AutorForm(forms.ModelForm):
    """
    Formulario basado en el modelo ``Autor``.

    ``ModelForm`` crea y valida los campos a partir del modelo. Los widgets
    únicamente controlan cómo se representa cada campo en HTML; las reglas
    principales de validación siguen proviniendo de ``Autor``.
    """

    class Meta:
        model = Autor
        fields = ["nombre", "apellido", "sexo", "nacionalidad"]
        labels = {
            "nombre": "Nombre",
            "apellido": "Apellido",
            "sexo": "Sexo",
            "nacionalidad": "País / Nacionalidad",
        }
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Escriba el nombre",
                }
            ),
            "apellido": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Escriba el apellido",
                }
            ),
            "sexo": forms.Select(attrs={"class": "form-select"}),
            "nacionalidad": forms.Select(attrs={"class": "form-select"}),
        }
