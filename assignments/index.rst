######
Tareas
######

.. toctree::
   :maxdepth: 2
   :caption: Contents:

****************
Tarea 3.1: Datos
****************

1.	Asigna el valor entero ``1985`` a la variable ``bttf`` y muestra su valor.
2.	Descubre el tipo del literal ``'Castle on the Hill'`` después de asignarlo a la variable ``song``.
3.	Asigna el valor ``False`` a la variable ``make_war`` y muestra su tipo.
4.	Asigna la expresión ``4 + 3`` a la variable ``result`` y muestra su valor y su tipo.
5.	Asigna la expresión ``result + 3.0`` a la variable ``result2`` y muestra su valor y su tipo. ¿Notas algo raro?
6.	Realiza la operación ``7 / 4`` y asígnala a la variable ``quotient``. Ahora realiza la operación ``7 // 4`` y asígnala a la variable ``quotient2``. Mira sus resultados y reflexiona.

Utiliza esta plantilla para hacer la tarea::

   import os

   # ↓ tu código debajo de aquí

   # ↑ tu código encima de aquí

   # =========== NO TOCAR ===========
   if os.getenv('CHECK'):
       print(
           locals().get('bttf', 'UNDEF'),
           locals().get('song', 'UNDEF'),
           locals().get('make_war', 'UNDEF'),
           locals().get('result', 'UNDEF'),
           locals().get('result2', 'UNDEF'),
           locals().get('quotient', 'UNDEF'),
           locals().get('quotient2', 'UNDEF'),
       )
   # ================================
