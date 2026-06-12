from django.db import models
from apps.common.models import ModeloAuditoria


class Revista(ModeloAuditoria):
    """Representa una revista que puede publicar varios artículos."""

    id_revista = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=200, unique=True, null=False, blank=False)
    issn = models.CharField(max_length=9, unique=True, null=False, blank=False)
    factor_impacto = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )

    class Meta:
        db_table = "revista"
        indexes = [models.Index(fields=["nombre"]), models.Index(fields=["issn"])]
        ordering = ("nombre",)

    def __str__(self) -> str:
        """Muestra el nombre y el ISSN en formularios y administración."""
        return f"{self.nombre} ({self.issn})"
