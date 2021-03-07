***********************
Tarea: Cadenas de texto
***********************

Se pide transformar una cadena de texto de entrada ``text`` en función de unas reglas:

- El **primer carácter** indica el número de veces que se repite la primera subcadena.
- El **último carácter** indica el número de veces que se repite la última subcadena.
- Las dos subcadenas de entrada están separadas *siempre* por un **guión medio**.
- La primera subcadena, además de repetirla, hay que pasarla a **mayúsculas**.
- La segunda subcadena, además de repetirla, hay que pasarla a **título**.
- Las dos subcadenas de salida deberán estar separadas por una **almohadilla**.

Utiliza esta plantilla para hacer la tarea::

    # asigna valores iniciales
    text = '2toc-3penny'

    # tu código debajo de aquí

Aquí tienes un **ejemplo** con el resultado que debería dar tu programa:

.. table::
    :align: left

    +-----------------+----------------------------+
    |     Entrada     |           Salida           |
    +=================+============================+
    | ``2toc-penny3`` | ``TOCTOC#PennyPennyPenny`` |
    +-----------------+----------------------------+

Las **variables de entrada** que debes inicializar en tu programa son las siguientes:

.. table::
    :align: left

    +----------+---------+------------------+
    |  Nombre  |  Tipo   |   Descripción    |
    +==========+=========+==================+
    | ``text`` | ``str`` | Texto de entrada |
    +----------+---------+------------------+

Las **variables de salida** que debes obtener en tu programa son las siguientes:

.. table::
    :align: left

    +------------+---------+------------------------------------------+
    |   Nombre   |  Tipo   |               Descripción                |
    +============+=========+==========================================+
    | ``result`` | ``str`` | Cadena de texto con las transformaciones |
    +------------+---------+------------------------------------------+

.. include:: ../notice.rst
