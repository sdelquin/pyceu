*************
Tarea: Listas
*************

Escribe un programa en Python que parta de una *cadena de texto* con notas de tipo entero entre 0 y 10 separadas por comas (sin espacios). El programa deberá calcular el **número de aprobados y el número de suspensos** que hay en la entrada.

Utiliza esta plantilla para hacer la tarea::

    # ASGMT lists

    # asigna valores iniciales
    marks = '3,4,3,2,7,8,9,1,1,5'

    # tu código debajo de aquí

Para los valores de entrada de la plantilla, el resultado debería ser::

    passed = 4
    failed = 6

.. hint::
    - La función ``split()`` te ayudará mucho en esta tarea.
    - Recorrer elementos con un bucle ``for`` suele ser una buena idea.
    - Recuerda usar variables acumuladoras.
    - Ten en cuenta que habrá que convertir cada número a entero usando la función ``int()``

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

    +------------+---------+---------------------+
    |   Nombre   |  Tipo   |     Descripción     |
    +============+=========+=====================+
    | ``passed`` | ``int`` | Número de aprobados |
    +------------+---------+---------------------+
    | ``failed`` | ``int`` | Número de suspensos |
    +------------+---------+---------------------+

.. include:: ../notice.rst
