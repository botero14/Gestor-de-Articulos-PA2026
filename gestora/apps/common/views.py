from django.shortcuts import render


def pagina_no_encontrada(request, exception=None):
    """
    Renderiza la plantilla personalizada para una URL que no existe.

    El estado HTTP 404 informa al navegador y a los clientes que el recurso no
    fue encontrado. ``exception`` es recibido por el manejador 404 de Django.
    """
    return render(request, "404.html", status=404)
