Usage
=====

.. _installation:

Installation from source
------------------------

Clone the `github <https://github.com/SK1Y101/Skiylia>`_ repository after forking and add the original repo as an upstream

.. code-block:: bash
   $ git clone https://github.com/<Your username>/<Fork name>.git
   $ cd <Fork name>
   $ git remote add upstream <https://github.com/SK1Y101/Skiylia>.git

You can now navigate to the source folder and run the skiylia interpreter!

.. code-block:: bash
   $ cd skiylia/src
   $ python3 skiylia.py ...

Executing a skiylia file is easy, simply pass the filepath at the interpreter level!

.. code-block:: bash
   $ python3 skiylia.py <file_path>.skiy

For extended information, the language additionally supplies a small help command

.. code-block:: bash
   $ python3 skiylia.py -h


Testing
-------

Testing Skiylia is easy, all you need is one dependency: `nox`

.. code-block:: bash
   $ python3 pip install nox

And then you're good to run the suite:

.. code-block:: bash
   $ nox -e tests

Nox is used for other stages of skiylia development (linting and formating)