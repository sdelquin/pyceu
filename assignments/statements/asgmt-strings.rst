***********************
Tarea: Cadenas de texto
***********************

Se pide transformar una cadena de texto de entrada ``text`` en función de unas reglas:

- El **primer carácter** indica el número de veces que se repite la primera subcadena. *Puedes suponer sólo números del 1 al 9*.
- El **último carácter** indica el número de veces que se repite la última subcadena. *Puedes suponer sólo números del 1 al 9*.
- Las dos subcadenas de entrada están separadas *siempre* por un **guión medio**.
- La primera subcadena, además de repetirla, hay que pasarla a **mayúsculas**.
- La segunda subcadena, además de repetirla, hay que pasarla a **título**.
- Las dos subcadenas de salida deberán estar separadas por una **almohadilla**.

Utiliza esta plantilla para hacer la tarea::

    # ASGMT strings

    # asigna valores iniciales
    text = '2toc-penny3'

    # tu código debajo de aquí

Para los valores de entrada de la plantilla, el resultado debería ser::

    result = 'TOCTOC#PennyPennyPenny'

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

.. important:: Recuerda que tu programa debe funcionar para distintas cadenas de entrada, y que las repeticiones de las cadenas también son variables según lo que se indique.

.. include:: ../notice.rst
