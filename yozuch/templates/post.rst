Demo post!
==========

Welcome to Yozuch! This is a demo post.

.. read-more::

Images
------

.. image:: /images/python-powered-w-200x80.png

You can put your images and other assets into ``assets`` directory.

Inline markup
-------------

*emphasis*


**strong**


``literal``

Lists
-----

* This is a bulleted list.
* It has two items, the second
  item uses two lines.


1. This is a numbered list.
2. It has two items too.


#. This is a numbered list.
#. It has two items too.


* this is
* a list

  * with a nested list
  * and some subitems

* and here the parent list continues

Tables
------

+------------------------+------------+----------+----------+
| Header row, column 1   | Header 2   | Header 3 | Header 4 |
| (header rows optional) |            |          |          |
+========================+============+==========+==========+
| body row 1, column 1   | column 2   | column 3 | column 4 |
+------------------------+------------+----------+----------+
| body row 2             | ...        | ...      |          |
+------------------------+------------+----------+----------+


=====  =====  =======
A      B      A and B
=====  =====  =======
False  False  False
True   False  False
False  True   False
True   True   True
=====  =====  =======

Syntax highlight
----------------

.. This is a comment.


.. code-block:: python

   logger = logging.getLogger('yozuch')

    class RejectFilter(logging.Filter):

        def __init__(self, reject):
            logging.Filter.__init__(self)
            self.reject = reject

        def filter(self, record):
            return not self.reject(record)


You can learn more about reStructuredText syntax at `Sphinx documentation <http://sphinx-doc.org/rest.html>`_ or at `official reStructuredText website <http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html>`_.

.. Post metadata below.

:tags: hello
