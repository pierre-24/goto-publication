=====
Usage
=====

Preamble: why ?
---------------

Modern article's PDFs generally includes DOI and even sometimes direct link to redirect you to that article you find interesting in the reference section.
Old articles generally dont, which requires to check on Google (or other) what is the website of the journal, then go into some *citation search* form (if it ever exists).

The goal here is to ease this process by providing a tool to perform **citation search**.
It is reduced to 3 (sometimes 4) components:

+ The journal **name** ;
+ The **volume** ;
+ The (starting) **page** or **article number** in some journal ;
+ And, yeah, sometimes, the **issue** is required.

In the following, only the 3 first information are required:

.. code:: console

    $ goto-publication get "Nature" 227 680 --doi
    doi: 10.1038/227680a0
    providerIcon: https://www.nature.com/favicon.ico
    providerName: Nature
    providerWebsite: https://www.nature.com/
    url: https://dx.doi.org/10.1038/227680a0

Note that there is two way to retrieve the information about an article:

+ By its **url**: this is the default and (usually) fastest way.
  In fact the goal is to take you as far as possible in the process in the less internet request possible.
  Sometimes, when *citation search* results in a predictible URL, no request is even needed.
  On the other hand, **there is no guarantee that the article exists**.
+ By its **DOI**: this is slower, but safer.
  This time, by performing as many requests as needed (generally 2 or 3, don't worry), the DOI that you'll get is guaranteed to be exact (otherwise, *not found* is reported).
  In the example above, the DOI was requested, and this is in fact the true DOI of `this article <https://dx.doi.org/10.1038/227680a0>`_.

.. note::

    A quick vocabulary fix:

    + A **provider** (= editor) provide different **journals**, which contains articles
    + Each journal is stored in a **registry**.
    + A journal has a **name** (= title) and an abbreviation (which normally follows the `ISO 4 convention <https://en.wikipedia.org/wiki/ISO_4>`_).

.. warning::

    The program comes with its own registry, which is a chemistry + physics oriented (since I'm the primary user of this tool).
    You can change that (see below), but it is currently not easy and well documented (future release will definitely fix that).

Detailed usage
--------------

.. program-output:: goto-publication --help

By default, the program outputs `YAML <https://yaml.org/spec/1.2/spec.html>`_, which is human friendly.
You can change this output format (for example if you need to use it in scripts further scripts) into JSON (with ``-f json``).

You can also select your own journal registry with  ``-J``.

Get article info
++++++++++++++++

.. warning:: **Legal stuffs**

    Don't forget that this results in real requests.
    Of course, the amount of request you need to make before getting ban by any editor is large, but a ban (even temporary) is probably not what you are looking for.
    Thus, don't try to use this to automate scraping.
    Even if you are not using the editor website in your browser, think as this as being the same: **the website policy still apply**.

    But don't worry, if you use this normally, nothing should happen :)

.. program-output:: goto-publication get --help

Get info about an article: retrieve either its DOI (with ``--DOI``) or its URL (see previous section).

For the moment, you need to give the **exact journal name**, as found in the registry (see below for suggestions).
That will be fix'd in future releases.

.. note::

    ``goto-publication`` takes advantage of the `Elsevier API <https://dev.elsevier.com/index.html>`_, which requires a key.
    By default, you are limited to URL:

    .. code:: console

        $ goto-publication get 'Chemical Physics' 493 200
        providerName: ScienceDirect (API)
        providerWebsite: https://www.sciencedirect.com/
        url: https://www.sciencedirect.com/search/advanced?pub=Chemical+Physics&volume=493&page=200
        $ goto-publication get 'Chemical Physics' 493 200 --doi
        message:
          journal: Not yet implemented (Chemical Physics [sd])

    But if you have an API key, you can set the environement variable ``$SD_API_KEY``.

    .. code:: console

        $ export SD_API_KEY=xxxxxxxxxxxxxxxxxxxx
        $ goto-publication get 'Chemical Physics' 493 200 --doi
        doi: 10.1016/j.chemphys.2017.04.003
        providerName: ScienceDirect (API)
        providerWebsite: https://www.sciencedirect.com/
        url: https://dx.doi.org/10.1016/j.chemphys.2017.04.003


Suggest journals
++++++++++++++++

.. program-output:: goto-publication suggest --help

Suggest a list of journal names based on the (partial) journal abbreviation (``-S abbr``, default) or title (``-S name``), sorted by similarity.

Count (``-c``) and cutoff (``-C``, between 0 and 1) are used to change the scope of the search.
The latter restrict the minimal amount of similarity required (`see underlying function <https://docs.python.org/3.7/library/difflib.html#difflib.get_close_matches>`_), while the first restrict the number of results.

Examples:

+ Search per abbreviation:

  .. code:: console

    $ goto-publication suggest "J am chem soc" -c 5
    suggestions:
    - Journal of the American Chemical Society
    - Journal of the Iranian Chemical Society
    - Journal of Chemical Documentation
    - Journal of the American Oil Chemists' Society
    - Journal of the Chinese Chemical Society

+ Search per name

  .. code:: console

    $ goto-publication suggest "journal american chemical" -S name -c 5
    suggestions:
    - Journal of the American Chemical Society
    - Journal of Materials Chemistry C
    - Journal of Materials Chemistry A
    - Journal of Medicinal Chemistry
    - Journal of the American Ceramic Society

+ Change the cutoff (default is ``-C 0.6``):

  .. code:: console

    $ goto-publication suggest "journal american chemical" -S name -c 5 -C 0.7
    suggestions:
    - Journal of the American Chemical Society
    - Journal of Materials Chemistry C
    - Journal of Materials Chemistry A

Registry content
++++++++++++++++

.. program-output:: goto-publication journals --help

List the journals as found in the registry.
``-c`` and ``-s`` allow to change the number and start.
For example, to get journal from 3 to 6,

.. code:: console

    $ goto-publication journals -c 3 -s 2
    journals:
    - abbreviation: ACS Appl Electron Mater
      journal: ACS Applied Electronic Materials
      providerName: American Chemical Society
      providerWebsite: https://pubs.acs.org/
    - abbreviation: ACS Appl Energy Mater
      journal: ACS Applied Energy Materials
      providerName: American Chemical Society
      providerWebsite: https://pubs.acs.org/
    - abbreviation: ACS Appl Mater  Interface
      journal: ACS Applied Materials & Interfaces
      providerName: American Chemical Society
      providerWebsite: https://pubs.acs.org/
    total: 1378

Note that there was a total of 1378 journal in the registry.

.. note::

    Most of the abbreviation are auto-generated from the name, so it is probably not exact.

.. program-output:: goto-publication journal --help

Given the **exact journal name**, gives a few information about it as found in the registry.
For example,

.. code:: console

    $ goto-publication journal "Journal of the American Chemical Society"
    abbreviation: J Am Chem Soc
    journal: Journal of the American Chemical Society
    providerName: American Chemical Society
    providerWebsite: https://pubs.acs.org/

It is the same information as above but for one single journal.

List providers
++++++++++++++

.. program-output:: goto-publication providers --help

List the different `providers <api-providers.html>`_ that the program handles, ordered alphabetically.
Again, ``-c`` and ``-s`` allows to navigate through the list.
For example,

.. code:: console

    $ goto-publication providers -c 3
    providers:
    - providerName: American Chemical Society
      providerWebsite: https://pubs.acs.org/
    - providerName: American Physical Society
      providerWebsite: https://journals.aps.org/
    - providerName: American Institute of Physics (AIP)
      providerWebsite: https://aip.scitation.org/
    total: 9
