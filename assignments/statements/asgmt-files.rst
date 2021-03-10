***************
Tarea: Ficheros
***************

Para esta tarea vamos a utilizar un fichero de datos que contiene puntos en el espacio (x, y), uno por cada línea. Una vez leído, el programa deberá calcular la `distancia eucídea <https://es.wikipedia.org/wiki/Distancia_euclidiana>`_ entre cada punto y el origen de coordenadas (0, 0). Por último, habrá que determinar cuál de todas ellas es la distancia mínima.

Puedes utilizar el siguiente fichero de datos como entrada a tu programa:

.. code-block:: text
    :caption: points.txt

    3 7
    1 9
    2 -4
    5 6
    2 7
    -1 4
    5 -3
    4 -1

.. note::
    - Guarda este contenido en un fichero llamado ``points.txt`` en la misma carpeta que tu código Python para que no tengas problemas de rutas.
    - Las coordenadas dentro de la misma línea están separadas por **espacio** y contienen **valores enteros** (para simplificar).

Utiliza esta plantilla para hacer la tarea::

    # asigna valores iniciales
    filename = 'points.txt'

    # tu código debajo de aquí
    f = open(filename)

Para los valores de entrada de la plantilla, el resultado debería ser::

    min_distance = 4.123105625617661

Las **variables de entrada** que debes inicializar en tu programa son las siguientes:

.. table::
    :align: left

    +--------------+---------+-----------------------------+
    |    Nombre    |  Tipo   |         Descripción         |
    +==============+=========+=============================+
    | ``filename`` | ``str`` | Nombre del fichero de datos |
    +--------------+---------+-----------------------------+

Las **variables de salida** que debes obtener en tu programa son las siguientes:

.. table::
    :align: left

    +------------------+-----------+-------------------------------------------+
    |      Nombre      |   Tipo    |                Descripción                |
    +==================+===========+===========================================+
    | ``min_distance`` | ``float`` | Distancia mínima al origen de coordenadas |
    +------------------+-----------+-------------------------------------------+

.. include:: ../notice.rst
