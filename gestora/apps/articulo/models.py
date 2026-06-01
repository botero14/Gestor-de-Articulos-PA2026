import os
from django.db import models
from django.db.models import UniqueConstraint

from apps.common.models import ModeloAuditoria
from apps.autor.models import Autor
from apps.revista.models import Revista


def ruta_pdf_articulo(instancia: "Articulo", nombre_archivo: str) -> str:
    """
    Ruta: articles/<id_articulo>/archivo.pdf
    Si el artículo aún no tiene id (antes del primer save), usa 'new'.
    """
    id_articulo = instancia.id_articulo or "new"
    base, ext = os.path.splitext(nombre_archivo)
    nombre_seguro = f"{base}{ext}".replace(" ", "_")
    return f"articles/{id_articulo}/{nombre_seguro}"


class Articulo(ModeloAuditoria):
    id_articulo = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=250, null=False, blank=False)
    resumen = models.TextField(null=False, blank=False)
    fecha_publicacion = models.DateField(null=False, blank=False)
  

    archivo_pdf = models.FileField(upload_to=ruta_pdf_articulo, null=False, blank=False)

    revista = models.ForeignKey(
        Revista,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articulos",
    )

    autores = models.ManyToManyField(
        Autor,
        through="ArticuloAutor",
        related_name="articulos",
    )

    class Meta:
        db_table = "articulo"
        ordering = ("-fecha_publicacion", "titulo")
        indexes = [
            models.Index(fields=["fecha_publicacion"]),
            models.Index(fields=["titulo"]),
        ]

    def __str__(self) -> str:
        return self.titulo


class ArticuloAutor(ModeloAuditoria):
    """
    Tabla débil (N–N): autoresxarticulos
    Se gestiona desde ArticuloAdmin con TabularInline.
    """

    id_articulo_autor = models.BigAutoField(primary_key=True)

    articulo = models.ForeignKey(
        Articulo, on_delete=models.CASCADE, related_name="articulo_autores"
    )
    autor = models.ForeignKey(
        Autor, on_delete=models.CASCADE, related_name="autor_articulos"
    )

    orden_autor = models.PositiveIntegerField(null=False, blank=False)

    class Meta:
        db_table = "articulo_autor"
        ordering = ("orden_autor",)
        constraints = [
            UniqueConstraint(fields=["articulo", "autor"], name="uq_articulo_autor"),
            UniqueConstraint(
                fields=["articulo", "orden_autor"], name="uq_articulo_orden_autor"
            ),
        ]

    def __str__(self) -> str:
        return f"{self.articulo} - {self.autor} (orden={self.orden_autor})"
