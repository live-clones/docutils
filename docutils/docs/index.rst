==========================================
 Docutils Project Documentation Overview
==========================================

:Author: David Goodger
:Contact: docutils-develop@lists.sourceforge.net
:Date: $Date$
:Revision: $Revision$
:Copyright: This document has been placed in the public domain.

The latest working documents may be accessed individually below, or
from the ``docs`` directory of the `Docutils distribution`_.

.. _Docutils distribution: https://docutils.sourceforge.io/#download

.. header::
  Docutils_ | Overview | About__ | Users__ | Reference__ | API_ | Developers__

.. _Docutils: https://docutils.sourceforge.io/
__ `project fundamentals`_
__ user_
__ ref_
__ howto_


.. contents::


Docutils Stakeholders
=====================

can be categorized in several groups:
  .. class:: details

  End-users
    users of reStructuredText and the Docutils tools.
    Although some are developers (e.g. Python developers utilizing
    reStructuredText for docstrings in their source), many are not.
  Client-developers
    developers using Docutils as a library,
    programmers developing *with* Docutils.
  Component-developers
    those who implement application-specific components,
    directives, and/or roles, separately from Docutils.
  Core-developers
    contributors to the Docutils codebase and
    participants in the Docutils project community.
  Re-implementers
    developers of alternate implementations of Docutils.

.. class:: details

There's a lot of overlap between these groups.
  Most (perhaps all) developers are also end-users.
  Core-developers are also client-developers, and may also
  be component-developers in other projects.
  Component-developers are also client-developers.


Project Fundamentals
====================

These files are for all `Docutils stakeholders`_.  They are kept at the
top level of the Docutils project directory.

`README <../README.html>`_:
   Project overview: quick-start, requirements,
   installation, and usage.

`COPYING <../COPYING.html>`_:
   Conditions for Docutils redistribution,
   with links to licenses.
`FAQ <../FAQ.html>`_:
  Docutils Frequently Asked Questions.  If you have a question or issue,
  there's a good chance it's already answered here.
`BUGS <../BUGS.html>`_:
  A list of known bugs, and how to report a bug.
`RELEASE-NOTES <../RELEASE-NOTES.html>`_:
  Summary of the major changes in recent releases and
  notice of future incompatible changes.
`HISTORY <../HISTORY.html>`_:
  Detailed change history log.
`THANKS <../THANKS.html>`_:
  Acknowledgements.


.. _user:

Introductory & Tutorial Material for End-Users
==============================================

Docutils-general:
  * `Docutils Front-End Tools <user/tools.html>`__
  * `Docutils Configuration <user/config.html>`__
  * `Docutils Mailing Lists <user/mailing-lists.html>`__
  * `Docutils Link List <user/links.html>`__

_`Writer-specific`:
  * `Docutils HTML Writers <user/html.html>`__
  * `Easy Slide Shows With reStructuredText & S5 <user/slide-shows.html>`__
  * `Docutils LaTeX Writer <user/latex.html>`__
  * `Man Page Writer for Docutils <user/manpage.html>`__
  * `Docutils ODF/OpenOffice/odt Writer <user/odt.html>`__

`reStructuredText <https://docutils.sourceforge.io/rst.html>`_:
  * `A ReStructuredText Primer <user/rst/quickstart.html>`__
    (see also the `text source <user/rst/quickstart.rst>`__)
  * `Quick reStructuredText <user/rst/quickref.html>`__ (user reference)
  * `reStructuredText Cheat Sheet <user/rst/cheatsheet.rst>`__ (text
    only; 1 page for syntax, 1 page directive & role reference)
  * `Demonstration <user/rst/demo.html>`_
    of most reStructuredText features
    (see also the `text source <user/rst/demo.rst>`__)

Editor support:
  * `Emacs support for reStructuredText <user/emacs.html>`_


.. _ref:

Reference Material for All Groups
=================================

Many of these files began as developer specifications, but now that
they're mature and used by end-users and client-developers, they have
become reference material.  Successful specs evolve into refs.

Docutils-general:
  * `The Docutils Document Tree <ref/doctree.html>`__ (incomplete)
  * `Docutils Generic DTD <ref/docutils.dtd>`__
  * `OASIS XML Exchange Table Model Declaration Module
    <ref/soextblx.dtd>`__ (CALS tables DTD module)
  * `Docutils Design Specification`_ (PEP 258)

reStructuredText_:
  * `An Introduction to reStructuredText <ref/rst/introduction.html>`__
    (includes the `Goals <ref/rst/introduction.html#goals>`__
    of reStructuredText)
  * `History of reStructuredText  <ref/rst/history.html>`__
  * `reStructuredText Markup Specification <ref/rst/restructuredtext.html>`__
  * `reStructuredText Directives <ref/rst/directives.html>`__
  * `reStructuredText Interpreted Text Roles <ref/rst/roles.html>`__
  * `reStructuredText Standard Definition Files
    <ref/rst/definitions.html>`_
  * `LaTeX syntax for mathematics <ref/rst/mathematics.html>`__
    (syntax used in "math" directive and role)

.. _peps:

Python Enhancement Proposals
  * `PEP 256: Docstring Processing System Framework`__ is a high-level
    generic proposal.  [:PEP:`256` in the `master repository`_]
  * `PEP 257: Docstring Conventions`__ addresses docstring style and
    touches on content.  [:PEP:`257` in the `master repository`_]
  * `PEP 258: Docutils Design Specification`__ is an overview of the
    architecture of Docutils.  It documents design issues and
    implementation details.  [:PEP:`258` in the `master repository`_]
  * `PEP 287: reStructuredText Docstring Format`__ proposes a standard
    markup syntax.  [:PEP:`287` in the `master repository`_]

  Please note that PEPs in the `master repository`_ developed
  independent from the local versions after submission.

  __ peps/pep-0256.html
  __ peps/pep-0257.html
  .. _PEP 258:
  .. _Docutils Design Specification:
  __ peps/pep-0258.html
  __ peps/pep-0287.html
  .. _master repository: https://peps.python.org

Prehistoric:
  `Setext Documents Mirror`__

  __ https://docutils.sourceforge.io/mirror/setext.html


.. _api:

API Reference Material for Client-Developers
============================================

`The Docutils Publisher <api/publisher.html>`__
  entry points for using Docutils as a library
`Docutils Runtime Settings <api/runtime-settings.html>`__
  configuration framework details
`Docutils Transforms <api/transforms.html>`__
  change the document tree in-place (resolve references, …)

The `Docutils Design Specification`_ (PEP 258) is a must-read for any
Docutils developer.


Docutils Enhancement Proposals
==============================

* `Enhancement Proposal Index <eps/index.html>`__


.. _howto:

Instructions for Developers
===========================

* `Deploying Docutils Securely <howto/security.html>`__
* `Inside A Docutils Command-Line Front-End Tool <howto/cmdline-tool.html>`__
* `Runtime Settings Processing <dev/runtime-settings-processing.html>`__
* `Writing HTML (CSS) Stylesheets for Docutils
  <howto/html-stylesheets.html>`__
* `Docutils Internationalization <howto/i18n.html>`__
* `Creating reStructuredText Directives <howto/rst-directives.html>`__
* `Creating reStructuredText Interpreted Text Roles
  <howto/rst-roles.html>`__


.. _dev:

Development Notes and Plans for Core-Developers
===============================================

Docutils-general:
  * `Docutils Project Policies <dev/policies.html>`__
  * `Docutils Testing <dev/testing.html>`__
  * `Docutils Hacker's Guide <dev/hacking.html>`__
  * `Docutils To Do List <dev/todo.html>`__
  * `Docutils Version Repository <dev/repository.html>`__
  * `Docutils Web Site <dev/website.html>`__
  * `Docutils Release Procedure <dev/release.html>`__
  * `Docutils Distributor's Guide <dev/distributing.html>`__

reStructuredText_:
  * `A Record of reStructuredText Syntax Alternatives
    <dev/rst/alternatives.html>`__
  * `Problems With StructuredText <dev/rst/problems.html>`__

Suspended projects and plans:
  * `Docstring Semantics <dev/semantics.html>`__ (incomplete)
  * `Python Source Reader <dev/pysource.html>`_ (incomplete)
  * `Docutils Python DTD <dev/pysource.dtd>`_
  * `Plan for Enthought API Documentation Tool <dev/enthought-plan.html>`_
  * `Enthought API Documentation Tool RFP <dev/enthought-rfp.html>`_

.. Emacs settings

   Local Variables:
   mode: indented-text
   mode: rst
   indent-tabs-mode: nil
   sentence-end-double-space: t
   fill-column: 70
   End:
