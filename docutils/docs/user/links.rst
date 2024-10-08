.. include:: ../header.rst

=====================
 Docutils_ Link List
=====================

:Author: Lea Wiemann, the Docutils team
:Contact: docutils-develop@lists.sourceforge.net
:Revision: $Revision$
:Date: $Date$
:Copyright: This document has been placed in the public domain.

.. title:: Docutils Links

.. contents::

This document contains links that users of Docutils_ and reStructuredText_
may find useful.

The most current version of this link list can always be found at
https://docutils.sourceforge.io/docs/user/links.html.
If you find outdated or broken links or want to suggest additions,
please `let us know`__ and we'll update the list here.

.. _Docutils: https://docutils.sourceforge.io/
.. _reStructuredText: https://docutils.sourceforge.io/rst.html
__ mailing-lists.html#docutils-users


Editors
-------

Advanced text editors with reStructuredText support, IDEs, and docutils GUIs:

* Emacs `rst mode <https://docutils.sourceforge.io/tools/editors/emacs>`__.

* `Vim <https://www.vim.org/index.php>`__:

  - `reStructuredText syntax highlighting mode
    <https://www.vim.org/scripts/script.php?script_id=973>`__,

  - `VST <https://www.vim.org/scripts/script.php?script_id=1334>`__ (Vim
    reStructuredText) plugin for Vim7 with folding.

  - `VOoM <https://www.vim.org/scripts/script.php?script_id=2657>`__
    plugin for Vim that emulates two-pane outliner with
    support for reStructuredText (since version 4.0b2).

  - `Riv: Take notes in rST <https://github.com/Rykka/riv.vim>`__ Vim
    plugin to take notes in reStructured text.

* `reStructuredText Language Support for Visual Studio Code`__

  __ https://github.com/vscode-restructuredtext/vscode-restructuredtext

* `reStructuredText editor plug-in for Eclipse`__

  __ http://resteditor.sourceforge.net/

* `JED <https://www.jedsoft.org/jed/>`__ programmers editor with
  `rst mode <httpss://jedmodes.sourceforge.io/mode/rst/>`__

* Gnome's gedit offers syntax highlighting and a reST preview pane.

  Latest version of the plugin is available from `bittner @ github`_
  (See also: `Gedit third party plugins`__).

  .. _bittner @ github:  https://github.com/bittner/gedit-reST-plugin
  __ https://wiki.gnome.org/Apps/Gedit/ThirdPartyPlugins-v3.8


* Gunnar Schwant's DocFactory_ is a wxPython GUI application for
  Docutils.

  .. _DocFactory: https://docutils.sourceforge.io/sandbox/gschwant/docfactory/doc/

* ReSTedit_ by Bill Bumgarner is a Docutils GUI for Mac OS X.

  .. _ReSTedit: https://svn.red-bean.com/restedit/trunk/README.html

* `ReText <https://pypi.org/project/ReText/>`_ is a simple but powerful
  editor for Markdown and reStructuredText markup languages.
  It is written in Python using PyQt libraries.

* Leo_ is an outliner_, written in Python using PyQt. It can be used as IDE
  for literal programming, as a filing cabinet holding any kind of data and
  as `document editor`__ with outlines containing reStructuredText markup.

  .. _Leo: https://leoeditor.com/
  .. _outliner: https://en.wikipedia.org/wiki/Outliner
  __ https://leoeditor.com/tutorial-rst3.html

* `NoTex <https://notex.ch>`_ is a browser-based reStructuredText editor
  with syntax highlighting and PDF/HTML export functionality using Sphinx.

* `rsted <https://github.com/anru/rsted>`_ is a "simple online editor for
  reStructuredText on Flask". You can try it on http://rst.ninjs.org/


Export
------

Projects providing additional export routes.

PDF
```

* `rst2pdf (reportlab)`__ is a tool to go directly from
  reStructuredText to PDF, via ReportLab__. No LaTeX installation
  is required.

  __ https://pypi.org/project/rst2pdf/
  __ https://pypi.org/project/reportlab/

* `rst2pdf (pdflatex)`__ by Martin Blais is a minimal front end
  producing LaTeX, compiling the LaTeX file, getting the produced
  output to the destination location and finally deleting all the
  messy temporary files that this process generates.

  __ https://docutils.sourceforge.io/sandbox/blais/rst2pdf/

* `rst2pdf (rubber)`__ is a front end for the generation of PDF
  documents from a reStructuredText source via LaTeX in one step
  cleaning up intermediate files. It uses the rubber__ Python wrapper
  for LaTeX and friends.

  __ https://docutils.sourceforge.io/sandbox/rst2pdf/README.html
  __ https://launchpad.net/rubber

* rlpdf_ is another PDF Writer based on ReportLabs.

  .. _rlpdf: https://docutils.sourceforge.io/sandbox/dreamcatcher/rlpdf/

* RinohType_ is a pure Python PDF Writer based on a document template and a
  style sheet (beta).

  .. _RinohType: https://pypi.python.org/pypi/RinohType

website generators and HTML variants
````````````````````````````````````

* The Sphinx_ Python Documentation Generator by Georg Brandl was
  originally created to translate the `Python documentation`_.
  In the meantime, there is a wide range of `Projects using Sphinx`__

  It can generate complete web sites (interlinked and indexed HTML pages),
  ePub, LaTeX, and others from a set of rST source files.

  .. _Sphinx: https://www.sphinx-doc.org
  __ https://www.sphinx-doc.org/en/master/examples.html

* The Nikola_ static site generator, uses reStructuredText by
  default.

  .. _nikola:  https://getnikola.com/

* Pelican_ is a static site generator (mainly for blogs). Articles/pages can
  be written in reStructuredText or Markdown_ format.

  .. _pelican: https://docs.getpelican.com

* tinkerer_ is a static bloggin framework based on Sphinx_.

  .. _tinkerer: https://pypi.org/project/Tinkerer/

* htmlnav_ by Gunnar Schwant, is an HTML writer which supports navigation
  bars.

  .. _htmlnav: https://docutils.sourceforge.io/sandbox/gschwant/htmlnav/

* rest2web, by Michael Foord, is a tool for creating web sites with
  reStructuredText. Development stalled, there is a fork at
  https://gitlab.com/wavexx/rest2web

* `html4trans <https://docutils.sourceforge.io/sandbox/html4trans/>`__
  produces XHTML conforming to the version 1.0 Transitional DTD that
  contains enough formatting information to be viewed by a lightweight HTML
  browser without CSS support.

* A `simple HTML writer`_ by Bill Bumgarner that doesn't rely on CSS
  stylesheets.

  .. _simple HTML writer: https://docutils.sourceforge.io/sandbox/bbum/DocArticle/

ePub
````

* rst2epub2_ by Matt Harrison includes the epublib (originally by Tim
  Tambin) and a rst2epub.py executable for the conversion.

  .. _rst2epub2: https://github.com/mattharrison/rst2epub2

* Sphinx_ provides ePub as output option, too.


Others
``````

* Pandoc_ is a document converter that can write Markdown_,
  reStructuredText, HTML, LaTeX, RTF, DocBook XML, and S5.

  .. _Pandoc: https://pandoc.org/

* restxsl_ by Michael Alyn Miller, lets you transform reStructuredText
  documents into XML/XHTML files using XSLT stylesheets.

  .. _restxsl: http://www.strangeGizmo.com/products/restxsl/

* An `XSLT script`__ by Ladislav Lhotka enables reStructuredText annotations
  to be included in RELAG NG XML schemas.

  __ https://www.cesnet.cz/doc/techzpravy/2006/rngrest/

* `DocBook Writer`_ by Oliver Rutherfurd.

  .. _DocBook Writer: https://docutils.sourceforge.io/sandbox/oliverr/docbook/

* Nabu_, written by Martin Blais, is a publishing system which
  extracts information from reStructuredText documents and stores it
  in a database.  Python knowledge is required to write extractor
  functions and to retrieve the data from the database again.

  .. _Nabu: https://github.com/blais/nabu

* The `pickle writer`_ by Martin Blais pickles the document tree to a binary
  string. Later unpickling will allow you to publish with other Writers.

  .. _pickle writer: https://docutils.sourceforge.io/sandbox/blais/pickle_writer/

* The `Texinfo Writer`_, by Jon Waltman converts reStructuredText to
  Texinfo, the documentation format used by the GNU project and the
  Emacs text editor.  Texinfo can be used to produce multiple output
  formats, including HTML, PDF, and Info.

  .. _Texinfo Writer: https://docutils.sourceforge.io/sandbox/texinfo-writer/README.html

* For `confluence CMS`_ see https://github.com/netresearch/rst2confluence.

  .. _confluence CMS: https://www.atlassian.com/software/confluence

* Deploying into wikis might be aided by deploy-rst_.

  .. _deploy-rst: https://github.com/netresearch/deploy-rst


Import
------

Convert other formats to reStructuredText:

* recommonmark_ is a Markdown_ (CommonMark_) parser for
  docutils originally created by Luca Barbato.

  Docutils "markdown" parser (new in Docutils 0.17) is a wrapper
  around recommonmark.

  .. _recommonmark: https://github.com/rtfd/recommonmark
  .. _Markdown: https://daringfireball.net/projects/markdown/syntax
  .. _CommonMark: https://commonmark.org/


* sxw2rest_, by Trent W. Buck, converts StarOffice XML Writer (SXW)
  files to reStructuredText. (link down)

  .. _sxw2rest: https://twb.ath.cx/~twb/darcs/sxw2rest/

* xml2rst_, an XSLT stylesheet written by Stefan Merten, converts XML
  dumps of the document tree (e.g. created with ``rst2xml``) back to
  reStructuredText.

  .. _xml2rst: http://www.merten-home.de/FreeSoftware/xml2rst/index.html

* xhtml2rest_, written by Antonios Christofides, is a simple utility
  to convert XHTML to reStructuredText.

  .. _xhtml2rest: https://docutils.sourceforge.io/sandbox/wiemann/xhtml2rest/

* DashTable_ by Gustav Klopp converts HTML tables into reStructuredText.
  Colspan and Rowspan supported!

  .. _DashTable: https://github.com/gustavklopp/DashTable

* Sphinx_ includes a `LaTeX to rST converter
  <https://svn.python.org/projects/doctools/converter/>`__ in its source code
  (trimmed to importing the old Python docs).

* Pandoc_ can read Markdown_ and (subsets of) HTML, and LaTeX and
  export to (amongst others) reStructuredText.

* PySource_, by Tony Ibbs, is an experimental Python source Reader.
  There is some related code in David Goodger's sandbox
  (pysource_reader_) and a `Python Source Reader`_ document.

  .. _PySource: https://docutils.sourceforge.io/sandbox/tibs/pysource/
  .. _pysource_reader: https://docutils.sourceforge.io/sandbox/davidg/pysource_reader/
  .. _Python Source Reader: https://docutils.sourceforge.io/docs/dev/pysource.html


Extensions
----------

Extend the reStructuredText syntax or the features of Docutils.
More extensions are in the `Docutils Sandbox`_.

* Beni Cherniavsky has written a generic `preprocessing module`_ for
  roles and/or directives and built preprocessors for TeX math for
  both LaTeX and HTML output on top of it.

  .. _preprocessing module: https://docutils.sourceforge.io/sandbox/cben/rolehack/

* Beni Cherniavsky maintains a Makefile_ for driving Docutils, hoping
  to handle everything one might do with Docutils.

  .. _Makefile: https://docutils.sourceforge.io/sandbox/cben/make/

* The `ASCII art to SVG converter`_ (aafigure) developed by
  Chris Liechti can parse ASCII art images, embedded in reST documents and
  output an image. This would mean that simple illustrations could be
  embedded as ASCII art in the reST source and still look nice when
  converted to e.g. HTML

  .. _ASCII art to SVG converter:
     https://docutils.sourceforge.io/sandbox/cliechti/aafigure/

* Quick and easy publishing reStructuredText source files as blog posts
  on blogger.com is possible with `rst2blogger`_ .

  .. _rst2blogger: https://github.com/dhellmann/rst2blogger#readme

.. _Docutils Sandbox: https://docutils.sourceforge.io/sandbox/README.html


Related Applications
--------------------

Applications using docutils/reStructuredText and helper applications.

* For Blogs (Weblogs), please see the `FAQ entry about Blogs`_.

* `Project Gutenberg`_ uses  Docutils for its "ebookmaker_"
  xetex, nroff, and epub generator (with some `extensions to rST`__).

  __ http://pgrst.pglaf.org/publish/181/181-h.html


* Text-Restructured_ at CPAN is a set of modules to parse
  reStructuredText documents and output them in various formats written
  in Perl_.
  Up to January 2021, the sources were stored in the Docutils repository_.
  After long inactivity (the last commit was r6498__
  2010-12-08), ``trunk/prest/`` was moved to the attic.

  __ https://sourceforge.net/p/docutils/code/6498/

.. _FAQ entry about Wikis: http://docutils.sf.net/FAQ.html
    #are-there-any-wikis-that-use-restructuredtext-syntax
.. _FAQ entry about Blogs: https://docutils.sourceforge.io/FAQ.html
    #are-there-any-weblog-blog-projects-that-use-restructuredtext-syntax
.. _Project Gutenberg: http://www.gutenberg.org
.. _ebookmaker: https://pypi.org/project/ebookmaker/
.. _Perl: https://www.perl.org
.. _Text-Restructured: https://metacpan.org/dist/Text-Restructured
.. _repository: ../dev/repository.html


Wikis
`````

* Trac_ supports `using reStructuredText`__ as an alternative to wiki markup.
  This includes support for TracLinks_ from within reStructuredText
  via a custom rST reference-directive or, even easier, an interpreted
  text role "trac".

  __ http://trac.edgewall.com//wiki/WikiRestructuredText

* MoinMoin_ includes a `ReStructuredText Parser
  <http://moinmo.in/HelpOnParsers/ReStructuredText>`__.

* Ian Bicking's experimental `wiki module`__ in the sandbox.

  __ https://docutils.sourceforge.io/sandbox/ianb/wiki

* Zope-based Zwiki_
  (requires Zope2, which reached end of life on December 31, 2020).

.. _TracLinks: http://trac.edgewall.com//wiki/TracLinks
.. _MoinMoin: http://moinmo.in/
.. _ZWiki: https://github.com/simonmichael/ZWiki


Tools
`````

* rstcheck_ Checks syntax of reStructuredText and code blocks nested within
  it. (Using the Sphinx syntax "code-block" for the "code" directive.)

  .. _rstcheck: https://pypi.python.org/pypi/rstcheck

* restview_ is a viewer for reStructuredText documents.

  Pass the name of a ReStructuredText document to restview, and it will
  launch a web server on localhost:random-port and open a web browser. It
  will also watch for changes in that file and automatically reload and
  rerender it. This is very convenient for previewing a document while
  you're editing it.

  .. _restview: https://mg.pov.lt/restview/


Development
```````````

* Sphinx_ extends the ReStructuredText syntax to better support the
  documentation of Software projects (but other documents
  can be written with it too).

* `Sphinx Extensions`_ allow automatic testing of code snippets,
  inclusion of docstrings from Python modules (API docs), and more.

* Trac_, a project management and bug/issue tracking system, supports
  `using reStructuredText
  <https://trac.edgewall.org/wiki/WikiRestructuredText>`__ as an
  alternative to wiki markup.


* PyLit_ provides a bidirectional text <--> code converter for *literate
  programming with reStructuredText*.

.. _Sphinx extensions: https://www.sphinx-doc.org/en/master/usage/extensions/
.. _Python documentation: https://docs.python.org/
.. _Trac: https://trac.edgewall.org
.. _PyLit: https://codeberg.org/milde/pylit


CMS Systems
```````````

* Plone_ and Zope_ both support reStructuredText markup.

* ZReST_, by Richard Jones, is a "ReStructuredText Document for Zope_"
  application that is complete and ready to install.

.. _Plone: https://plone.org/
.. _Zope: https://www.zope.dev/
.. _ZReST: https://docutils.sourceforge.io/sandbox/richard/ZReST/


Presentations
`````````````

* rst2html5_ transform restructuredtext documents to html5 + twitter's
  bootstrap css, deck.js or reveal.js

  .. _rst2html5: https://github.com/marianoguerra/rst2html5

* landslide_ generates HTML5 slideshows from markdown, ReST, or textile.

  .. _landslide: https://github.com/adamzap/landslide

* `native support for S5 <slide-shows.s5.html>`_.

* The `PythonPoint interface`_ by Richard Jones produces PDF
  presentations using ReportLabs' PythonPoint.

  .. _PythonPoint interface:
     https://docutils.sourceforge.io/sandbox/richard/pythonpoint/

* rst2beamer_ generates a LaTeX source that uses the `Beamer` document class.
  Can be converted to PDF slides with pdfLaTeX/XeLaTeX/LuaLaTeX.

  .. _rst2beamer: https://docutils.sourceforge.io/sandbox/rst2beamer/

* InkSlide_ quick and easy presentations using Inkscape_. InkSlide uses
  reStructuredText for markup, although it renders only a subset of rst.

  .. _InkSlide: http://wiki.inkscape.org/wiki/index.php/InkSlide
  .. _Inkscape: http://inkscape.org/

* rst2outline_ translates a reStructuredText document to a plain text
  outline. This can then be transformed to PowerPoint.

  .. _rst2outline: https://docutils.sourceforge.io/sandbox/rst2outline/

* Pandoc_ can also be used to produce slides

.. TODO: update with input from
   https://stackoverflow.com/questions/2746692/restructuredtext-tool-support
