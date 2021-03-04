******************
Tarea 3.2: Números
******************

Dada una ecuación de segundo grado :math:`ax^2 + bx + c = 0` calcula los valores de :math:`x` que satisfacen la igualdad. No te preocupes de los casos en los que la ecuación no tiene solución o en los que hay infinitas soluciones.

Utiliza esta plantilla para hacer la tarea::

    import os
    import sys

    # ↓ asigna valores iniciales
    a = 3
    b = 5
    c = 6
    # ↑ asigna valores iniciales

    # =========== NO TOCAR ===========
    if os.getenv('CHECK'):
        a, b, c = [int(v) for v in sys.argv[1:]]
    # ================================

    # ↓ tu código debajo de aquí

    # ↑ tu código encima de aquí

    # =========== NO TOCAR ===========
    if os.getenv('CHECK'):
        print(locals().get('x1', 'UNDEF'), locals().get('x2', 'UNDEF'))
    # ================================

Puedes comprobar soluciones con `esta calculadora online <http://es.onlinemschool.com/math/assistance/equation/quadratic/>`_.

.. include:: ../notice.rst
