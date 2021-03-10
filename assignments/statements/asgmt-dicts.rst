*******************
Tarea: Diccionarios
*******************

Escribe un programa en Python que use una *cadena de texto* con nombres de alumnado y sus notas. El código deberá *convertir esta cadena de texto en su correspondiente diccionario*, donde las **claves** serán los nombres del alumnado y los **valores** sus calificaciones (**convertidas a entero**).

Utiliza esta plantilla para hacer la tarea::

    # asigna valores iniciales
    marks = 'juan:1,antonio:7,inma:9,pepe:3,sara:5'

    # tu código debajo de aquí

    Para los valores de entrada de la plantilla, el resultado debería ser::
    
        notebook = {'juan': 1, 'antonio': 7, 'inma': 9, 'pepe': 3, 'sara': 5}

.. important::
    - Fíjate que los bloques de alumnado están separados por comas ``,`` y dentro de ese bloque, el nombre y la calificación están separados por dos puntos ``:``
    - La función ``split()`` es un poderoso aliado.
    - Hay que *convertir las notas* de ``str`` a ``int`` antes de almacenarlas en el diccionario.

Las **variables de entrada** que debes inicializar en tu programa son las siguientes:

.. table::
    :align: left

    +-----------+---------+-------------------------------------------+
    |  Nombre   |  Tipo   |                Descripción                |
    +===========+=========+===========================================+
    | ``marks`` | ``str`` | ``<nombre>:<nota>,<nombre>:<nota>,`` etc. |
    +-----------+---------+-------------------------------------------+

.. note:: Por simplificar, usaremos sólo nombre de pila en cada alumno/a y notas con valores enteros.

Las **variables de salida** que debes obtener en tu programa son las siguientes:

.. table::
    :align: left

    +--------------+----------+------------------------------------------------------------------------------------------------------------------+
    |    Nombre    |   Tipo   |                                                   Descripción                                                    |
    +==============+==========+==================================================================================================================+
    | ``notebook`` | ``dict`` | Diccionario cuyas claves son nombres (**cadenas de texto**) y cuyos valores son notas (**convertidas a entero**) |
    +--------------+----------+------------------------------------------------------------------------------------------------------------------+

.. include:: ../notice.rst
