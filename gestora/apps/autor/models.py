from django.db import models
from django_countries.fields import CountryField
from apps.common.models import ModeloAuditoria


class Autor(ModeloAuditoria):
    """Representa un autor almacenado en la tabla ``autor``."""

    class Sexo(models.TextChoices):
        MASCULINO = "M", "Masculino"
        FEMENINO = "F", "Femenino"

    id_autor = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100, null=False, blank=False)
    apellido = models.CharField(max_length=100, null=False, blank=False)
    nacionalidad = CountryField(null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=Sexo.choices, null=False, blank=False)

    class Meta:
        db_table = "autor"
        indexes = [models.Index(fields=["apellido", "nombre"])]
        ordering = ("apellido", "nombre")

    def __str__(self) -> str:
        """Devuelve el nombre legible que Django muestra en formularios."""
        return f"{self.nombre} {self.apellido}"


class PerfilAutor(ModeloAuditoria):
    """Almacena la información adicional asociada a un único autor."""

    id_perfil = models.BigAutoField(primary_key=True)

    autor = models.OneToOneField(
        Autor,
        on_delete=models.CASCADE,
        related_name="perfil",
        null=False,
        blank=False,
    )

    imagen_perfil = models.ImageField(
        upload_to="authors_profile_img/", null=True, blank=True
    )
    orcid = models.CharField(max_length=19, unique=True, null=True, blank=True)
    afiliacion = models.CharField(max_length=150, null=True, blank=True)
    biografia = models.TextField(null=True, blank=True)
    sitio_web = models.URLField(null=True, blank=True)

    class Meta:
        db_table = "perfil_autor"

    def __str__(self) -> str:
        """Devuelve una descripción legible del perfil."""
        return f"Perfil: {self.autor}"
