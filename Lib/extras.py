"""Small everyday helpers added by sid-python.

This module is not part of official Python.

    unique(iterable, key=None)                 remove duplicates, keep order
    first(iterable, default=None, where=None)  first item, or first match
    group_by(iterable, key)                    sort items into groups by key
    deep_get(data, *keys, default=None)        safely reach into nested data
    human_size(size, binary=False)             1536000 -> '1.5 MB'
    slugify(text)                              'Hello World!' -> 'hello-world'
    timer(label='Elapsed', show=True)          time a block of code
"""

import re
import time
import unicodedata

__all__ = ['deep_get', 'first', 'group_by', 'human_size', 'slugify', 'timer',
           'unique']

_DECIMAL_UNITS = ('KB', 'MB', 'GB', 'TB', 'PB')
_BINARY_UNITS = ('KiB', 'MiB', 'GiB', 'TiB', 'PiB')


def unique(iterable, key=None):
    """Return a list of the items of iterable with duplicates removed.

    The first of each group of duplicates is kept and the order is unchanged.
    If key is given, items are duplicates when key(item) is the same.  Items
    that cannot be hashed, such as lists, are allowed but are slower to check.
    """
    seen = set()
    seen_unhashable = []
    result = []
    for item in iterable:
        marker = item if key is None else key(item)
        try:
            if marker in seen:
                continue
            seen.add(marker)
        except TypeError:
            if marker in seen_unhashable:
                continue
            seen_unhashable.append(marker)
        result.append(item)
    return result


def first(iterable, default=None, *, where=None):
    """Return the first item of iterable, or default if there is none.

    If where is given, return the first item for which where(item) is true.
    """
    for item in iterable:
        if where is None or where(item):
            return item
    return default


def group_by(iterable, key):
    """Return a dict that maps each key(item) to the list of its items.

    Groups are in the order their key first appears, and the items in each
    group keep their order.  Unlike itertools.groupby(), items with the same
    key do not need to be next to each other.
    """
    groups = {}
    for item in iterable:
        k = key(item)
        try:
            group = groups[k]
        except KeyError:
            group = groups[k] = []
        group.append(item)
    return groups


def deep_get(data, *keys, default=None):
    """Follow keys and indexes into nested data, without raising an error.

    Return default if any step is missing:

        >>> deep_get({'user': {'pets': ['Rex']}}, 'user', 'pets', 0)
        'Rex'
        >>> deep_get({'user': {}}, 'user', 'pets', 0, default='none')
        'none'
    """
    for key in keys:
        try:
            data = data[key]
        except (KeyError, IndexError, TypeError):
            return default
    return data


def human_size(size, *, binary=False):
    """Return a number of bytes as easy-to-read text, such as '1.5 MB'.

    Units step by 1000 (KB, MB, ...).  If binary is true they step by 1024
    and use the matching names (KiB, MiB, ...).
    """
    base = 1024 if binary else 1000
    value = abs(size)
    if value < base:
        return f'{size} B'
    for unit in _BINARY_UNITS if binary else _DECIMAL_UNITS:
        value /= base
        # Compare the rounded value so that 999999 gives '1.0 MB'
        # and not '1000.0 KB'.
        if round(value, 1) < base:
            break
    sign = '-' if size < 0 else ''
    return f'{sign}{value:.1f} {unit}'


def slugify(text):
    """Return text in a form that is safe for URLs and file names.

    The result has only lowercase ASCII letters, digits and single hyphens.
    Accents are removed, and any other non-ASCII letters are dropped, so the
    result can be empty.
    """
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


class timer:
    """Context manager that measures how long a block of code takes.

        with timer('Loading') as t:
            load_everything()

    This prints a line such as 'Loading: 1.500 seconds' when the block ends,
    even if it raises an exception.  The time in seconds is also available
    as t.elapsed.  Pass show=False to skip printing.
    """

    def __init__(self, label='Elapsed', *, show=True):
        self.label = label
        self.show = show
        self.elapsed = None

    def __enter__(self):
        self.elapsed = None
        self._start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.elapsed = time.perf_counter() - self._start
        if self.show:
            print(f'{self.label}: {self.elapsed:.3f} seconds')
