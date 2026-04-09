# TCN_web
Sistema de venta de boletos de autobús automatizado en el estado de Baja California en su versión web.

Para correr el proyecto desde 0, sigue el flujo de los siguientes comandos:

1. Hacer las migraciones
python manage.py migrate

2. Realizar los inserts de catalogos necesarios que NO se realizan en la aplicacion web
python manage.py loaddata datos_iniciales.json

3. Crear un administrador o super usuario (en caso de no tenerlo)
python manage.py createsuperuser

4. Correr el servidor (reemplazar la direccion IP por la que estes usando)
python manage.py runserver 0.0.0.0:8000 