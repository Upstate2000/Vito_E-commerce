## Requisitos
- Git instalado
- Python 3.10+
- pip (gestor de paquetes)
- virtualenv o el módulo venv integrado
- pillow

## Instalación
1. Clonar el repositorio.
git clone <url-del-repo>
cd myshop

2. Crea y activa virtualenv:
  python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

3. Instala dependencias:
   pip install -U pip
   pip install -r requirements.txt
5. Crear el archivo de entorno.
cp .env.example .env
# editar .env según sea necesario

5. Configurar la base de datos SQLite.
- No necesitas crear la base de datos manualmente. Django creará el archivo SQLite cuando ejecutes las migraciones.

6. Ejecuta migraciones:
   python manage.py makemigrations
   python manage.py migrate

7. Crea superusuario:
   python manage.py createsuperuser

8. Ejecutar servidor de desarrollo:
   python manage.py runserver
