*******************
Tarea: Diccionarios
*******************

Escribe un programa en Python que use, por un lado, una *cadena de texto* con palabras y, por otro, una *letra*. El código deberá *obtener un diccionario* donde las **claves** serán las palabras y los **valores** serán el número de veces que aparece la *letra* en cada *palabra*.

Utiliza esta plantilla para hacer la tarea::

    # ASGMT dicts

    # asigna valores iniciales
    words = 'aro|clara|patata|brillo'
    letter = 'a'

    # tu código debajo de aquí

Para los valores de entrada de la plantilla, el resultado debería ser::

    letter_counter = {'aro': 1, 'clara': 2, 'patata': 3, 'brillo': 0}

.. hint::
    - De cara a "dividir" la cadena de texto, fíjate que las palabras están separadas por barras verticales ``|``.
    - La función ``split()`` es un poderoso aliado.
    - Existen formas sencillas de contar el número de veces que aparece un carácter en una cadena de texto.

Las **variables de entrada** que debes inicializar en tu programa son las siguientes:

.. table::
    :align: left

    +------------+---------+------------------------------------------------+
    |   Nombre   |  Tipo   |                  Descripción                   |
    +============+=========+================================================+
    | ``words``  | ``str`` | Palabras separadas por barra vertical          |
    +------------+---------+------------------------------------------------+
    | ``letter`` | ``str`` | Letra que se usará para buscar sus apariciones |
    +------------+---------+------------------------------------------------+

Las **variables de salida** que debes obtener en tu programa son las siguientes:

.. table::
    :align: left

    +--------------------+----------+-----------------------------------------------------------------------------------------------------------------------+
    |       Nombre       |   Tipo   |                                                      Descripción                                                      |
    +====================+==========+=======================================================================================================================+
    | ``letter_counter`` | ``dict`` | Diccionario cuyas claves son palabras (**cadenas de texto**) y cuyos valores son el número de apariciones de la letra |
    +--------------------+----------+-----------------------------------------------------------------------------------------------------------------------+

.. include:: ../notice.rst
