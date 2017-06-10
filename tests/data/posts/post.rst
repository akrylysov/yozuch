测试
====

内容


*emphasis*


**strong**


``literal``


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


| These lines are
| broken exactly like in
| the source file.


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


.. This is a comment.


.. code-block:: python

   logger = logging.getLogger('yozuch')

    class RejectFilter(logging.Filter):

        def __init__(self, reject):
            logging.Filter.__init__(self)
            self.reject = reject

        def filter(self, record):
            return not self.reject(record)


`Internal page reference </documents/page.rst>`_
`Internal post reference </posts/post-readmore.rst>`_

.. image:: image.png

:tags: tag1
:author: author1
:date: 2013-10-02
