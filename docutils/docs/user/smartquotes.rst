.. include:: ../header.rst

=========================
Smart Quotes for Docutils
=========================

:Author: Günter Milde,
         based on SmartyPants by John Gruber, Brad Choate, and Chad Miller
:Contact: docutils-develop@lists.sourceforge.net
:Revision: $Revision$
:Date: $Date$
:License: Released under the terms of the `2-Clause BSD license`_
:Abstract: This document describes the Docutils `smartquotes` module.

.. _2-Clause BSD license: http://opensource.org/licenses/BSD-2-Clause

.. contents::

Description
===========

The `"smart_quotes" configuration setting`_ triggers the SmartQuotes
transformation on Text nodes that includes the following steps:

- Straight quotes (``"`` and ``'``) into "curly" quote characters
- dashes (``--`` and ``---``) into en- and em-dash entities
- three consecutive dots (``...`` or ``. . .``) into an ellipsis entity.

This means you can write, edit, and save your documents using plain old
ASCII -- straight quotes, plain dashes, and plain dots -- while Docutils
generates documents with typographical quotes, dashes, and ellipses.

Advantages:

* Typing speed (especially when blind-typing).
* The possibility to change the quoting style of the
  complete document with just one configuration option.
* Typographical quotes with just 7-bit ASCII characters in the source.

However, there are `algorithmic shortcomings`_ for 2 reasons:

* Dual use of the "ASCII-apostrophe" (') as single quote and apostrophe.
* Languages that do not use whitespace around words.

So, please consider also
`Why You Might Not Want to Use "Smart" Quotes in Your Documents`_.

.. _"smart_quotes" configuration setting:
.. _"smart_quotes" setting: config.html#smart-quotes


Escaping
========

The `SmartQuotes` transform does not modify characters in literal text
such as source code, maths, or literal blocks.

If you need literal straight quotes (or plain hyphens and periods) in normal
text, you can `backslash escape`_ the characters to preserve
ASCII-punctuation.

.. class:: booktabs

=========  ========= == ========  ==========
Input      Output       Input     Output
=========  ========= == ========  ==========
``\\``     \\           ``\...``  \...
``\"``     \"           ``\--``   \--
``\'``     \'           ``\```    \`
=========  ========= == ========  ==========

This is useful, for example, when you want to use straight quotes as
foot and inch marks:

  6\'2\" tall; a 17\" monitor.

.. _backslash escape: ../ref/rst/restructuredtext.html#escaping-mechanism


Localization
============

Quotation marks have a `variety of forms`__ in different languages and
media.

__ https://en.wikipedia.org/wiki/Quotation_mark#Summary_table

`SmartQuotes` inserts quotation marks depending on the language of the
current block element and the value of the `"smart_quotes" setting`_.\
[#x-altquot]_
There is built-in support for the following languages:\ [#smartquotes-locales]_

.. class:: run-in

:af: .. class:: language-af

    "'Afrikaans' quotes"

:af-x-altquot: .. class:: language-af-x-altquot

    "'Afrikaans' alternative quotes"

:ca: .. class:: language-ca

    "'Catalan' quotes"

:ca-x-altquot: .. class:: language-ca-x-altquot

    "'Catalan' alternative quotes"

:cs: .. class:: language-cs

    "'Czech' quotes"

:cs-x-altquot: .. class:: language-cs-x-altquot

    "'Czech' alternative quotes"

:da: .. class:: language-da

    "'Danish' quotes"

:da-x-altquot: .. class:: language-da-x-altquot

    "'Danish' alternative quotes"

:de: .. class:: language-de

    "'German' quotes"

:de-x-altquot: .. class:: language-de-x-altquot

    "'German' alternative quotes"

:de-ch: .. class:: language-de-ch

    "'Swiss-German' quotes"

:el: .. class:: language-el

    "'Greek' quotes"

:en: .. class:: language-en

    "'English' quotes"

:en-uk-x-altquot: .. class:: language-en-uk-x-altquot

    "'British' alternative quotes" (swaps single and double quotes)

:eo: .. class:: language-eo

    "'Esperanto' quotes"

:es: .. class:: language-es

    "'Spanish' quotes"

:es-x-altquot: .. class:: language-es-x-altquot

    "'Spanish' alternative quotes"

:et: .. class:: language-et

    "'Estonian' quotes" (no secondary quote listed in Wikipedia)

:et-x-altquot: .. class:: language-et-x-altquot

    "'Estonian' alternative quotes"

:eu: .. class:: language-eu

    "'Basque' quotes"

:fi: .. class:: language-fi

    "'Finnish' quotes"

:fi-x-altquot: .. class:: language-fi-x-altquot

    "'Finnish' alternative quotes"

:fr: .. class:: language-fr

    "'French' quotes"

:fr-x-altquot: .. class:: language-fr-x-altquot

    "'French' alternative quotes"

:fr-ch: .. class:: language-fr-ch

    "'Swiss-French' quotes"

:fr-ch-x-altquot: .. class:: language-fr-ch-x-altquot

    "'Swiss-French' alternative quotes" (narrow no-break space, see
    http://typoguide.ch/)

:gl: .. class:: language-gl

    "'Galician' quotes"

:he: .. class:: language-he

    "'Hebrew' quotes"

:he-x-altquot: .. class:: language-he-x-altquot

    "'Hebrew' alternative quotes"

:hr: .. class:: language-hr

    "'Croatian' quotes"

:hr-x-altquot: .. class:: language-hr-x-altquot

    "'Croatian' alternative quotes"

:hsb: .. class:: language-hsb

    "'Upper Sorbian' quotes"

:hsb-x-altquot: .. class:: language-hsb-x-altquot

    "'Upper Sorbian' alternative quotes"

:hu: .. class:: language-hu

    "'Hungarian' quotes"

:is: .. class:: language-is

    "'Icelandic' quotes"

:it: .. class:: language-it

    "'Italian' quotes"

:it-ch: .. class:: language-it-ch

    "'Swiss-Italian' quotes"

:it-x-altquot: .. class:: language-it-x-altquot

    "'Italian' alternative quotes"

:ja: .. class:: language-ja

    "'Japanese' quotes"

:lt: .. class:: language-lt

    "'Lithuanian' quotes"

:lv: .. class:: language-lv

    "'Latvian' quotes"

:nl: .. class:: language-nl

    "'Dutch' quotes"

:nl-x-altquot: .. class:: language-nl-x-altquot

    "'Dutch' alternative quotes"

    .. # 'nl-x-altquot2': '””’’',

:pl: .. class:: language-pl

    "'Polish' quotes"

:pl-x-altquot: .. class:: language-pl-x-altquot

    "'Polish' alternative quotes"

:pt: .. class:: language-pt

    "'Portuguese' quotes"

:pt-br: .. class:: language-pt-br

    "'Portuguese (Brazil)' quotes"

:ro: .. class:: language-ro

    "'Romanian' quotes"

:ru: .. class:: language-ru

    "'Russian' quotes"

:sh: .. class:: language-sh

    "'Serbo-Croatian' quotes"

:sh-x-altquot: .. class:: language-sh-x-altquot

    "'Serbo-Croatian' alternative quotes"

:sk: .. class:: language-sk

    "'Slovak' quotes"

:sk-x-altquot: .. class:: language-sk-x-altquot

    "'Slovak' alternative quotes"

:sl: .. class:: language-sl

    "'Slovenian' quotes"

:sl-x-altquot: .. class:: language-sl-x-altquot

    "'Slovenian' alternative quotes"

:sr: .. class:: language-sr

    "'Serbian' quotes"

:sr-x-altquot: .. class:: language-sr-x-altquot

    "'Serbian' alternative quotes"

:sv: .. class:: language-sv

    "'Swedish' quotes"

:sv-x-altquot: .. class:: language-sv-x-altquot

    "'Swedish' alternative quotes"

:tr: .. class:: language-tr

    "'Turkish' quotes"

:tr-x-altquot: .. class:: language-tr-x-altquot

    "'Turkish' alternative quotes"

.. 'tr-x-altquot2': '“„‘‚', # antiquated?

:uk: .. class:: language-uk

    "'Ukrainian' quotes"

:uk-x-altquot: .. class:: language-uk-x-altquot

    "'Ukrainian' alternative quotes"

:zh-cn: .. class:: language-zh-cn

    "'Chinese (China)' quotes"

:zh-tw: .. class:: language-zh-tw

    "'Chinese (Taiwan)' quotes"

Quotes in text blocks in a non-configured language are kept as plain quotes:

:undefined: .. class:: language-undefined-example

    "'Undefined' quotes"

.. [#x-altquot] Tags with the non-standard extension ``-x-altquot`` define
   the quote set used with the `"smart_quotes" setting`_ value ``"alt"``.

.. [#smartquotes-locales] The definitions for language-dependend
   typographical quotes can be extended or overwritten using the
   `"smartquotes_locales" setting`_.

   The following example ensures a correct leading apostrophe in ``'s
   Gravenhage`` (at the cost of incorrect leading single quotes) in Dutch
   and sets French quotes to double and single guillemets with inner
   spacing::

     smartquote-locales: nl: „”’’
                         fr: « : »:‹ : ›

.. _"smartquotes_locales" setting: config.html#smartquotes-locales


Caveats
=======

Why You Might Not Want to Use "Smart" Quotes in Your Documents
--------------------------------------------------------------

For one thing, you might not care.

Most normal, mentally stable individuals do not take notice of proper
typographic punctuation. Many design and typography nerds, however, break
out in a nasty rash when they encounter, say, a restaurant sign that uses
a straight apostrophe to spell "Joe's".

If you're the sort of person who just doesn't care, you might well want to
continue not caring. Using straight quotes -- and sticking to the 7-bit
ASCII character set in general -- is certainly a simpler way to live.

Even if you *do* care about accurate typography, you still might want to
think twice before "auto-educating" the quote characters in your documents.
As there is always a chance that the algorithm gets it wrong, you may
instead prefer to use the compose key or some other means to insert the
correct Unicode characters into the source.


Algorithmic Shortcomings
------------------------

The ASCII character (u0027 APOSTROPHE) is used for apostrophe and single
quotes. If used inside a word, it is converted into an apostrophe:

   .. class:: language-fr

   Il dit : "C'est 'super' !"

At the beginning or end of a word, it cannot be distinguished from a single
quote by the algorithm.

The `right single quotation mark`_ character -- used to close a secondary
(inner) quote in English -- is also "the preferred character to use for
apostrophe" (Unicode_). Therefore, "educating" works as expected for
apostrophes at the end of a word, e.g.,

  Mr. Hastings' pen; three days' leave; my two cents' worth.

However, when apostrophes are used at the start of leading contractions,
"educating" will turn the apostrophe into an *opening* secondary quote. In
English, this is *not* the apostrophe character, e.g., ``'Twas brillig``
is "miseducated" to

  'Twas brillig.

In other locales (French, Italian, German, ...), secondary closing quotes
differ from the apostrophe. A text like::

   .. class:: language-de-CH

   "Er sagt: 'Ich fass' es nicht.'"

becomes

   «Er sagt: ‹Ich fass› es nicht.›»

with a single closing guillemet in place of the apostrophe.

In such cases, it's best to use the recommended apostrophe character (’) in
the source:

   | ’Twas brillig, and the slithy toves
   | Did gyre and gimble in the wabe;
   | All mimsy were the borogoves,
   | And the mome raths outgrabe.

.. _right single quotation mark:
    http://www.fileformat.info/info/unicode/char/2019/index.htm
.. _Unicode: https://www.unicode.org/charts/PDF/U2000.pdf

History
=======

The smartquotes module is an adaption of "SmartyPants_" to Docutils.

`John Gruber`_ did all of the hard work of writing this software in Perl for
`Movable Type`_ and almost all of this useful documentation.  `Chad Miller`_
ported it to Python to use with Pyblosxom_.

Portions of the SmartyPants original work are based on Brad Choate's nifty
MTRegex plug-in.  `Brad Choate`_ also contributed a few bits of source code to
this plug-in.  Brad Choate is a fine hacker indeed.
`Jeremy Hedley`_ and `Charles Wiltgen`_ deserve mention for exemplary beta
testing of the original SmartyPants.

Internationalization and adaption to Docutils by Günter Milde.

.. _SmartyPants: http://daringfireball.net/projects/smartypants/
.. _Pyblosxom: http://pyblosxom.bluesock.org/
.. _Movable Type: http://www.movabletype.org/
.. _John Gruber: http://daringfireball.net/
.. _Chad Miller: http://web.chad.org/
.. _Brad Choate: http://bradchoate.com/
.. _Jeremy Hedley: http://antipixel.com/
.. _Charles Wiltgen: http://playbacktime.com/
.. _Rael Dornfest: http://raelity.org/
