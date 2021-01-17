# demo-Wellness

Api en Python desarrollada para la demo técnica de la empresa Wellness Tech Group.


## Frameworks y librerias 

Para el desarrollo de la API se han utilizado:

1. **Flask**: Framework que contiene los elementos necesarios para realizar una API en python.
2. **SQLAlchemy**: ORM para acceder a la base de datos, en este caso **MySQL**.

Ambas han sido seleccionadas porque ya estaba familiarizado con ellas previamente. Si hubiese tenido más tiempo hubiera utilizado otro ORM más popular o incluso código PL/SQL. 

## Instalación y configuración

Para el proyecto será necesario tener instalado Python y tener acceso a una base de datos MySQL (puede ser en local). Una vez instalados, tendremos que instalar las dependencias de python, para ello se ejecutará el comando (hay que estar en el directorio del proyecto): 

```
pip install -r requirements.txt
```

Una vez finalice la instalación de dependencias, tendremos que modificar la configuración del proyecto en el fichero _**config.yml**_, en el que nos encontraremos las siguientes propiedades, las cuales tendremos que modificar para nuestro entorno propio:

- **api**
  - host: Host donde se lanzará el servidor (por defecto localhost)
  - port: Puerto donde se ejecutará (por defecto 3000)
  - jwtSecret: Clave secreta para el encriptado del JWT. No se debe publicar nunca la utilizada.
- **database**
  - host: Dirección del servidor de base de datos (MySQL) (Puede ser localhost)
  - port: Puerto del servidor de base de datos
  - database: Nombre del esquema que utilizaremos (No es necesario que esté creado previamente)
  - username: Usuario que utilizaremos para conectarnos a la base de datos
  - password: Contraseña del usuario anterio

## Estructura del proyecto

Debido a que es una demo, no hay demasiados archivos y, por tanto, he decidido no crear directorios que contuvieran como mucho un par de archivos. Aún así, el proyecto tendrá una carpeta docs, con los documentos enviados por parte de Wellness Tech Group. En cuanto al directorio raíz nos encontraremos los siguientes archivos:

- **README.md**: Este mismo documento.
- **requirements.txt**: Documento con todas las dependencias necesarias para la correcta ejecución del proyecto.
- **config.yml**: Fichero de configuración, comentado con más detalle en la sección anterior.
- **server.py**: Fichero ejecutable que lanza la aplicacion de Flask, escuchara en el puerto indicado, en el fichero de configuración.
- **models.py**: Además de contener la definición de los objetos que se guardaran en base de datos, se puede ejecutar el fichero para crear la estructura de base de datos e inicializarla con los datos del csv */docs/Monitoring report.csv*
- **database.py:** Contiene ciertas funciones utiles para la conexión con base de datos.
- **auth.py**: Rutas de la API para el módulo de autenticación.
- **energy.py**: Rutas de la API para el módulo de energía (parte obligatoria de la demo)
- **demo.postman_collection.json**: Colección de postman que contiene las 5 llamadas que se han implementado.

## Ejecución

Para ejecutar el proyecto habrá que lanzar los siguientes dos comandos (en el directorio del proyecto):

```
python models.py
```

```
python server.py
```

El primer comando creará la base de datos y la inicializará con los datos del csv, mostrando por pantalla cada vez que se insertan 500 registros puesto que se realiza una petición a la base de datos cada 500 objetos para optimizar el rendimiento.

El segundo, se encargará de lanzar la API de Flask.


## API

Ya que, por falta de tiempo, no he implementado swagger u otro documentador de API, añado la colección de postman para que se pueda utilizar las peticiones rápidamente. La colección tendrá dos variables, host (dirección y puerto del servidor de la API, ej: localhost:3000) y token (token para la autenticación), y 5 llamadas:
 
1. **POST /user/signup**: Recibe en el body un username y password, del usuario que se va a crear. Devuelve un 200 ok con el usuario que se ha almacenado en base de datos (como mejora habría que eliminar que no se muestre la contraseña aunque este _hasheada_, o un 400 en caso de que el nombre de usuario ya exista.
1. **POST /user/login** Recibe en el body un username y password. Devuelve un 200 y el token que se debe añadir a la variable comentada anteriormente para autenticarnos con ese usuario, o un 401 en caso de que el usuario o la contraseña no sean correctos.
1. **GET /user**: Devuelve un 200 y el usuario que ha iniciado sesión o un 401 en caso de no tener token o que este sea incorrecto. Dependiendo como se vaya a utilizar la API podría ser conveniente implementar una caducidad en el token.
1. **GET /energy**: Devuelve todas los datos almacenados de energía entre dos fechas dadas. Las fechas se deben pasar como parámetros, es decir, añadiendo a la url, por ejemplo, la cadena: ?startDate=01/08/2019&endDate=02/08/2019. Las fechas deben ir en formato dd/mm/yyyy, en caso contrario, se devolverá un 400. Esta petición se utilizaría para implementar el gráfico de abajo a la izquierda en la imagen _dashboard.png_. Cabe destacar, que apareceran todas las energías almacenadas del día incluyendo los del día de inicio y fin. Es decir, en el ejemplo anterior aparecerían desde 01/08/2019 00:00:00 hasta 02/08/2019 23:59:59 
1. **GET /energy/fechaInicio/fechaFin**: Devuelve el consumo y consumo reactivo agrupado por días, las fechas funcionan de la misma forma que en la petición anterior, salvo que el patrón es dd-mm-yyyy, puesto que las / entraría en conflico con la url. Habría tenido más sentido utilizar parámetros como en el anterior, pero ya que es una demostración técnica he preferido realizar distintas implementaciones. Esta petición servirá para implementar el gráfico inferior de la derecha, ya que suma todos los consumos por día, devolviendo esta suma para cada día desde la fecha de inicio hasta la fecha de fin indicadas en la URL.


 

## Mejoras y siguientes pasos

1. Implementaría una petición similar a /energy/starDate/endDate pero para agrupar los datos por meses. Para implementar el apartado _Datos eléctricos del mes en curso_ de la imagen _dashboard.png_ 
1. Añadiría Swagger para documentar la API correctamente.
1. No utilizaría literales en el código. Puesto que es un proyecto pequeño, he optado por no crear cualquier texto o número en constantes ya que alargaría el tiempo de desarrollo, pero falicita mucho el mantenimiento.
1. Utilizaría una estructura de directorios para organizar los archivos (models, controllers, routes...), no ha sido necesario puesto que la demo no es demasiado grande.
1. Añadiría más seguridad al login:
  1. Implementando _salts_ para las contraseñas.
  1. En lugar de codificar la id del usuario con el jwt, añadiría una nueva columna única de cada usuario y la usaría junto más datos.
1. Documentaría más el código para facilitar el mantenimiento y comprensión.
1. Dockerizaría la aplicación y base de datos para que sea mas simple de ejecutar.
