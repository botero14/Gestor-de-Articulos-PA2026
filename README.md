# Gestor de Artículos Científicos - PA2026

Este proyecto es un sistema de gestión de artículos científicos y autores desarrollado como parte de las asignaturas de Programación de la Universidad de La Guajira. Permite administrar la información de publicaciones académicas, perfiles de autores y el orden de autoría mediante una arquitectura relacional en Django.

---

## Tecnologías y Versiones

![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![Uniguajira](https://img.shields.io/badge/Universidad-de%20La%20Guajira-00875A?style=for-the-badge)

El entorno de desarrollo está configurado y garantizado para funcionar bajo las siguientes versiones de software:

- **Python:** `3.14.x` (o superior)
- **Django:** `5.2.x`
- **Base de Datos:** SQLite 3 (Entorno de desarrollo local) / Compatible con MySQL.

### Librerías del Entorno (`requirements.txt`)

- `django>=5.2,<5.3`
- `django-countries>=7.5` _(Para la gestión de nacionalidades en el modelo Author)_

---

## Instrucciones para Levantar el Servidor

Sigue estos pasos en la terminal de tu sistema (PowerShell, CMD o Terminal de Linux/WSL) para ejecutar el proyecto localmente.

```bash
python -m venv entorno
source entorno/bin/activate|
```

### 1. Clonar el repositorio y navegar al proyecto

```bash
git clone [https://github.com/botero14/Gestor-de-Articulos-PA2026.git](https://github.com/botero14/Gestor-de-Articulos-PA2026.git)
cd Gestor-de-Articulos-PA2026/gestora
```

## 2. Instalar las dependencias

```bash
pip install -r requirements.txt
```
