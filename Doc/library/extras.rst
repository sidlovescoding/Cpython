:mod:`!extras` --- Everyday helper functions
============================================

.. module:: extras
   :synopsis: Small everyday helpers added by sid-python.

**Source code:** :source:`Lib/extras.py`

--------------

This module is a sid-python addition and is not part of official Python.
It collects a few small helpers for common jobs.


.. function:: unique(iterable, key=None)

   Return a list of the items of *iterable* with duplicates removed.  The first
   of each group of duplicates is kept and the order is unchanged.  If *key* is
   given, items are duplicates when ``key(item)`` is the same.  Items that
   cannot be hashed, such as lists, are allowed but are slower to check.

   ::

      >>> unique([3, 1, 3, 2, 1])
      [3, 1, 2]


.. function:: first(iterable, default=None, *, where=None)

   Return the first item of *iterable*, or *default* if there is none.  If
   *where* is given, return the first item for which ``where(item)`` is true.

   ::

      >>> first([1, 2, 3, 4], where=lambda n: n > 2)
      3


.. function:: group_by(iterable, key)

   Return a :class:`dict` that maps each ``key(item)`` to a list of the items
   of *iterable* with that key.  Groups are in the order their key first
   appears, and the items in each group keep their order.  This is like
   ``Object.groupBy()`` in JavaScript and ``groupBy`` in Kotlin.

   Unlike :func:`itertools.groupby`, items with the same key do not need to be
   next to each other::

      >>> group_by(['apple', 'bean', 'avocado', 'beet'], key=lambda w: w[0])
      {'a': ['apple', 'avocado'], 'b': ['bean', 'beet']}


.. function:: deep_get(data, *keys, default=None)

   Follow *keys* and indexes into nested data, without raising an error.
   Return *default* if any step is missing.

   ::

      >>> deep_get({'user': {'pets': ['Rex']}}, 'user', 'pets', 0)
      'Rex'
      >>> deep_get({'user': {}}, 'user', 'pets', 0, default='none')
      'none'


.. function:: human_size(size, *, binary=False)

   Return a number of bytes as easy-to-read text.  Units step by 1000 (KB, MB
   and so on).  If *binary* is true they step by 1024 and use the matching names
   (KiB, MiB and so on).

   ::

      >>> human_size(1536000)
      '1.5 MB'
      >>> human_size(1024, binary=True)
      '1.0 KiB'


.. function:: slugify(text)

   Return *text* in a form that is safe for URLs and file names, with only
   lowercase ASCII letters, digits and single hyphens.  Accents are removed and
   any other non-ASCII letters are dropped, so the result can be empty.

   ::

      >>> slugify('Café Crème!')
      'cafe-creme'


.. class:: timer(label='Elapsed', *, show=True)

   Context manager that measures how long a block of code takes.  When the block
   ends, even with an exception, it prints a line such as
   ``Loading: 1.500 seconds``, unless *show* is false.

   ::

      with timer('Loading') as t:
          load_everything()

   .. attribute:: elapsed

      The time taken in seconds, or ``None`` until the block has ended.
