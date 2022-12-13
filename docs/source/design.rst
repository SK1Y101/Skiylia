Design documentation
====================

Skiylia is based on Python, both in the design and literal sense.
The first compiler/interpreter will be written in Python, and a lot of it's design takes inspiration from the language.

File style
==========

Skiyla programs are plain text files with the `.skiy` extension.
They make heavy use of whitespace to define blocks of code, as readability is a core design principle,
we reccomend a single tab (or 4 space) indentation per line.

Comments
~~~~~~~~

Skiylia defines both inline and multiline comments, both of which can follow other language structures
Inline comments are preceded by a `//` double slash and two spaces, and terminate at the end of the line.
.. code-block::
    //  This is an inline comment

Multiline comments are preceded- and followed- by a `///` tripple slash and seperated from the content of a comment by a space.
Each newline should begin with an indent, such that all multiline comments begin in the same column. They can also contain single
line comments, though this can break up readability, and is not reccomended.
.. code-block::
    /// This is a multi-
        line comment ///

    /// This is also
        a completely // valid
        multiline comment ///

