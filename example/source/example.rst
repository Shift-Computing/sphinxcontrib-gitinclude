example
=======

.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
Include setup.py without specifying the path to the git repo (uses the one in conf.py)

.. gitinclude:: setup.py main
   :language: python

Include __init__.py with specifying a path to the repository (you can use absolute or relative paths):

.. gitinclude:: src/sphinxcontrib/gitinclude/__init__.py main ..
   :language: python

Include __init__.py with specifying a path to the repository (relative):

.. gitinclude:: src/sphinxcontrib/gitinclude/__init__.py main ..
   :language: python

Show a diff using hashes, feel free to use any git tag or ref:

.. gitinclude:: source/conf.py fe074165f6ad764812398dfeeaf6323d3ea428ed
   :diff: 92e1ac5da036491225a357af4e8045fd59b2bdcd
   :language: python

.. _Sphinx: http://www.sphinx-doc.org/en/stable/

Show some inline code:

.. code:: python

   for item in container:
        if search_something(item):
           # Found it!
           process(item)
           break
    else:
        # Didn't find anything..
        not_found_in_container()
