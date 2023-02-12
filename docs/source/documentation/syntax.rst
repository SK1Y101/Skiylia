Syntax
======

Skiylia is designed as a python-esque language, while drawing some minor concepts from c-like languages.

Scripts are stored in ``.skiy`` plain text files. As Skiylia is based on an execution-time interpreter,
programs are run directly from source without being compiled beforehand.

.. Indentation
.. ~~~~~~~~~~~

.. Skiylia makes heavy use of whitespace to define blocks of code, as readability is a core design principle,
.. we reccomend a single tab (or 4 space) indentation per line.

.. Skiylia Code is subdivided into lines. These lines are abstractions that can follow the literal lines as defined by
.. newlines within the files, but do not have to. For example, a multiline comment counts as a single abstract line, even
.. if it may span multiple literal lines.
.. The indentation of a line must match the one before it, increment by one if the line before it opened a new code block,
.. or decrement by at least one if closing one (or more) code blocks.

Comments
--------

Inline comments are preceded by a ``//`` double slash, and terminate at the end of the line.


.. literalinclude:: examples/comments/single_comment.skiy
    :caption: An example of a single-line comment


Multiline comments are preceded- and followed- by a ``///`` tripple slash.
Each newline should begin with an indent, such that all multiline comments begin in the same column.
They can also contain single line comments, and is not reccomended for standard practice, but does
allow you to comment out blocks of code.


.. literalinclude:: examples/comments/multiline_comment.skiy
    :caption: An example of a multi-line comment

Reserved words
--------------

Skiylia (as of :ref:`0.1.0 pre-alpha <0.1.0-pre-alpha>`) does not reserve any words.
This is `very likely`_ to change in future releases.

Precedence
----------

A table of precedence for Skiylia expressions is given below. Operations lower down the table bind less tightly than those above
and are evaluated later. (think order of operations in mathematics)

.. table:: Comparison syntax
   :widths: auto

   =========== ========================== ===========
   Operator    Description                Association
   =========== ========================== ===========
   ``-`` ``+`` Negation, Absolute         Right
   ``*`` ``/`` Multiplication, Division   Left
   ``+`` ``-`` Addition, Subtraction      Left
   =========== =========================== ===========