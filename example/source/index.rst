.. examle documentation master file, created by
   sphinx-quickstart on Sat Mar 26 20:46:58 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to examle's documentation!
==================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

.. gitinclude:: pwman/ui/cli.py v0.9.11 /home/oznt/Software/pwman3/
   :language: python

.. gitinclude:: pwman/ui/cli.py v0.9.11 /home/oznt/Software/pwman3/
   :language: python
   :diff: v0.9.1

.. gitinclude:: pwman/ui/cli.py v0.9.1
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
