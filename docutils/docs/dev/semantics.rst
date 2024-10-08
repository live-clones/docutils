.. include:: ../header.rst

=====================
 Docstring Semantics
=====================
:Author: David Goodger
:Contact: docutils-develop@lists.sourceforge.net
:Revision: $Revision$
:Date: $Date$
:Copyright: This document has been placed in the public domain.

These are notes for a possible future PEP providing the final piece of
the Python docstring puzzle: docstring semantics or documentation
methodology.  `PEP 257`_, Docstring Conventions, sketches out some
guidelines, but does not get into methodology details.

I haven't explored documentation methodology more because, in my
opinion, it is a completely separate issue from syntax, and it's even
more controversial than syntax.  Nobody wants to be told how to lay
out their documentation, a la JavaDoc_.  I think the JavaDoc way is
butt-ugly, but it *is* an established standard for the Java world.
Any standard documentation methodology has to be formal enough to be
useful but remain light enough to be usable.  If the methodology is
too strict, too heavy, or too ugly, many/most will not want to use it.

I think a standard methodology could benefit the Python community, but
it would be a hard sell.  A PEP would be the place to start.  For most
human-readable documentation needs, the free-form text approach is
adequate.  We'd only need a formal methodology if we want to extract
the parameters into a data dictionary, index, or summary of some kind.


PythonDoc
=========

(Not to be confused with Daniel Larsson's pythondoc_ project.)

A Python version of the JavaDoc_ semantics (not syntax).  A set of
conventions which are understood by the Docutils.  What JavaDoc has
done is to establish a syntax that enables a certain documentation
methodology, or standard *semantics*.  JavaDoc is not just syntax; it
prescribes a methodology.

- Use field lists or definition lists for "tagged blocks".  By this I
  mean that field lists can be used similarly to JavaDoc's ``@tag``
  syntax.  That's actually one of the motivators behind field lists.
  For example, we could have::

      """
      :Parameters:
          - `lines`: a list of one-line strings without newlines.
          - `until_blank`: Stop collecting at the first blank line if
            true (1).
          - `strip_indent`: Strip common leading indent if true (1,
            default).

      :Return:
          - a list of indented lines with minimum indent removed;
          - the amount of the indent;
          - whether or not the block finished with a blank line or at
            the end of `lines`.
      """

  This is taken straight out of docutils/statemachine.py, in which I
  experimented with a simple documentation methodology.  Another
  variation I've thought of exploits the Grouch_-compatible
  "classifier" element of definition lists.  For example::

      :Parameters:
          `lines` : [string]
              List of one-line strings without newlines.
          `until_blank` : boolean
              Stop collecting at the first blank line if true (1).
          `strip_indent` : boolean
              Strip common leading indent if true (1, default).

- Field lists could even be used in a one-to-one correspondence with
  JavaDoc ``@tags``, although I doubt if I'd recommend it.  Several
  ports of JavaDoc's ``@tag`` methodology exist in Python, most
  recently Ed Loper's "epydoc_".


Other Ideas
===========

- Can we extract comments from parsed modules?  Could be handy for
  documenting function/method parameters::

      def method(self,
                 source,        # path of input file
                 dest           # path of output file
                ):

  This would save having to repeat parameter names in the docstring.

  Idea from Mark Hammond's 1998-06-23 Doc-SIG post, "Re: [Doc-SIG]
  Documentation tool":

      it would be quite hard to add a new param to this method without
      realising you should document it

- Frederic Giacometti's `iPhrase Python documentation conventions`_ is
  an attachment to his Doc-SIG post of 2001-05-30.


.. _PEP 257: https://peps.python.org/pep-0257
.. _JavaDoc: http://java.sun.com/j2se/javadoc/
.. _pythondoc: http://starship.python.net/crew/danilo/pythondoc/
.. _Grouch: http://www.mems-exchange.org/software/grouch/
.. _epydoc: http://epydoc.sourceforge.net/
.. _iPhrase Python documentation conventions:
   https://mail.python.org/pipermail/doc-sig/2001-May/001840.html

.. Emacs settings

   Local Variables:
   mode: indented-text
   mode: rst
   indent-tabs-mode: nil
   sentence-end-double-space: t
   fill-column: 70
   End:
