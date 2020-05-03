==========
Installing
==========

.. warning::

    You need need Python >= 3.5 and pip >= 20.

If you just want to use ``goto-publication``
--------------------------------------------

The easiest way is to use ``pip``:

.. code:: console

   $ pip3 install git+https://github.com/pierre-24/goto-publication.git@dev


Note that you can add use ``install --user`` instead, to install the package without being superuser (see `the pypa documentation <https://pip.pypa.io/en/stable/user_guide/#user-installs>`_).
You will probably need to add ``$HOME/.local/bin`` to ``$PATH`` for this to work:

.. code-block:: bash

  $ echo 'PATH=$HOME/.local/bin:$PATH' >> ~/.bashrc

Then, `find more details about usage here <usage.html>`_


If you want to contribute
-------------------------

First, you need to `fork the repository <https://help.github.com/en/github/getting-started-with-github/fork-a-repo>`_
Then, clone this repository:

.. code-block:: bash

    # using SSH (recommended):
    git clone git@github.com:<YOUR_GITHUB_NAME>/goto-publication.git

    # or using HTTPS
    git clone https://github.com/<YOUR_GITHUB_NAME>/goto-publication.git


Then, you first need a *virtualenv*:

.. code:: bash

    cd goto-publication
    python3 -m venv venv
    source venv/bin/activate

Don't forget to do the last line each time you want to run the code.

Finally, you can install the dependencies (including developement dependencies):

.. code:: bash

    # use make (easier):
    make init

    # or do it explicitly:
    pip install -e .
    pip install goto-publication[dev]

You also need to add an ``upstream`` repository:

.. code:: bash

    # here with SSH (you can use https instead)
    git remote add upstream git@github.com:pierre-24/goto-publication.git

    # fetch repository and all its content
    git fetch upstream

To start working on the project, create a new branch:

.. code:: bash

    git checkout -b my_super_feature_branch upstream/dev

... But don't forget to check the `contribution rules <contributing.html>`_ first ;)