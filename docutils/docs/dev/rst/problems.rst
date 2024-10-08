.. include:: ../../header2.rst

==============================
 Problems With StructuredText
==============================
:Author: David Goodger
:Contact: docutils-develop@lists.sourceforge.net
:Revision: $Revision$
:Date: $Date$
:Copyright: This document has been placed in the public domain.

There are several problems, unresolved issues, and areas of
controversy within StructuredText_ (Classic and Next Generation).  In
order to resolve all these issues, this analysis brings all of the
issues out into the open, enumerates all the alternatives, and
proposes solutions to be incorporated into the reStructuredText_
specification.


.. contents::


Formal Specification
====================

The description in the original StructuredText.py has been criticized
for being vague.  For practical purposes, "the code *is* the spec."
Tony Ibbs has been working on deducing a `detailed description`_ from
the documentation and code of StructuredTextNG_.  Edward Loper's
STMinus_ is another attempt to formalize a spec.

For this kind of a project, the specification should always precede
the code.  Otherwise, the markup is a moving target which can never be
adopted as a standard.  Of course, a specification may be revised
during lifetime of the code, but without a spec there is no visible
control and thus no confidence.


Understanding and Extending the Code
====================================

The original StructuredText_ is a dense mass of sparsely commented
code and inscrutable regular expressions.  It was not designed to be
extended and is very difficult to understand.  StructuredTextNG_ has
been designed to allow input (syntax) and output extensions, but its
documentation (both internal [comments & docstrings], and external) is
inadequate for the complexity of the code itself.

For reStructuredText to become truly useful, perhaps even part of
Python's standard library, it must have clear, understandable
documentation and implementation code.  For the implementation of
reStructuredText to be taken seriously, it must be a sterling example
of the potential of docstrings; the implementation must practice what
the specification preaches.


Section Structure via Indentation
=================================

Setext_ required that body text be indented by 2 spaces.  The original
StructuredText_ and StructuredTextNG_ require that section structure
be indicated through indentation, as "inspired by Python".  For
certain structures with a very limited, local extent (such as lists,
block quotes, and literal blocks), indentation naturally indicates
structure or hierarchy.  For sections (which may have a very large
extent), structure via indentation is unnecessary, unnatural and
ambiguous.  Rather, the syntax of the section title *itself* should
indicate that it is a section title.

The original StructuredText states that "A single-line paragraph whose
immediately succeeding paragraphs are lower level is treated as a
header." Requiring indentation in this way is:

- Unnecessary.  The vast majority of docstrings and standalone
  documents will have no more than one level of section structure.
  Requiring indentation for such docstrings is unnecessary and
  irritating.

- Unnatural.  Most published works use title style (type size, face,
  weight, and position) and/or section/subsection numbering rather
  than indentation to indicate hierarchy.  This is a tradition with a
  very long history.

- Ambiguous.  A StructuredText header is indistinguishable from a
  one-line paragraph followed by a block quote (precluding the use of
  block quotes).  Enumerated section titles are ambiguous (is it a
  header? is it a list item?).  Some additional adornment must be
  required to confirm the line's role as a title, both to a parser and
  to the human reader of the source text.

Python's use of significant whitespace is a wonderful (if not
original) innovation, however requiring indentation in ordinary
written text is hypergeneralization.

reStructuredText_ indicates section structure through title adornment
style (as exemplified by this document).  This is far more natural.
In fact, it is already in widespread use in plain text documents,
including in Python's standard distribution (such as the toplevel
README_ file).


Character Escaping Mechanism
============================

No matter what characters are chosen for markup, some day someone will
want to write documentation *about* that markup or using markup
characters in a non-markup context.  Therefore, any complete markup
language must have an escaping or encoding mechanism.  For a
lightweight markup system, encoding mechanisms like SGML/XML's '&ast;'
are out.  So an escaping mechanism is in.  However, with carefully
chosen markup, it should be necessary to use the escaping mechanism
only infrequently.

reStructuredText_ needs an escaping mechanism: a way to treat
markup-significant characters as the characters themselves.  Currently
there is no such mechanism (although ZWiki uses '!').  What are the
candidates?

1. ``!``
   (http://www.zope.org/DevHome/Members/jim/StructuredTextWiki/NGEscaping)
2. ``\``
3. ``~``
4. doubling of characters

The best choice for this is the backslash (``\``).  It's "the single
most popular escaping character in the world!", therefore familiar and
unsurprising.  Since characters only need to be escaped under special
circumstances, which are typically those explaining technical
programming issues, the use of the backslash is natural and
understandable.  Python docstrings can be raw (prefixed with an 'r',
as in 'r""'), which would obviate the need for gratuitous doubling-up
of backslashes.

(On 2001-03-29 on the Doc-SIG mailing list, GvR endorsed backslash
escapes, saying, "'nuff said.  Backslash it is." Although neither
legally binding nor irrevocable nor any kind of guarantee of anything,
it is a good sign.)

The rule would be: An unescaped backslash followed by any markup
character escapes the character.  The escaped character represents the
character itself, and is prevented from playing a role in any markup
interpretation.  The backslash is removed from the output.  A literal
backslash is represented by an "escaped backslash," two backslashes in
a row.

A carefully constructed set of recognition rules for inline markup
will obviate the need for backslash-escapes in almost all cases; see
`Delimitation of Inline Markup`_ below.

When an expression (requiring backslashes and other characters used
for markup) becomes too complicated and therefore unreadable, a
literal block may be used instead.  Inside literal blocks, no markup
is recognized, therefore backslashes (for the purpose of escaping
markup) become unnecessary.

We could allow backslashes preceding non-markup characters to remain
in the output.  This would make describing regular expressions and
other uses of backslashes easier.  However, this would complicate the
markup rules and would be confusing.


Blank Lines in Lists
====================

Oft-requested in Doc-SIG (the earliest reference is dated 1996-08-13)
is the ability to write lists without requiring blank lines between
items.  In docstrings, space is at a premium.  Authors want to convey
their API or usage information in as compact a form as possible.
StructuredText_ requires blank lines between all body elements,
including list items, even when boundaries are obvious from the markup
itself.

In reStructuredText, blank lines are optional between list items.
However, in order to eliminate ambiguity, a blank line is required
before the first list item and after the last.  Nested lists also
require blank lines before the list start and after the list end.


Bullet List Markup
==================

StructuredText_ includes 'o' as a bullet character.  This is dangerous
and counter to the language-independent nature of the markup.  There
are many languages in which 'o' is a word.  For example, in Spanish::

    Llamame a la casa
    o al trabajo.

    (Call me at home or at work.)

And in Japanese (when romanized)::

    Senshuu no doyoubi ni tegami
    o kakimashita.

    ([I] wrote a letter on Saturday last week.)

If a paragraph containing an 'o' word wraps such that the 'o' is the
first text on a line, or if a paragraph begins with such a word, it
could be misinterpreted as a bullet list.

In reStructuredText_, 'o' is not used as a bullet character.  '-',
'*', and '+' are the possible bullet characters.


Enumerated List Markup
======================

StructuredText enumerated lists are allowed to begin with numbers and
letters followed by a period or right-parenthesis, then whitespace.
This has surprising consequences for writing styles.  For example,
this is recognized as an enumerated list item by StructuredText::

    Mr. Creosote.

People will write enumerated lists in all different ways.  It is folly
to try to come up with the "perfect" format for an enumerated list,
and limit the docstring parser's recognition to that one format only.

Rather, the parser should recognize a variety of enumerator styles.
It is also recommended that the enumerator of the first list item be
ordinal-1 ('1', 'A', 'a', 'I', or 'i'), as output formats may not be
able to begin a list at an arbitrary enumeration.

An initial idea was to require two or more consistent enumerated list
items in a row.  This idea proved impractical and was dropped.  In
practice, the presence of a proper enumerator is enough to reliably
recognize an enumerated list item; any ambiguities are reported by the
parser.  Here's the original idea for posterity:

    The parser should recognize a variety of enumerator styles, mark
    each block as a potential enumerated list item (PELI), and
    interpret the enumerators of adjacent PELIs to decide whether they
    make up a consistent enumerated list.

    If a PELI is labeled with a "1.", and is immediately followed by a
    PELI labeled with a "2.", we've got an enumerated list.  Or "(A)"
    followed by "(B)".  Or "i)" followed by "ii)", etc.  The chances
    of accidentally recognizing two adjacent and consistently labeled
    PELIs, are acceptably small.

    For an enumerated list to be recognized, the following must be
    true:

    - the list must consist of multiple adjacent list items (2 or
      more)
    - the enumerators must all have the same format
    - the enumerators must be sequential


Definition List Markup
======================

StructuredText uses ' -- ' (whitespace, two hyphens, whitespace) on
the first line of a paragraph to indicate a definition list item.  The
' -- ' serves to separate the term (on the left) from the definition
(on the right).

Many people use ' -- ' as an em-dash in their text, conflicting with
the StructuredText usage.  Although the Chicago Manual of Style says
that spaces should not be used around an em-dash, Peter Funk pointed
out that this is standard usage in German (according to the Duden, the
official German reference), and possibly in other languages as well.
The widespread use of ' -- ' precludes its use for definition lists;
it would violate the "unsurprising" criterion.

A simpler, and at least equally visually distinctive construct
(proposed by Guido van Rossum, who incidentally is a frequent user of
' -- ') would do just as well::

    term 1
        Definition.

    term 2
        Definition 2, paragraph 1.

        Definition 2, paragraph 2.

A reStructuredText definition list item consists of a term and a
definition.  A term is a simple one-line paragraph.  A definition is a
block indented relative to the term, and may contain multiple
paragraphs and other body elements.  No blank line precedes a
definition (this distinguishes definition lists from block quotes).


Literal Blocks
==============

The StructuredText_ specification has literal blocks indicated by
'example', 'examples', or '::' ending the preceding paragraph.  STNG
only recognizes '::'; 'example'/'examples' are not implemented.  This
is good; it fixes an unnecessary language dependency.  The problem is
what to do with the sometimes- unwanted '::'.

In reStructuredText_ '::' at the end of a paragraph indicates that
subsequent *indented* blocks are treated as literal text.  No further
markup interpretation is done within literal blocks (not even
backslash-escapes).  If the '::' is preceded by whitespace, '::' is
omitted from the output; if '::' was the sole content of a paragraph,
the entire paragraph is removed (no 'empty' paragraph remains).  If
'::' is preceded by a non-whitespace character, '::' is replaced by
':' (i.e., the extra colon is removed).

Thus, a section could begin with a literal block as follows::

    Section Title
    -------------

    ::

        print "this is example literal"


Tables
======

The table markup scheme in classic StructuredText was horrible.  Its
omission from StructuredTextNG is welcome, and its markup will not be
repeated here.  However, tables themselves are useful in
documentation.  Alternatives:

1. This format is the most natural and obvious.  It was independently
   invented (no great feat of creation!), and later found to be the
   format supported by the `Emacs table mode`_::

       +------------+------------+------------+--------------+
       |  Header 1  |  Header 2  |  Header 3  |  Header 4    |
       +============+============+============+==============+
       |  Column 1  |  Column 2  | Column 3 & 4 span (Row 1) |
       +------------+------------+------------+--------------+
       |    Column 1 & 2 span    |  Column 3  | - Column 4   |
       +------------+------------+------------+ - Row 2 & 3  |
       |      1     |      2     |      3     | - span       |
       +------------+------------+------------+--------------+

   Tables are described with a visual outline made up of the
   characters '-', '=', '|', and '+':

   - The hyphen ('-') is used for horizontal lines (row separators).
   - The equals sign ('=') is optionally used as a header separator
     (as of version 1.5.24, this is not supported by the Emacs table
     mode).
   - The vertical bar ('|') is used for for vertical lines (column
     separators).
   - The plus sign ('+') is used for intersections of horizontal and
     vertical lines.

   Row and column spans are possible simply by omitting the column or
   row separators, respectively.  The header row separator must be
   complete; in other words, a header cell may not span into the table
   body.  Each cell contains body elements, and may have multiple
   paragraphs, lists, etc.  Initial spaces for a left margin are
   allowed; the first line of text in a cell determines its left
   margin.

2. Below is a simpler table structure.  It may be better suited to
   manual input than alternative #1, but there is no Emacs editing
   mode available.  One disadvantage is that it resembles section
   titles; a one-column table would look exactly like section &
   subsection titles. ::

       ============ ============ ============ ==============
         Header 1     Header 2     Header 3     Header 4
       ============ ============ ============ ==============
         Column 1     Column 2    Column 3 & 4 span (Row 1)
       ------------ ------------ ---------------------------
           Column 1 & 2 span       Column 3    - Column 4
       ------------------------- ------------  - Row 2 & 3
             1            2            3       - span
       ============ ============ ============ ==============

   The table begins with a top border of equals signs with a space at
   each column boundary (regardless of spans).  Each row is
   underlined.  Internal row separators are underlines of '-', with
   spaces at column boundaries.  The last of the optional head rows is
   underlined with '=', again with spaces at column boundaries.
   Column spans have no spaces in their underline.  Row spans simply
   lack an underline at the row boundary.  The bottom boundary of the
   table consists of '=' underlines.  A blank line is required
   following a table.

3. A minimalist alternative is as follows::

       ====  =====  ========  ========  =======  ====  =====  =====
       Old State    Input     Action             New State    Notes
       -----------  --------  -----------------  -----------
       ids   types  new type  sys.msg.  dupname  ids   types
       ====  =====  ========  ========  =======  ====  =====  =====
       --    --     explicit  --        --       new   True
       --    --     implicit  --        --       new   False
       None  False  explicit  --        --       new   True
       old   False  explicit  implicit  old      new   True
       None  True   explicit  explicit  new      None  True
       old   True   explicit  explicit  new,old  None  True   [1]
       None  False  implicit  implicit  new      None  False
       old   False  implicit  implicit  new,old  None  False
       None  True   implicit  implicit  new      None  True
       old   True   implicit  implicit  new      old   True
       ====  =====  ========  ========  =======  ====  =====  =====

   The table begins with a top border of equals signs with one or more
   spaces at each column boundary (regardless of spans).  There must
   be at least two columns in the table (to differentiate it from
   section headers).  Each line starts a new row.  The rightmost
   column is unbounded; text may continue past the edge of the table.
   Each row/line must contain spaces at column boundaries, except for
   explicit column spans.  Underlines of '-' can be used to indicate
   column spans, but should be used sparingly if at all.  Lines
   containing column span underlines may not contain any other text.
   The last of the optional head rows is underlined with '=', again
   with spaces at column boundaries.  The bottom boundary of the table
   consists of '=' underlines.  A blank line is required following a
   table.

   This table sums up the features.  Using all the features in such a
   small space is not pretty though::

       ========  ========  ========
                 Header 2 & 3 Span
                 ------------------
       Header 1  Header 2  Header 3
       ========  ========  ========
       Each      line is   a new row.
       Each row  consists  of one line only.
       Row       spans     are not possible.
       The last  column    may spill over to the right.
       Column spans are possible with an underline joining columns.
       ----------------------------
       The span  is        limited to the row above the underline.
       ========  ========  ========

4. As a variation of alternative 3, bullet list syntax in the first
   column could be used to indicate row starts.  Multi-line rows are
   possible, but row spans are not.  For example::

       ===== =====
       col 1 col 2
       ===== =====
       - 1   Second column of row 1.
       - 2   Second column of row 2.
             Second line of paragraph.
       - 3   Second column of row 3.

             Second paragraph of row 3,
             column 2
       ===== =====

   Column spans would be indicated on the line after the last line of
   the row.  To indicate a real bullet list within a first-column
   cell, simply nest the bullets.

5. In a further variation, we could simply assume that whitespace in
   the first column implies a multi-line row; the text in other
   columns is continuation text.  For example::

       ===== =====
       col 1 col 2
       ===== =====
       1     Second column of row 1.
       2     Second column of row 2.
             Second line of paragraph.
       3     Second column of row 3.

             Second paragraph of row 3,
             column 2
       ===== =====

   Limitations of this approach:

   - Cells in the first column are limited to one line of text.

   - Cells in the first column *must* contain some text; blank cells
     would lead to a misinterpretation.  An empty comment ("..") is
     sufficient.

6. Combining alternative 3 and 4, a bullet list in the first column
   could mean multi-line rows, and no bullet list means single-line
   rows only.

Alternatives 1 and 5 has been adopted by reStructuredText.


Delimitation of Inline Markup
=============================

StructuredText specifies that inline markup must begin with
whitespace, precluding such constructs as parenthesized or quoted
emphatic text::

    "**What?**" she cried.  (*exit stage left*)

The `reStructuredText markup specification`_ allows for such
constructs and disambiguates inline markup through a set of
recognition rules.  These recognition rules define the context of
markup start-strings and end-strings, allowing markup characters to be
used in most non-markup contexts without a problem (or a backslash).
So we can say, "Use asterisks (*) around words or phrases to
*emphasisze* them." The '(*)' will not be recognized as markup.  This
reduces the need for markup escaping to the point where an escape
character is *almost* (but not quite!) unnecessary.


Underlining
===========

StructuredText uses '_text_' to indicate underlining.  To quote David
Ascher in his 2000-01-21 Doc-SIG mailing list post, "Docstring
grammar: a very revised proposal":

    The tagging of underlined text with _'s is suboptimal.  Underlines
    shouldn't be used from a typographic perspective (underlines were
    designed to be used in manuscripts to communicate to the
    typesetter that the text should be italicized -- no well-typeset
    book ever uses underlines), and conflict with double-underscored
    Python variable names (__init__ and the like), which would get
    truncated and underlined when that effect is not desired.  Note
    that while *complete* markup would prevent that truncation
    ('__init__'), I think of docstring markups much like I think of
    type annotations -- they should be optional and above all do no
    harm.  In this case the underline markup does harm.

Underlining is not part of the reStructuredText specification.


Inline Literals
===============

StructuredText's markup for inline literals (text left as-is,
verbatim, usually in a monospaced font; as in HTML <TT>) is single
quotes ('literals').  The problem with single quotes is that they are
too often used for other purposes:

- Apostrophes: "Don't blame me, 'cause it ain't mine, it's Chris'.";

- Quoting text:

      First Bruce: "Well Bruce, I heard the prime minister use it.
      'S'hot enough to boil a monkey's bum in 'ere your Majesty,' he
      said, and she smiled quietly to herself."

  In the UK, single quotes are used for dialogue in published works.

- String literals: s = ''

Alternatives::

    'text'    \'text\'    ''text''    "text"    \"text\"    ""text""
    #text#     @text@      `text`     ^text^    ``text''    ``text``

The examples below contain inline literals, quoted text, and
apostrophes.  Each example should evaluate to the following HTML::

    Some <TT>code</TT>, with a 'quote', "double", ain't it grand?
    Does <TT>a[b] = 'c' + "d" + `2^3`</TT> work?

    0. Some code, with a quote, double, ain't it grand?
       Does a[b] = 'c' + "d" + `2^3` work?
    1. Some 'code', with a \'quote\', "double", ain\'t it grand?
       Does 'a[b] = \'c\' + "d" + `2^3`' work?
    2. Some \'code\', with a 'quote', "double", ain't it grand?
       Does \'a[b] = 'c' + "d" + `2^3`\' work?
    3. Some ''code'', with a 'quote', "double", ain't it grand?
       Does ''a[b] = 'c' + "d" + `2^3`'' work?
    4. Some "code", with a 'quote', \"double\", ain't it grand?
       Does "a[b] = 'c' + "d" + `2^3`" work?
    5. Some \"code\", with a 'quote', "double", ain't it grand?
       Does \"a[b] = 'c' + "d" + `2^3`\" work?
    6. Some ""code"", with a 'quote', "double", ain't it grand?
       Does ""a[b] = 'c' + "d" + `2^3`"" work?
    7. Some #code#, with a 'quote', "double", ain't it grand?
       Does #a[b] = 'c' + "d" + `2^3`# work?
    8. Some @code@, with a 'quote', "double", ain't it grand?
       Does @a[b] = 'c' + "d" + `2^3`@ work?
    9. Some `code`, with a 'quote', "double", ain't it grand?
       Does `a[b] = 'c' + "d" + \`2^3\`` work?
    10. Some ^code^, with a 'quote', "double", ain't it grand?
        Does ^a[b] = 'c' + "d" + `2\^3`^ work?
    11. Some ``code'', with a 'quote', "double", ain't it grand?
        Does ``a[b] = 'c' + "d" + `2^3`'' work?
    12. Some ``code``, with a 'quote', "double", ain't it grand?
        Does ``a[b] = 'c' + "d" + `2^3\``` work?

Backquotes (#9 & #12) are the best choice.  They are unobtrusive and
relatviely rarely used (more rarely than ' or ", anyhow).  Backquotes
have the connotation of 'quotes', which other options (like carets,
#10) don't.

Analogously with ``*emph*`` & ``**strong**``, double-backquotes (#12)
could be used for inline literals.  If single-backquotes are used for
'interpreted text' (context-sensitive domain-specific descriptive
markup) such as function name hyperlinks in Python docstrings, then
double-backquotes could be used for absolute-literals, wherein no
processing whatsoever takes place.  An advantage of double-backquotes
would be that backslash-escaping would no longer be necessary for
embedded single-backquotes; however, embedded double-backquotes (in an
end-string context) would be illegal.  See `Backquotes in
Phrase-Links`__ in `Record of reStructuredText Syntax Alternatives`__.

__ alternatives.html#backquotes-in-phrase-links
__ alternatives.html

Alternative choices are carets (#10) and TeX-style quotes (#11).  For
examples of TeX-style quoting, see
http://www.zope.org/Members/jim/StructuredTextWiki/CustomizingTheDocumentProcessor.

Some existing uses of backquotes:

1. As a synonym for repr() in Python.
2. For command-interpolation in shell scripts.
3. Used as open-quotes in TeX code (and carried over into plaintext
   by TeXies).

The inline markup start-string and end-string recognition rules
defined by the `reStructuredText markup specification`_ would allow
all of these cases inside inline literals, with very few exceptions.
As a fallback, literal blocks could handle all cases.

Outside of inline literals, the above uses of backquotes would require
backslash-escaping.  However, these are all prime examples of text
that should be marked up with inline literals.

If either backquotes or straight single-quotes are used as markup,
TeX-quotes are too troublesome to support, so no special-casing of
TeX-quotes should be done (at least at first).  If TeX-quotes have to
be used outside of literals, a single backslash-escaped would suffice:
\``TeX quote''.  Ugly, true, but very infrequently used.

Using literal blocks is a fallback option which removes the need for
backslash-escaping::

    like this::

        Here, we can do ``absolutely'' anything `'`'\|/|\ we like!

No mechanism for inline literals is perfect, just as no escaping
mechanism is perfect.  No matter what we use, complicated inline
expressions involving the inline literal quote and/or the backslash
will end up looking ugly.  We can only choose the least often ugly
option.

reStructuredText will use double backquotes for inline literals, and
single backqoutes for interpreted text.


Hyperlinks
==========

There are three forms of hyperlink currently in StructuredText_:

1. (Absolute & relative URIs.)  Text enclosed by double quotes
   followed by a colon, a URI, and concluded by punctuation plus white
   space, or just white space, is treated as a hyperlink::

       "Python":http://www.python.org/

2. (Absolute URIs only.)  Text enclosed by double quotes followed by a
   comma, one or more spaces, an absolute URI and concluded by
   punctuation plus white space, or just white space, is treated as a
   hyperlink::

       "mail me", mailto:me@mail.com

3. (Endnotes.)  Text enclosed by brackets link to an endnote at the
   end of the document: at the beginning of the line, two dots, a
   space, and the same text in brackets, followed by the end note
   itself::

       Please refer to the fine manual [GVR2001].

       .. [GVR2001] Python Documentation, Release 2.1, van Rossum,
          Drake, et al., http://www.python.org/doc/

The problem with forms 1 and 2 is that they are neither intuitive nor
unobtrusive (they break design goals 5 & 2).  They overload
double-quotes, which are too often used in ordinary text (potentially
breaking design goal 4).  The brackets in form 3 are also too common
in ordinary text (such as [nested] asides and Python lists like [12]).

Alternatives:

1. Have no special markup for hyperlinks.

2. A. Interpret and mark up hyperlinks as any contiguous text
      containing '://' or ':...@' (absolute URI) or '@' (email
      address) after an alphanumeric word.  To de-emphasize the URI,
      simply enclose it in parentheses:

          Python (http://www.python.org/)

   B. Leave special hyperlink markup as a domain-specific extension.
      Hyperlinks in ordinary reStructuredText documents would be
      required to be standalone (i.e. the URI text inline in the
      document text).  Processed hyperlinks (where the URI text is
      hidden behind the link) are important enough to warrant syntax.

3. The original Setext_ introduced a mechanism of indirect hyperlinks.
   A source link word ('hot word') in the text was given a trailing
   underscore::

       Here is some text with a hyperlink_ built in.

   The hyperlink itself appeared at the end of the document on a line
   by itself, beginning with two dots, a space, the link word with a
   leading underscore, whitespace, and the URI itself::

       .. _hyperlink http://www.123.xyz

   Setext used ``underscores_instead_of_spaces_`` for phrase links.

With some modification, alternative 3 best satisfies the design goals.
It has the advantage of being readable and relatively unobtrusive.
Since each source link must match up to a target, the odd variable
ending in an underscore can be spared being marked up (although it
should generate a "no such link target" warning).  The only
disadvantage is that phrase-links aren't possible without some
obtrusive syntax.

We could achieve phrase-links if we enclose the link text:

1. in double quotes::

       "like this"_

2. in brackets::

       [like this]_

3. or in backquotes::

       `like this`_

Each gives us somewhat obtrusive markup, but that is unavoidable.  The
bracketed syntax (#2) is reminiscent of links on many web pages
(intuitive), although it is somewhat obtrusive.  Alternative #3 is
much less obtrusive, and is consistent with interpreted text: the
trailing underscore indicates the interpretation of the phrase, as a
hyperlink.  #3 also disambiguates hyperlinks from footnote references.
Alternative #3 wins.

The same trailing underscore markup can also be used for footnote and
citation references, removing the problem with ordinary bracketed text
and Python lists::

    Please refer to the fine manual [GVR2000]_.

    .. [GVR2000] Python Documentation, van Rossum, Drake, et al.,
       http://www.python.org/doc/

The two-dots-and-a-space syntax was generalized by Setext for
comments, which are removed from the (visible) processed output.
reStructuredText uses this syntax for comments, footnotes, and link
target, collectively termed "explicit markup".  For link targets, in
order to eliminate ambiguity with comments and footnotes,
reStructuredText specifies that a colon always follow the link target
word/phrase.  The colon denotes 'maps to'.  There is no reason to
restrict target links to the end of the document; they could just as
easily be interspersed.

Internal hyperlinks (links from one point to another within a single
document) can be expressed by a source link as before, and a target
link with a colon but no URI.  In effect, these targets 'map to' the
element immediately following.

As an added bonus, we now have a perfect candidate for
reStructuredText directives, a simple extension mechanism: explicit
markup containing a single word followed by two colons and whitespace.
The interpretation of subsequent data on the directive line or
following is directive-dependent.

To summarize::

    .. This is a comment.

    .. The line below is an example of a directive.
    .. version:: 1

    This is a footnote [1]_.

    This internal hyperlink will take us to the footnotes_ area below.

    Here is a one-word_ external hyperlink.

    Here is `a hyperlink phrase`_.

    .. _footnotes:
    .. [1] Footnote text goes here.

    .. external hyperlink target mappings:
    .. _one-word: http://www.123.xyz
    .. _a hyperlink phrase: http://www.123.xyz

The presence or absence of a colon after the target link
differentiates an indirect hyperlink from a footnote, respectively.  A
footnote requires brackets.  Backquotes around a target link word or
phrase are required if the phrase contains a colon, optional
otherwise.

Below are examples using no markup, the two StructuredText hypertext
styles, and the reStructuredText hypertext style.  Each example
contains an indirect link, a direct link, a footnote/endnote, and
bracketed text.  In HTML, each example should evaluate to::

    <P>A <A HREF="http://spam.org">URI</A>, see <A HREF="#eggs2000">
    [eggs2000]</A> (in Bacon [Publisher]).  Also see
    <A HREF="http://eggs.org">http://eggs.org</A>.</P>

    <P><A NAME="eggs2000">[eggs2000]</A> "Spam, Spam, Spam, Eggs,
    Bacon, and Spam"</P>

1. No markup::

       A URI http://spam.org, see eggs2000 (in Bacon [Publisher]).
       Also see http://eggs.org.

       eggs2000 "Spam, Spam, Spam, Eggs, Bacon, and Spam"

2. StructuredText absolute/relative URI syntax
   ("text":http://www.url.org)::

       A "URI":http://spam.org, see [eggs2000] (in Bacon [Publisher]).
       Also see "http://eggs.org":http://eggs.org.

       .. [eggs2000] "Spam, Spam, Spam, Eggs, Bacon, and Spam"

   Note that StructuredText does not recognize standalone URIs,
   forcing doubling up as shown in the second line of the example
   above.

3. StructuredText absolute-only URI syntax
   ("text", mailto:you@your.com)::

       A "URI", http://spam.org, see [eggs2000] (in Bacon
       [Publisher]).  Also see "http://eggs.org", http://eggs.org.

       .. [eggs2000] "Spam, Spam, Spam, Eggs, Bacon, and Spam"

4. reStructuredText syntax::

    4. A URI_, see [eggs2000]_ (in Bacon [Publisher]).
       Also see http://eggs.org.

       .. _URI: http:/spam.org
       .. [eggs2000] "Spam, Spam, Spam, Eggs, Bacon, and Spam"

The bracketed text '[Publisher]' may be problematic with
StructuredText (syntax 2 & 3).

reStructuredText's syntax (#4) is definitely the most readable.  The
text is separated from the link URI and the footnote, resulting in
cleanly readable text.

.. _StructuredText: https://zopestructuredtext.readthedocs.org/
.. _Setext: https://docutils.sourceforge.io/mirror/setext.html
.. _reStructuredText: https://docutils.sourceforge.io/rst.html
.. _detailed description:
   http://homepage.ntlworld.com/tibsnjoan/docutils/STNG-format.html
.. _STMinus: http://www.cis.upenn.edu/~edloper/pydoc/stminus.html
.. _StructuredTextNG:
   http://www.zope.org/DevHome/Members/jim/StructuredTextWiki/StructuredTextNG
.. _README: http://cvs.sourceforge.net/cgi-bin/viewcvs.cgi/~checkout~/
   python/python/dist/src/README
.. _Emacs table mode: http://table.sourceforge.net/
.. _reStructuredText Markup Specification:
   ../../ref/rst/restructuredtext.html

.. Emacs settings

   Local Variables:
   mode: indented-text
   mode: rst
   indent-tabs-mode: nil
   sentence-end-double-space: t
   fill-column: 70
   End:
