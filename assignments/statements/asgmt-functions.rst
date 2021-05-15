****************
Tarea: Funciones
****************

En esta tarea vamos a trabajar con *números primos*. Al final se tratará de conseguir escribir un programa que calcule los :math:`n` primeros números primos. Para ello vamos a utilizar *funciones* en nuestro programa.

Necesitaremos 2 funciones::

    def is_prime(n):
        # Devuelve True si "n" es primo y False en otro caso
    
    def get_primes(how_many):
        # Devuelve una lista con los "how_many" primeros primos

.. important:: La función ``get_primes()`` hará uso de la función ``is_prime()``.

Escribe un programa en Python que dado un número entero (indicando cuántos primos se quieren calcular) genere **una lista** con dichos números primos.

Utiliza esta plantilla para hacer la tarea::

    # ASGMT functions

    # asigna valores iniciales
    num_primes = 10

    # tu código debajo de aquí
    def is_prime(n):
        # código de la función

    def get_primes(how_many):
        primes = []
        i = 2
        while len(primes) < how_many:
            if is_prime(i):
                primes.append(i)
            i += 1
        return primes
    
    primes = get_primes(num_primes)  # no borrar esta línea

Para los valores de entrada de la plantilla, el resultado debería ser::

    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

Las **variables de entrada** que debes inicializar en tu programa son las siguientes:

.. table::
    :align: left

    +----------------+---------+---------------------------------------+
    |     Nombre     |  Tipo   |              Descripción              |
    +================+=========+=======================================+
    | ``num_primes`` | ``int`` | Cantidad de números primos a calcular |
    +----------------+---------+---------------------------------------+

Las **variables de salida** que debes obtener en tu programa son las siguientes:

.. table::
    :align: left

    +------------+----------+-----------------------------------------+
    |   Nombre   |   Tipo   |               Descripción               |
    +============+==========+=========================================+
    | ``primes`` | ``list`` | Lista con los números primos calculados |
    +------------+----------+-----------------------------------------+

.. include:: ../notice.rst
