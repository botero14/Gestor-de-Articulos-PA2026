from django.test import TestCase
from django.urls import reverse

from .models import Autor


class AutorViewsTests(TestCase):
    def setUp(self):
        self.autor = Autor.objects.create(
            nombre="Gabriel",
            apellido="García Márquez",
            sexo=Autor.Sexo.MASCULINO,
            nacionalidad="CO",
        )

    def test_editar_autor_actualiza_el_mismo_registro(self):
        response = self.client.post(
            reverse("autor:editar_autor", args=[self.autor.pk]),
            {
                "nombre": "Gabriel José",
                "apellido": "García Márquez",
                "sexo": Autor.Sexo.MASCULINO,
                "nacionalidad": "CO",
            },
        )

        self.assertRedirects(response, reverse("autor:lista_autores"))
        self.autor.refresh_from_db()
        self.assertEqual(self.autor.nombre, "Gabriel José")
        self.assertEqual(Autor.objects.count(), 1)

    def test_eliminar_autor_requiere_confirmacion_post(self):
        url = reverse("autor:eliminar_autor", args=[self.autor.pk])

        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code, 200)
        self.assertTrue(Autor.objects.filter(pk=self.autor.pk).exists())

        response_post = self.client.post(url)
        self.assertRedirects(response_post, reverse("autor:lista_autores"))
        self.assertFalse(Autor.objects.filter(pk=self.autor.pk).exists())
