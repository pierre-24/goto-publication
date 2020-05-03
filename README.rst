================
goto-publication
================

.. image:: https://travis-ci.org/pierre-24/goto-publication.svg?branch=dev
    :target: https://travis-ci.org/pierre-24/goto-publication


*Citation-based URL/DOI searches*, by `Pierre Beaujean <https://pierrebeaujean.net>`_.
CLI version of `that previous project <https://github.com/pierre-24/goto-publication-old/>`_.

Because the journal, the volume and the page (and, sometimes, yeah, the issue) should be enough to find an article (for which, of course, you don't have the DOI).

.. note::

    Since I have a (quantum) chemistry background, I will limit this project to the journals that are in the chemistry and physics fields.
    I'm working on that, but feel free to propose `improvements <https://github.com/pierre-24/goto-publication/pulls>`_.


Installation and usage
----------------------

If you want to use goto-publication, just install it through ``pip``:

.. code:: console

   $ pip3 install git+https://github.com/pierre-24/goto-publication.git@dev

Then, you can get the url directing to an article, by:

.. code:: console

    $ goto-publication get "Nature" 227 680
    providerIcon: https://www.nature.com/favicon.ico
    providerName: Nature
    providerWebsite: https://www.nature.com/
    url: https://www.nature.com/search?journal_identifier=nature&volume=227&spage=680

which links to `this article <https://www.nature.com/articles/227680a0>`_

Or directly (but it is slower) its DOI:

.. code:: console

    $ goto-publication get "Nature" 227 680 --doi
    doi: 10.1038/227680a0
    providerIcon: https://www.nature.com/favicon.ico
    providerName: Nature
    providerWebsite: https://www.nature.com/
    url: https://dx.doi.org/10.1038/227680a0


In the documentation, you can find more information about the `installation <ghpage>`_  (also for contributors) and the `usage of the different commands <ghpage2>`_.
