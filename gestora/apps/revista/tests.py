from django.test import TestCase
from django.urls import reverse

from .models import Revista


class RevistaViewsTests(TestCase):
    def setUp(self):
        self.revista = Revista.objects.create(
            nombre="Revista inicial",
            issn="1111-2222",
            factor_impacto="1.25",
        )

    def test_listar_revistas(self):
        response = self.client.get(reverse("revista:lista_revistas"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "revista/lista_revistas.html")

    def test_crear_revista(self):
        response = self.client.post(
            reverse("revista:crear_revista"),
            {
                "nombre": "Revista de prueba",
                "issn": "1234-5678",
                "factor_impacto": "2.50",
            },
        )

        self.assertRedirects(response, reverse("revista:lista_revistas"))
        self.assertTrue(
            Revista.objects.filter(nombre="Revista de prueba").exists()
        )

    def test_editar_revista_actualiza_el_mismo_registro(self):
        response = self.client.post(
            reverse("revista:editar_revista", args=[self.revista.pk]),
            {
                "nombre": "Revista actualizada",
                "issn": "1111-2222",
                "factor_impacto": "4.50",
            },
        )

        self.assertRedirects(response, reverse("revista:lista_revistas"))
        self.revista.refresh_from_db()
        self.assertEqual(self.revista.nombre, "Revista actualizada")
        self.assertEqual(Revista.objects.count(), 1)

    def test_eliminar_revista(self):
        response = self.client.post(
            reverse("revista:eliminar_revista", args=[self.revista.pk])
        )

        self.assertRedirects(response, reverse("revista:lista_revistas"))
        self.assertFalse(Revista.objects.filter(pk=self.revista.pk).exists())
