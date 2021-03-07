********************
Tarea: Condicionales
********************

Criterios de promoción LOMCE en la ESO:

*El alumnado promocionará de curso cuando haya superado todas las materias cursadas o tenga
evaluación negativa en dos materias como máximo, siempre que estas dos no se correspondan
simultáneamente con Lengua Castellana y Literatura, y Matemáticas; y repetirá curso cuando tenga
evaluación negativa en tres o más materias, o bien en Lengua Castellana y Literatura, y Matemáticas
de forma simultánea.*

Se pide hacer un programa que diga si el alumnado de la ESO promocionará al siguiente curso teniendo en cuenta el número de suspensos y las calificaciones en Lengua y Matemáticas.

Utiliza esta plantilla para hacer la tarea::

    # asigna valores iniciales
    num_fails = 2
    spanish_grade = 7
    maths_grade = 3

    # tu código debajo de aquí

Para los valores de entrada de la plantilla, el resultado debería ser::

    promote = True

Las **variables de entrada** que debes inicializar en tu programa son las siguientes:

.. table::
    :align: left

    +-------------------+---------+---------------------------------------------+
    |      Nombre       |  Tipo   |                 Descripción                 |
    +===================+=========+=============================================+
    | ``num_fails``     | ``int`` | Número de suspensos                         |
    +-------------------+---------+---------------------------------------------+
    | ``spanish_grade`` | ``int`` | Calificación numérica (0-10) de Lengua      |
    +-------------------+---------+---------------------------------------------+
    | ``maths_grade``   | ``int`` | Calificación numérica (0-10) de Matemáticas |
    +-------------------+---------+---------------------------------------------+

Las **variables de salida** que debes obtener en tu programa son las siguientes:

.. table::
    :align: left

    +-------------+----------+----------------------------------------------+
    |   Nombre    |   Tipo   |                 Descripción                  |
    +=============+==========+==============================================+
    | ``promote`` | ``bool`` | Verdadero si promociona. Falso en otro caso. |
    +-------------+----------+----------------------------------------------+

.. rubric:: Árbol de decisiones

El siguiente diagrama explica el árbol de decisiones:

.. only:: latex

    .. image:: img/eso-promote.png

.. only:: html

    .. image:: img/eso-promote.svg

.. include:: ../notice.rst
