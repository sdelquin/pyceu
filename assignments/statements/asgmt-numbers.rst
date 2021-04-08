******************
Tarea: Números
******************

Dada una ecuación de segundo grado :math:`ax^2 + bx + c = 0` calcula los valores de :math:`x` que satisfacen la igualdad.

.. math::
    :nowrap:

    \begin{eqnarray*}
       x1 & = & \frac{-b + \sqrt{b^2 - 4ac}}{2a} \\
       x2 & = & \frac{-b - \sqrt{b^2 - 4ac}}{2a}
    \end{eqnarray*}

*No te preocupes de los casos en los que la ecuación no tiene solución o en los que hay infinitas soluciones.*

Utiliza esta plantilla para hacer la tarea::

    # asigna valores iniciales
    a = 1
    b = -5
    c = -84

    # tu código debajo de aquí

Para los valores de entrada de la plantilla, el resultado debería ser::

    x1 = 12
    x2 = -7 

.. tip::
    - Trata de *separar los cálculos* parciales en variables intermedias.
    - No repitas cálculos, intenta *reutilizar variables* con cálculos ya hechos.
    - Recuerda que la *raíz cuadrada* se puede expresar en términos de *exponenciación*.

.. note:: Puedes comprobar tus soluciones con `esta calculadora online <http://es.onlinemschool.com/math/assistance/equation/quadratic/>`_ o bien utilizar datos de entrada de algunas `ecuaciones ya resueltas <https://www.superprof.es/apuntes/escolar/matematicas/algebra/ecuaciones/ejercicios-ecuaciones-de-segundo-grado.html>`_.

Las **variables de entrada** que debes inicializar en tu programa son las siguientes:

.. table::
    :align: left

    +--------+---------+----------------------------+
    | Nombre |  Tipo   |        Descripción         |
    +========+=========+============================+
    | ``a``  | ``int`` | Coeficiente de :math:`x^2` |
    +--------+---------+----------------------------+
    | ``b``  | ``int`` | Coeficiente de :math:`x`   |
    +--------+---------+----------------------------+
    | ``c``  | ``int`` | Término independiente      |
    +--------+---------+----------------------------+

Las **variables de salida** que debes obtener en tu programa son las siguientes:

.. table::
    :align: left

    +--------+-----------+---------------------------------+
    | Nombre |   Tipo    |           Descripción           |
    +========+===========+=================================+
    | ``x1`` | ``float`` | Primera solución de la ecuación |
    +--------+-----------+---------------------------------+
    | ``x2`` | ``float`` | Segunda solución de la ecuación |
    +--------+-----------+---------------------------------+

.. include:: ../notice.rst
