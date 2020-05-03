============
Contributing
============

You first need to `install <./installing.html#if-you-want-to-contribute>`_ if you want to contribute to the code.

Design rules
------------

+ The code is written in Python 3, and follows the (in)famous `PEP-8 <http://legacy.python.org/dev/peps/pep-0008/>`_. You can check it by running ``make lint``, which launch the ``flake`` utility. Type annotation (with ``typing``) must be used if possible.
+ Codes and comments are written in english.
+ The code is documented using docstrings and Sphinx. The docstrings must contains the basic description of the function, as well as a description of the parameters.
+ The code is tested. You can launch the test series by using ``make test``.
  Every functionality should be provided with at least one unit test.
  Every script should be provided with at least one unit test.
  You may need test files to do so, but try to make them small.
+ The package is documented. You can generate this documentation by using ``make doc``. Non-basic stuffs should be explained in this documentation. Don't forget to cite some articles or website if needed.


Workflow
--------

Adapted from the (in)famous `Git flow <http://nvie.com/posts/a-successful-git-branching-model/>`_.

+ Development is mad in ``dev`` branch, while ``master`` contains the production version (and is protected from edition).
+ Functionality are added through pull request (PR) in the ``dev`` branch. Do not work in ``dev`` directly, but create a new branch (``git checkout -b my_branch upstream/dev``).
+ Theses pull requests should be (normally) unitary, and include unit test(s) and documentation if needed. The test suite must succeed for the pull request to be accepted.
+ At some (random) points, ``dev`` will be merged by the maintainer into ``master`` to create a new version, with a tag of the form ``release-vXX``.

