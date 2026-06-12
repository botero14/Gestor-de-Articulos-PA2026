import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse

from apps.autor.models import Autor
from apps.revista.models import Revista

from .models import Articulo, ArticuloAutor


class ArticuloViewsTests(TestCase):
    def setUp(self):
        self.autor = Autor.objects.create(
            nombre="Ada",
            apellido="Lovelace",
            sexo=Autor.Sexo.FEMENINO,
            nacionalidad="GB",
        )
        self.revista = Revista.objects.create(
            nombre="Revista científica",
            issn="8765-4321",
            factor_impacto="3.25",
        )

    def test_listar_articulos(self):
        response = self.client.get(reverse("articulo:lista_articulos"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "articulo/lista_articulos.html")

    def test_crear_articulo_con_autor(self):
        with tempfile.TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                response = self.client.post(
                    reverse("articulo:crear_articulo"),
                    {
                        "titulo": "Artículo de prueba",
                        "resumen": "Resumen del artículo.",
                        "fecha_publicacion": "2026-06-12",
                        "revista": self.revista.pk,
                        "autores": [self.autor.pk],
                        "archivo_pdf": SimpleUploadedFile(
                            "articulo.pdf",
                            b"%PDF-1.4 contenido de prueba",
                            content_type="application/pdf",
                        ),
                    },
                )

        self.assertRedirects(response, reverse("articulo:lista_articulos"))
        articulo = Articulo.objects.get(titulo="Artículo de prueba")
        self.assertTrue(
            ArticuloAutor.objects.filter(
                articulo=articulo,
                autor=self.autor,
                orden_autor=1,
            ).exists()
        )

    def test_editar_articulo_actualiza_datos_y_autores(self):
        segundo_autor = Autor.objects.create(
            nombre="Alan",
            apellido="Turing",
            sexo=Autor.Sexo.MASCULINO,
            nacionalidad="GB",
        )

        with tempfile.TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                articulo = Articulo.objects.create(
                    titulo="Título original",
                    resumen="Resumen original",
                    fecha_publicacion="2026-06-01",
                    revista=self.revista,
                    archivo_pdf=SimpleUploadedFile(
                        "original.pdf",
                        b"%PDF-1.4 contenido original",
                        content_type="application/pdf",
                    ),
                )
                ArticuloAutor.objects.create(
                    articulo=articulo,
                    autor=self.autor,
                    orden_autor=1,
                )

                response = self.client.post(
                    reverse("articulo:editar_articulo", args=[articulo.pk]),
                    {
                        "titulo": "Título actualizado",
                        "resumen": "Resumen actualizado",
                        "fecha_publicacion": "2026-06-12",
                        "revista": self.revista.pk,
                        "autores": [segundo_autor.pk],
                    },
                )

                self.assertRedirects(
                    response,
                    reverse("articulo:lista_articulos"),
                )
                articulo.refresh_from_db()

        self.assertEqual(articulo.titulo, "Título actualizado")
        self.assertEqual(Articulo.objects.count(), 1)
        self.assertQuerySetEqual(
            articulo.articulo_autores.values_list("autor_id", flat=True),
            [segundo_autor.pk],
        )

    def test_eliminar_articulo(self):
        with tempfile.TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                articulo = Articulo.objects.create(
                    titulo="Artículo para eliminar",
                    resumen="Resumen",
                    fecha_publicacion="2026-06-12",
                    revista=self.revista,
                    archivo_pdf=SimpleUploadedFile(
                        "eliminar.pdf",
                        b"%PDF-1.4 contenido",
                        content_type="application/pdf",
                    ),
                )
                response = self.client.post(
                    reverse("articulo:eliminar_articulo", args=[articulo.pk])
                )

        self.assertRedirects(response, reverse("articulo:lista_articulos"))
        self.assertFalse(Articulo.objects.filter(pk=articulo.pk).exists())
