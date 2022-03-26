=========================
 sphinxcontrib-gitinclude
=========================

.. image:: https://github.com/oz123/sphinxcontrib-gitinclude/workflows/tests/badge.svg
   :target: https://github.com/oz123/sphinxcontrib-gitinclude/actions?query=workflow%3Atests

.. image:: https://coveralls.io/repos/github/o123/sphinxcontrib-gitinclude/badge.svg
   :target: https://coveralls.io/github/github.com/sphinxcontrib-gitinclude


https://sphinxcontrib-gitinclude.readthedocs.org

A Sphinx_ extension to insert code snippets from a git repository,
helping you to keep a repository of versions working code examples.


Installation
============

Install this extension from PyPI_::

   pip install sphinxcontrib-gitinclude

The extension requires Sphinx 3.7.0 and Python Python 3 (Python
3.6+ is tested) at least.

Usage
=====

Just add this extension to ``extensions``::

   extensions = ['sphinxcontrib.gitinclude']

Now you can use a new directive ``gitinclude`` to
insert code from a git repository. 

Please refer to the documentation_ for comprehensive information about usage and
configuration of this extension.

Development and Support
=======================

Please refer to the documentation_ for information on support and the
development process.

Credits
=======

This extension is heavily based on sphinxcontrib-programoutput.

.. _Sphinx: http://www.sphinx-doc.org/en/stable/
.. _PyPI: http://pypi.python.org/pypi/sphinxcontrib-gitinclude
.. _documentation: http://sphinxcontrib-gitinclude.readthedocs.org