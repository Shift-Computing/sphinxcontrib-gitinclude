.. examle documentation master file, created by
   sphinx-quickstart on Sat Mar 26 20:46:58 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to examle's documentation!
==================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Include setup.py without specifying the path to the git repo (uses the one in conf.py)

.. gitinclude:: setup.py main
   :language: python

Include __init__.py with specifying a path to the repository (absolute):

.. gitinclude:: src/sphinxcontrib/gitinclude/__init__.py main /home/oznt/Software/sphinxcontrib-gitinclude
   :language: python

Include __init__.py with specifying a path to the repository (relative):

.. gitinclude:: src/sphinxcontrib/gitinclude/__init__.py main ..
   :language: python

.. gitinclude:: pwman/ui/cli.py v0.9.1
   :diff: v0.9.0
   :language: python

.. code:: python

   for item in container:
        if search_something(item):
           # Found it!
           process(item)
           break
    else:
        # Didn't find anything..
        not_found_in_container()
   
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
