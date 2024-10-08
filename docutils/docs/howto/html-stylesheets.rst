.. include:: ../header.rst

==============================================
 Writing HTML (CSS) Stylesheets for Docutils_
==============================================

:Author: Lea Wiemann
:Contact: docutils-develop@lists.sourceforge.net
:Date: $Date$
:Revision: $Revision$
:Copyright: This document has been placed in the public domain.

.. _Docutils: https://docutils.sourceforge.io/


The look of Docutils' HTML output is customizable via CSS stylesheets.
The default stylesheets can be found in the
``docutils/writers/html*/`` directories of the ``html4css1`` and
``html-base`` writers in the Docutils installation.  Use the front-end
command (``rst2html`` or ``rst2html5``) with the
``--help`` option and look at the description of the ``--stylesheet-path``
command-line option for the exact machine-specific location.

To customize the look of HTML documents, you can override the settings
of the default stylesheet in your own stylesheet. Specify both, the
default stylesheet and your stylesheet to the ``--stylesheet`` or
``--stylesheet-path`` command line option (or the corresponding
settings in a configuration_ file), e.g. ::

  rst2html --stylesheet=html4css1.css,transition-stars.css

This is the preferable approach if you want to embed the stylesheet(s), as
this ensures that an up-to-date version of ``html4css1.css`` is embedded.

Alternatively, copy the default style sheet to the same place as your
output HTML files will go and place a new file (e.g. called
``my-docutils.css``) in the same directory and use the following
template::

    /*
    :Author: Your Name
    :Contact: Your Email Address
    :Copyright: This stylesheet has been placed in the public domain.

    Stylesheet for use with Docutils.  [Optionally place a more
    detailed description here.]
    */

    @import url(html4css1.css);

    /* Your customizations go here.  For example: */

    h1, h2, h3, h4, h5, h6, p.topic-title {
      font-family: sans-serif }

For help on the CSS syntax, see, e.g., the `W3C Specification`_, the
`WDG's guide to Cascading Style Sheets`__, or the `MDN Web Docs`__.

.. _W3C Specification: https://www.w3.org/Style/CSS/#specs
__ http://www.htmlhelp.com/reference/css/
__ https://developer.mozilla.org/en-US/docs/Web/CSS

It is important that you do not edit a copy of ``html4css1.css``
directly because ``html4css1.css`` may be updated with a new
release of Docutils.

Also make sure that you import ``html4css1.css`` (using "``@import
url(html4css1.css);``") because the definitions contained in the
default stylesheet are required for correct rendering (margins,
alignment, etc.).

If you think your stylesheet is fancy and you would like to let others
benefit from your efforts, you are encouraged to post the stylesheet to the
Docutils-users_ mailing list. It might find its place in the `stylesheet
collection`_ in the Docutils Sandbox_.

If you decide to share your stylesheet with other users of Docutils,
please keep website-specific customizations not applicable to
Docutils' HTML code in a separate stylesheet.

.. base for relative links is /docutils/docs/howto/

.. _Docutils-users: ../user/mailing-lists.html#docutils-users
.. _configuration: ../user/config.rst
.. _sandbox: ../../../sandbox
.. _stylesheet collection: ../../../sandbox/stylesheets/


.. Emacs settings

   Local Variables:
   mode: indented-text
   mode: rst
   indent-tabs-mode: nil
   sentence-end-double-space: t
   fill-column: 70
   End:
