This is Python version 3.15.2
=============================

.. image:: https://github.com/sidlovescoding/Cpython/actions/workflows/sid-python.yml/badge.svg?branch=sid-python
   :alt: sid-python build status on GitHub Actions
   :target: https://github.com/sidlovescoding/Cpython/actions/workflows/sid-python.yml

.. image:: https://github.com/python/cpython/actions/workflows/build.yml/badge.svg?branch=main&event=push
   :alt: CPython build status on GitHub Actions
   :target: https://github.com/python/cpython/actions

.. image:: https://dev.azure.com/python/cpython/_apis/build/status/Azure%20Pipelines%20CI?branchName=main
   :alt: CPython build status on Azure DevOps
   :target: https://dev.azure.com/python/cpython/_build/latest?definitionId=4&branchName=main

.. image:: https://img.shields.io/badge/discourse-join_chat-brightgreen.svg
   :alt: Python Discourse chat
   :target: https://discuss.python.org/


Copyright © 2001 Python Software Foundation.  All rights reserved.

See the end of this file for further copyright and license information.

.. contents::

sid-python: changes from official Python
----------------------------------------

This is **sid-python**, a personal version of CPython 3.14.  It is still
installed and run as ``python``; ``sys.version`` ends with ``(sid-python)``.
Everything below is in addition to official Python 3.14, and each change has
tests.

New built-in functions
^^^^^^^^^^^^^^^^^^^^^^

- ``clamp(value, lo, hi)`` limits *value* to the range *lo* to *hi*:
  ``clamp(15, 0, 10)`` returns ``10``.
- ``flatten(iterable)`` returns a flat list of the items of nested
  iterables: ``flatten([1, [2, [3]]])`` returns ``[1, 2, 3]``.  Strings and
  bytes are kept whole.

New ``extras`` module
^^^^^^^^^^^^^^^^^^^^^

Everyday helpers: ``unique()``, ``first()``, ``group_by()`` (like
``Object.groupBy()`` in JavaScript), ``deep_get()``, ``human_size()``,
``slugify()`` and the ``timer`` context manager.  See
``Doc/library/extras.rst``.

New REPL commands
^^^^^^^^^^^^^^^^^

In the interactive interpreter, type ``history`` to list recent input or
``help-me`` for a list of commands and keyboard shortcuts.

Bug fixes
^^^^^^^^^

These fix open bugs from the `CPython issue tracker
<https://github.com/python/cpython/issues>`_ that are not yet fixed in
official Python:

- `gh-59598 <https://github.com/python/cpython/issues/59598>`_:
  ``json.JSONDecoder.raw_decode()`` skips leading whitespace.
- `gh-105426 <https://github.com/python/cpython/issues/105426>`_:
  ``gzip.GzipFile`` can seek backwards when the gzip data does not start at
  the beginning of the file.
- `gh-106980 <https://github.com/python/cpython/issues/106980>`_:
  ``tarfile`` gives a clear error instead of "seeking backwards is not
  allowed" when a link in a stream cannot be extracted.
- `gh-108931 <https://github.com/python/cpython/issues/108931>`_:
  ``http.cookiejar`` removes expired cookies stored without a leading dot.
- `gh-110501 <https://github.com/python/cpython/issues/110501>`_:
  ``mailbox`` strips any line ending from the "From " line.
- `gh-111066 <https://github.com/python/cpython/issues/111066>`_: setting
  the ``memo`` of the C ``pickle.Unpickler`` keeps its entries and no longer
  crashes with an empty dict.
- `gh-131715 <https://github.com/python/cpython/issues/131715>`_:
  ``http.server.BaseHTTPRequestHandler.end_headers()`` works before any
  header is sent.
- `gh-141998 <https://github.com/python/cpython/issues/141998>`_: text typed
  for ``input()`` in the REPL is not syntax highlighted.
- `gh-161222 <https://github.com/python/cpython/issues/161222>`_:
  ``email.utils.encode_rfc2231()`` no longer writes ``None`` as the charset.
- `gh-161289 <https://github.com/python/cpython/issues/161289>`_:
  ``reprlib`` truncation accounts for a custom ``fillvalue``.
- `gh-161452 <https://github.com/python/cpython/issues/161452>`_:
  ``python -m random N`` prints an integer for an integer *N* <= 0.

Documentation fixes for ``os.remove()`` (gh-121509),
``types.MappingProxyType`` (gh-117956) and the ``FOR_ITER`` bytecode
(gh-121399) are included too.

Testing
^^^^^^^

Every push to the ``sid-python`` branch builds it and runs the full test
suite on Linux, macOS and Windows (``.github/workflows/sid-python.yml``).


General Information
-------------------

- Website: https://www.python.org
- Source code: https://github.com/python/cpython
- Issue tracker: https://github.com/python/cpython/issues
- Documentation: https://docs.python.org
- Developer's Guide: https://devguide.python.org/

Contributing to CPython
-----------------------

For more complete instructions on contributing to CPython development,
see the `Developer Guide`_.

.. _Developer Guide: https://devguide.python.org/

Using Python
------------

Installable Python kits, and information about using Python, are available at
`python.org`_.

.. _python.org: https://www.python.org/

Build Instructions
------------------

On Unix, Linux, BSD, macOS, and Cygwin::

    ./configure
    make
    make test
    sudo make install

This will install Python as ``python3``.

You can pass many options to the configure script; run ``./configure --help``
to find out more.  On macOS case-insensitive file systems and on Cygwin,
the executable is called ``python.exe``; elsewhere it's just ``python``.

Building a complete Python installation requires the use of various
additional third-party libraries, depending on your build platform and
configure options.  Not all standard library modules are buildable or
usable on all platforms.  Refer to the
`Install dependencies <https://devguide.python.org/getting-started/setup-building.html#build-dependencies>`_
section of the `Developer Guide`_ for current detailed information on
dependencies for various Linux distributions and macOS.

On macOS, there are additional configure and build options related
to macOS framework and universal builds.  Refer to `Mac/README.rst
<https://github.com/python/cpython/blob/main/Mac/README.rst>`_.

On Windows, see `PCbuild/readme.txt
<https://github.com/python/cpython/blob/main/PCbuild/readme.txt>`_.

To build Windows installer, see `Tools/msi/README.txt
<https://github.com/python/cpython/blob/main/Tools/msi/README.txt>`_.

If you wish, you can create a subdirectory and invoke configure from there.
For example::

    mkdir debug
    cd debug
    ../configure --with-pydebug
    make
    make test

(This will fail if you *also* built at the top-level directory.  You should do
a ``make clean`` at the top-level first.)

To get an optimized build of Python, ``configure --enable-optimizations``
before you run ``make``.  This sets the default make targets up to enable
Profile Guided Optimization (PGO) and may be used to auto-enable Link Time
Optimization (LTO) on some platforms.  For more details, see the sections
below.

Profile Guided Optimization
^^^^^^^^^^^^^^^^^^^^^^^^^^^

PGO takes advantage of recent versions of the GCC or Clang compilers.  If used,
either via ``configure --enable-optimizations`` or by manually running
``make profile-opt`` regardless of configure flags, the optimized build
process will perform the following steps:

The entire Python directory is cleaned of temporary files that may have
resulted from a previous compilation.

An instrumented version of the interpreter is built, using suitable compiler
flags for each flavor. Note that this is just an intermediary step.  The
binary resulting from this step is not good for real-life workloads as it has
profiling instructions embedded inside.

After the instrumented interpreter is built, the Makefile will run a training
workload.  This is necessary in order to profile the interpreter's execution.
Note also that any output, both stdout and stderr, that may appear at this step
is suppressed.

The final step is to build the actual interpreter, using the information
collected from the instrumented one.  The end result will be a Python binary
that is optimized; suitable for distribution or production installation.


Link Time Optimization
^^^^^^^^^^^^^^^^^^^^^^

Enabled via configure's ``--with-lto`` flag.  LTO takes advantage of the
ability of recent compiler toolchains to optimize across the otherwise
arbitrary ``.o`` file boundary when building final executables or shared
libraries for additional performance gains.


What's New
----------

We have a comprehensive overview of the changes in the `What's new in Python
3.15 <https://docs.python.org/3.15/whatsnew/3.15.html>`_ document.  For a more
detailed change log, read `Misc/NEWS
<https://github.com/python/cpython/tree/main/Misc/NEWS.d>`_, but a full
accounting of changes can only be gleaned from the `commit history
<https://github.com/python/cpython/commits/main>`_.

If you want to install multiple versions of Python, see the section below
entitled "Installing multiple versions".


Documentation
-------------

`Documentation for Python 3.15 <https://docs.python.org/3.15/>`_ is online,
updated daily.

It can also be downloaded in many formats for faster access.  The documentation
is downloadable in HTML, EPUB, and reStructuredText formats; the latter version
is primarily for documentation authors, translators, and people with special
formatting requirements.

For information about building Python's documentation, refer to `Doc/README.rst
<https://github.com/python/cpython/blob/main/Doc/README.rst>`_.


Testing
-------

To test the interpreter, type ``make test`` in the top-level directory.  The
test set produces some output.  You can generally ignore the messages about
skipped tests due to optional features which can't be imported.  If a message
is printed about a failed test or a traceback or core dump is produced,
something is wrong.

By default, tests are prevented from overusing resources like disk space and
memory.  To enable these tests, run ``make buildbottest``.

If any tests fail, you can re-run the failing test(s) in verbose mode.  For
example, if ``test_os`` and ``test_gdb`` failed, you can run::

    make test TESTOPTS="-v test_os test_gdb"

If the failure persists and appears to be a problem with Python rather than
your environment, you can `file a bug report
<https://github.com/python/cpython/issues>`_ and include relevant output from
that command to show the issue.

See `Running & Writing Tests <https://devguide.python.org/testing/run-write-tests.html>`_
for more on running tests.

Installing multiple versions
----------------------------

On Unix and Mac systems if you intend to install multiple versions of Python
using the same installation prefix (``--prefix`` argument to the configure
script) you must take care that your primary python executable is not
overwritten by the installation of a different version.  All files and
directories installed using ``make altinstall`` contain the major and minor
version and can thus live side-by-side.  ``make install`` also creates
``${prefix}/bin/python3`` which refers to ``${prefix}/bin/python3.X``.  If you
intend to install multiple versions using the same prefix you must decide which
version (if any) is your "primary" version.  Install that version using
``make install``.  Install all other versions using ``make altinstall``.

For example, if you want to install Python 2.7, 3.6, and 3.15 with 3.15 being the
primary version, you would execute ``make install`` in your 3.15 build directory
and ``make altinstall`` in the others.


Release Schedule
----------------

See `PEP 790 <https://peps.python.org/pep-0790/>`__ for Python 3.15 release details.


Copyright and License Information
---------------------------------


Copyright © 2001 Python Software Foundation.  All rights reserved.

Copyright © 2000 BeOpen.com.  All rights reserved.

Copyright © 1995-2001 Corporation for National Research Initiatives.  All
rights reserved.

Copyright © 1991-1995 Stichting Mathematisch Centrum.  All rights reserved.

See the `LICENSE <https://github.com/python/cpython/blob/main/LICENSE>`_ for
information on the history of this software, terms & conditions for usage, and a
DISCLAIMER OF ALL WARRANTIES.

This Python distribution contains *no* GNU General Public License (GPL) code,
so it may be used in proprietary projects.  There are interfaces to some GNU
code but these are entirely optional.

All trademarks referenced herein are property of their respective holders.
