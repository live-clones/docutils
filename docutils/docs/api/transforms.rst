.. include:: ../header.txt

=====================
 Docutils Transforms
=====================

:Author: David Goodger
:Contact: docutils-develop@lists.sourceforge.net
:Revision: $Revision$
:Date: $Date$
:Copyright: This document has been placed in the public domain.


.. contents::
   :depth: 2

Introduction
============

Transforms change the `document tree`_ in-place, add to the tree, or prune it.
Transforms resolve references and footnote numbers, process
`interpreted text`_, and do other context-sensitive processing.
Each transform is a subclass of `docutils.transforms.Transform`.

There are `transforms added by components`_, others (e.g.
``parts.Contents``) are added by the parser, if a corresponding directive_ is
found in the document.

To add a transform, components (objects inheriting from
`docutils.Component` like Readers, Parsers, Writers, Input, Output) overwrite
the ``get_transforms()`` method of their base class. After the Reader has
finished processing, the Publisher calls
``Transformer.populate_from_components()`` with a list of components and all
transforms returned by the component's ``get_transforms()`` method are
stored in a `transformer object` attached to the document tree.


For more about transforms and the Transformer object, see also `PEP
258`_. (The ``default_transforms()`` attribute of component classes mentioned
there is deprecated. Use the ``get_transforms()`` method instead.)

.. _priority:

Transforms Listed in Priority Order
===================================

Transform classes each have a `default priority` attribute which is used by
the Transformer to apply transforms in order (low to high). The default
priority can be overridden when adding transforms to the Transformer object.


==================================  ============================  ========
Transform: module.Class             Added By                      Priority
==================================  ============================  ========
misc_.ClassAttribute                `"class"`_ (d/p)              210

references_.Substitutions           standalone (r), pep (r)       220

references_.PropagateTargets        standalone (r), pep (r)       260

frontmatter.\ DocTitle_             standalone (r)                320

frontmatter.\ DocInfo_              standalone (r)                340

frontmatter.\ SectSubTitle_         standalone (r)                350

peps_.Headers                       pep (r)                       360

peps_.Contents                      pep (r)                       380

universal_.StripClassesAndElements  Writer (w)                    420

references_.AnonymousHyperlinks     standalone (r), pep (r)       440

references_.IndirectHyperlinks      standalone (r), pep (r)       460

peps_.TargetNotes                   pep (r)                       520

references_.TargetNotes             peps.TargetNotes (t/p)        0

misc_.CallBack                      peps.TargetNotes (t/p)        1

references_.TargetNotes             `"target-notes"`_ (d/p)       540

references_.Footnotes               standalone (r), pep (r)       620

references_.ExternalTargets         standalone (r), pep (r)       640

references_.InternalTargets         standalone (r), pep (r)       660

parts_.SectNum                      `"sectnum"`_ (d/p)            710

parts_.Contents                     `"contents"`_ (d/p),          720
                                    peps.Contents (t/p)

universal_.StripComments            Reader (r)                    740

peps_.PEPZero                       peps.Headers (t/p)            760

components.Filter                   *not used*                    780

universal_.Decorations              Reader (r)                    820

misc_.Transitions                   standalone (r), pep (r)       830

universal_.Validate                 Parser                        835

universal_.ExposeInternals          Reader (r)                    840

references_.DanglingReferences      standalone (r), pep (r)       850

universal_.SmartQuotes              Parser                        855

universal_.Messages                 Writer (w)                    860

universal_.FilterMessages           Writer (w)                    870

universal_.TestMessages             DocutilsTestSupport           880

writer_aux_.Compound                *not used, to be removed*     910

writer_aux_.Admonitions             _html_base (w),               920
                                    latex2e (w)

misc_.CallBack                      n/a                           990
==================================  ============================  ========

Key:

* (r): Reader
* (w): Writer
* (d): Directive
* (t): Transform
* (/p): Via a `\<pending>`_ element


Transform Priority Range Categories
-----------------------------------

====  ====  ================================================
 Priority
----------  ------------------------------------------------
From   To   Category
====  ====  ================================================
   0    99  immediate execution (added by another transform)
 100   199  very early (non-standard)
 200   299  very early
 300   399  early
 400   699  main
 700   799  late
 800   899  very late
 900   999  very late (non-standard)
====  ====  ================================================


Transforms added by components
===============================

readers.Reader:
  | universal.Decorations,
  | universal.ExposeInternals,
  | universal.StripComments

readers.ReReader:
  None

readers.standalone.Reader:
  | references.Substitutions,
  | references.PropagateTargets,
  | frontmatter.DocTitle,
  | frontmatter.SectionSubTitle,
  | frontmatter.DocInfo,
  | references.AnonymousHyperlinks,
  | references.IndirectHyperlinks,
  | references.Footnotes,
  | references.ExternalTargets,
  | references.InternalTargets,
  | references.DanglingReferences,
  | misc.Transitions

readers.pep.Reader:
  | references.Substitutions,
  | references.PropagateTargets,
  | references.AnonymousHyperlinks,
  | references.IndirectHyperlinks,
  | references.Footnotes,
  | references.ExternalTargets,
  | references.InternalTargets,
  | references.DanglingReferences,
  | misc.Transitions,
  | peps.Headers,
  | peps.Contents,
  | peps.TargetNotes

parsers.rst.Parser
  universal.SmartQuotes

writers.Writer:
  | universal.Messages,
  | universal.FilterMessages,
  | universal.StripClassesAndElements

writers.UnfilteredWriter
  None

writers.latex2e.Writer
  writer_aux.Admonitions

writers._html_base.Writer:
  writer_aux.Admonitions

writers.odf_odt.Writer:
  removes references.DanglingReferences


Transforms Reference
====================

Incomplete. See also `Transforms Listed in Priority Order`_
and the sources in `docutils/transforms`__.

__ https://docutils.sourceforge.io/docutils/transforms/


DocInfo
-------

.. class:: field-indent-12em

:Module: frontmatter_
:Added by:  standalone Reader
:Default priority_: 340
:Configuration_ setting: docinfo_xform_ (default: True)

Given a document starting [#pre-docinfo]_ with a field list, the DocInfo
transform converts fields with registered `bibliographic field`_ names to
the corresponding document tree elements becoming child elements of the
`\<docinfo>`_ element (except for "dedication" and "abstract", which
become `\<topic>`_ elements after <docinfo>).

.. [#pre-docinfo] A document title and subtitle, header and footer,
   as well as body elements that do not show up in the output
   before the field list don't prevent the DocInfo transformation.
   See the `DocTitle examples`_ and `PreBibliographic Elements`_
   in the Appendix for details.

For example, this document fragment::

    <document>
        <title>
            Document Title
        <field_list>
            <field>
                <field_name>
                    Author
                <field_body>
                    <paragraph>
                        A. Name
            <field>
                <field_name>
                    Status
                <field_body>
                    <paragraph>
                        $RCSfile$
        ...

will be transformed to::

    <document>
        <title>
            Document Title
        <docinfo>
            <author>
                A. Name
            <status>
                frontmatter.py
        ...


DocTitle
--------

.. class:: field-indent-12em

:Module: frontmatter_
:Added by:  standalone Reader
:Default priority_: 320
:Configuration_ setting: doctitle_xform_ (default: True)

Under the conditions explained below, the DocTitle transform converts
the document's first section title(s) to a document title and
subtitle.

1. If the document contains a single top-level section as its first body
   element, [#pre-doctitle]_ the top-level section's title is used
   as `document title`_ and default `metadata title`_. The top-level
   section's contents become the document's immediate contents.

   .. _step 2:

2. If step 1 successfully determines the document title, the transform
   checks for a subtitle:
   If the lone top-level section itself contains a single second-level
   section as its first element, [#pre-doctitle]_ that section's
   title is promoted to the document's subtitle, and that section's
   contents become the document's immediate contents.

The transform can be disabled with the doctitle_xform_ configuration
setting or the corresponding ``--no-doc-title`` command line option.

.. [#pre-doctitle] Header and footer as well as body elements that
   do not show up in the output before the section don't stop the
   transformation of the section title to document title or subtitle.
   See `PreBibliographic Elements`_ in the Appendix for details.

.. _DocTitle examples:

Examples
~~~~~~~~

The input text ::

    Top-Level Title
    ===============
    A paragraph.

is parsed to the following document tree::

    <document>
        <section names="top-level\ title">
            <title>
                Top-Level Title
            <paragraph>
                A paragraph.

The DocTitle transform converts it to::

    <document names="top-level\ title" title="Top-Level Title">
        <title>
            Top-Level Title
        <paragraph>
            A paragraph.

Given this input with a lone section and sub-section::

    Top-Level Title
    ===============
    Second-Level Title
    ~~~~~~~~~~~~~~~~~~

    A paragraph.

the result after parsing and running the DocTitle transform is::

    <document names="top-level\ title">
        <title>
            Top-Level Title
        <subtitle names="second-level\ title">
            Second-Level Title
        <paragraph>
            A paragraph.

(Note that the implicit hyperlink target generated by the
"Second-Level Title" is preserved on the "subtitle" element
itself.)

--------------

The following examples do *not* comply with the conditions:

i. More than one top-level section::

       Top-Level Title
       ===============
       A paragraph.

       Another Top-Level Title
       =======================
       Another paragraph.

   The DocTitle transform will leave the document tree as-is.
   The document has no title. It is recommended to set the
   `metadata title`_ with the `"title"`_ directive.

#. More than one second-level section::

       Top-Level Title
       ===============
       Second-Level Title
       ~~~~~~~~~~~~~~~~~~
       A paragraph.

       Another Second-Level Title
       ~~~~~~~~~~~~~~~~~~~~~~~~~~
       Another paragraph.

   Step 2 is skipped. "Top-Level Title" becomes the document title;
   "Second-Level Title" and "Another Second-Level Title" become titles of
   top-level sections.

   This is what you normally want in a document with title but no
   subtitle.

#. Body elements before the first section: [#pre-doctitle]_ ::

       .. note:: This element would not stop the transform, if it were
          nested in a header.

       Top-Level Title
       ===============
       A paragraph.

   The DocTitle transform will leave the document tree as-is.
   The document has no title.


#. A `configuration file`_ entry "``doctitle_xform: False``"
   or converting with the CLI command ::

      docutils --no-doc-title example.rst > example.html

   The DocTitle transform is skipped. The document has no title.


SectSubTitle
------------

.. class:: field-indent-12em

:Module: frontmatter_
:Added by:  standalone Reader
:Default priority_: 350
:Configuration_ setting: sectsubtitle_xform_ (default: False)

The SectSubTitle transform works like `step 2`_ of the DocTitle_
transform, but for sections.

For example, ::

    <section>
        <title>
            Title
        <section>
            <title>
                Subtitle
            ...

is transformed into ::

    <section>
        <title>
            Title
        <subtitle>
            Subtitle
        ...

This transform is disabled by default.


Appendix
========

PreBibliographic Elements
-------------------------

The document tree elements `\<comment>`_, `\<decoration>`_,
`\<footer>`_, `\<header>`_, `\<meta>`_, `\<pending>`_, `\<raw>`_,
`\<substitution_definition>`_, `\<subtitle>`_, `\<system_message>`_,
`\<target>`_, and `\<title>`_ are ignored when the DocTitle_ and DocInfo_
transforms check for elements before frontmatter candidates.

This means that in the reStructuredText source, comments_,
`hyperlink targets`_, `substitution definitions`_, and the directives_
`"class"`_, `"default-role"`_, `"footer"`_, `"header"`_, `"meta"`_,
`"raw"`_, `"sectnum"`_, `"sectnum"`_, `"target-notes"`_, and `"title"`_
may be placed before the `document title`_ or `bibliographic fields`_.

The DocTitle_ transform inserts document title and subtitle before these
elements.  DocInfo_ inserts the bibliographic fields before
`\<comment>`_, `\<raw>`_, `\<substitution_definition>`_, and `\<target>`_.

For example, the document source::

  .. a comment
  .. |today| date::
  .. _hypertarget: http://example.org
  .. class:: spam
  .. role:: ham
  .. default-role:: ham
  .. footer:: footer text
  .. header:: header text
  .. meta:: :test: value
  .. raw:: html

     raw html text
  .. sectnum::
  .. target-notes::
  .. title:: metadata document title

  Top-Level Title
  ===============
  Second-Level Title
  ~~~~~~~~~~~~~~~~~~

  :date: |today|

is parsed and transformed to::

  <document ids="top-level-title" names="top-level\ title"
            title="metadata document title">
      <title>
          Top-Level Title
      <subtitle ids="second-level-title" names="second-level\ title">
          Second-Level Title
      <meta content="value" name="test">
      <decoration>
          <header>
              <paragraph>
                  header text
          <footer>
              <paragraph>
                  footer text
      <docinfo>
          <date>
              2024-03-01
      <comment xml:space="preserve">
          a comment
      <substitution_definition names="today">
          2024-03-01
      <target ids="hypertarget" names="hypertarget" refuri="http://example.org">
      <raw classes="spam" format="html" xml:space="preserve">
          raw html text



.. References
   ==========

.. _PEP 258: ../peps/pep-0258.html#transformer

.. _configuration:
.. _configuration file:
.. _configuration setting: ../user/config.html
.. _docinfo_xform: ../user/config.html#docinfo-xform
.. _doctitle_xform: ../user/config.html#doctitle-xform
.. _sectsubtitle_xform: ../user/config.html#sectsubtitle-xform

.. _directive:
.. _directives: ../ref/rst/directives.html
.. _"class": ../ref/rst/directives.html#class
.. _"contents": ../ref/rst/directives.html#table-of-contents
.. _"default-role": ../ref/rst/directives.html#default-role
.. _"footer": ../ref/rst/directives.html#footer
.. _"header": ../ref/rst/directives.html#header
.. _"meta": ../ref/rst/directives.html#meta
.. _"raw": ../ref/rst/directives.html#raw
.. _"sectnum": ../ref/rst/directives.html#sectnum
.. _"target-notes": ../ref/rst/directives.html#target-notes
.. _"title": ../ref/rst/directives.html#title

.. _document tree: ../ref/doctree.html
.. _`<comment>`: ../ref/doctree.html#comment
.. _`<docinfo>`: ../ref/doctree.html#docinfo
.. _`<decoration>`: ../ref/doctree.html#decoration
.. _`<footer>`: ../ref/doctree.html#footer
.. _`<header>`: ../ref/doctree.html#header
.. _`<meta>`:  ../ref/doctree.html#meta
.. _`<pending>`:  ../ref/doctree.html#pending
.. _`<raw>`: ../ref/doctree.html#raw
.. _`<substitution_definition>`: ../ref/doctree.html#substitution-definition
.. _`<subtitle>`: ../ref/doctree.html#subtitle
.. _`<system_message>`: ../ref/doctree.html#system-message
.. _`<target>`: ../ref/doctree.html#target
.. _`<title>`: ../ref/doctree.html#title
.. _`<topic>`: ../ref/doctree.html#topic
.. _metadata title: ../ref/doctree.html#title-attribute

.. reStructuredText Markup Specification
.. _bibliographic field:
.. _bibliographic fields:
    ../ref/rst/restructuredtext.html#bibliographic-fields
.. _comments: ../ref/rst/restructuredtext.html#comments
.. _document title:   ../ref/rst/restructuredtext.html#document-title
.. _hyperlink targets: ../ref/rst/restructuredtext.html#hyperlink-targets
.. _interpreted text: ../ref/rst/restructuredtext.html#interpreted-text
.. _registered bibliographic field names:
    ../ref/rst/restructuredtext.html#bibliographic-field-names
.. _substitution definitions:
    ../ref/rst/restructuredtext.html#substitution-definitions

.. transform class sources
.. _frontmatter: ../../docutils/transforms/frontmatter.py
.. _misc:        ../../docutils/transforms/misc.py
.. _parts:       ../../docutils/transforms/parts.py
.. _peps:        ../../docutils/transforms/peps.py
.. _references:  ../../docutils/transforms/references.py
.. _universal:   ../../docutils/transforms/universal.py
.. _writer_aux:  ../../docutils/transforms/writer_aux.py
