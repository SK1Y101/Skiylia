Design documentation
====================

Skiylia is based on Python, both in the design and literal sense.
The first compiler/interpreter will be written in Python, and a lot of it's design takes inspiration from the language.

File style
==========

Skiyla programs are plain text files with the ``.skiy`` extension.

indentation
~~~~~~~~~~~

They make heavy use of whitespace to define blocks of code, as readability is a core design principle,
we reccomend a single tab (or 4 space) indentation per line.

Skiylia Code is subdivided into lines. These lines are abstractions that can follow the literal lines as defined by
newlines within the files, but do not have to. For example, a multiline comment counts as a single abstract line, even
if it may span multiple literal lines.
The indentation of a line must match the one before it, increment by one if the line before it opened a new code block,
or decrement by at least one if closing one (or more) code blocks.

Comments
~~~~~~~~

Skiylia defines both inline and multiline comments, both of which can follow other language structures
Inline comments are preceded by a ``//`` double slash and two spaces, and terminate at the end of the line.

.. tabs::

    .. code-tab:: skiylia

        //  This is an inline comment

   .. code-tab:: python

        #  This is an inline comment


.. .. code-block:: skiylia
..    :caption: Inline comment

..     //  This is an inline comment


Multiline comments are preceded- and followed- by a ``///`` tripple slash and seperated from the content of a comment by a space.
Each newline should begin with an indent, such that all multiline comments begin in the same column. They can also contain single
line comments, though this can break up readability, and is not reccomended.

.. tabs::

    .. code-tab:: skiylia

        /// This is a multi-
            line comment ///

        /// This is also
            a completely // valid
            multiline comment ///

   .. code-tab:: python

        ''' This is a multi-
            line comment '''

        ''' This is also
            a completely # valid
            multiline comment '''


.. .. code-block:: none
..     :caption: Multi-line comment

..     /// This is a multi-
..         line comment ///

..     /// This is also
..         a completely // valid
        multiline comment ///


Data Types
~~~~~~~~~~

Skiyia implements the following datatypes

* Boolean   - ``true``, ``false``
* None      - ``null``
* String    - ``"hello world"``
* Number    - ``1.25``
    * Int   - ``1``       - Will not appear in v1.0
    * Float - ``1.5``     - Will not appear in v1.0
    * Frac  - ``3/2``     - Will not appear in v1.0
    * Cplx  - ``3+9j``    - Will not appear in v1.0
    * Sci   - ``5E+10``   - Will not appear in v1.0
    * Radix
        * Bin- ``0b1010``  - Will not appear in v1.0
        * Ter- ``0t1T10``  - Will not appear in v1.0
        * Oct- ``0o1743``  - Will not appear in v1.0
        * hHx- ``0x7FE3``  - Will not appear in v1.0

Expressions
===========

Arithmatic
~~~~~~~~~~

* Addition          - ``1 + 2``
* Subtraction       - ``3 - 1``
* Multiplication    - ``5 * 4``
* Division          - ``6 / 7``
* Exponentiation    - ``7 ** 9``  - Will not appear in v1.0

* Prefix
    * Negation      - ``--a``     - Will not appear in v1.0
    * Addition      - ``++a``     - Will not appear in v1.0
* Postfix
    * Negation      - ``a--``     - Will not appear in v0.1
    * Addition      - ``a++``     - Will not appear in v0.1

Comparative
~~~~~~~~~~~

.. table:: Comparison syntax
   :widths: auto

   ====================  ======================  =========================================================================================    ============
   Function              Example Syntax          Explanation                                                                                  Status
   ====================  ======================  =========================================================================================    ============
   Less than             ``a < b``
   Less or equal         ``a <= b``                                                                                                           Not in v0.1
   Greater than          ``a > b``
   Greater or equal      ``a >= b``                                                                                                           Not in v0.1
   Equality              ``a == b``              a and b must have the same value, ie: 3.0 == 3 (True)
   Strict Equality       ``a === b``             a and b must have the same value and datatype, ie: 3.0 === 3 (False), int(3.0) === 3 (True)  Not in v0.1
   Fuzzy Equality        ``a ~~ b``              a and b must have the same datatype, ie: 4 ~~ 5 (True), "4" ~~ 4 (False)                     Not in v0.1
   Inequality            ``a != b``, ``a <> b``  as above, inverted
   Strict Inequality     ``a !== b``             as above, inverted                                                                           Not in v0.1
   Fuzzy Inequality      ``a !~ b``              as above, inverted                                                                           Not in v0.1
   Three way compare     ``a <=> b``             a>b: 1, a==b, 0, a<b, -1                                                                     Not in v0.1
   ====================  ======================  =========================================================================================    ============


Many of these operations will be included in later versions of Skiylia.