=========================
 sphinxcontrib-gitinclude
=========================

.. image:: https://readthedocs.org/projects/sphinxcontrib-gitinclude/badge/?version=latest
   :target: https://readthedocs.org/projects/sphinxcontrib-gitinclude/?badge=latest

A Sphinx_ extension to insert code snippets from a git repository,
helping you to keep a repository of versions working code examples.

Installation
============

Install this extension from PyPI_::

   pip install sphinxcontrib-gitinclude

The extension requires Sphinx 3.7.0 or later and Python 3.7 or later.

Usage
=====

Just add this extension to ``extensions``::

   extensions = ['sphinxcontrib.gitinclude']

Now you can use a new directive ``gitinclude`` to
insert code from a git repository. 

For more information on how to use this project see the example directory
with a project that uses this directive.

.. _Sphinx: http://www.sphinx-doc.org/en/stable/
.. _PyPI: http://pypi.python.org/pypi/sphinxcontrib-gitinclude
.. _documentation: http://sphinxcontrib-gitinclude.readthedocs.org
