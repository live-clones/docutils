.. include:: ../header.txt

============================
 The Docutils Document Tree
============================

A Guide to the Docutils DTD
***************************

:Author: David Goodger
:Contact: docutils-develop@lists.sourceforge.net
:Revision: $Revision$
:Date: $Date$
:Copyright: This document has been placed in the public domain.


.. contents:: :depth: 1

This document describes the XML_ data structure of Docutils_ documents:
the relationships and semantics of elements and attributes.
The Docutils document structure is formally defined by the
`Docutils Generic DTD`_ XML document type definition, `docutils.dtd`_,
which is the definitive source for details of element structural
relationships.

The reader is assumed to have some familiarity with XML or SGML,
and an understanding of the data structure meaning of "tree".
For a list of introductory articles, see, e.g.,
`Introducing the Extensible Markup Language (XML)`_.

Docutils implements the Document tree data structure in the Python_
module docutils.nodes_.  For details, see its internal API documentation
("docstrings").

The reStructuredText_ markup language is used for illustrative examples
throughout this document.  For a gentle introduction, see `A
ReStructuredText Primer`_.  For complete technical details, see the
`reStructuredText Markup Specification`_.


-------------------
 Element Hierarchy
-------------------

The Docutils document model uses strict element content models.

Below is a *simplified* diagram of the hierarchy of elements in the
Docutils document tree structure.
An element may contain elements immediately below it in the diagram.
Element types in square brackets indicate recursive or one-to-many
relationships: structural elements (sections) may contain sub-sections,
some body elements may contain other body elements, etc.
The `element reference`_ details valid parents and children
for each element.

.. raw:: html

   <style type="text/css"><!--
     table.e-hierarchy {border: 1px solid}
     table.e-hierarchy td {border: 0px; padding: 0.5em}
     table.e-hierarchy a {color: black; text-decoration: underline}
     /* root element */
     table.e-hierarchy tr:first-child  {background: tomato}
     table.e-hierarchy td:nth-child(2) {background: tomato}
     table.e-hierarchy td:nth-child(3) {background: tomato}
     /* structural elements */
     table.e-hierarchy tr:nth-child(2) {background: limegreen}
     table.e-hierarchy tr:nth-child(3) td:first-child {background: limegreen}
     /* structural subelements */
     table.e-hierarchy tr:nth-child(3) td:nth-child(2) {background: mediumseagreen}
     /* body elements */
     table.e-hierarchy tr:nth-child(4) > td {background: orchid}
     table.e-hierarchy tr:nth-child(5) td:nth-child(2){background: orchid}
     table.e-hierarchy tr:nth-child(5) td:nth-child(3){background: orchid}
     /* body subelements */
     table.e-hierarchy tr:nth-child(5) > td {background: thistle}
     table.e-hierarchy tr:nth-child(6) td:first-child {background: thistle}
     /* inline elements */
     table.e-hierarchy tr:nth-child(6) td:nth-child(2){background: gold}
     /* text */
     table.e-hierarchy tr:last-child  {background: khaki}
   --></style>

.. table::
   :class: e-hierarchy
   :width: 65%
   :widths: 1 2 1 1
   :align: center

   +------------------------------------------+
   | `root element`_ (`\<document>`_)         |
   +---+------------------------------+---+---+
   | [`structural elements`_]         |   |   |
   +---+------------------------------+---+   +
   |   | [`structural subelements`_]      |   |
   +---+----------------------------------+---+
   | [`body elements`_]                       |
   +---+------------------------------+---+---+
   | [`body subelements`_]            |   |   |
   +---+------------------------------+---+   +
   |   | [`inline elements`_]             |   |
   +---+----------------------------------+---+
   | text                                     |
   +------------------------------------------+

Every element has a unique structure and semantics, but elements may be
classified into general categories according to their place and role in
the document. Some elements belong to more than one category.

.. contents:: :local:


Alternatively, we may classify elements by their content model:

.. class:: description

_`Compound elements`
  | may contain child elements but no text data.
  | Examples: `\<bullet_list>`_, `\<footnote>`_, `\<table>`_

_`Simple elements`
  | may contain text data.
  | Most simple elements have a mixed content model (`%text.model`_).
    However, only `inline elements`_ may be intermixed with text. [#]_
  | Examples: `\<paragraph>`_ (mixed), `\<literal_block>`_ (text-only)

_`Empty elements`
  | contain neither child elements nor text.
  | Category members: `\<colspec>`_, `\<image>`_, `\<meta>`_,
    `\<pending>`_, `\<transition>`_

.. [#] This is unlike the much looser HTML_ document model,
   where paragraphs and text data may occur at the same level.


Element Categories
==================

Root Element
------------

Every Docutils document contains exactly one root element.
The root element has no parent. It may contain `structural elements`_,
all `structural subelements`_, and `body elements`_.
It does not directly contain text.

.. class:: field-indent-11em

:Category members: `\<document>`_
:Docutils class:   ``nodes.Root``


Structural Elements
-------------------

Structural elements group other elements to provide a document structure.
They are child elements of the `root element`_ or other structural
elements. Structural elements may contain specific structural elements,
`structural subelements`_, or `body elements`_.

.. class:: field-indent-11em

:Category members: `\<section>`_, `\<sidebar>`_, `\<topic>`_
:Docutils class:   ``nodes.Structural``


Structural Subelements
----------------------

Structural subelements are child elements of the `root element`_ or
specific `structural elements`_.  Their content model varies
(see the respective element reference section for details).

.. class:: narrow run-in

:Category members:
  .. class:: narrow run-in

  :empty: `\<meta>`_, `\<transition>`_
  :simple: `\<title>`_, `\<subtitle>`_
  :compound: `\<decoration>`_, `\<docinfo>`_

:Docutils class: ``nodes.SubStructural``


Decorative Elements
-------------------

Decorative elements are used to generate page headers and footers. They
are child elements of `\<decoration>`_ and contain `body elements`_.

.. class:: field-indent-11em

:Category members: `\<footer>`_, `\<header>`_
:Docutils class:   ``nodes.Decorative``


Bibliographic Elements
----------------------

Bibliographic elements store document meta-data like title or author.
They are child elements of `\<docinfo>`_.
The elements `\<authors>`_ and `\<field>`_ are `compound elements`_,
the others are `simple elements`_ containing text and `inline elements`_.

.. class:: field-indent-11em

:Category members: `\<address>`_, `\<author>`_, `\<authors>`_,
                   `\<contact>`_, `\<copyright>`_, `\<date>`_,
                   `\<field>`_, `\<organization>`_, `\<revision>`_,
                   `\<status>`_, `\<version>`_
:Docutils class:   ``nodes.Bibliographic``
:Parameter entity: `%bibliographic.elements`_


.. _simple body elements:
.. _compound body elements:

Body Elements
-------------

Body elements are children of the `root element`, `structural elements`_,
or compound body elements. Compound body elements may contain `body
subelements`_ or further body elements.

.. class:: narrow run-in

:Category members:
  .. class:: narrow run-in

  :empty:
    `\<image>`_ , `\<pending>`_
  :simple:
    `\<comment>`_, `\<doctest_block>`_, `\<literal_block>`_, `\<math_block>`_,
    `\<paragraph>`_, `\<raw>`_, `\<reference>`_, `\<rubric>`_,
    `\<substitution_definition>`_, `\<target>`_
  :compound:
    `\<admonition>`_, `\<attention>`_, `\<block_quote>`_, `\<bullet_list>`_,
    `\<caution>`_, `\<citation>`_, `\<compound>`_, `\<container>`_,
    `\<danger>`_, `\<definition_list>`_, `\<enumerated_list>`_, `\<error>`_,
    `\<field_list>`_, `\<figure>`_, `\<footnote>`_, `\<hint>`_,
    `\<important>`_, `\<line_block>`_, `\<note>`_, `\<option_list>`_,
    `\<system_message>`_, `\<table>`_, `\<tip>`_, `\<warning>`_

:Docutils class: ``nodes.Body``

:Parameter entity: `%body.elements`_


Body Subelements
----------------

Body subelements always occur within specific parent elements
(e.g. `\<bullet_list>`_ contains `\<list_item>`_), never at the
body element level (beside paragraphs, etc.).
Body subelements may be `compound elements`_ (containing `body elements`_ or
further body subelements) or `simple elements`_.

.. class:: narrow run-in

:Category members:
  .. class:: narrow run-in

  :empty:
    `\<colspec>`_
  :simple:
    `\<attribution>`_, `\<caption>`_, `\<classifier>`_,
    `\<field_name>`_, `\<label>`_, `\<line>`_,
    `\<option_argument>`_, `\<option_string>`_, `\<term>`_, `\<title>`_
  :compound:
    `\<definition>`_, `\<definition_list_item>`_, `\<description>`_,
    `\<entry>`_, `\<field>`_, `\<field_body>`_,
    `\<legend>`_, `\<list_item>`_,
    `\<option>`_, `\<option_group>`_, `\<option_list_item>`_,
    `\<row>`_, `\<tbody>`_, `\<tgroup>`_, `\<thead>`_

:Docutils class: ``nodes.Part``



Inline Elements
---------------

Inline elements are contained within simple `body elements`_ or other
inline elements.
Inline elements are `simple elements`_: All inline elements may contain
text data, most inline elements may also contain further inline elements.

.. class:: narrow run-in

:Category members:
  `\<abbreviation>`_, `\<acronym>`_, `\<citation_reference>`_, `\<emphasis>`_,
  `\<footnote_reference>`_, `\<generated>`_, `\<image>`_, `\<inline>`_,
  `\<literal>`_, `\<math>`_, `\<problematic>`_, `\<raw>`_, `\<reference>`_,
  `\<strong>`_, `\<subscript>`_, `\<substitution_reference>`_,
  `\<superscript>`_, `\<target>`_, `\<title_reference>`_
:Docutils class: ``nodes.Inline``

:Parameter entity: `%inline.elements`_


-------------------
 Element Reference
-------------------

.. contents:: :local:
              :depth: 1

Each element in the DTD (document type definition) is described in its
own section below.  Each section contains the following items:

* Summary description (up to two sentences).

* Details (of element relationships and semantics):

  :Category: One or more references to the element categories in
    `Element Hierarchy`_ above.  Some elements belong to more than one
    category.

  :Analogues: Describes analogous elements in well-known document
    models such as HTML_ or DocBook_.  Lists similarities and
    differences.

  :Processing: Lists formatting or rendering recommendations for the
    element.

  :Parents: A list of elements which may contain the element.

  :Children: A list of elements which may occur within the element
    followed by the formal XML content model from the `Docutils DTD`_.

  :Attributes: Describes (or refers to descriptions of) the possible
    values and semantics of each attribute.

  :Parameter Entities:
    Lists the `parameter entities <parameter entity reference_>`__
    which directly or indirectly include the element (if applicable).

* Additional free text description and explanations (optional).

* Examples: reStructuredText_ examples are shown along with
  fragments of the document trees resulting from parsing.
  _`Pseudo-XML` is used for the results of parsing and processing.
  Pseudo-XML is a representation of XML where nesting is indicated by
  indentation and end-tags are not shown.  Some of the precision of
  real XML is given up in exchange for easier readability.  For
  example, the following are equivalent:

  Real XML::

        <document>
        <section ids="a-title" names="a title">
        <title>A Title</title>
        <paragraph>A paragraph.</paragraph>
        </section>
        </document>

  Pseudo-XML::

        <document>
            <section ids="a-title" names="a title">
                <title>
                    A Title
                <paragraph>
                    A paragraph.

--------------------

Many of the element reference sections below are marked "_`to be
completed`".  Please help complete this document by contributing to
its writing.


<abbreviation>
==============

The <abbreviation> element is an inline element representing an
*abbreviation*, a shortened or contracted form of a word or phrase
used to represent the whole.

:Category:   `Inline Elements`_
:Analogues:  <abbreviation> is analogous to the DocBook_ <abbrev> element
             and similar to the HTML_ <abbr> element.
             (In HTML 5, the <abbr> element is also used for acronyms.)
:Processing: May be used to semantically mark the presence of an
             abbreviation in the text for styling or scripting purposes.
             Writers may ignore the element and just render its contents.
:Parents:    All elements employing the `%text.model`_ parameter
             entity in their content models may contain <abbreviation>.
:Children:   <abbreviation> elements may contain text data
             plus `inline elements`_ (`%text.model`_).
:Attributes: The <abbreviation> element contains only the `common attributes`_.

Examples
--------

The reStructuredText `"abbreviation" role`_ creates an <abbreviation> element::

    :abbreviation:`St` is a common abbreviation for "street".

Pseudo-XML_ fragment from simple parsing::

    <paragraph>
        <abbreviation>
            St
        is a common abbreviation for "street".


<acronym>
=========

The <acronym> element is an inline element used to represent an
*acronym* (abbreviation formed by the initial letters of other words).

:Category:   `Inline Elements`_
:Analogues:  <acronym> is analogous to the DocBook_ <acronym> element.
             In HTML_, the <abbr> element is used for both,
             abbreviations and acronyms.
:Processing: May be used to semantically mark the presence of an
             acronym in the text for styling or scripting purposes.
             Writers may ignore the element and just render its contents.
:Parents:    All elements employing the `%text.model`_ parameter
             entity in their content models may contain <acronym>.
:Children:   <acronym> elements may contain text data
             plus `inline elements`_ (`%text.model`_).
:Attributes: The <acronym> element contains only the `common attributes`_.

Examples
--------

The reStructuredText `"acronym" role`_ creates an <acronym> element::

    `WWW`:acronym: is the acronym for the world wide web.

Pseudo-XML_ fragment from simple parsing::

    <paragraph>
        <acronym>
            WWW
        is the acronym for the world wide web.


<address>
===========

The <address> element holds the surface mailing address information
for the author(s) (individual or group) of the document, or a third-party
contact address.

:Category:   `Bibliographic Elements`_
:Analogues:  <address> is analogous to the DocBook_ <address> element.
:Processing: As with the `\<literal_block>`_ element, newlines and other
             whitespace is significant and must be preserved.
             However, a monospaced typeface need not be used.
             See also `\<docinfo>`_.
:Parents:    The following elements may contain <address>:
             `\<docinfo>`_, `\<authors>`_.
:Children:   <address> elements contain text data plus `inline elements`_
             (`%text.model`_).
:Attributes: The <address> element contains the `common attributes`_
             plus `xml:space`_.
:Parameter Entities: The `%bibliographic.elements`_ parameter entity
             directly includes <address>.

Examples
--------

In reStructuredText, "address" is one of the registered
`bibliographic fields`_::

    Document Title
    ==============

    :Address: 123 Example Ave.
              Example, EX

Complete pseudo-XML_ result after parsing and applying transforms_::

    <document ids="document-title" names="document title">
        <title>
            Document Title
        <docinfo>
            <address>
                123 Example Ave.
                Example, EX

See `\<docinfo>`_ for a more complete example, including processing
context.


<admonition>
============

The <admonition> element is a generic, titled *admonition*,
a distinctive and self-contained notice.

:Category:   `Compound Body Elements`_

:Analogues:  The generic <admonition> has no direct analogues in common DTDs.
             It can be emulated with primitives and type effects.
             The specific admonitions `\<caution>`_, `\<note>`_,
             `\<tip>`_, and `\<warning>`_ are analogous to the
             respective DocBook_ elements.

:Processing: Rendered distinctly (inset and/or in a box, etc.).

:Parents:    All elements employing the `%body.elements`_
             or `%structure.model`_ parameter entities in
             their content models may contain <admonition>.

:Children:   <admonition> elements begin with a `\<title>`_ and may contain
             one or more `body elements`_.

:Attributes: The <admonition> element contains only the `common attributes`_.

:Parameter Entities: The `%body.elements`_ parameter entity directly
             includes <admonition>.  The `%structure.model`_
             parameter entity indirectly includes <admonition>.

See also the _`specific admonition elements`
`\<attention>`_ `\<caution>`_, `\<danger>`_, `\<error>`_, `\<hint>`_,
`\<important>`_, `\<note>`_, `\<tip>`_, and `\<warning>`_.

Examples
--------

The reStructuredText `"admonition" directive`_ creates a generic
<admonition> element::

    .. admonition:: By the way...

       You can make up your own admonition too.

Pseudo-XML_ fragment from simple parsing::

    <admonition class="admonition-by-the-way">
        <title>
            By the way...
        <paragraph>
            You can make up your own admonition too.


<attention>
===========

The <attention> element is a specific *admonition*, a distinctive and
self-contained notice.

:Category:   `Compound Body Elements`_
:Analogues:  <attention> has no direct analogues in common DTDs.
             It can be emulated with primitives and type effects.
:Processing: Rendered distinctly (inset and/or in a box, etc.),
             with the generated title "Attention!" (or similar).
:Parents:    All elements employing the `%body.elements`_ or
             `%structure.model`_ parameter entities in their
             content models may contain <attention>.
:Children:   <attention> elements contain one or more `body elements`_.
:Attributes: The <attention> element contains only the `common attributes`_.
:Parameter Entities: The `%body.elements`_ parameter entity
             directly includes <attention>.  The `%structure.model`_
             parameter entity indirectly includes <attention>.

See also the generic `\<admonition>`_ and the other
`specific admonition elements`_.

Examples
--------

A reStructuredText `"attention" directive`_::

    .. Attention:: All your base are belong to us.

Pseudo-XML_ fragment from simple parsing::

    <attention>
        <paragraph>
            All your base are belong to us.


<attribution>
=============

`To be completed`_.


<author>
========

The <author> element holds the name of the author (or one of the authors)
of the document.

:Category:   `Bibliographic Elements`_
:Analogues:  <author> is analogous to the DocBook_ <author> element.
:Processing: See `\<docinfo>`_.
:Parents:    The following elements may contain <author>:
             `\<docinfo>`_, `\<authors>`_.
:Children:   <author> elements may contain text data plus `inline elements`_
             (`%text.model`_).
:Attributes: The <author> element contains only the `common attributes`_.
:Parameter Entities: The `%bibliographic.elements`_ parameter entity
             directly includes <author>.

Examples
--------

In reStructuredText, "author" is one of the registered
`bibliographic fields`_::

    Document Title
    ==============

    :Author: J. Random Hacker

Complete pseudo-XML_ result after parsing and applying transforms_::

    <document ids="document-title" names="document title">
        <title>
            Document Title
        <docinfo>
            <author>
                J. Random Hacker

See `\<docinfo>`_ for a more complete example, including processing
context.


<authors>
=========

The <authors> element is a container for author information for
documents with multiple authors.

:Category:   `Bibliographic Elements`_
:Analogues:  <authors> is analogous to the DocBook_ <authorgroup> element.
:Processing: See `\<docinfo>`_.
:Parents:    Only the `\<docinfo>`_ element contains <authors>.
:Children:   <authors> elements may contain the following elements:
             `\<author>`_, `\<organization>`_, `\<address>`_, `\<contact>`_::

               ((author, organization?, address?, contact?)+)
:Attributes: The <authors> element contains only the `common attributes`_.
:Parameter Entities: The `%bibliographic.elements`_ parameter entity
             directly includes <authors>.

Examples
--------

In reStructuredText, "authors" is one of the registered
`bibliographic fields`_::

    Document Title
    ==============

    :Authors: J. Random Hacker; Jane Doe

Complete pseudo-XML_ result after parsing and applying transforms_::

    <document ids="document-title" names="document title">
        <title>
            Document Title
        <docinfo>
            <authors>
                <author>
                    J. Random Hacker
                <author>
                    Jane Doe

In reStructuredText, multiple author's names are separated with
semicolons (";") or commas (","); semicolons take precedence.
There is currently no way to represent the author's organization,
address, or contact in a reStructuredText "Authors" field.

See `\<docinfo>`_ for a more complete example, including processing
context.


<block_quote>
=============

The <block_quote> element is used for quotations set off from the
main text (standalone).

:Category:   `Compound Body Elements`_
:Analogues:  <block_quote> is analogous to the <blockquote> element
             in both HTML and DocBook_.
:Processing: <block_quote> elements serve to set their contents off from the
             main text, typically with indentation and/or other decoration.
:Parents:    All elements employing the `%body.elements`_
             or `%structure.model`_ parameter entities in their
             content models may contain <block_quote>.
:Children:   <block_quote> elements contain `body elements`_
             followed by an optional `\<attribution>`_ element.
:Attributes: The <block_quote> element contains only the `common attributes`_.
:Parameter Entities: The `%body.elements`_ parameter entity
             directly includes <block_quote>.  The `%structure.model`_
             parameter entity indirectly includes <block_quote>.

Examples
--------

In reStructuredText, an indented text block without preceding markup
is a `block quote`_::

    As a great palaeontologist once said,

        This theory, that is mine, is mine.

        -- Anne Elk (Miss)

Pseudo-XML_ fragment from simple parsing::

    <paragraph>
        As a great palaeontologist once said,
    <block_quote>
        <paragraph>
            This theory, that is mine, is mine.
        <attribution>
            Anne Elk (Miss)



<bullet_list>
=============

The <bullet_list> element contains `\<list_item>`_ elements which are
uniformly marked with bullets.  Bullets are typically simple dingbats
(symbols) such as circles and squares.

:Category:   `Compound Body Elements`_
:Analogues:  <bullet_list> is analogous to the HTML<ul> element [#]_
             and to the DocBook_ <itemizedlist> element.
:Processing: Each list item should begin a new vertical block,
             prefaced by a bullet/dingbat.
:Parents:    All elements employing the `%body.elements`_ or
             `%structure.model`_ parameter entities in their content models
             may contain <bullet_list>.
:Children:   <bullet_list> elements contain one or more
             `\<list_item>`_ elements.
:Attributes: The <bullet_list> element contains the `common attributes`_
             plus bullet_.
:Parameter Entities: The `%body.elements`_ parameter entity directly includes
             <bullet_list>.  The `%structure.model`_ parameter entity
             indirectly includes <bullet_list>.

.. [#] HTML's <ul> is short for "unordered list", which we consider to be
   a misnomer. "Unordered" implies that the list items may be randomly
   rearranged without affecting the meaning of the list. Bullet lists
   *are* often ordered; the ordering is simply left implicit.


Examples
--------

A reStructuredText `bullet list`_::

    - Item 1, paragraph 1.

      Item 1, paragraph 2.

    - Item 2.

Pseudo-XML_ fragment from simple parsing::

    <bullet_list bullet="-">
        <list_item>
            <paragraph>
                Item 1, paragraph 1.
            <paragraph>
                Item 1, paragraph 2.
        <list_item>
            <paragraph>
                Item 2.

See `\<list_item>`_ for another example.


<caption>
=========

`To be completed`_.


<caution>
=========

The <caution> element is a specific *admonition*, a distinctive and
self-contained notice. See also the generic `\<admonition>`_ and the
other `specific admonition elements`_.

:Category:   `Compound Body Elements`_
:Analogues:  <caution> is analogous to the `DocBook \<caution>`_ element.
:Processing: Rendered distinctly (inset and/or in a box, etc.), with the
             generated title "Caution" (or similar).
:Parents:    All elements employing the `%body.elements`_ or
             `%structure.model`_ parameter entities in their
             content models may contain <caution>.
:Children:   <caution> elements contain one or more `body elements`_.
:Attributes: The <caution> element contains only the `common attributes`_.
:Parameter Entities: The `%body.elements`_ parameter entity
             directly includes <caution>. The `%structure.model`_
             parameter entity indirectly includes <caution>.

Examples
--------

A reStructuredText `"caution" directive`_::

    .. Caution:: Don't take any wooden nickels.

Pseudo-XML_ fragment from simple parsing::

    <caution>
        <paragraph>
            Don't take any wooden nickels.


<citation>
==========

`To be completed`_.


<citation_reference>
====================

`To be completed`_.


<classifier>
============

The <classifier> element contains the classification or type
of the `\<term>`_ being defined in a `\<definition_list>`_.
For example, it can be used to indicate the type of a variable.

:Category:   `Body Subelements`_ (simple)
:Analogues:  <classifier> has no direct analogues in common DTDs.
             It can be emulated with primitives or type effects.
:Processing: See `\<definition_list_item>`_.
:Parents:    Only the `\<definition_list_item>`_ element contains <classifier>.
:Children:   <classifier> elements may contain text data plus
             `inline elements`_ (`%text.model`_).
:Attributes: The <classifier> element contains only the `common attributes`_.

Examples
--------

A reStructuredText `definition list`_ with classifiers::

    name : string
        Customer name.
    i : int
        Temporary index variable.

Pseudo-XML_ fragment from simple parsing::

    <definition_list>
        <definition_list_item>
            <term>
                name
            <classifier>
                string
            <definition>
                <paragraph>
                    Customer name.
        <definition_list_item>
            <term>
                i
            <classifier>
                int
            <definition>
                <paragraph>
                    Temporary index variable.


<colspec>
=========

The <colspec> element contains specifications for a column in a `\<table>`_.

:Category:   `Body Subelements`_
:Analogues:  <colspec> is  defined in the `XML Exchange Table Model DTD`_.
             [#extblx]_  It is analogous to the DocBook_ <colspec> element.
             The HTML_ <col> element is related but has different semantics.
:Processing: See the `Exchange Table Model`_.
:Parents:    Only the `\<tgroup>`_ element contains <colspec>.
:Children:   The <colspec> element has no content.
:Attributes: <colspec> elements accept the colnum_, colname_,
             colwidth_, colsep_, rowsep_, align_, char_, and charoff_
             attributes.  However, of these only colwidth_ is used by
             Docutils -- currently with a different interpretation
             (see below).
             Via the `%tbl.colspec.att`_ parameter entity, <colspec>
             supports also the `common attributes`_ and `stub`_.

             .. attention::
                In contrast to the definition in the `Exchange Table Model`_,
                unitless values of the "colwidth" are interpreted as
                proportional values, not fixed values with unit "pt".

                .. The reference implementation `html4css2` converts
                   column widths values to percentages.

                Future versions of Docutils may use the standard form
                ``number*``, e.g., “5*” for 5 times the proportion.

Examples
--------

See `\<table>`_.


<comment>
=========

`To be completed`_.


<compound>
==========

The <compound> element combines multiple `body elements`_
to a single logical paragraph.

:Category:   `Body Elements`_

:Analogues:  The <compound> element has no direct analogues in common DTDs.
             In HTML, it can be emulated with <div> and CSS styling. [#]_

:Processing: Typically rendered as multiple distinct text blocks, with
             the possibility of variations to emphasize their logical
             unity (cf. the `"compound" directive`_).

:Parents:    All elements employing the `%body.elements`_
             or `%structure.model`_ parameter entities in
             their content models may contain <compound>.

:Children:   <compound> elements contain one or more `body elements`_.

:Attributes: The <compound> element contains only the `common attributes`_.

:Parameter Entities: The `%body.elements`_ parameter entity directly
             includes <compound>.  The `%structure.model`_
             parameter entity indirectly includes <compound>.


.. [#] The Docutils counterpart to HTML’s <div> is the `\<container>`_ element.

Examples
--------

The reStructuredText `"compound" directive`_ creates a
<compound> element::

    .. compound::

       The 'rm' command is very dangerous.  If you are logged
       in as root and enter ::

           cd /
           rm -rf *

       you will erase the entire contents of your file system.


Pseudo-XML_ fragment from simple parsing::

    <compound>
        <paragraph>
            The 'rm' command is very dangerous.  If you are logged
            in as root and enter
        <literal_block xml:space="preserve">
            cd /
            rm -rf *
        <paragraph>
            you will erase the entire contents of your file system.


<contact>
=========

The <contact> element holds contact information for the author
(individual or group) of the document, or a third-party contact.
It is typically used for an email or web address.

:Category:   `Bibliographic Elements`_
:Analogues:  <contact> is analogous to the DocBook_ <email> element.
             The HTML <address> element serves a similar purpose.
:Processing: See `\<docinfo>`_.
:Parents:    The following elements may contain <contact>:
             `\<docinfo>`_, `\<authors>`_.
:Children:   <contact> elements may contain text data
             plus `inline elements`_ (`%text.model`_).
:Attributes: The <contact> element contains only the `common attributes`_.
:Parameter Entities: The `%bibliographic.elements`_ parameter entity
             directly includes <contact>.

Examples
--------

In reStructuredText, "contact" is one of the registered
`bibliographic fields`_::

    Document Title
    ==============

    :Contact: jrh@example.com

Complete pseudo-XML_ result after parsing and applying transforms_::

    <document ids="document-title" names="document title">
        <title>
            Document Title
        <docinfo>
            <contact>
                <reference refuri="mailto:jrh@example.com">
                    jrh@example.com

See `\<docinfo>`_ for a more complete example, including processing
context.


<container>
===========

The <container> element groups multiple `body elements`_ for user- or
application-specific purposes.

:Category:   `Body Elements`_

:Analogues:  The <container> element is analogous to the HTML <div>
             element or the SVG <g> element.

:Processing: Can be used for styling or scripting purposes.
             An example is a frame or background colour) based
             on the value of the classes_ attribute.

:Parents:    All elements employing the `%body.elements`_
             or `%structure.model`_ parameter entities in
             their content models may contain <container>.

:Children:   <container> elements contain one or more `body elements`_.

:Attributes: The <container> element contains only the `common attributes`_.

:Parameter Entities:
             The `%body.elements`_ parameter entity directly
             includes <container>.  The `%structure.model`_
             parameter entity indirectly includes <container>.

Examples
--------

The reStructuredText `"container" directive`_ creates a
<container> element::

    .. container:: green boxed-equation

       .. math:: -1^2 = 1

       This paragraph is in the box, too.

Pseudo-XML_ fragment from simple parsing::

    <container classes="framed square">
        <math_block xml:space="preserve">
            -1^2 = 1
        <paragraph>
            This paragraph is in the box, too.

The HTML output can be placed in a common box with the custom CSS rule ::

    div.framed {border: solid;
             padding: 1em;}


<copyright>
===========

The <copyright> element contains the document's copyright statement.


:Category:   `Bibliographic Elements`_
:Analogues:  <copyright> is analogous to the DocBook_ <copyright> element.
:Processing: See `\<docinfo>`_.
:Parents:    Only the `\<docinfo>`_ element contains <copyright>.
:Children:   <copyright> elements may contain text data plus
             `inline elements`_ (`%text.model`_).
:Attributes: The <copyright> element contains only the `common attributes`_.
:Parameter Entities: The `%bibliographic.elements`_ parameter entity
             directly includes <copyright>.

Examples
--------

In reStructuredText, "copyright" is one of the registered
`bibliographic fields`_::

    Document Title
    ==============

    :Copyright: This document has been placed in the public domain.

Complete pseudo-XML_ result after parsing and applying transforms_::

    <document ids="document-title" names="document title">
        <title>
            Document Title
        <docinfo>
            <copyright>
                This document has been placed in the public domain.

See `\<docinfo>`_ for a more complete example,
including processing context.


<danger>
========

The <danger> element is a specific *admonition*, a distinctive and
self-contained notice.

:Category:   `Compound Body Elements`_
:Analogues:  <danger> has no direct analogues in common DTDs.
             It can be emulated with primitives and type effects.
:Processing: Rendered distinctly (inset and/or in a box, etc.),
             with the generated title "!DANGER!" (or similar).
:Parents:    All elements employing the `%body.elements`_
             or `%structure.model`_ parameter entities
             in their content models may contain <danger>.
:Children:   <danger> elements contain one or more `body elements`_.
:Attributes: The <danger> element contains only the `common attributes`_.
:Parameter Entities: The `%body.elements`_ parameter entity
             directly includes <danger>.  The `%structure.model`_
             parameter entity indirectly includes <danger>.

See also the generic `\<admonition>`_ and the other
`specific admonition elements`_.

Examples
--------

A reStructuredText `"danger" directive`_::

    .. DANGER:: Mad scientist at work!

Pseudo-XML_ fragment from simple parsing::

    <danger>
        <paragraph>
            Mad scientist at work!


<date>
======

The <date> element contains the date of publication, release, or
last modification of the document.

:Category:   `Bibliographic Elements`_
:Analogues:  <date> is analogous to the DocBook_ <date> element.
:Processing: Often used with the RCS/CVS keyword "Date".  See `\<docinfo>`_.
:Parents:    Only the `\<docinfo>`_ element contains <date>.
:Children:   <date> elements may contain text data plus `inline elements`_
             (`%text.model`_).
:Attributes: The <date> element contains only the `common attributes`_.
:Parameter Entities: The `%bibliographic.elements`_ parameter entity
             directly includes <date>.

Examples
--------

In reStructuredText, "date" is one of the registered
`bibliographic fields`_::

    Document Title
    ==============

    :Date: 2002-08-20

Complete pseudo-XML_ result after parsing and applying transforms_::

    <document ids="document-title" names="document title">
        <title>
            Document Title
        <docinfo>
            <date>
                2002-08-20

See `\<docinfo>`_ for a more complete example,
including processing context.


<decoration>
============

The <decoration> element is a container for `\<header>`_ and `\<footer>`_
elements and potential future extensions.  These elements are used for
notes, time/datestamp, processing information, etc.

:Category:   `Structural Subelements`_
:Analogues:  There are no direct analogies to <decoration> in HTML or
             in DocBook.
:Processing: See the individual `decorative elements`_.
:Parents:    Only the `\<document>`_ element contains <decoration>.
:Children:   <decoration> elements may contain the `decorative elements`_
             `\<header>`_ and/or `\<footer>`_.
             Although the content model doesn't specifically require
             contents, no empty <decoration> elements are ever created.
:Attributes: The <decoration> element contains only the `common attributes`_.

Examples
--------
See `\<header>`_ and `\<footer>`_.


<definition>
============

The <definition> element is a container for the body elements
used to define a `\<term>`_ in a `\<definition_list>`_.

:Category:   `Body Subelements`_ (compound)
:Analogues:  <definition> is analogous to the HTML <dd> element
             and to the DocBook_ <listitem> element
             (inside a <variablelistentry> element).
:Processing: See `\<definition_list_item>`_.
:Parents:    Only `\<definition_list_item>`_ elements contain <definition>.
:Children:   <definition> elements contain `body elements`_.
:Attributes: The <definition> element contains only the `common attributes`_.

Examples
--------
See the examples for the `\<definition_list>`_,
`\<definition_list_item>`_, and `\<classifier>`_ elements.


<definition_list>
=================

The <definition_list> element contains a list of terms and their
definitions.  It can be used for glossaries or dictionaries, to
describe or classify things, for dialogues, or to itemize subtopics.

:Category:   `Compound Body Elements`_
:Analogues:  <definition_list> is analogous to the HTML <dl> element
             and to the DocBook_ <variablelist> element.
:Processing: See `\<definition_list_item>`_.
:Parents:    All elements employing the `%body.elements`_
             or `%structure.model`_ parameter entities in their
             content models may contain <definition_list>.
:Children:   <definition_list> elements contain one or more
             `\<definition_list_item>`_ elements.
:Attributes: The <definition_list> element contains only the
             `common attributes`_.
:Parameter Entities: The `%body.elements`_ parameter entity
             directly includes <definition_list>. The `%structure.model`_
             parameter entity indirectly includes <definition_list>.

See also `\<field_list>`_.

Examples
--------

A reStructuredText `definition list`_. The classifier is optional. ::

    Term
        Definition.

    Term : classifier
        The ' : ' indicates a classifier in
        definition list item terms only.

Pseudo-XML_ fragment from simple parsing::

    <definition_list>
        <definition_list_item>
            <term>
                Term
            <definition>
                <paragraph>
                    Definition.
        <definition_list_item>
            <term>
                Term
            <classifier>
                classifier
            <definition>
                <paragraph>
                    The ' : ' indicates a classifier in
                    definition list item terms only.

See `\<definition_list_item>`_ and `\<classifier>`_ for further examples.


<definition_list_item>
======================

A wrapper for a set of terms (with optional classifiers) and the
associated definition in a `\<definition_list>`_.

:Category:   `Body Subelements`_ (compound)

:Analogues:  <definition_list_item> is analogous to the
             DocBook_ <variablelistentry> element.

:Processing: The optional `\<classifier>`_\ s can be rendered differently
             from the `\<term>`_.  They should be separated visually,
             typically by spaces plus a colon or dash.

:Parents:    Only the `\<definition_list>`_ element contains
             <definition_list_item>.

:Children:   <definition_list_item> elements each contain
             one or more `\<term>`_ elements,
             zero or more `\<classifier>`_ elements,
             and a `\<definition>`_::

               ((term, classifier*)+, definition)

             Changed in Docutils 0.22: allow multiple terms.

:Attributes: The <definition_list_item> element contains only the
             `common attributes`_.

Examples
--------

A complex reStructuredText_ `definition list`_::

    Tyrannosaurus Rex : carnivore
        Big and scary; the "Tyrant King".

    Brontosaurus : herbivore
      ..

        All brontosauruses are thin at one end,
        much much thicker in the middle
        and then thin again at the far end.

        -- Anne Elk (Miss)

Pseudo-XML_ fragment from simple parsing::

    <definition_list>
        <definition_list_item>
            <term>
                Tyrannosaurus Rex
            <classifier>
                carnivore
            <definition>
                <paragraph>
                    Big and scary; the "Tyrant King".
        <definition_list_item>
            <term>
                Brontosaurus
            <classifier>
                herbivore
            <definition>
                <comment xml:space="preserve">
                <block_quote>
                    <paragraph>
                        All brontosauruses are thin at one end,
                        much much thicker in the middle
                        and then thin again at the far end.
                    <attribution>
                        Anne Elk (Miss)

See `\<definition_list>`_ and `\<classifier>`_ for further examples.


<description>
=============

The <description> element is the part of an `\<option_list>`_ item that
contains the description of a command-line option or group of options.

:Category:   `Body Subelements`_
:Analogues:  <description> has no direct analogues in common DTDs.
:Processing: See `\<option_list>`_.
:Parents:    Only the `\<option_list_item>`_ element contains <description>.
:Children:   <description> elements may contain `body elements`_.
:Attributes: The <description> element contains only the `common attributes`_.

Examples
--------
See the examples for the `\<option_list>`_ element.


<docinfo>
=========

The <docinfo> element is a container for *displayed* document bibliographic
data, or meta-data (data about the document).  It corresponds to the
front matter of a book, such as the title page and copyright page.

:Category:   `Structural Subelements`_

:Analogues:  <docinfo> is analogous to DocBook_ <info> elements.
             There are no directly analogous HTML elements; the <meta>
             element carries some of the same information, albeit invisibly.

:Processing: The <docinfo> element may be rendered as a two-column table or
             in other styles.  It may even be invisible or omitted from the
             processed output.  Meta-data may be extracted from <docinfo>
             children; for example, HTML ``<meta>`` tags may be constructed.

             When Docutils_ transforms a reStructuredText_ `\<field_list>`_
             into a <docinfo> element (see the examples below), RCS/CVS
             keywords are normally stripped from simple (one paragraph)
             field bodies.  For complete details, please see `RCS Keywords`_
             in the `reStructuredText Markup Specification`_.

:Parents:    Only the `\<document>`_ element contains <docinfo>.

:Children:   <docinfo> elements contain `bibliographic elements`_.

:Attributes: The <docinfo> element contains only the `common attributes`_.

See also the `\<meta>`_ element (for hidden meta-data).


Examples
--------

`Bibliographic data`_ is represented in reStructuredText by a
`field list <rST field list_>`__ as the first visible element of a
`document <rST document_>`__ (after optional document title and subtitle).
The field list is transformed into a <docinfo> element and its children
by the `DocInfo transform`_. [#abstract-dedication]_

Source::

    Docinfo Example
    ===============

    :Author: J. Random Hacker
    :Contact: jrh@example.com
    :Date: 2002-08-18
    :Status: Work In Progress
    :Version: 1
    :Filename: $RCSfile$
    :Copyright: This document has been placed in the public domain.

Complete pseudo-XML_ result after parsing and applying transforms_::

    <document ids="docinfo-example" names="docinfo example">
        <title>
            Docinfo Example
        <docinfo>
            <author>
                J. Random Hacker
            <contact>
                <reference refuri="mailto:jrh@example.com">
                    jrh@example.com
            <date>
                2002-08-18
            <status>
                Work In Progress
            <version>
                1
            <field classes="filename">
                <field_name>
                    Filename
                <field_body>
                    <paragraph>
                        doctree.txt
            <copyright>
                This document has been placed in the public domain.

Note that "Filename" is a non-standard <docinfo> field, so becomes a
generic ``field`` element.  Also note that the "RCSfile" keyword
syntax has been stripped from the "Filename" data.

See `\<field_list>`_ for a `reStructuredText field list`_ example
in a non-bibliographic context.  Also see the individual examples
for the various `bibliographic elements`_.

.. [#abstract-dedication] Exceptions are the fields "abstract" and
   "dedication" that are transformed to `\<topic>`_ elements
   adjacent to the <docinfo>.


<doctest_block>
===============

The <doctest_block> element is a Python-specific variant of a
`\<literal_block>`_.

:Category:   `Simple Body Elements`_
:Analogues:  <doctest_block> is analogous to the HTML <pre> element
             and to the DocBook_ <programlisting> and <screen> elements.
:Processing: As with `\<literal_block>`_, <doctest_block> elements are
             typically rendered in a monospaced typeface.  It is crucial
             that all whitespace and line breaks are preserved in the
             rendered form.
:Parents:    All elements employing the `%body.elements`_ or
             `%structure.model`_ parameter entities in their content models
             may contain <doctest_block>.
:Children:   <doctest_block> elements may contain text data
             plus `inline elements`_ (`%text.model`_):
:Attributes: The <doctest_block> element contains the `common attributes`_
             plus `xml:space`_.
:Parameter Entities: The `%body.elements`_ parameter entity
             directly includes <doctest_block>.  The `%structure.model`_
             parameter entity indirectly includes <doctest_block>.

<doctest_block> elements are used for interactive Python interpreter
sessions, which are distinguished by their input prompt: ``>>>``.
They are meant to illustrate usage by example, and provide an elegant
and powerful testing environment via the `doctest module`_ in the
Python standard library.

.. _doctest module: https://docs.python.org/3/library/doctest.html

Examples
--------

A reStructuredText `doctest block`_::

    This is an ordinary paragraph.

    >>> print('this is a Doctest block')
    this is a Doctest block

Pseudo-XML_ fragment from simple parsing::

    <paragraph>
        This is an ordinary paragraph.
    <doctest_block xml:space="preserve">
        >>> print('this is a Doctest block')
        this is a Doctest block


<document>
==========

The <document> element is the root (topmost) element of the Docutils
document tree.

:Category:   `Root Element`_

:Analogues:  <document> is analogous to the HTML <html> element and to
             several DocBook_ elements such as <book>.

:Parents:    The <document> element has no parents.

:Children:   <document> elements may contain `structural elements`_,
             `structural subelements`_, and `body elements`_

             .. parsed-literal::

               ( (title, subtitle?)?,
                 meta*,
                 decoration?,
                 (docinfo, transition?)?,
                 `%structure.model`_; )

             See the `%structure.model`_ parameter entity for details of
             the body of a <document>.

:Attributes: The <document> element contains the `common attributes`_
             plus an optional title_ attribute which stores the document
             title metadata.

<document> is the direct or indirect ancestor of every other element in
the tree.  It encloses the entire document tree.  It is the starting
point for a document.


Depending on the source of the data and the stage of processing,
the <document> may not initially contain a `\<title>`_.
A document title is not directly representable in reStructuredText_.
Instead, the `DocTitle transform`_ may promote a lone top-level section
title to become the document `\<title>`_, and similarly a lone
second-level (sub)section's title to become the document `\<subtitle>`_.

The contents of "`\<decoration>`_" may be specified in a document,
constructed programmatically, or both.

The "`\<docinfo>`_" may be transformed from an initial `\<field_list>`_.


Examples
--------

A minimal reStructuredText_ document with title::

    A Title
    =======

    A paragraph.

Complete pseudo-XML_ result from simple parsing::

    <document>
        <section ids="a-title" names="a title">
            <title>
                A Title
            <paragraph>
                A paragraph.

After applying transforms_, the section title is promoted to become the
document title::

    <document ids="a-title" names="a title">
        <title>
            A Title
        <paragraph>
            A paragraph.


<emphasis>
==========

The <emphasis> element is an inline element representing
text that has *stress emphasis*.

:Category:   `Inline Elements`_
:Analogues:  <emphasis> is analogous to the HTML_ <em> element
             and the DocBook_ <emphasis> element.
:Processing: Typically displayed in italic type.
:Parents:    All elements employing the `%text.model`_ parameter
             entity in their content models may contain <emphasis>.
:Children:   <emphasis> elements may contain text data
             plus `inline elements`_ (`%text.model`_).
:Attributes: The <emphasis> element contains only the `common attributes`_.

Examples
--------

The reStructuredText there are two `emphasis markup`_ alternatives::

    There are :emphasis:`two` ways to *emphasize* text.

Pseudo-XML_ fragment from simple parsing::

    <paragraph>
        There are
        <emphasis>
            two
         ways to
        <emphasis>
            emphasize
         text.


<entry>
=======

The <entry> element represents one cell of a `\<table>`_.

:Category:   `Body Subelements`_
:Analogues:  <entry> is defined in the `XML Exchange Table Model DTD`_.
             [#extblx]_  It is analogous to the DocBook_ <entry> element.
             HTML_ differentiates between header entries <td>
             and data entries <td>.
:Processing: Render content in a table cell.  The morecols_ and morerows_
             attributes may be used to define an entry spanning several
             table cells.  See the `Exchange Table Model`_ for details.
:Parents:    The `\<thead>`_ and `\<tbody>`_ elements contain <entry> elements.
:Children:   <entry> elements may contain `body elements`_
             (via the `%tbl.entry.mdl`_ parameter entity).
:Attributes: The <entry> element accepts the colname_, namest_,
             nameend_, morerows_, colsep_, rowsep_, align_, char_,
             charoff_, and valign_ attributes (ignored by Docutils) and
             (via the `%tbl.entry.att`_ parameter entity)
             the `common attributes`_ and morecols_.

Examples
--------

See `\<table>`_.


<enumerated_list>
=================

The <enumerated_list> element contains `\<list_item>`_ elements which are
uniformly marked with enumerator labels.

:Category:   `Compound Body Elements`_

:Analogues:  <enumerated_list> is analogous to the HTML <ol> element
             and to the DocBook_ <orderedlist> element.

:Processing: Each list item should begin a new vertical block, prefaced
             by a enumeration marker (such as "1.").

:Parents:    All elements employing the `%body.elements`_ or
             `%structure.model`_ parameter entities in their content models
             may contain <enumerated_list>.

:Children:   <enumerated_list> elements contain one or more
             `\<list_item>`_ elements.

:Attributes: The <enumerated_list> element contains the `common attributes`_
             plus enumtype_, prefix_, suffix_, and start_.

:Parameter Entities:
             The `%body.elements`_ parameter entity directly includes
             <enumerated_list>.  The `%structure.model`_ parameter entity
             indirectly includes <enumerated_list>.

Examples
--------

A reStructuredText `enumerated list`_::

    1. Item 1.

       (A) Item A.
       (B) Item B.
       (C) Item C.

    2. Item 2.

Pseudo-XML_ fragment from simple parsing::

    <enumerated_list enumtype="arabic" prefix="" suffix=".">
        <list_item>
            <paragraph>
                Item 1.
            <enumerated_list enumtype="upperalpha" prefix="(" suffix=")">
                <list_item>
                    <paragraph>
                        Item A.
                <list_item>
                    <paragraph>
                        Item B.
                <list_item>
                    <paragraph>
                        Item C.
        <list_item>
            <paragraph>
                Item 2.

See `\<list_item>`_ for another example.


<error>
=======

The <error> element is a specific *admonition*, a distinctive and
self-contained notice.

:Category:   `Compound Body Elements`_
:Analogues:  <error> has no direct analogues in common DTDs.
             It can be emulated with primitives and type effects.
:Processing: Rendered distinctly (inset and/or in a box, etc.),
             with the generated title "Error" (or similar).
:Parents:    All elements employing the `%body.elements`_ or
             `%structure.model`_ parameter entities in their content models
             may contain <error>.
:Children:   <error> elements contain one or more `body elements`_.
:Attributes: The <error> element contains only the `common attributes`_.
:Parameter Entities: The `%body.elements`_ parameter entity directly includes
             <error>.  The `%structure.model`_ parameter entity indirectly
             includes <error>.

See also the generic `\<admonition>`_ and the other `specific admonition
elements`_.

Examples
--------

A reStructuredText `"error" directive`_::

    .. Error:: Does not compute.

Pseudo-XML_ fragment from simple parsing::

    <error>
        <paragraph>
            Does not compute.


<field>
=======

The <field> element contains one item of a `\<field_list>`_,
a pair of `\<field_name>`_ and `\<field_body>`_ elements.

:Category:   `Body Subelements`_
:Analogues:  <field> has no direct analogues in common DTDs.
             HTML5 uses <div> elements inside <dl> lists for
             grouping <dt>/<dd> pairs.
:Processing: See `\<field_list>`_.
:Parents:    The following elements may contain <field>:
             `\<docinfo>`_, `\<field_list>`_
:Children:   Each <field> element contains one `\<field_name>`_ and one
             `\<field_body>`_ element.
:Attributes: The <field> element contains only the `common attributes`_.
:Parameter Entities: The `%bibliographic.elements`_ parameter entity
             directly includes <field>.

Examples
--------
See the examples for the `\<field_list>`_ and `\<docinfo>`_ elements.


<field_body>
============

The <field_body> element is analogous to a database field's data.

:Category:   `Body Subelements`_
:Analogues:  <field_body> is analogous to the HTML <dd> element.
:Processing: See `\<field_list>`_.
:Parents:    Only the `\<field>`_ element contains <field_body>.
:Children:   <field_body> elements may contain `body elements`_.
:Attributes: The <field_body> element contains only the `common attributes`_.

Examples
--------
See the examples for the `\<field_list>`_ and `\<docinfo>`_ elements.


<field_list>
============

The <field_list> element contains two-column table-like structures
resembling database records (label & data pairs).

:Category:   `Compound Body Elements`_
:Analogues:  <field_list> is analogue to the HTML <dl> element.
:Processing: A <field_list> is typically rendered as a two-column list,
             where the first column contains "labels" (usually with a
             colon suffix). However, field lists are often used for
             extension syntax or special processing.  Such structures do
             not survive as field lists to be rendered.
:Parents:    All elements employing the `%body.elements`_ or
             `%structure.model`_ parameter entities in their
             content models may contain <field_list>.
:Children:   <field_list> elements contain one or more `\<field>`_ elements.
:Attributes: The <field_list> element contains only the `common attributes`_.
:Parameter Entities: The `%body.elements`_ parameter entity
             directly includes <field_list>.  The `%structure.model`_
             parameter entity indirectly includes <field_list>.

Field lists are often meant for further processing.
In reStructuredText_, field lists are used to represent bibliographic
fields (contents of the `\<docinfo>`_ element) and `directive`_ options.


Examples
--------

A reStructuredText `field list <rST field list_>`__::

    :Author: Me
    :Version: 1
    :Date: 2001-08-11
    :Parameter i: integer

Pseudo-XML_ fragment from simple parsing::

    <field_list>
        <field>
            <field_name>
                Author
            <field_body>
                <paragraph>
                    Me
        <field>
            <field_name>
                Version
            <field_body>
                <paragraph>
                    1
        <field>
            <field_name>
                Date
            <field_body>
                <paragraph>
                    2001-08-11
        <field>
            <field_name>
                Parameter i
            <field_body>
                <paragraph>
                    integer


<field_name>
============

The <field_name> element is analogous to a database field's name.

:Category:   `Body Subelements`_ (simple)
:Analogues:  <field_name> is analogous to the HTML <dt> element.
:Processing: See `\<field_list>`_.
:Parents:    Only the `\<field>`_ element contains <field_name>.
:Children:   <field_name> elements may contain text data
             plus `inline elements`_ (`%text.model`_).
:Attributes: The <field_name> element contains only the `common attributes`_.

Examples
--------
See the examples for the `\<field_list>`_ and `\<docinfo>`_ elements.


<figure>
========

`To be completed`_.


<footer>
========

The <footer> element is a container element whose contents are meant
to appear at the bottom of a web page, or repeated at the bottom of
every printed page.

:Category:   `Decorative Elements`_
:Analogues:  <footer> is analogous to the HTML5 <footer> element. There
             are no direct analogies to <footer> in HTML4 or DocBook.
             Equivalents are typically constructed from primitives and/or
             generated by the processing system.
:Parents:    Only the `\<decoration>`_ element contains <footer>.
:Children:   <footer> elements may contain `body elements`_.
:Attributes: The <footer> element contains only the `common attributes`_.

The <footer> element may contain processing information (datestamp, a
link to Docutils_, etc.) as well as custom content.


Examples
--------

A document may get a <footer> decoration even without use of the
reStructuredText `"footer" directive`_::

    A paragraph.

Complete pseudo-XML_ result after parsing and applying transforms_,
assuming that the datestamp_ command-line option or configuration
setting has been supplied::

    <document>
        <decoration>
            <footer>
                <paragraph>
                    Generated on: 2002-08-20.
        <paragraph>
            A paragraph.


<footnote>
==========

The <footnote> element is used for labelled notes_ that provide
additional context to a passage of text (*footnotes* or *endnotes*).
The corresponding footnote mark in running text is set by the
`\<footnote_reference>`_ element.

.. _notes: https://en.wikipedia.org/wiki/Note_(typography)

:Category:   `Compound Body Elements`_

:Analogues:  <footnote> has no direct analogues in DocBook or HTML.

             The `DocBook \<footnote>`_ element combines features of
             <footnote> and `\<footnote_reference>`_.

             The DPub ARIA role `"doc-footnote"`__ may be used to mark a
             (conforming__) `HTML emulation`__ as "ancillary information,
             such as a citation or commentary, that provides additional
             context to a referenced passage of text".

             For collections of notes that occur at the end of a section,
             the DPub ARIA role `"doc-endnotes"`__ is more appropriate.

             The corresponding types in the `EPUB 3 Structural Semantics
             Vocabulary`__ are "footnote" and "endnote".

             __ https://www.w3.org/TR/dpub-aria-1.0/#doc-footnote
             __ https://www.w3.org/TR/html-aria/#docconformance
             __ https://www.w3.org/TR/html51/
                common-idioms-without-dedicated-elements.html#footnotes
             __ https://www.w3.org/TR/dpub-aria-1.0/#doc-endnotes
             __ https://www.w3.org/TR/epub-ssv-11/#notes

:Processing: A <footnote> element should be set off from the rest of the
             document, e.g. with a border or using a smaller font size.

             Footnotes may "float" to the bottom or margin of a page or a
             dedicated section.

:Parents:    All elements employing the `%body.elements`_ or
             `%structure.model`_ parameter entities in their content models
             may contain <footnote>.

:Children:   <footnote> elements begin with an optional [#]_ `\<label>`_
             and contain `body elements`_. ::

                 (label?, (%body.elements;)+)

:Attributes: The <footnote> element contains the `common attributes`_
             plus auto_ and backrefs_.

:Parameter Entities: The `%body.elements`_ parameter entity
             directly includes <footnote>.  The `%structure.model`_
             parameter entity indirectly includes <footnote>.

.. [#] The footnote label will become mandatory in Docutils 1.0.

Examples
--------

reStructuredText uses `explicit markup blocks`_ for `footnotes`_::

    .. [1] This is a footnote.

Pseudo-XML_ fragment from simple parsing::

    <footnote ids="id1" names="1">
        <label>
            1
        <paragraph>
            This is a footnote.


<footnote_reference>
====================

The <footnote_reference> element is an inline element representing a
cross reference to a `\<footnote>`_ (a footnote mark).

:Category:   `Inline Elements`_
:Analogues:  The <footnote_reference> element resembles
             the `DocBook \<footnoteref>`_ element or
             the  LaTeX ``\footnotemark`` command.
             There is no equivalent in HTML. The <a> element can be used
             to provide a link to the corresponding footnote.
:Processing: A <footnote_reference> should generate a mark matching the
             `\<label>`_ of the referenced footnote. The mark is
             typically formatted as superscript or enclosed in square
             brackets.
:Parents:    All elements employing the `%text.model`_ parameter entity
             in their content models may contain <footnote-reference>.
:Children:   <footnote_reference> elements contain text data only.
:Attributes: The <footnote_reference> element contains the
             `common attributes`_ plus auto_, refid_, and refname_.

Examples
--------

A reStructuredText `footnote reference`_ and footnote_::

    [#]_ is an auto-numbered footnote reference.

    .. [#] Auto-numbered footnote 1.

Pseudo-XML_ fragment from simple parsing::

    <paragraph>
        <footnote_reference auto="1" ids="id1">
         is an auto-numbered footnote reference.
    <footnote auto="1" ids="id3">
        <paragraph>
            Auto-numbered footnote 1.

The ``references.Footnotes`` Docutils transform_ resolves this to::

    <paragraph>
        <footnote_reference auto="1" ids="id1" refid="id2">
            1
         is an auto-numbered footnote reference.
    <footnote auto="1" backrefs="id1" ids="id2" names="1">
        <label>
            1
        <paragraph>
            Auto-numbered footnote 1.


<generated>
===========

Docutils wraps <generated> elements around text that is inserted
(generated) by Docutils; i.e., text that was not in the document,
like section numbers inserted by the "sectnum" directive.

`To be completed`_.


<header>
========

The <header> element is a container element whose contents are meant
to appear at the top of a web page, or at the top of every printed
page.

:Category:   `Decorative Elements`_
:Analogues:  <header> is analogous to the HTML5 <header> element.
             There are no direct analogies to <header> in HTML4 or DocBook.
             Equivalents are typically constructed from primitives and/or
             generated by the processing system.
:Parents:    Only the `\<decoration>`_ element contains <header>.
:Children:   <header> elements may contain `body elements`_.
:Attributes: The <header> element contains only the `common attributes`_.

Examples
--------

A reStructuredText `"header" directive`_::

    .. header:: This space for rent.

Pseudo-XML_ fragment from simple parsing::

    <document>
        <decoration>
            <header>
                <paragraph>
                    This space for rent.


<hint>
======

The <hint> element is a specific *admonition*, a distinctive and
self-contained notice.

:Category:   `Compound Body Elements`_
:Analogues:  <hint> has no direct analogues in common DTDs.
             It can be emulated with primitives and type effects.
:Processing: Rendered distinctly (inset and/or in a box, etc.),
             with the generated title "Hint" (or similar).
:Parents:    All elements employing the `%body.elements`_ or
             `%structure.model`_ parameter entities in their
             content models may contain <hint>.
:Children:   <hint> elements contain one or more `body elements`_.
:Attributes: The <hint> element contains only the `common attributes`_.
:Parameter Entities: The `%body.elements`_ parameter entity
             directly includes <hint>.  The `%structure.model`_
             parameter entity indirectly includes <hint>.

See also the generic `\<admonition>`_ and the other
`specific admonition elements`_.

Examples
--------

A reStructuredText `"hint" directive`_::

    .. Hint:: It's bigger than a bread box.

Pseudo-XML_ fragment from simple parsing::

    <hint>
        <paragraph>
            It's bigger than a bread box.


<image>
=======

The <image> element refers to an image resource that should be included
in the document.

:Categories: `Body Elements`_, `Inline Elements`_
:Analogues:  <image> is analogous to the `HTML \<img>`_,
             `DocBook \<imagedata>`_, and `SVG \<image>`_ elements.
:Processing: The specified image is included into the output document.
             Depending on the output format, this is done by referring to
             the image URI or by embedding the image data.
:Parents:    All elements employing the `%body.elements`_,
             `%text.model`_, or `%structure.model`_ parameter entities
             in their content models may contain <image>.
:Children:   The <image> element has no content.
:Attributes: The <image> element contains the `common attributes`_ plus
             uri_, alt_, align_, height_, width_, scale_, and loading_.
:Parameter Entities:
             The `%body.elements`_ and `%inline.elements`_ parameter
             entities directly include <image>.  The `%structure.model`_
             and `%text.model`_ parameter entities indirectly include <image>.

It is up to the author to ensure compatibility of the image data format
with the output format or user agent (LaTeX engine, HTML browser, ...).
The `reStructuredText Directives` documentation contains a non exhaustive
`table of compatible image formats`_.

Examples
--------

A reStructuredText `"image" directive`_::

    .. image:: picture.jpeg
       :width: 20 mm
       :alt: alternate text

Pseudo-XML_ fragment from simple parsing::

    <image alt="alternate text" uri="picture.jpeg" width="20mm">

.. _HTML <img>: https://html.spec.whatwg.org/multipage/embedded-content.html
                #the-img-element
.. _SVG <image>: https://svgwg.org/svg2-draft/embedded.html#ImageElement


<important>
===========

The <important> element is a specific *admonition*, a distinctive and
self-contained notice.

:Category:   `Compound Body Elements`_
:Analogues:  <important> is analogous to the `DocBook \<important>`_ element.
:Processing: Rendered distinctly (inset and/or in a box, etc.),
             with the generated title "Important" (or similar).
:Parents:    All elements employing the `%body.elements`_ or
             `%structure.model`_ parameter entities in their
             content models may contain <important>.
:Children:   <important> elements contain one or more `body elements`_.
:Attributes: The <important> element contains only the `common attributes`_.
:Parameter Entities: The `%body.elements`_ parameter entity
             directly includes <important>.  The `%structure.model`_
             parameter entity indirectly includes <important>.

See also the generic `\<admonition>`_ and the other
`specific admonition elements`_.

Examples
--------

A reStructuredText `"important" directive`_::

    .. Important::

       * Wash behind your ears.
       * Clean up your room.
       * Back up your data.

Pseudo-XML_ fragment from simple parsing::

    <important>
        <bullet_list>
            <list_item>
                <paragraph>
                    Wash behind your ears.
            <list_item>
                <paragraph>
                    Clean up your room.
            <list_item>
                <paragraph>
                    Back up your data.


<inline>
========

The <inline> element is a generic inline container.

:Category:   `Inline Elements`_
:Analogues:  <inline> is analogous to the HTML <span> element.
:Processing: Writers_ typically pass the classes_ attribute to the output
             document and leave styling to the backend or a custom
             stylesheet_. They may also process the classes_ attribute
             and convert the <inline> element to a specific element or
             render the content distinctly for specific class values.
             Moreover, writers may ignore the element and just render
             the content.
:Parents:    All elements employing the `%text.model`_ parameter
             entity in their content models may contain <inline>.
:Children:   <inline> elements may contain text data
             plus `inline elements`_ (`%text.model`_).
:Attributes: The <inline> element contains only the `common attributes`_.

Examples
--------

`Custom interpreted text roles`_ create <inline> elements
(unless they are based on a `standard role`_).

This reStructuredText source fragment creates and uses a custom role::

    .. role:: custom

    An example of using :custom:`interpreted text`

Pseudo-XML_ fragment from simple parsing::

    <paragraph>
        An example of using
        <inline classes="custom">
            interpreted text


<label>
=======

`To be completed`_.


<legend>
========

`To be completed`_.


<line>
======

The <line> element contains a single line of text,
part of a `\<line_block>`_.

:Category:   `Body Subelements`_ (simple)
:Analogues:  <line> has no direct analogues in common DTDs.
             It can be emulated with primitives or type effects.
:Processing: See `\<line_block>`_.
:Parents:    Only the `\<line_block>`_ element contains <line>.
:Children:   <line> elements may contain text data plus `inline elements`_.
:Attributes: The <line> element contains only the `common attributes`_.

Examples
--------
See `\<line_block>`_.


<line_block>
============

The <line_block> element contains a sequence of lines and nested line
blocks.

:Category:   `Compound Body Elements`_

:Analogues:  <line_block> is analogous to the DocBook_ <literallayout>
             element and to the HTML <pre> element (with modifications to
             typeface styles).

:Processing: Line breaks (implied between elements) and leading whitespace
             (indicated by nesting) is significant and must be preserved.
             Unlike <literal_block>, <line_block> elements are
             typically rendered in an ordinary text typeface.

:Parents:    All elements employing the `%body.elements`_ or
             `%structure.model`_ parameter entities in their content models
             may contain <line_block>.

:Children:   <line_block> elements may contain `\<line>`_ elements and
             nested <line_block> elements. ::

               (line | line_block)+

:Attributes: The <line_block> element contains only the `common attributes`_.

:Parameter Entities: The `%body.elements`_ parameter entity
             directly includes <line_block>.  The `%structure.model`_
             parameter entity indirectly includes <line_block>.

<line_block> elements are commonly used for verse and addresses.
See `\<literal_block>`_ for an alternative useful for
program listings and interactive computer sessions.

Examples
--------

A reStructuredText `line block`_::

    Take it away, Eric the Orchestra Leader!

    | A one, two, a one two three four
    |
    | Half a bee, philosophically,
    |     must, *ipso facto*, half not be.
    | But half the bee has got to be,
    |     *vis a vis* its entity.  D'you see?
    |
    | But can a bee be said to be
    |     or not to be an entire bee,
    |         when half the bee is not a bee,
    |             due to some ancient injury?
    |
    | Singing...

Pseudo-XML_ fragment from simple parsing::

    <paragraph>
        Take it away, Eric the Orchestra Leader!
    <line_block>
        <line>
            A one, two, a one two three four
        <line>
        <line>
            Half a bee, philosophically,
        <line_block>
            <line>
                must,
                <emphasis>
                    ipso facto
                , half not be.
        <line>
            But half the bee has got to be,
        <line_block>
            <line>
                <emphasis>
                    vis a vis
                 its entity.  D'you see?
            <line>
        <line>
            But can a bee be said to be
        <line_block>
            <line>
                or not to be an entire bee,
            <line_block>
                <line>
                    when half the bee is not a bee,
                <line_block>
                    <line>
                        due to some ancient injury?
                    <line>
        <line>
            Singing...


<list_item>
===========

The <list_item> element is a container for the elements of a list
item.

:Category:   `Body Subelements`_ (compound)
:Analogues:  <list_item> is analogous to the HTML <li> element
             and to the DocBook_ <listitem> element.
:Processing: See `\<bullet_list>`_ or `\<enumerated_list>`_.
:Parents:    The `\<bullet_list>`_ and `\<enumerated_list>`_ elements
             contain <list_item>.
:Children:   <list_item> elements may contain `body elements`_.
:Attributes: The <list_item> element contains only the `common attributes`_.

Examples
--------

A reStructuredText `enumerated list`_ with a nested `bullet list`_::

    1. Outer list, item 1.

       * Inner list, item 1.
       * Inner list, item 2.

    2. Outer list, item 2.

Pseudo-XML_ fragment from simple parsing::

    <enumerated_list enumtype="arabic" prefix="" suffix=".">
        <list_item>
            <paragraph>
                Outer list, item 1.
            <bullet_list bullet="*">
                <list_item>
                    <paragraph>
                        Inner list, item 1.
                <list_item>
                    <paragraph>
                        Inner list, item 2.
        <list_item>
            <paragraph>
                Outer list, item 2.

See `\<bullet_list>`_ or `\<enumerated_list>`_ for further examples.


<literal>
=========

`To be completed`_.


<literal_block>
===============

The <literal_block> element contains a block of text where line
breaks and whitespace are significant and must be preserved.

Details
-------

:Category:   `Simple Body Elements`_
:Analogues:  <literal_block> is analogous to the HTML <pre> element
             and to the DocBook_ <programlisting> and <screen> elements.
:Processing: <literal_block> elements are typically rendered in a
             monospaced typeface.  It is crucial that all whitespace and
             line breaks are preserved in the rendered form.
:Parents:    All elements employing the `%body.elements`_ or
             `%structure.model`_ parameter entities in their content models
             may contain <literal_block>.
:Children:   <literal_block> elements may contain text data
             plus `inline elements`_ (`%text.model`_).
:Attributes: The <literal_block> element contains the `common attributes`_
             plus `xml:space`_.
:Parameter Entities: The `%body.elements`_ parameter entity
             directly includes <literal_block>.  The `%structure.model`_
             parameter entity indirectly includes <literal_block>.

<literal_block> elements are commonly used for program listings and
interactive computer sessions.
See `\<line_block>`_ for an alternative useful for verse and addresses.

Examples
--------

A reStructuredText `"parsed-literal" directive`_::

    .. parsed-literal::

        if parsed_literal:
            text = 'is parsed for reStructuredText_ markup'
            spaces_and_linebreaks = 'are preserved'
            markup_processing = **True**

Pseudo-XML_ fragment from simple parsing::

    <literal_block xml:space="preserve">
        if parsed_literal:
            text = 'is parsed for
        <reference name="reStructuredText" refid="restructuredtext">
            reStructuredText
         markup'
            spaces_and_linebreaks = 'are preserved'
            markup_processing =
        <strong>
            True

<literal-block> elements are also generated by a `literal block`_ and
the `"code" directive`_.


<math>
======

The <math> element contains text in `LaTeX math format` [#latex-math]_
that is typeset as mathematical notation (inline formula).

:Category:   `Inline Elements`_
:Analogues:  <math> is analogous to a HTML/MathML <math> element or
             the LaTeX (``$ math $``) mode.
:Processing: Rendered as mathematical notation.
             If the output format does not support math typesetting,
             the content may be inserted verbatim.
:Parents:    All elements employing the `%text.model`_
             parameter entitiy in their content models may contain <math>.
:Children:   <math> elements contain text data only.
:Attributes: The <math> element contains only the `common attributes`_.

Example
-------

reStructuredText source::

    Euler's identity is the equality :math:`e^{i\pi + 1 = 0`.

Pseudo-XML_ fragment from simple parsing::

    <paragraph>
        Euler’s identity is the equality
        <math>
            e^{\mathrm{i}\pi + 1 = 0
        .

.. [#latex-math] For details of the supported mathematical language, see
   the `"math" directive`_


<math_block>
============

The <math_block> element contains a block of text in `LaTeX math format`
[#latex-math]_ that is typeset as mathematical notation (display formula).

:Category:   `Simple Body Elements`_
:Analogues:  <math_block> is analogous to a HTML/MathML <math> element
             displayed as block-level element or a LaTeX ``equation*``
             environment.
:Processing: Rendered in a block as mathematical notation, typically
             centered or with indentation
             If the output format does not support math typesetting,
             the content may be inserted verbatim.
:Parents:    All elements employing the `%body.elements`_ or
             `%structure.model`_ parameter entities in their content models
             may contain <math_block>.
:Children:   <math_block> elements contain text data only.
:Attributes: The <math_block> element contains the `common attributes`_
             plus `xml:space`_.

Example
-------

The reStructuredText `"math" directive`_ generates a <math_block> element::

    Euler's identity is the equality

    .. math:: e^{i\pi + 1 = 0

Pseudo-XML_ fragment from simple parsing::

    <paragraph>
        Euler’s identity is the equality
    <math_block xml:space="preserve">
        e^{i\pi + 1 = 0


<meta>
======

The <meta> element is a container for "hidden" document
bibliographic data, or meta-data (data about the document).

:Category:   `Structural Subelements`_

:Analogues:  <meta> is analogous to the `HTML <meta> element`_
             or the file properties in ODT or PDF documents.

:Processing: The <meta> element is stored as metadata if the export
             format supports this. It is typically invisible and may be
             omitted from the processed output.

             Meta-data may also be extracted from `\<docinfo>`_ children
             or the `\<document>`_ attributes (title).

:Parents:    Only the `\<document>`_ element contains <meta>.
:Children:   The <meta> element has no content.
:Attributes: The <meta> element contains the attributes
             *content*, *dir*, *http-equiv*, *lang*, *media*, *name*, and
             *scheme* that correspond to the respective attributes of the
             `HTML <meta> element`_.

See also the `\<docinfo>`_ element for displayed meta-data.
The document's `title attribute`_ stores the metadata document title.

Example
-------

A reStructuredText `"meta" directive`_::

    .. meta::
       :description lang=en: An amusing story
       :description lang=fr: Un histoire amusant

Pseudo-XML_ fragment from simple parsing::

    <meta content="An amusing story" lang="en" name="description">
    <meta content="Un histoire amusant" lang="fr" name="description">

.. _HTML <meta> element:
    https://html.spec.whatwg.org/multipage/semantics.html#the-meta-element


<note>
======

The <note> element is a specific *admonition*, a distinctive and
self-contained notice.

:Category:   `Compound Body Elements`_
:Analogues:  <note> is analogous to the `DocBook \<note>`_ element.
:Processing: Rendered distinctly (inset and/or in a box, etc.),
             with the generated title "Note" (or similar).
:Parents:    All elements employing the `%body.elements`_ or
             `%structure.model`_ parameter entities in their content models
             may contain <note>.
:Children:   <note> elements contain one or more `body elements`_.
:Attributes: The <note> element contains only the `common attributes`_.
:Parameter Entities: The `%body.elements`_ parameter entity
             directly includes <note>.  The `%structure.model`_
             parameter entity indirectly includes <note>.

See also the generic `\<admonition>`_ and the other
`specific admonition elements`_.

Examples
--------

A reStructuredText `"note" directive`_::

    .. Note:: Admonitions can be handy to break up a
       long boring technical document.

Pseudo-XML_ fragment from simple parsing::

    <note>
        <paragraph>
            Admonitions can be handy to break up a
            long boring technical document.


<option>
========

The <option> element groups an option string together with zero or
more option argument placeholders.

:Category:   `Body Subelements`_
:Analogues:  <option> has no direct analogues in common DTDs.
:Processing: See `\<option_list>`_.
:Parents:    Only the `\<option_group>`_ element contains <option>.
:Children:   <option> elements start with an `\<option_string>`_ and
             may contain `\<option_argument>`_ elements::

                 (option_string, option_argument*)

:Attributes: The <option> element contains only the `common attributes`_.

Note that reStructuredText_ currently supports only one argument per
option.

Examples
--------
See the examples for the `\<option_list>`_ element.


<option_argument>
=================

The <option_argument> element contains placeholder text for option
arguments.

:Category:   `Body Subelements`_
:Analogues:  <option_argument> has no direct analogues in common DTDs.
:Processing: The value of the "delimiter" attribute is prefixed to the
             <option_argument>, separating it from its
             `\<option_string>`_ or a preceding <option_argument>.
             The <option_argument> text is typically rendered in a
             monospaced typeface, possibly italicized or otherwise
             altered to indicate its placeholder nature.
:Parents:    Only the `\<option>`_ element contains <option_argument>.
:Children:   <option_argument> elements contain text data only.
:Attributes: The <option_argument> element contains
             the `common attributes`_ plus delimiter_.

Examples
--------
See the examples for the `\<option_list>`_ element.


<option_group>
==============

The <option_group> element groups together one or more `\<option>`_
elements, all synonyms.

:Category:   `Body Subelements`_
:Analogues:  <option_group> has no direct analogues in common DTDs.
:Processing: Typically `\<option>`_ elements within an <option_group> are
             joined together in a comma-separated list.
:Parents:    Only the `\<option_list_item>`_ element contains <option_group>.
:Children:   <option_group> elements contain one or more `\<option>`_
             elements.
:Attributes: The <option_group> element contains only the `common attributes`_.

Examples
--------
See the examples for the `\<option_list>`_ element.


<option_list>
=============

Each <option_list> element contains a two-column list of command-line
options and descriptions, documenting a program's options.

:Category:   `Compound Body Elements`_
:Analogues:  <option_list> has no direct analogues in common DTDs.
             It can be emulated with primitives such as tables.
:Processing: An <option_list> is typically rendered as a two-column list,
             where the first column contains option strings and
             arguments, and the second column contains descriptions.
:Parents:    All elements employing the `%body.elements`_ or
             `%structure.model`_ parameter entities in their
             content models may contain <option_list>.
:Children:   <option_list> elements contain one or more `\<option_list_item>`_
             elements.
:Attributes: The <option_list> element contains only the `common attributes`_.
:Parameter Entities: The `%body.elements`_ parameter entity
             directly includes <option_list>.  The `%structure.model`_
             parameter entity indirectly includes <option_list>.

Examples
--------

A reStructuredText `option list`_::

    -a            command-line option "a"
    -1 file, --one=file, --two file
                  Multiple options with arguments.

Pseudo-XML_ fragment from simple parsing::

    <option_list>
        <option_list_item>
            <option_group>
                <option>
                    <option_string>
                        -a
            <description>
                <paragraph>
                    command-line option "a"
        <option_list_item>
            <option_group>
                <option>
                    <option_string>
                        -1
                    <option_argument delimiter=" ">
                        file
                <option>
                    <option_string>
                        --one
                    <option_argument delimiter="=">
                        file
                <option>
                    <option_string>
                        --two
                    <option_argument delimiter=" ">
                        file
            <description>
                <paragraph>
                    Multiple options with arguments.


<option_list_item>
==================

The <option_list_item> element is a container for a pair of
`\<option_group>`_ and `\<description>`_ elements.

:Category:   `Body Subelements`_
:Analogues:  <option_list_item> has no direct analogues in common DTDs.
:Processing: See `\<option_list>`_.
:Parents:    Only the `\<option_list>`_ element contains <option_list_item>.
:Children:   Each <option_list_item> element contains one `\<option_group>`_
             and one `\<description>`_ element.
:Attributes: The <option_list_item> element contains only the
             `common attributes`_.

Examples
--------
See the examples for the `\<option_list>`_ element.


<option_string>
===============

The <option_string> element contains the text of a command-line option.

:Category:   `Body Subelements`_
:Analogues:  <option_string> has no direct analogues in common DTDs.
:Processing: The <option_string> text is typically rendered in a
             monospaced typeface.
:Parents:    Only the `\<option>`_ element contains <option_string>.
:Children:   <option_string> elements contain text data only.
:Attributes: The <option_string> element contains only the
             `common attributes`_.

Examples
--------
See the examples for the `\<option_list>`_ element.


<organization>
==============

The <organization> element contains the name of document author's
organization, or the organization responsible for the document.

:Category:   `Bibliographic Elements`_
:Analogues:  <organization> is analogous to the DocBook_ <orgname>,
             <corpname>, or <publishername> elements.
:Processing: See `\<docinfo>`_.
:Parents:    Only the `\<docinfo>`_ element contains <organization>.
:Children:   <organization> elements may contain text data
             plus `inline elements`_ (`%text.model`_).
:Attributes: The <organization> element contains only the
             `common attributes`_.
:Parameter Entities: The `%bibliographic.elements`_ parameter entity
             directly includes <organization>.

Examples
--------

In reStructuredText, "organization" is one of the registered
`bibliographic fields`_::

    Document Title
    ==============

    :Organization: Humankind

Complete pseudo-XML_ result after parsing and applying transforms_::

    <document ids="document-title" names="document title">
        <title>
            Document Title
        <docinfo>
            <organization>
                Humankind

See `\<docinfo>`_ for a more complete example, including processing
context.


<paragraph>
===========

The <paragraph> element contains the text and inline elements of a
single paragraph, a fundamental building block of documents.

:Category:   `Simple Body Elements`_
:Analogues:  <paragraph> is analogous to the HTML <p> element
             and to the DocBook_ <para> elements.
:Parents:    All elements employing the `%body.elements`_ or
             `%structure.model`_ parameter entities in their content models
             may contain <paragraph>.
:Children:   <paragraph> elements may contain text data
             plus `inline elements`_ (`%text.model`_).
:Attributes: The <paragraph> element contains only the `common attributes`_.
:Parameter Entities: The `%body.elements`_ parameter entity
             directly includes <paragraph>.  The `%structure.model`_
             parameter entity indirectly includes <paragraph>.

Examples
--------

In reStructuredText_, blocks of left-aligned text are paragraphs unless
marked up as another body element::

    A paragraph must be
    left-aligned.

Pseudo-XML_ fragment from simple parsing::

    <paragraph>
        A paragraph must be
        left-aligned.


<pending>
=========

`To be completed`_.


<problematic>
=============

`To be completed`_.


<raw>
=====

The <raw> element contains non-reStructuredText data that is to be passed
untouched to the Writer.

:Category:   `Simple Body Elements`_, `Inline Elements`_
:Analogues:  The <raw> element has no direct analogues in common DTDs.
:Processing: Passed untouched to the Writer_.
             The interpretation is up to the Writer.
             A Writer may ignore <raw> elements not matching its format_.
:Parents:    All elements employing the `%body.elements`_,
             `%structure.model`_, or `%text.model`_ parameter entities
             in their content models may contain <raw>.
:Children:   <raw> elements contain text data only.
:Attributes: The <raw> element contains the `common attributes`_
             plus format_ and `xml:space`_.
:Parameter Entities:
             The `%body.elements`_ and `%inline.elements`_ parameter
             entities directly include <raw>.  The `%structure.model`_
             and `%text.model`_ parameter entities indirectly include <raw>.

Examples
--------

The reStructuredText `"raw" directive`_ [#]_ creates a <raw> element::

    .. raw:: html

       <hr width=50 size=10>

Pseudo-XML_ fragment from simple parsing::

    <raw format="html" xml:space="preserve">
        <hr width=50 size=10>

.. [#] For raw data pass-through in inline context, use `custom
   interpreted text roles`_ derived from the `"raw" role`_.


<reference>
===========

`To be completed`_.


<revision>
==========

The <revision> element contains the revision number of the document.
It can be used alone or in conjunction with `\<version>`_.

:Category:   `Bibliographic Elements`_
:Analogues:  <revision> is analogous to but simpler than the DocBook_
             <revision> element.  It closely matches the DocBook
             <revnumber> element, but in a simpler context.
:Processing: Often used with the RCS/CVS keyword "Revision".
             See `\<docinfo>`_.
:Parents:    Only the `\<docinfo>`_ element contains <revision>.
:Children:   <revision> elements may contain text data
             plus `inline elements`_ (`%text.model`_).
:Attributes: The <revision> element contains only the `common attributes`_.
:Parameter Entities: The `%bibliographic.elements`_ parameter entity
             directly includes <revision>.

Examples
--------

In reStructuredText, "revision" is one of the registered
`bibliographic fields`_::

    Document Title
    ==============

    :Version: 1
    :Revision: b

Complete pseudo-XML_ result after parsing and applying transforms_::

    <document ids="document-title" names="document title">
        <title>
            Document Title
        <docinfo>
            <version>
                1
            <revision>
                b

See `\<docinfo>`_ for a more complete example, including processing
context.


<row>
=====

The <row> element represents one row of a `\<table>`_.

:Category:   `Body Subelements`_
:Analogues:  <row> is defined in the `XML Exchange Table Model DTD`_.
             [#extblx]_  It is analogous to the HTML_ <tr> element
             and the DocBook_ <row> element.
:Processing: Render content as a table row.
             See the `Exchange Table Model`_ for details.
:Parents:    The `\<thead>`_ and `\<tbody>`_ elements contain <row> elements.
:Children:   A <row> element contains one or more `\<entry>`_ elements.
:Attributes: The <row> element may contain the rowsep_ and valign_
             attributes (ignored by Docutils) and (via the
             `%tbl.row.att`_ parameter entity) the `common attributes`_.

Examples
--------

See `\<table>`_.


<rubric>
========

     rubric n. 1. a title, heading, or the like, in a manuscript,
     book, statute, etc., written or printed in red or otherwise
     distinguished from the rest of the text. ...

     -- Random House Webster's College Dictionary, 1991

A rubric is like an informal heading that doesn't correspond to the
document's structure.

`To be completed`_.


<section>
=========

The <section> element is the main unit of hierarchy for Docutils documents.

:Category:   `Structural Elements`_

:Analogues:  <section> is analogous to the section elements in DocBook_ and
             HTML_. However, unlike ``<h1>`` … ``<h6>`` in HTML_ and
             ``<sect1>`` … ``<sect5>`` in DocBook_, the level is not
             incorporated into the element name.

:Parents:    The following elements may contain <section>:
             `\<document>`_, `\<section>`_

:Children:   <section> elements begin with a `\<title>`_,
             followed by an optional `\<subtitle>`_.
             They may contain `structural elements`_, `body elements`_,
             and `\<transition>`_ elements:

             .. parsed-literal::

                (title, subtitle?, `%structure.model`_;)

:Attributes: The <section> element contains only the `common attributes`_.

:Parameter Entities: The `%section.elements`_ parameter entity
             directly includes <section>.  The `%structure.model`_
             parameter entity indirectly includes <section>.

The Docutils document model uses a simple, recursive model for section
structure.  A `\<document>`_ node may contain <section> elements.
Sections in turn may contain other <section> elements, without limit.
The level (depth) of a section element is determined from its physical
nesting level.

Paragraphs and other `body elements`_ may occur before a <section>,
but not after it.


Examples
--------

reStructuredText does not impose a fixed number and order of section_
title adornment styles. The order enforced will be the order as
encountered. ::

    Title 1
    =======
    Paragraph 1.

    Title 2
    -------
    Paragraph 2.

    Title 3
    =======
    Paragraph 3.

    Title 4
    -------
    Paragraph 4.

Complete pseudo-XML_ result after parsing::

    <document>
        <section ids="title-1" names="title 1">
            <title>
                Title 1
            <paragraph>
                Paragraph 1.
            <section ids="title-2" names="title 2">
                <title>
                    Title 2
                <paragraph>
                    Paragraph 2.
        <section ids="title-3" names="title 3">
            <title>
                Title 3
            <paragraph>
                Paragraph 3.
            <section ids="title-4" names="title 4">
                <title>
                    Title 4
                <paragraph>
                    Paragraph 4.


<sidebar>
=========

Sidebars are like miniature, parallel documents that occur inside other
documents, providing related or reference material.
Their content is outside of the flow of the document's main text.

:Category:   `Structural Elements`_

:Analogues:  <sidebar> is analogous to the DocBook_ <sidebar> and
             the HTML <aside> elements.

:Processing: A <sidebar> element should be set off from the rest of the
             document somehow, typically with a border.  Sidebars
             typically "float" to the side of the page and the document's
             main text flows around them.

:Parents:    The following elements may contain <sidebar>:
             `\<document>`_, `\<section>`_.

:Children:   <sidebar> elements begin with optional
             `\<title>`_ and `\<subtitle>`_ and contain
             `body elements`_ and `\<topic>`_ elements.
             There must not be a <subtitle> without title. ::

               ((title, subtitle?)?,
                (%body.elements; | topic)+)

:Attributes: The <sidebar> element contains only the `common attributes`_.

:Parameter Entities: The `%structure.model`_ parameter entity
             directly includes <sidebar>.

The <sidebar> element is a non-recursive `\<section>`_-like construct.
<sidebar> elements cannot nest inside body elements, so you can't have a
<sidebar> inside a `\<table>`_ or a list, or inside another <sidebar>
or `\<topic>`_.


Examples
--------

A reStructuredText `"sidebar" directive`_::

    .. sidebar:: Optional Title
       :subtitle: If Desired

       Body.

Pseudo-XML_ fragment from simple parsing::

    <sidebar>
        <title>
            Optional Title
        <subtitle>
            If Desired
        <paragraph>
            Body.


<status>
========

The <status> element contains a status statement for the document,
such as "Draft", "Final", "Work In Progress", etc.

:Category:   `Bibliographic Elements`_
:Analogues:  <status> is analogous to the DocBook_ <status> element.
:Processing: See `\<docinfo>`_.
:Parents:    Only the `\<docinfo>`_ element contains <status>.
:Children:   <status> elements may contain text data
             plus `inline elements`_ (`%text.model`_).
:Attributes: The <status> element contains only the `common attributes`_.
:Parameter Entities: The `%bibliographic.elements`_ parameter entity
             directly includes <status>.

Examples
--------

In reStructuredText, "status" is one of the registered
`bibliographic fields`_::

    Document Title
    ==============

    :Status: Work In Progress

Complete pseudo-XML_ result after parsing and applying transforms_::

    <document ids="document-title" names="document title">
        <title>
            Document Title
        <docinfo>
            <status>
                Work In Progress

See `\<docinfo>`_ for a more complete example, including processing
context.


<strong>
========

The <strong> element is an inline element representing
text that has **strong importance**, **seriousness**, or **urgency**.

:Category:   `Inline Elements`_
:Analogues:  <strong> is analogous to the HTML_ <strong> element.
:Processing: Typically displayed in boldface.
:Parents:    All elements employing the `%text.model`_ parameter
             entity in their content models may contain <strong>.
:Children:   <strong> elements may contain text data
             plus `inline elements`_ (`%text.model`_).
:Attributes: The <strong> element contains only the `common attributes`_.

Examples
--------

The reStructuredText there are two alternatives to mark text with
`strong emphasis`_::

    There are :strong:`two` ways to **strongly emphasize** text.

Pseudo-XML_ fragment from simple parsing::

    <paragraph>
        There are
        <strong>
            two
         ways to
        <strong>
            strongly emphasize
         text.


<subscript>
===========

The <subscript> element is an inline element representing text which
should be displayed as subscript.

:Category:   `Inline Elements`_
:Analogues:  <subscript> is analogous to the HTML_ <sub> element
             and the DocBook_ <subscript> element.
:Processing: Typically rendered with a lowered baseline using smaller text.
:Parents:    All elements employing the `%text.model`_ parameter
             entity in their content models may contain <subscript>.
:Children:   <subscript> elements may contain text data
             plus `inline elements`_ (`%text.model`_).
:Attributes: The <subscript> element contains only the `common attributes`_.

Examples
--------

The reStructuredText `"subscript" role`_ creates a <subscript> element::

    The chemical formula for water is H\ :sub:`2`\ O.

Pseudo-XML_ fragment from simple parsing::

    <paragraph>
        The chemical formula for water is H
        <subscript>
            2
        O.


<substitution_definition>
=========================

The <substitution_definition> element stores a
reStructuredText `substitution definition`_.

`To be completed`_.


<substitution_reference>
========================

`To be completed`_.


<subtitle>
==========

The <subtitle> element stores the subtitle of a `\<document>`_,
`\<section>`_, or `\<sidebar>`_.

:Category:   `Structural Subelements`_
:Analogues:  <subtitle> is analogous to the DocBook_ <subtitle> element.
             In HTML, subtitles are represented by a <p> element inside
             a <hgroup_> element.
:Processing: A document's subtitle is usually rendered smaller
             than its `\<title>`_.
:Parents:    The `\<document>`_, `\<section>`_, and `\<sidebar>`_ elements
             may contain <subtitle>.
:Children:   <subtitle> elements may contain text data
             plus `inline elements`_ (`%text.model`_).
:Attributes: The <subtitle> element contains only the `common attributes`_.

Examples
--------

In reStructuredText, a lone second-level section title immediately after
the “document title” can become the document subtitle::

    =======
     Title
    =======
    ----------
     Subtitle
    ----------

    A paragraph.

Complete pseudo-XML_ result after parsing and applying the
`DocTitle transform`_::

    <document ids="title" names="title">
        <title>
            Title
        <subtitle ids="subtitle" names="subtitle">
            Subtitle
        <paragraph>
            A paragraph.

Note how two section levels have collapsed, promoting their titles to
become the document's title and subtitle.  Since there is only one
structural element (document), the subsection's ``ids`` and ``names``
attributes are stored in the <subtitle> element.

.. _hgroup: https://html.spec.whatwg.org/multipage/sections.html
            #the-hgroup-element


<superscript>
=============

The <superscript> element is an inline element representing text which
should be displayed as superscript.

:Category:   `Inline Elements`_
:Analogues:  <superscript> is analogous to the HTML_ <sup> element
             and the DocBook_ <superscript> element.
:Processing: Typically rendered with a raised baseline using smaller text.
:Parents:    All elements employing the `%text.model`_ parameter
             entity in their content models may contain <superscript>.
:Children:   <superscript> elements may contain text data
             plus `inline elements`_ (`%text.model`_).
:Attributes: The <superscript> element contains only the `common attributes`_.

Examples
--------

The reStructuredText `"superscript" role`_ creates a <superscript> element::

    Key events of the 20\ :sup:`th` century.

Pseudo-XML_ fragment from simple parsing::

    <paragraph>
        Key events of the 20
        <superscript>
            th
         century.


<system_message>
================

`To be completed`_.


<table>
=======

The <table> element represents a data arrangement with rows and columns.

:Category:   `Body Elements`_

:Analogues:  <table> is defined in the `XML Exchange Table Model DTD`_.
             [#extblx]_  It is analogous to the HTML_ and DocBook_
             <table> elements.

:Processing: Content is arranged in rows and columns forming a grid.
             See the `Exchange Table Model`_ for details.

:Parents:    `\<document>`_, `\<section>`_ and all `body elements`_
             may contain <table>.

:Children:   <table> elements begin with an optional `\<title>`_ (caption)
             and may contain one or more `\<tgroup>`_ elements::

               (title?, tgroup+)

:Attributes: The <table> element may contain the frame_, colsep_,
             rowsep_, and pgwide_ attributes (ignored by Docutils)
             and (via the `%bodyatt`_ parameter entity)
             the `common attributes`_, align_, and width_.

:Parameter Entities: The `%body.elements`_ parameter entity
             directly includes <table>.  The `%structure.model`_
             parameter entity indirectly includes <table>.

.. [#extblx] The `Docutils Document Model` includes, via the `%calstblx`_
   parameter entity, the `XML Exchange Table Model DTD`_ to define the
   table elements `\<colspec>`_, `\<entry>`_, `\<row>`_, `\<table>`_,
   `\<tbody>`_, `\<tgroup>`_, and `\<thead>`_.

Examples
--------

In reStructuredText, tables can be specified via the
`"table" <"table" directive_>`__, `"csv-table"`_, or `"list-table"`_
directives or directly as `grid table`_ or `simple table`_, e.g. ::

    ======== ====
     bread   £2
     butter  £30
    ======== ====

Pseudo-XML_ fragment from simple parsing::

    <table>
        <tgroup cols="2">
            <colspec colwidth="8">
            <colspec colwidth="4">
            <tbody>
                <row>
                    <entry>
                        <paragraph>
                            bread
                    <entry>
                        <paragraph>
                            £2
                <row>
                    <entry>
                        <paragraph>
                            butter
                    <entry>
                        <paragraph>
                            £30


<target>
========

`To be completed`_.


<tbody>
=======

The <tbody> element identifies the rows that form the *body*
of a `\<table>`_ (as distinct from the header rows).

:Category:   `Body Subelements`_
:Analogues:  <tbody> is defined in the `XML Exchange Table Model DTD`_.
             [#extblx]_  It is analogous to the HTML_ <tbody> and
             the DocBook_ <tbody> (db.cals.tbody) elements.
:Processing: Render content as table body.
:Parents:    Only the `\<tgroup>`_ element contains <tbody>.
:Children:   A <tbody> element contains one or more `\<row>`_ elements.
:Attributes: The <tbody> element may contain valign_ (ignored by Docutils)
             and (via the `%tbl.tbody.att`_ parameter entity)
             the `common attributes`_.

Examples
--------

See `\<table>`_.


<term>
======

The <term> element contains a word or phrase being defined in a
`\<definition_list>`_.

:Category:   `Body Subelements`_ (simple)
:Analogues:  <term> is analogous to the HTML <dt> element
             and to the DocBook_ <term> element.
:Processing: See `\<definition_list_item>`_.
:Parents:    Only the `\<definition_list_item>`_ element contains <term>.
:Children:   <term> elements may contain text data
             plus `inline elements`_ (`%text.model`_).
:Attributes: The <term> element contains only the `common attributes`_.

Examples
--------
See the examples for the `\<definition_list>`_,
`\<definition_list_item>`_, and `\<classifier>`_ elements.


<tgroup>
========

The <tgroup> element identifies a logically complete portion of a
`\<table>`_.

:Category:   `Body Subelements`_
:Analogues:  <tgroup> is defined in the `XML Exchange Table Model DTD`_.
             [#extblx]_  It is analogous to the DocBook_ <tgroup> element.
             There is no corresponding HTML element (the <colgroup>
             element has a different purpose and semantics).
:Processing: See the `Exchange Table Model`_.
:Parents:    Only the `\<table>`_ element contains <tgroup>.
:Children:   <tgroup> elements contain one or more `\<colspec>`_
             elements, followed by an optional `\<thead>`_ and a
             `\<tbody>`_ (cf. the `%tbl.tgroup.mdl`_ parameter entity).
             The number of <colspec>s, must not exceed the value of the cols_
             attribute.  Docutils expects one <colspec> per column.
:Attributes: The <tgroup> element must contain a cols_ attribute and may
             contain colsep_, rowsep_, and align_ (ignored by Docutils).
             Via the `%tbl.tgroup.att`_ parameter entity, <tgroup>
             supports the `common attributes`_.

Tables usually consist of a single <tgroup>. Complex tables with widely
varying column specifications may be easier to code using multiple
<tgroup>s. However, this is not supported by `table markup in
reStructuredText <rST tables_>`__ and Docutils table handling routines.

Examples
--------

See `\<table>`_.


<thead>
=======

The <thead> element identifies the row(s) that form the head of
a `\<table>`_ (as distinct from the body rows).

:Category:   `Body Subelements`_
:Analogues:  <thead> is defined in the `XML Exchange Table Model DTD`_.
             [#extblx]_ It is analogous to the HTML_ and DocBook_
             <thead> elements.
:Processing: Header rows are always rendered at the beginning of the
             table and often presented in an alternate typographic style,
             such as boldface.
             In paged media, if a table spans across multiple pages,
             header rows are printed at the top of each new page.
:Parents:    Only the `\<tgroup>`_ element contains <thead>.
:Children:   A <thead> element contains one or more `\<row>`_ elements.
:Attributes: The <thead> element contains the valign_ attribute
             (ignored by Docutils) and (via the `%tbl.thead.att`_
             parameter entity) the `common attributes`_.

Examples
--------

See `\<table>`_.


<tip>
=====

The <tip> element is a specific *admonition*, a distinctive and
self-contained notice.

:Category:   `Compound Body Elements`_
:Analogues:  <tip> is analogous to the `DocBook \<tip>`_ element.
:Processing: Rendered distinctly (inset and/or in a box, etc.),
             with the generated title "Tip" (or similar).
:Parents:    All elements employing the `%body.elements`_ or
             `%structure.model`_ parameter entities in their content models
             may contain <tip>.
:Children:   <tip> elements contain one or more `body elements`_.
:Attributes: The <tip> element contains only the `common attributes`_.
:Parameter Entities: The `%body.elements`_ parameter entity
             directly includes <tip>. The `%structure.model`_
             parameter entity indirectly includes <tip>.

See also the generic `\<admonition>`_ and the other `specific admonition
elements`_.

Examples
--------

A reStructuredText `"tip" directive`_::

    .. Tip:: 15% if the service is good.

Pseudo-XML_ fragment from simple parsing::

    <tip>
        <paragraph>
            15% if the service is good.


<title>
=======

The <title> element stores the title of a `\<document>`_, `structural
elements`_, or a generic `\<admonition>`_.  It is also used for the
caption of a `\<table>`_.

:Category:   `Structural Subelements`_, `Body Subelements`_
:Analogues:  <title> is analogous to the DocBook_ <title> element and
             the HTML_ header elements (<h1> etc.) while the HTML <title>
             element corresponds to a <document>'s `title attribute`_.
             As child of a `\<table>`_, <title> corresponds to
             the HTML <caption> element.
:Parents:    The following elements may contain <title>:
             `\<admonition>`_, `\<document>`_, `\<section>`_,
             `\<sidebar>`_, `\<table>`_, `\<topic>`_.
:Children:   <title> elements may contain text data
             plus `inline elements`_ (`%text.model`_).
:Attributes: The <title> element contains the `common attributes`_
             plus refid_ (used as a backlink to a table of contents entry)
             and auto_.

The <title> of a document may differ from its *metadata title*
stored in the `title attribute`_.

Examples
--------

Section_ titles are marked up with "underlines" below the title text (or
underlines and matching overlines)::

    A Title
    =======

    A paragraph.

    Next section's title
    ====================

Pseudo-XML_ fragment from simple parsing::

    <section ids="a-title" names="a\ title">
        <title>
            A Title
        <paragraph>
            A paragraph.
    <section ids="next-section-s-title" names="next\ section's\ title">
        <title>
            Next section’s title

See also the examples for `\<admonition>`_, `\<document>`_,
`\<section>`_, `\<sidebar>`_, `\<subtitle>`_, `\<table>`_,
and `\<topic>`_.


<title_reference>
=================

The <title_reference> element is an inline element representing
the titles of a cited creative work.

:Category:   `Inline Elements`_
:Analogues:  <title_reference> is analogous to the HTML_ <cite> element
             and the DocBook_ <citetitle> element.
:Processing: Typically displayed in italic type.
:Parents:    All elements employing the `%text.model`_ parameter
             entity in their content models may contain <title_reference>.
:Children:   <title_reference> elements may contain text data
             plus `inline elements`_ (`%text.model`_).
:Attributes: The <title_reference> element contains only the
             `common attributes`_.

Examples
--------

The reStructuredText `"title-reference" role`_ creates a <title_reference>
element::

    The term "spam" is derived from the 1970 :title:`Spam` sketch.


Pseudo-XML_ fragment from simple parsing::

    <paragraph>
        The term “spam” is derived from the 1970
        <title_reference>
            Spam
         sketch.


<topic>
=======

The <topic> element represents a non-recursive section-like construct for
content that is separate from the flow of the document.

:Category:   `Structural Elements`_

:Analogues:  <topic> is analogous to the DocBook_ <simplesect> element
             and the HTML_ <aside> element.

:Processing: A <topic> element should be set off from the rest of the
             document somehow, such as with indentation or a border.
             In contrast to a `\<sidebar>`_, it should not float.

:Parents:    The following elements may contain <topic>:
             `\<document>`_, `\<section>`_, `\<sidebar>`_

:Children:   <topic> elements may begin with a `\<title>`_ and contain
             `body elements`_::

                 (title?, (%body.elements;)+)

:Attributes: The <topic> element accepts the `common attributes`_.

:Parameter Entities: The `%structure.model`_ parameter entity
             directly includes <topic>.

Topics are terminal, "leaf" mini-sections, like block quotes with titles,
or textual figures.  A <topic> is just like a `\<section>`_, except that
it has no subsections, it does not get listed in the ToC, and it doesn't
have to conform to section placement rules.
You may place a <topic> in the middle of a <section> and continue the same
section after it --- something that cannot be done with a nested <section>.

Topics cannot nest inside topics, or `body elements`_
(tables, lists, block quotes, etc).

.. Tip:: Use a `\<rubric>`_ element to get an informal heading inside a
         table, list, or inside another <topic>.

Docutils uses the <topic> element also for a generated `table of contents`_,
and the "abstract" and "dedication" `bibliographic fields`_.

Examples
--------

A reStructuredText `"topic" directive`_::

    .. topic:: Title

       Body.

Pseudo-XML_ fragment from simple parsing::

    <topic>
        <title>
            Title
        <paragraph>
            Body.


<transition>
============

The <transition> element separates body elements and sections, dividing a
`\<section>`_ into untitled divisions.

:Category:   `Structural Subelements`_
:Analogues:  <transition> is analogous to the HTML <hr> element.
:Processing: The <transition> element is typically rendered as vertical
             whitespace (more than that separating paragraphs), with or
             without a horizontal line or row of asterisks.  In novels,
             transitions are often represented as a row of three
             well-spaced asterisks with vertical space above and below.
:Parents:    The following elements may contain <transition>:
             `\<document>`_, `\<section>`_
:Children:   The <transition> element has no content.
:Attributes: The <transition> element contains only the `common attributes`_.
:Parameter Entities: The `%structure.model`_ parameter entity
             directly includes <transition>.

A transition may not begin or end a section [#]_ or document, nor may two
transitions be immediately adjacent.

See also `Doctree Representation of Transitions`__ in
`A Record of reStructuredText Syntax Alternatives`__.

.. [#] In reStructuredText markup, a transition may appear to fall at
   the end of a section immediately before another section.
   A transform_ recognizes this case and moves the transition so it
   separates the sections.

__ ../dev/rst/alternatives.html#doctree-representation-of-transitions
__ ../dev/rst/alternatives.html


Examples
--------

A transition_ in the reStructuredText source::

    Paragraph 1.

    --------

    Paragraph 2.

Complete pseudo-XML_ result after parsing::

    <document>
        <paragraph>
            Paragraph 1.
        <transition>
        <paragraph>
            Paragraph 2.


<version>
=========

The <version> element contains the version number of the document.
It can be used alone or in conjunction with `\<revision>`_.

:Category:   `Bibliographic Elements`_
:Analogues:  <version> may be considered analogous to the DocBook_
             <revision>, <revnumber>, or <biblioid> elements.
:Processing: Sometimes used with the RCS/CVS keyword "Revision".
             See `\<docinfo>`_ and `\<revision>`_.
:Parents:    Only the `\<docinfo>`_ element contains <version>.
:Children:   <version> elements may contain text data
             plus `inline elements`_ (`%text.model`_).
:Attributes: The <version> element contains only the `common attributes`_.
:Parameter Entities: The `%bibliographic.elements`_ parameter entity
             directly includes <version>.

Examples
--------

In reStructuredText, "version" is one of the registered
`bibliographic fields`_::

    Document Title
    ==============

    :Version: 1.1

Complete pseudo-XML_ result after parsing and applying transforms_::

    <document ids="document-title" names="document title">
        <title>
            Document Title
        <docinfo>
            <version>
                1.1

See `\<docinfo>`_ for a more complete example, including processing
context.


<warning>
=========

The <warning> element is a specific *admonition*, a distinctive and
self-contained notice.

:Category:   `Compound Body Elements`_
:Analogues:  <warning> is analogous to the `DocBook \<warning>`_ element.
:Processing: Rendered distinctly (inset and/or in a box, etc.),
             with the generated title "Warning" (or similar).
:Parents:    All elements employing the `%body.elements`_ or
             `%structure.model`_ parameter entities in their content models
             may contain <warning>.
:Children:   <warning> elements contain one or more `body elements`_.
:Attributes: The <warning> element contains only the `common attributes`_.
:Parameter Entities: The `%body.elements`_ parameter entity
             directly includes <warning>.  The `%structure.model`_
             parameter entity indirectly includes <warning>.

See also the generic `\<admonition>`_ and the other
`specific admonition elements`_.

Examples
--------

A reStructuredText `"warning" directive`_::

    .. WARNING:: Reader discretion is strongly advised.

Pseudo-XML_ fragment from simple parsing::

    <warning>
        <paragraph>
            Reader discretion is strongly advised.


---------------
Attribute Types
---------------

.. contents:: :local:

Standard Attribute Types
========================

*Standard attribute types* are defined in the
`attribute types <XML attribute types_>`__ section
of the `XML 1.0 specification` [xml1.0]_.

_`CDATA`
    Character data.  CDATA attributes may contain arbitrary text.

_`NMTOKEN`
    A "name token".  One or more of letters, digits, ".", "-", and
    "_".

_`NMTOKENS`
    One or more space-separated NMTOKEN_ values.

_`EnumeratedType`
    The attribute value may be one of a specified list of values.


Custom Attribute Types
======================

The Docutils DTD defines *custom attribute types* via `parameter entities
<parameter entity reference_>`__ that resolve to standard attribute types
to highlight specific attribute value constraints.
In the docutils.nodes_ reference implementation, values are stored using
the specified Python data types.

_`%classnames.type`
  | Space-separated list of `class names`_.  Resolves to NMTOKEN_.
  | Used in the `classes`_ attribute.  Python data type: ``list[str]``.

_`%idref.type`
  | A reference to another element by its identifier_.
    Resolves to NMTOKEN_. [#id-vc]_
  | Used in the `refid`_ attribute.  Python data type: ``str``.

  .. _identifier: identifiers_

_`%idrefs.type`
  | Space separated list of references to other elements by their identifiers_.
    Resolves to NMTOKENS_. [#id-vc]_
  | Used in the `backrefs`_ attribute.  Python data type: ``list[str]``.

_`%ids.type`
  | A space-separated list of unique `identifiers`_.
    Resolves to NMTOKENS_. [#id-vc]_
  | Used in the `ids`_ attribute.  Python data type: ``list[str]``.

_`%measure`
  | A number which may be immediately followed by a unit or percent sign.
    Resolves to CDATA_.
  | Used in the `height`_ and `width`_ attributes.  Python data type: ``str``.

_`%number`
  | The attribute value must be a positive interger.  Resolves to NMTOKEN_.
  | Used in the level_, morecols_, morerows_, scale_, and start_ attributes.
    Python data type: ``int``.

_`%refname.type`
  | A `reference name`_.  Resolves to CDATA_.
  | Used in the `refname`_ attribute.  Python data type: ``str``.

_`%refnames.type`
  | Space-separated list of `reference names`_.  Resolves to CDATA_.
  | Used in the `names`_ and `dupnames`_ attributes.
    Python data type: ``list[str]``.

  Backslash escaping is used for space characters inside a `reference
  name`.

_`%yesorno`
  | Boolean: False if zero ("0"), true for any other value.
    Resolves to NMTOKEN_.
  | Used in the anonymous_, colsep_, ltrim_, rtrim_, rowsep_,
    and `stub`_ attributes.
    Python data type: ``int``.


Names and identifiers
=====================

The following names and identifiers are used in the
`custom attribute types`_.

.. class:: description

_`Class names`
  define sub-classes of existing elements.

  Docutils employs the `identifier normalization`_ to ensure class names
  conform to both, HTML4.1 and CSS1.0 `name` requirements (the regular
  expression ``[a-z](-?[a-z0-9]+)*``).

  In reStructuredText, custom class names can be specified using the
  `"class" directive`_, a directive's `class option`_, or `custom
  interpreted text roles`_.

  Class names are used in the classes_ attribute (`%classnames.type`_).

  .. _reference name:

_`Reference names`
  are identifiers assigned in the markup.

  Reference names may consist of any text.
  Whitespace is normalized. [#whitespace-normalization]_

  In reStructuredText, `reference names <rST reference names_>`__
  originate from `internal hyperlink targets`_, a directive's `name
  option`_, or the element's title or content and are used for internal
  cross-references.

  Hyperlinks_, footnotes_, and citations_ all share the same namespace
  for reference names. Comparison ignores case.

  Substitutions_ use a distinct namespace.  Comparison is case-sensitive
  but forgiving.

  Reference names are used in the name_, names_, refname_, and dupnames_
  attributes (`%refname.type`_ or `%refnames.type`_).

_`Identifiers`
  are used for cross references in generated documents.

  Docutils employs the `identifier normalization`_ to comply with
  restrictions in the supported output formats (HTML4.1__, HTML5__,
  `polyglot HTML`__, LaTeX__, ODT__, manpage, XML__).

  Identifiers cannot be specified directly in reStructuredText.
  Docutils generates them from `reference names`_ or from the
  auto_id_prefix_, prepending the id_prefix_ and appending numbers
  for disambiguation if required.

  Identifiers are used in the ids_, refid_, and backrefs_ attributes
  (`%ids.type`_, `%idref.type`_, or `%idrefs.type`_) [#id-vc]_.

.. [#whitespace-normalization] Adjacent spaces, horizontal or vertical
   tabs, newlines, carriage returns, or form feeds, are replaced by a
   single space.  Leading and trailing whitespace is removed.

.. [#id-vc] Docutils cannot use the ID, IDREF, and IDREFS standard types
   because it does not adhere to the `One ID per Element Type`_ validity
   constraint.

__ https://www.w3.org/TR/html401/types.html#type-name
__ https://www.w3.org/TR/html50/dom.html#the-id-attribute
__ https://www.w3.org/TR/html-polyglot/#id-attribute
__ https://tex.stackexchange.com/questions/18311/
   what-are-the-valid-names-as-labels
__ https://help.libreoffice.org/6.3/en-US/text/swriter/01/04040000.html
   ?DbPAR=WRITER#bm_id4974211
__ `XML attribute types`_


Common Attributes
=================

Through the `%basic.atts`_ parameter entity, all elements support the
following attributes: ids_, names_ or dupnames_, source_, and classes_.


---------------------
 Attribute Reference
---------------------

.. contents:: :local:
              :depth: 1

``alt``
=======

Attribute type: `CDATA`_.  Default value: none.

The ``alt`` attribute is used to store a text description in the
`\<image>`_ element.


``align``
=========

Attribute type: EnumeratedType_.  Default value: none (inherit).

The ``align`` attribute is used in the `\<figure>`_ and `\<table>`_
elements via the `%align-h.att`_ parameter entity
and in `\<image>`_ via the `%align-hv.att`_ parameter entity
to specify the alignment of the element within its parent element.

The `Exchange Table Model`_ uses ``align`` in the `\<colspec>`_,
`\<entry>`_, end `\<tgroup>`_ elements to specify the text alignment in
table cells.  It cannot be specified in reStructuredText and is ignored
by Docutils writers.



``anonymous``
=============

Attribute type: `%yesorno`_.  Default value: none (implies no).

The ``anonymous`` attribute is used for unnamed hyperlinks in the
`\<target>`_ and `\<reference>`_ elements (via the `%anonymous.att`_
parameter entity).


``auto``
========

Attribute type: `CDATA`_.  Default value: none.

The ``auto`` attribute is used to indicate automatically-numbered
`\<footnote>`_, `\<footnote_reference>`_ and `\<title>`_ elements
(via the `%auto.att`_ parameter entity).


``backrefs``
============

Attribute type: `%idrefs.type`_.  Default value: none.

The ``backrefs`` attribute contains a space-separated list of identifier_
references, used for backlinks from `\<footnote>`_, `\<citation>`_, and
`\<system_message>`_ elements (via the `%backrefs.att`_ parameter entity).


``bullet``
==========

Attribute type: `CDATA`_.  Default value: none.

The ``bullet`` attribute is used in the `\<bullet_list>`_ element to
record the style of bullet from the input data.  In documents processed
from reStructuredText_, it contains one of "-", "+", or "*".
It may be ignored in processing.


``classes``
===========

Attribute type: `%classnames.type`_.  Default value: none.

The ``classes`` attribute is a space separated list containing zero or
more `class names`_.

The purpose of the attribute is to indicate an "is-a" variant relationship,
to allow an extensible way of defining sub-classes of existing elements.
It can be used to carry context forward between a Docutils Reader_ and
Writer_, when a custom structure is reduced to a standardized document
tree.  One common use is in conjunction with stylesheets, to add
selection criteria. It should not be used to carry formatting
instructions or arbitrary content.

The ``classes`` attribute's contents should be ignorable.  Writers that
are not familiar with the variant expressed should be able to ignore
the attribute.

``classes`` is one of the `common attributes`_, shared by all
Docutils elements.

.. _reader: ../peps/pep-0258.html#readers
.. _writer:
.. _writers: ../peps/pep-0258.html#writers


``char``
========

Attribute type: CDATA_.  Default value: "" (no aligning character).

The ``char`` attribute is used in the `\<colspec>`_ and `\<entry>`_
elements to specify an alignment character.

The attribute is defined in the `Exchange Table Model`_ (which see
for details). It cannot be specified in reStructuredText and is
ignored by Docutils.


``charoff``
===========

Attribute type: NMTOKEN_.  Default value: "50" (i.e. 50%).

The ``charoff`` attribute is used in `\<colspec>`_ and `\<entry>`_
elements to specify the horizontal offset of the alignment character
when align_ is "char".

The attribute is defined in the `Exchange Table Model`_ (which see
for details). It cannot be specified in reStructuredText and is
ignored by Docutils.


``colname``
===========

Attribute type: NMTOKEN_.  Default value: none.

Name (identifier) of a table column.

The ``colname`` attribute is used in the `\<colspec>`_ element name a
table column and in the `\<entry>`_ element to reference a named column.

The attribute is defined in the `Exchange Table Model`_ (which see
for details). It cannot be specified in reStructuredText and is
ignored by Docutils.


``colnum``
===========

Attribute type: NMTOKEN_.  Default value: none.

The ``colnum`` attribute is used in the `\<colspec>`_ element.
The attribute is defined in the `Exchange Table Model`_ (which see for
details). It serves no functional purpose other than a consistency check.


``cols``
=========

Attribute type: NMTOKEN_.  Default value: none.

The ``cols`` attribute is used in the `\<tgroup>`_ element.
It stores the number of columns in a table group.

The attribute is defined in the `Exchange Table Model`_ (which see
for details).


``colsep``
==========

Attribute type: `%yesorno`_.  Default value: none.

The ``colsep`` attribute is used in the `\<colspec>`_, `\<entry>`_,
`\<table>`_, and `\<tgroup>`_ elements to specify the presence or absence
of a column separator (vertical ruling).

The attribute is defined in the `Exchange Table Model`_ (which see
for details). It cannot be specified in reStructuredText and is
ignored by Docutils.


``colwidth``
============

Attribute type: CDATA_.  Default value: "1*" (`sic!`__)

Column width specification used in the `\<colspec>`_ element.

Either proportional measure of the form number*, e.g., “5*” for 5 times
the proportion, or “*” (which is equivalent to “1*”); fixed measure,
e.g., 2pt for 2 point, 3pi for 3 pica.

The fixed unit values are case insensitive. The standard list of allowed
unit values is “pt” (points), “cm” (centimeters), “mm” (millimeters),
“pi” (picas), and “in” (inches). The default fixed unit should be
interpreted as “pt” if neither a proportion nor a fixed unit is
specified.

Defined in the `Exchange Table Model`_.

__
.. important::
   Currently, Docutils only allows unitless integers in the ``colwidth``
   attribute and interprets them as proportions.


``delimiter``
=============

Attribute type: `CDATA`_.  Default value: none.

The ``delimiter`` attribute is used in the `\<option_argument>`_ element
and contains the text preceding the <option_argument>: either the text
separating it from the `\<option_string>`_ (typically either "=" or " ")
or the text between option arguments (typically either "," or " ").


``dupnames``
============

Attribute type: `%refnames.type`_.  Default value: none.

``dupnames`` is one of the `common attributes`_, shared by all
Docutils elements. It replaces the `names`_ attribute when there
has been a naming conflict.


``enumtype``
============

Attribute type: EnumeratedType_, one of "arabic", "loweralpha",
"upperalpha", "lowerroman", or "upperroman".  Default value: none.

The ``enumtype`` attribute is used in the `\<enumerated_list>`_ element
to record the intended enumeration sequence.

Supported values:
    .. class:: field-indent-8em

    :arabic:     1, 2, 3, ...
    :loweralpha: a, b, c, ..., z
    :upperalpha: A, B, C, ..., Z
    :lowerroman: i, ii, iii, iv, ..., mmmmcmxcix [4999]
    :upperroman: I, II, III, IV, ..., MMMMCMXCIX [4999]


``format``
==========

Attribute type: NMTOKENS_.  Default value: none.

The ``format`` attribute is a string containing one or more space
separated output format names.

The ``format`` attribute is used in the `\<raw>`_ element.


``frame``
=========

| Attribute type: EnumeratedType_ (top|bottom|topbot|all|sides|none).
| Default value: none (implied).

The ``frame`` attribute may be used in the `\<table>`_ element to
specify the table's outer frame.

The attribute is defined in the `Exchange Table Model`_ (which see
for details). It cannot be specified in reStructuredText and is
ignored by Docutils.


``height``
==========

Attribute type: `%measure`_.  Default value: none.

The ``height`` attribute is used in the `\<image>`_ element.


``ids``
=======

Attribute type: `%ids.type`_.  Default value: none.

The ``ids`` attribute is a space separated list containing one or more
unique `identifiers`_, typically assigned by the system.

``ids`` is one of the `common attributes`_, shared by all Docutils
elements.

.. TODO:
   * Use 'id' for primary identifier key?
   * Keep additional keys in `ids`
     or in the preceding target elements?


``level``
=========

Attribute type: `%number`_.  Default value: none.

The ``level`` attribute is used in the `\<system_message>`_ element.


``line``
=========

Attribute type: `%number`_.  Default value: none.

The ``line`` attribute is used in the `\<system_message>`_ element.


``ltrim``
=========

Attribute type: `%yesorno`_.  Default value: none (implies no).

The ``ltrim`` attribute is used in the `\<substitution_definition>`_ element.


``loading``
===========

Attribute type: EnumeratedType_, one of "embed", "link", or "lazy".
Default value: none.

The ``loading`` attribute is used in the `\<image>`_ element to
indicate the preferred handling by the Docutils writer_. [#]_
The default depends on the writer and the image_loading_
configuration setting.

New in Docutils 0.21

.. [#] Currently only recognized by the HTML5 writer.
   The ODF/ODT writer always embeds images in the
   output document, XML and LaTeX writers link to the image.
   The behaviour may change for the ODT and XML writers
   (images cannot be embedded in a LaTeX source).


``morecols``
============

Attribute type: `%number`_.  Default value: none.

The ``morecols`` attribute is used in the `\<entry>`_ element
to specify an entry that spans several physical table columns.
It is similar to the ``colspan`` attribute of HTML table cells
(<th> and <td>).

The ``morecols`` attribute is defined in the `%tbl.entry.att`_ parameter
entity extending the `Exchange Table Model`_.


``morerows``
============

Attribute type: `%number`_.  Default value: none.

The ``morerows`` attribute is used in the `\<entry>`_ element
to specify an entry that spans several physical table rows.
It is similar to the ``rowspan`` attribute of HTML table cells
(<th> and <td>).

The attribute is defined in the `Exchange Table Model`_ (which see
for details).


``name``
=========

Attribute type: `NMTOKEN`_ or `CDATA`_.
Default value: none.

The ``name`` attribute in the `\<meta>`_ element accepts `NMTOKEN`_ values.
The output format may limit valid values to a set of keywords
(EnumeratedType_).

The ``name`` attribute in the `\<reference>`_ element holds the
`reference name`_ of the referenced element.  Whitespace is normalized
but case is preserved.  The attribute will no longer be used with
<reference> elements in Docutils 1.0.


``names``
=========

Attribute type: `%refnames.type`_.  Default value: none.

The ``names`` attribute is a space-separated list containing
`reference names`_ of an element.
Spaces inside a name are backslash-escaped.

Each name in the list must be unique; if there are name conflicts (two or
more elements want to the same name), the contents will be transferred to
the `dupnames`_ attribute on the duplicate elements. An element may have
at most one of the ``names`` or ``dupnames`` attributes, but not both.

``names`` is one of the `common attributes`_, shared by all
Docutils elements.


``namest``
==========

Attribute type: NMTOKEN_.  Default value: none.


The ``namest`` attribute is used in the `\<entry>`_ element to specify the
leftmost column of a span.

The attribute is defined in the `Exchange Table Model`_ (which see
for details). It is ignored by Docutils which uses the morecols_
attribute instead.


``nameend``
===========

Attribute type: NMTOKEN_.  Default value: none.

The ``nameend`` attribute is used in the `\<entry>`_ element to specify the
rightmost column of a span.

The attribute is defined in the `Exchange Table Model`_ (which see
for details). It is ignored by Docutils which uses the morecols_
attribute instead.


``pgwide``
==========

Attribute type: `%yesorno`_.  Default value: none (implies no).

The ``pgwide`` attribute is used in the `\<table>`_ element to make the
table span the full page width.

The attribute is defined in the `Exchange Table Model`_ (which see
for details). It cannot be specified in reStructuredText and is
ignored by Docutils.


``prefix``
==========

Attribute type: `CDATA`_.  Default value: none.

The ``prefix`` attribute is used in the `\<enumerated_list>`_ element
to store the formatting characters used before the enumerator.

In documents originating from reStructuredText_ data, it will contain
either "" (empty string) or "(" (left parenthesis).
Writers may ignore this attribute.


``refid``
=========

Attribute type: `%idref.type`_.  Default value: none.

The ``refid`` attribute contains a reference to another element via its
`identifier`_.

``refid`` is used by the `\<citation_reference>`_, `\<footnote_reference>`_,
`\<problematic>`_, `\<reference>`_, `\<target>`_, and `\<title>`_ elements
(via the `%refid.att`_ and `%reference.atts`_ parameter entities).


``refname``
===========

Attribute type: `%refname.type`_.  Default value: none.

The ``refname`` attribute contains a reference to one of the `names`_ of
another element.

``refname`` is used by the `\<citation_reference>`_, `\<footnote_reference>`_,
`\<reference>`_, `\<substitution_reference>`_, and `\<target>`_ elements. [#]_

On a `\<target>`_ element, ``refname`` indicates an `indirect target`_
which may resolve to either an internal or external reference.
Docutils transforms_ replace the ``refname`` attribute with a refid_
pointing to the same element.

.. [#] Via the `%refname.att`_ and `%reference.atts`_ parameter entities.


``refuri``
==========

Attribute type: `CDATA`_.  Default value: none.

The ``refuri`` attribute contains an external reference to a URI.
It is used by the `\<target>`_, `\<reference>`_,
`\<footnote_reference>`_, and `\<citation_reference>`_ elements
(via the `%reference.atts`_ parameter entity).


``rowsep``
==========

Attribute type: `%yesorno`_.  Default value: none (implies no).

The ``rowsep`` attribute may be used in the `\<colspec>`_, `\<entry>`_,
`\<row>`_, `\<table>`_, and `\<tgroup>`_ elements to specify the presence
or absence of row separators (horizontal ruling).

The attribute is defined in the `Exchange Table Model`_ (which see
for details). It cannot be specified in reStructuredText and is
ignored by Docutils.


``rtrim``
=========

Attribute type: `%yesorno`_.  Default value: none (implies no).

The ``rtrim`` attribute is used in the `\<substitution_definition>`_ element.


``scale``
==========

Attribute type: `%number`_.  Default value: none.

The ``scale`` attribute is used in the `\<image>`_ element to store
a uniform scaling factor (integer percentage value).


``source``
==========

Attribute type: `CDATA`_.  Default value: none.

The ``source`` attribute is used to store the path or URI of the
source text that was used to produce the document tree.

It is one of the `common attributes`_, declared for all Docutils
elements but typically only used with the `\<document>`_ and
`\<system_message>`_ elements.

.. note:: All ``docutils.nodes.Node`` instances also support an
   *internal* ``source`` attribute that is used when reporting
   processing problems.


``start``
=========

Attribute type: `%number`_.  Default value: none (implies 1).

The ``start`` attribute is used in the `\<enumerated_list>`_ element to
store the ordinal value of the first item in the list, in decimal.

For lists beginning at value 1 ("1", "a", "A", "i", or "I"),
this attribute may be omitted.


``stub``
=========

Attribute type: `%yesorno`_.  Default value: none.

The ``stub`` attribute is used in the `\<colspec>`_ element to
mark a table column as containing *stubs* (row titles, on the left).
See also the `"csv-table"`_ and `"list-table"`_ directives.

The attribute is defined in the `%tbl.colspec.att`_ parameter
entity extending the `Exchange Table Model`_.


``suffix``
==========

Attribute type: `CDATA`_.  Default value: none.

The ``suffix`` attribute is used in the `\<enumerated_list>`_ element
to store the formatting characters used after the enumerator.

In documents originating from reStructuredText_ data, it will contain
either "." (period) or ")" (right parenthesis). Depending on the
capabilities of the output format, this attribute may or may not affect
processing.


.. _title attribute:

``title``
=========

Attribute type: `CDATA`_.  Default value: none.

The ``title`` attribute stores the *metadata title* of a `\<document>`_.
It is set by the `"title" directive`_ or the `DocTitle transform`_.
This title is typically not part of the rendered document.
It is, for example, used as `HTML <title> element`_ and shown in a
browser's title bar, in a user's history or bookmarks, or in search results.

.. _HTML <title> element:
    https://html.spec.whatwg.org/multipage/semantics.html#the-title-element

``type``
=========

Attribute type: NMTOKEN_.  Default value: none.

The ``type`` attribute is used in the `\<system_message>`_ element.


``uri``
=======

Attribute type: `CDATA`_.  Default value: none.

The ``uri`` attribute is used in the `\<image>`_ and `\<figure>`_
elements to refer to the image via a `URI Reference`_ (URI or
`relative reference`_).

.. _URI Reference: https://www.rfc-editor.org/rfc/rfc3986.html#section-4.1
.. _relative reference: https://www.rfc-editor.org/rfc/rfc3986.html#section-4.2


``valign``
==========

| Attribute type: `EnumeratedType`_ (top|middle|bottom).
| Default value: none (inherit).

The ``valign`` attribute is used in the `\<entry>`_, `\<row>`_,
`\<tbody>`_, and `\<thead>`_ elements to specify the vertical text
alignment within entries.

The attribute is defined in the `Exchange Table Model`_ (which see
for details). It cannot be specified in reStructuredText and is
ignored by Docutils.


``width``
==========

Attribute type: `%measure`_.  Default value: none.

The ``width`` attribute is used in the `\<figure>`_, `\<image>`_,
and `\<table>`_ elements.


``xml:space``
=============

| Attribute type: `EnumeratedType`_, one of "default" or "preserve".
| Default value: "preserve" (fixed).

The ``xml:space`` attribute is a standard XML attribute for
whitespace-preserving elements.  It is used by the `\<address>`_,
`\<comment>`_, `\<doctest_block>`_, `\<literal_block>`_, `\<math_block>`_,
and `\<raw>`_ elements (via the `%fixedspace.att`_ parameter entity).
It is a fixed attribute, meant to communicate to an XML parser that the
element contains significant whitespace.  The attribute value should not
be set in a document instance.

----------------------------
 Parameter Entity Reference
----------------------------

`Parameter entities`_ are used to simplify the DTD (to share definitions
and reduce duplication) and to allow the DTD to be customized by
wrapper DTDs (external client DTDs that use or import the Docutils
DTD).  Parameter entities may be overridden by wrapper DTDs, replacing
the definitions below with custom definitions.  Empty placeholder entities
whose names begin with "additional" are provided to allow easy extension
by wrapper DTDs.

.. _parameter entities: https://www.w3.org/TR/REC-xml/#dt-PE

.. contents:: :local:

In addition, the Docutils DTD defines parameter entities for
`custom attribute types`_.

Attribute Entities
==================

``%align-h.att``
----------------

The ``%align-h.att`` parameter entity contains the align_
attribute for horizontal alignment.

Entity definition::

    align (left | center | right) #IMPLIED

The `\<figure>`_ and `\<table>`_ elements directly employ the
``%align-h.att`` parameter entity in their attribute lists.


``%align-hv.att``
-----------------

The ``%align-hv.att`` parameter entity contains the align_
attribute for horizontal and vertical alignment.

Entity definition::

    align (top | middle | bottom | left | center | right) #IMPLIED

The `\<image>`_ element directly employs the ``%align-hv.att``
parameter entity in its attribute list.

``%anonymous.att``
------------------

The ``%anonymous.att`` parameter entity contains the anonymous_
attribute, used for unnamed hyperlinks.

Entity definition::

    anonymous %yesorno; #IMPLIED

The `\<reference>`_ and `\<target>`_ elements directly employ the
``%anonymous.att`` parameter entity in their attribute lists.


``%auto.att``
-------------

The ``%auto.att`` parameter entity contains the auto_ attribute, used
to indicate an automatically-numbered footnote or title.

Entity definition::

    auto CDATA #IMPLIED

The `\<footnote>`_, `\<footnote_reference>`_, and `\<title>`_ elements
directly employ the ``%auto.att`` parameter entity in their attribute
lists.


``%backrefs.att``
-----------------

The ``%backrefs.att`` parameter entity contains the backrefs_
attribute, a space-separated list of id references, for backlinks.

Entity definition::

    backrefs %idrefs.type; #IMPLIED

The `\<citation>`_, `\<footnote>`_, and `\<system_message>`_ elements
directly employ the ``%backrefs.att`` parameter entity in their
attribute lists.


``%basic.atts``
---------------

The ``%basic.atts`` parameter entity lists the `common attributes`_.

Entity definition:

.. parsed-literal::

    ids_      NMTOKENS  #IMPLIED
    names_    CDATA     #IMPLIED
    dupnames_ CDATA     #IMPLIED
    source_   CDATA     #IMPLIED
    classes_  NMTOKENS  #IMPLIED
    %additional.basic.atts;

The ``%additional.basic.atts`` parameter entity can be used by
wrapper DTDs to extend ``%basic.atts``.


``%bodyatt``
------------

The ``%bodyatt`` parameter entity is defined in the `Exchange Table Model`_
to allow customization of the `\<table>`_ element's attribute list.

The Docutils DTD redefines it to add align_, width_, and the `common
attributes`_.

.. note:: This parameter entity is only used for backward compatibility.
          Docutils versions >= 1.0 will use the ``%tbl.table.att``
          parameter entity instead.


``%fixedspace.att``
-------------------

The ``%fixedspace.att`` parameter entity contains the `xml:space`_
attribute, a standard XML attribute for whitespace-preserving
elements.

Entity definition::

    xml:space (default | preserve) #FIXED 'preserve'

The ``%fixedspace.att`` parameter entity is directly employed in the
attribute lists of the following elements: `\<address>`_, `\<comment>`_,
`\<doctest_block>`_, `\<literal_block>`_, `\<math_block>`_, `\<raw>`_.


``%reference.atts``
-------------------

The ``%reference.atts`` parameter entity groups together the refuri_,
refid_, and refname_ attributes.

Entity definition:

.. parsed-literal::

    `%refuri.att`_;
    `%refid.att`_;
    `%refname.att`_;
    %additional.reference.atts;

The ``%additional.reference.atts`` parameter entity can be used by
wrapper DTDs to extend ``%additional.reference.atts``.

The `\<citation_reference>`_, `\<footnote_reference>`_, `\<reference>`_,
and `\<target>`_ elements directly employ the ``%reference.att``
parameter entity in their attribute lists.


``%refid.att``
--------------

The ``%refid.att`` parameter entity contains the refid_ attribute, an
internal reference to the `ids`_ attribute of another element.

Entity definition::

    refid %idref.type; #IMPLIED

The `\<title>`_ and `\<problematic>`_ elements directly employ the
``%refid.att`` parameter entity in their attribute lists.

Via `%reference.atts`_, the ``%refid.att`` parameter entity is
indirectly employed in the attribute lists of the `\<citation_reference>`_,
`\<footnote_reference>`_, `\<reference>`_, and `\<target>`_ elements.


``%refname.att``
----------------

The ``%refname.att`` parameter entity contains the refname_
attribute, an internal reference to the `names`_ attribute of another
element.  On a `\<target>`_ element, ``refname`` indicates an indirect
target which may resolve to either an internal or external
reference.

Entity definition::

    refname %refname.type; #IMPLIED

The `\<substitution_reference>`_ element directly employs the
``%refname.att`` parameter entity in its attribute list.

Via `%reference.atts`_, the ``%refname.att`` parameter entity is
indirectly employed in the attribute lists of the `\<citation_reference>`_,
`\<footnote_reference>`_, `\<reference>`_, and `\<target>`_ elements.


``%refuri.att``
---------------

The ``%refuri.att`` parameter entity contains the refuri_ attribute,
an external reference to a URI.

Entity definition::

    refuri CDATA #IMPLIED

Via `%reference.atts`_, the ``%refuri.att`` parameter entity is
indirectly employed in the attribute lists of the `\<citation_reference>`_,
`\<footnote_reference>`_, `\<reference>`_, and `\<target>`_ elements.

``%tbl.colspec.att``
--------------------

The ``%tbl.colspec.att`` parameter entity is defined in the
`Exchange Table Model`_ to allow customization of the `\<colspec>`_
element's attribute list.

The Docutils DTD redefines it to add stub_ and the `common attributes`_.


``%tbl.entry.att``
------------------

The ``%tbl.entry.att`` parameter entity is defined in the
`Exchange Table Model`_ to allow customization of the `\<entry>`_
element's attribute list.

The Docutils DTD redefines it to add morecols_ and the `common attributes`_.


``%tbl.row.att``
----------------

The ``%tbl.row.att`` parameter entity is defined in the
`Exchange Table Model`_ to allow customization of the `\<row>`_
element's attribute list.

The Docutils DTD redefines it to add the `common attributes`_.


``%tbl.tbody.att``
------------------

The ``%tbl.tbody.att`` parameter entity is defined in the
`Exchange Table Model`_ to allow customization of the `\<tbody>`_
element's attribute list.

The Docutils DTD redefines it to add the `common attributes`_.


``%tbl.tgroup.att``
-------------------

The ``%tbl.tgroup.att`` parameter entity is defined in the
`Exchange Table Model`_ to allow customization of the `\<tgroup>`_
element's attribute list.

The Docutils DTD redefines it to add the `common attributes`_.


``%tbl.thead.att``
------------------

The ``%tbl.thead.att`` parameter entity is defined in the
`Exchange Table Model`_ to allow customization of the `\<thead>`_
element's attribute list.

The Docutils DTD redefines it to add the `common attributes`_.


Element Category Entities
=========================

``%bibliographic.elements``
---------------------------

The ``%bibliographic.elements`` parameter entity contains an OR-list of all
`Bibliographic Elements`_.

The ``%additional.bibliographic.elements`` parameter entity can be used by
wrapper DTDs to extend ``%bibliographic.elements``.

Only the `\<docinfo>`_ element directly employs the
``%bibliographic.elements`` parameter entity in its content model.


``%body.elements``
------------------

The ``%body.elements`` parameter entity contains an OR-list of all
`Body Elements`_.

The ``%additional.body.elements`` parameter entity can be used by
wrapper DTDs to extend ``%body.elements``.

The ``%body.elements`` parameter entity is directly employed in the
content models of the following elements: `\<admonition>`_,
`\<attention>`_, `\<block_quote>`_, `\<caution>`_, `\<citation>`_,
`\<compound>`_, `\<danger>`_, `\<definition>`_, `\<description>`_,
`\<entry>`_, `\<error>`_, `\<field_body>`_, `\<footer>`_, `\<footnote>`_,
`\<header>`_, `\<hint>`_, `\<important>`_, `\<legend>`_, `\<list_item>`_,
`\<note>`_, `\<sidebar>`_, `\<system_message>`_, `\<tip>`_, `\<topic>`_,
and `\<warning>`_

Via `%structure.model`_, the ``%body.elements`` parameter entity is
indirectly employed in the content models of the `\<document>`_ and
`\<section>`_ elements.


``%inline.elements``
--------------------

The ``%inline.elements`` parameter entity contains an OR-list of all
`Inline Elements`_.

The ``%additional.inline.elements`` parameter entity can be used by
wrapper DTDs to extend ``%inline.elements``.

The ``%inline.elements`` parameter entity is employed in the
`%text.model`_ parameter entity.


``%section.elements``
---------------------

The ``%section.elements`` parameter entity contains the `\<section>`_
element.

The ``%additional.section.elements`` parameter entity can be used
by wrapper DTDs to extend ``%section.elements``.

Via `%structure.model`_, the ``%section.elements`` parameter entity
is indirectly employed in the content models of the `\<document>`_ and
`\<section>`_ elements.


Model Entities
==============

%calstblx
---------

The ``%calstblx`` parameter entity is used to include the `XML Exchange
Table Model DTD` [tm9901]_ as `external DTD subset`_ defining the table
elements `\<colspec>`_, `\<entry>`_, `\<row>`_, `\<table>`_, `\<tbody>`_,
`\<tgroup>`_, and `\<thead>`_.

Entity definition::

    <!ENTITY % calstblx PUBLIC
        "-//OASIS//DTD XML Exchange Table Model 19990315//EN"
        "soextblx.dtd">



``%structure.model``
--------------------

The ``%structure.model`` parameter entity encapsulates the
hierarchical structure of a document and of its constituent parts.
See the discussion of the `element hierarchy`_ above.

Simplified entity definition:

.. parsed-literal::

   ( ( `%body.elements`_; | topic | sidebar | transition )*,
     ( `%section.elements`_; | transition )* )

Each `\<document>`_ or `\<section>`_ contains zero or more
body elements, topics, sidebars, or transitions,
followed by zero or more sections (whose contents include this model),
or transitions.

The actual entity definition is more complex,

.. parsed-literal::

   ( ( (`%body.elements`_; | topic | sidebar)+, transition? )*,
     ( (`%section.elements`_;),
       (transition?, (`%section.elements`_;) )* )? )

to impose the following restrictions:

* A `\<transition>`_ may not be the first element (i.e. it may
  not occur at the beginning of a document or directly after
  a title, subtitle, meta or decoration element).

* Transitions must be separated by other elements (body elements,
  sections, etc.).  In other words, a transition may not be
  immediately adjacent to another transition.

An additional restriction cannot be expressed in the language of DTDs: [#]_

* A transition may not occur at the end of a document or section.

The ``%structure.model`` parameter entity is directly employed in the
content models of the `\<document>`_ and `\<section>`_ elements.

.. [#] Docutils imposes it in the `misc.Transitions` transform_.


``%tbl.entry.mdl``
-------------------

The ``%tbl.entry.mdl`` parameter entity is defined in
the `Exchange Table Model`_ to allow customization of
the `\<entry>`_ element's content model.

The Docutils DTD changes it to allow all `body elements`_
(including nested tables)::

    (%body.elements;)*


``%tbl.tgroup.mdl``
-------------------

The ``%tbl.tgroup.mdl`` parameter entity is defined in the
`Exchange Table Model`_ to allow customization of the `\<tgroup>`_
element's content model.

The Docutils DTD changes it to require at least one <colspec> element::

    colspec+,thead?,tbody


``%text.model``
---------------

The ``%text.model`` parameter entity is used by `simple elements`_ to
represent text data mixed with `inline elements`_.

Entity definition:

.. parsed-literal::

    (#PCDATA | `%inline.elements`_;)*

The ``%text.model`` parameter entity is directly employed in the content
models of the following elements: `\<abbreviation>`_,
`\<acronym>`_, `\<address>`_, `\<attribution>`_, `\<author>`_,
`\<caption>`_, `\<classifier>`_, `\<contact>`_, `\<copyright>`_,
`\<date>`_, `\<doctest_block>`_, `\<emphasis>`_, `\<field_name>`_,
`\<generated>`_, `\<inline>`_, `\<line>`_, `\<literal>`_,  `\<literal_block>`_,
`\<organization>`_, `\<paragraph>`_, `\<problematic>`_,
`\<reference>`_, `\<revision>`_, `\<rubric>`_,
`\<status>`_, `\<strong>`_, `\<subscript>`_, `\<substitution_definition>`_,
`\<substitution_reference>`_, `\<subtitle>`_, `\<superscript>`_,
`\<target>`_, `\<term>`_, `\<title>`_, `\<title_reference>`_, `\<version>`_


------------
Bibliography
------------

.. [DocBook5.1] `DocBook 5.1: The Definitive Guide`,
                Norman Walsh,
                https://tdg.docbook.org/tdg/5.1/.


.. [html.spec]  `HTML Living Standard`,
                WHATWG (Apple, Google, Mozilla, Microsoft),
                https://html.spec.whatwg.org.

.. [xml1.0]    `Extensible Markup Language (XML) 1.0`,

.. [tm9901]     .. _XML Exchange Table Model DTD:
                .. _Exchange Table Model:

                `XML Exchange Table Model DTD`,
                OASIS Technical Memorandum 9901:1999,
                http://www.oasis-open.org/html/tm9901.html.
                W3C Recommendation,
                https://www.w3.org/TR/xml/.

.. _DocBook: https://tdg.docbook.org/tdg/5.1/.
.. _DocBook <caution>: https://tdg.docbook.org/tdg/5.1/caution.html
.. _DocBook <footnote>: https://tdg.docbook.org/tdg/5.1/footnote.html
.. _DocBook <footnoteref>: https://tdg.docbook.org/tdg/5.1/footnoteref.html
.. _DocBook <imagedata>: https://tdg.docbook.org/tdg/5.1/imagedata
.. _DocBook <important>: https://tdg.docbook.org/tdg/5.1/important.html
.. _DocBook <note>: https://tdg.docbook.org/tdg/5.1/note.html
.. _DocBook <tip>: https://tdg.docbook.org/tdg/5.1/tip.html
.. _DocBook <warning>: https://tdg.docbook.org/tdg/5.1/warning.html

.. _HTML: https://html.spec.whatwg.org/multipage/.

.. _Python: https://www.python.org/

.. _XML: https://developer.mozilla.org/en-US/docs/Web/XML/XML_introduction
.. _Introducing the Extensible Markup Language (XML):
    http://xml.coverpages.org/xmlIntro.html
.. _XMLSpec: https://www.w3.org/XML/1998/06/xmlspec-report.htm
.. _external DTD subset: https://www.w3.org/TR/xml11/#dt-doctype
.. _XML attribute types: https://www.w3.org/TR/REC-xml/#sec-attribute-types
.. _One ID per Element Type: https://www.w3.org/TR/REC-xml/#one-id-per-el


.. _Docutils: https://docutils.sourceforge.io/.
.. _reStructuredText: https://docutils.sourceforge.io/rst.html

.. _docutils.nodes: https://docutils.sourceforge.io/docutils/nodes.py

.. _Docutils Generic DTD:
.. _Docutils DTD:
.. _docutils.dtd: docutils.dtd

.. _auto_id_prefix: ../user/config.html#auto-id-prefix
.. _datestamp:      ../user/config.html#datestamp
.. _id_prefix:      ../user/config.html#id-prefix
.. _image_loading:  ../user/config.html#image-loading
.. _stylesheet:     ../user/config.html#stylesheet

.. _transform:
.. _transforms:         ../api/transforms.html
.. _DocInfo transform:  ../api/transforms.html#docinfo
.. _DocTitle transform: ../api/transforms.html#doctitle

.. _A ReStructuredText Primer: ../user/rst/quickstart.html
.. _reStructuredText Markup Specification: rst/restructuredtext.html
.. _bibliographic data:
.. _bibliographic fields:   rst/restructuredtext.html#bibliographic-fields
.. _block quote:            rst/restructuredtext.html#block-quotes
.. _bullet list:            rst/restructuredtext.html#bullet-lists
.. _citations:              rst/restructuredtext.html#citations
.. _definition list:        rst/restructuredtext.html#definition-lists
.. _directive:              rst/restructuredtext.html#directives
.. _doctest block:          rst/restructuredtext.html#doctest-blocks
.. _emphasis markup:        rst/restructuredtext.html#emphasis
.. _enumerated list:        rst/restructuredtext.html#enumerated-lists
.. _explicit markup blocks: rst/restructuredtext.html#explicit-markup-blocks
.. _footnote reference:     rst/restructuredtext.html#footnote-references
.. _grid table:             rst/restructuredtext.html#grid-tables
.. _indirect target:      rst/restructuredtext.html#indirect-hyperlink-targets
.. _internal hyperlink targets:
                          rst/restructuredtext.html#internal-hyperlink-targets
.. _line block:             rst/restructuredtext.html#line-blocks
.. _literal block:          rst/restructuredtext.html#literal-blocks
.. _footnotes:
.. _footnote:               rst/restructuredtext.html#footnotes
.. _hyperlinks:             rst/restructuredtext.html#hyperlinks
.. _option list:            rst/restructuredtext.html#option-lists
.. _RCS Keywords:           rst/restructuredtext.html#rcs-keywords
.. _rST document:           rst/restructuredtext.html#document
.. _reStructuredText field list:
.. _rST field list:         rst/restructuredtext.html#field-lists
.. _rST reference names:    rst/restructuredtext.html#reference-names
.. _rST tables:             rst/restructuredtext.html#tables
.. _section:                rst/restructuredtext.html#sections
.. _simple table:           rst/restructuredtext.html#simple-tables
.. _strong emphasis:        rst/restructuredtext.html#strong-emphasis
.. _substitution definition:
.. _substitutions:          rst/restructuredtext.html#substitution-definitions
.. _transition:             rst/restructuredtext.html#transitions

.. _standard role:              rst/roles.html
.. _"abbreviation" role:        rst/roles.html#abbreviation
.. _"acronym" role:             rst/roles.html#acronym
.. _"raw" role:                 rst/roles.html#raw
.. _"subscript" role:           rst/roles.html#subscript
.. _"superscript" role:         rst/roles.html#superscript
.. _"title-reference" role:     rst/roles.html#title-reference

.. _"admonition" directive:     rst/directives.html#admonition
.. _"attention" directive:      rst/directives.html#attention
.. _"caution" directive:        rst/directives.html#caution
.. _"class" directive:          rst/directives.html#class
.. _class option:               rst/directives.html#class-option
.. _"code" directive:           rst/directives.html#code
.. _"compound" directive:       rst/directives.html#compound-paragraph
.. _"container" directive:      rst/directives.html#container
.. _"contents" directive:
.. _table of contents:          rst/directives.html#table-of-contents
.. _"csv-table":                rst/directives.html#csv-table
.. _"danger" directive:         rst/directives.html#danger
.. _"error" directive:          rst/directives.html#error
.. _"footer" directive:         rst/directives.html#footer
.. _"header" directive:         rst/directives.html#header
.. _"hint" directive:           rst/directives.html#hint
.. _identifier normalization:   rst/directives.html#identifier-normalization
.. _"image" directive:          rst/directives.html#image
.. _"important" directive:      rst/directives.html#important
.. _"list-table":               rst/directives.html#list-table
.. _"math" directive:           rst/directives.html#math
.. _"meta" directive:           rst/directives.html#meta
.. _name option:                rst/directives.html#name
.. _"note" directive:           rst/directives.html#note
.. _"parsed-literal" directive: rst/directives.html#parsed-literal
.. _"raw" directive:            rst/directives.html#raw
.. _"sidebar" directive:        rst/directives.html#sidebar
.. _"table" directive:          rst/directives.html#table
.. _"tip" directive:            rst/directives.html#tip
.. _"topic" directive:          rst/directives.html#topic
.. _"title" directive:          rst/directives.html#title
.. _"warning" directive:        rst/directives.html#admonition
.. _custom interpreted text roles:
    rst/directives.html#custom-interpreted-text-roles
.. _table of compatible image formats: rst/directives.html#image-formats


.. Emacs settings

   Local Variables:
   mode: indented-text
   indent-tabs-mode: nil
   sentence-end-double-space: t
   fill-column: 70
   End:
