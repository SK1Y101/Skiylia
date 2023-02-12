Error Handling
==============

Syntax errors
-------------

These are simple instances of the code not following Skiylia's grammar, ie:

```skiylia
3 + / 6
```

Skiylia will detect these errors and show an error message as it does so:

```
[Line 1, Char 5] Skiylia Error: Expected expression.
```

Skiylia will inform you of the location, error type, and a handy short description.