Overview
--------

This directory contains the documentation published on [ReadTheDocs].

The pages are generated using [Sphinx] from [reStructuredText] sources.
It also **runs** `partycrasher/rest_service.py`.

[ReadTheDocs]: http://partycrasher.rtfd.io/
[Sphinx]: http://www.sphinx-doc.org/en/1.4.8/
[ReStructuredText]: http://docutils.sourceforge.net/rst.html

Building on your machine
------------------------

You need to install Sphinx and all its associated tools:

    pip install -r requirements.txt

Then you can build the documentation using Sphinx:

    make html

This will lump the documentation into `_build/`.


Automatically Generated REST API Documentation
----------------------------------------------

REST API endpoint documentation is extracted from the docstrings in
`partycrasher/rest_service.py`.

`conf.py` imports `partycrasher/rest_service.py`. Defined within
`conf.py` is the function `create_rest_api_docs()`. This function scans
all Flask endpoints in the `rest_service.py`, extracting their
docstrings. It then concatenates the docstrings into the file
`rest-api.rst`. Preamble information is provided in
`rest-api.rst.template`.

**Note**: Any code that runs on import in `partycrasher/rest_service.py`
will run when the documentation is being generated! So if you don't want
the documentation build to fail, don't add anything to sinister to the
run on import!


Adding a new page
-----------------

1. Add a new `.rst` file to this directory.
2. Add the name of your `.rst` file without the extension to
   `index.rst` under the `.. toctree::` directive.


Managing the automatic build
----------------------------

Go to the [project page] to manage the documentation build.

[project page]: https://readthedocs.org/projects/partycrasher/
