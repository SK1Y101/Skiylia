Data types
==========

These are the particles of code that make up Skiylia programs, the chunks of bits and bytes that get operated upon.

Strings
-------

Strings in Skiylia are an array of any bytes enclosed by string deliminators. This is typically used to denote text, 
but there are few restrictions on what can be stored.

.. literalinclude:: examples/strings/string_quotes.skiy
    :caption: String literals are surrounded by `"`, `'` or `\``

Strings can span multiple lines, so long as they are enclosed correctly!

.. literalinclude:: examples/strings/multi_string.skiy
    :caption: Newlines are not a problem

Interpolation
~~~~~~~~~~~~~

Strings allow interpolation; If an expression within the string is enclosed by `{}`, the expression is evaluated.

.. literalinclude:: examples/strings/string_interp.skiy
    :caption: Multiple interpolations are possible in a single string

Arbitary depth of interpolation is possible, but reccomended against for the purpose of readability

.. literalinclude:: examples/strings/string_interp_nest.skiy
    :caption: Nested interpolation