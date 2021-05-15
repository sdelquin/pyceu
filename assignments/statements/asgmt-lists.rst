*************
Tarea: Listas
*************

Escribe un programa en Python que parta de una *cadena de texto* con notas entre 0 y 10 separadas por comas (sin espacios). El programa deberá calcular el **número de notas diferentes** que hay en la entrada, independientemente de que se repitan o no.

Utiliza esta plantilla para hacer la tarea::

    # ASGMT lists

    # asigna valores iniciales
    marks = '3,4,3,2,7,8,9,1,1,5'

    # tu código debajo de aquí

Para los valores de entrada de la plantilla, el resultado debería ser::

    unique_num_marks = 8

.. hint::
    - La función ``split()`` te ayudará mucho en esta tarea.
    - Recorrer elementos con un bucle ``for`` suele ser una buena idea.
    - Para añadir elementos a una lista inicialmente vacía tienes la función ``append()``.
    - No te olvides de que ``len()`` nos sirve para calcular la longitud de una lista.

Las **variables de entrada** que debes inicializar en tu programa son las siguientes:

.. table::
    :align: left

    +-----------+---------+---------------------------+
    |  Nombre   |  Tipo   |        Descripción        |
    +===========+=========+===========================+
    | ``marks`` | ``str`` | Notas separadas por comas |
    +-----------+---------+---------------------------+

Las **variables de salida** que debes obtener en tu programa son las siguientes:

.. table::
    :align: left

    +----------------------+---------+-------------------------------------+
    |        Nombre        |  Tipo   |             Descripción             |
    +======================+=========+=====================================+
    | ``unique_num_marks`` | ``int`` | Número de notas diferentes (únicas) |
    +----------------------+---------+-------------------------------------+

.. include:: ../notice.rst
