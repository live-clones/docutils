.. include:: ../../header2.rst

==================================================
 A Record of reStructuredText Syntax Alternatives
==================================================

:Author: David Goodger
:Contact: docutils-develop@lists.sourceforge.net
:Revision: $Revision$
:Date: $Date$
:Copyright: This document has been placed in the public domain.

The following are ideas, alternatives, and justifications that were
considered for reStructuredText syntax, which did not originate with
Setext_ or StructuredText_.  For an analysis of constructs which *did*
originate with StructuredText or Setext, please see `Problems With
StructuredText`_.  See the `reStructuredText Markup Specification`_
for full details of the established syntax.

The ideas are divided into sections:

* Implemented_: already done.  The issues and alternatives are
  recorded here for posterity.

* `Not Implemented`_: these ideas won't be implemented.

* Tabled_: these ideas should be revisited in the future.

* `To Do`_: these ideas should be implemented.  They're just waiting
  for a champion to resolve issues and get them done.

* `... Or Not To Do?`_: possible but questionable.  These probably
  won't be implemented, but you never know.

.. _Setext: https://docutils.sourceforge.io/mirror/setext.html
.. _StructuredText: https://zopestructuredtext.readthedocs.org/
.. _Problems with StructuredText: problems.html
.. _reStructuredText Markup Specification:
   ../../ref/rst/restructuredtext.html


.. contents::

-------------
 Implemented
-------------

Field Lists
===========

Prior to the syntax for field lists being finalized, several
alternatives were proposed.

1. Unadorned :RFC:`822` everywhere::

       Author: Me
       Version: 1

   Advantages: clean, precedent (RFC822-compliant).  Disadvantage:
   ambiguous (these paragraphs are a prime example).

   Conclusion: rejected.

2. Special case: use unadorned :RFC:`822` for the very first or very last
   text block of a document::

       """
       Author: Me
       Version: 1

       The rest of the document...
       """

   Advantages: clean, precedent (RFC822-compliant).  Disadvantages:
   special case, flat (unnested) field lists only, still ambiguous::

       """
       Usage: cmdname [options] arg1 arg2 ...

       We obviously *don't* want the like above to be interpreted as a
       field list item.  Or do we?
       """

   Conclusion: rejected for the general case, accepted for specific
   contexts (PEPs, email).

3. Use a directive::

       .. fields::

          Author: Me
          Version: 1

   Advantages: explicit and unambiguous, RFC822-compliant.
   Disadvantage: cumbersome.

   Conclusion: rejected for the general case (but such a directive
   could certainly be written).

4. Use Javadoc-style::

       @Author: Me
       @Version: 1
       @param a: integer

   Advantages: unambiguous, precedent, flexible.  Disadvantages:
   non-intuitive, ugly, not RFC822-compliant.

   Conclusion: rejected.

5. Use leading colons::

       :Author: Me
       :Version: 1

   Advantages: unambiguous, obvious (*almost* RFC822-compliant),
   flexible, perhaps even elegant.  Disadvantages: no precedent, not
   quite RFC822-compliant.

   Conclusion: accepted!

6. Use double colons::

       Author:: Me
       Version:: 1

   Advantages: unambiguous, obvious? (*almost* RFC822-compliant),
   flexible, similar to syntax already used for literal blocks and
   directives.  Disadvantages: no precedent, not quite
   RFC822-compliant, similar to syntax already used for literal blocks
   and directives.

   Conclusion: rejected because of the syntax similarity & conflicts.

Why is RFC822 compliance important?  It's a universal Internet
standard, and super obvious.  Also, I'd like to support the PEP format
(ulterior motive: get PEPs to use reStructuredText as their standard).
But it *would* be easy to get used to an alternative (easy even to
convert PEPs; probably harder to convert python-deviants ;-).

Unfortunately, without well-defined context (such as in email headers:
RFC822 only applies before any blank lines), the RFC822 format is
ambiguous.  It is very common in ordinary text.  To implement field
lists unambiguously, we need explicit syntax.

The following question was posed in a footnote:

   Should "bibliographic field lists" be defined at the parser level,
   or at the DPS transformation level?  In other words, are they
   reStructuredText-specific, or would they also be applicable to
   another (many/every other?) syntax?

The answer is that bibliographic fields are a
reStructuredText-specific markup convention.  Other syntaxes may
implement the bibliographic elements explicitly.  For example, there
would be no need for such a transformation for an XML-based markup
syntax.


Interpreted Text "Roles"
========================

The original purpose of interpreted text was as a mechanism for
descriptive markup, to describe the nature or role of a word or
phrase.  For example, in XML we could say "<function>len</function>"
to mark up "len" as a function.  It is envisaged that within Python
docstrings (inline documentation in Python module source files, the
primary market for reStructuredText) the role of a piece of
interpreted text can be inferred implicitly from the context of the
docstring within the program source.  For other applications, however,
the role may have to be indicated explicitly.

Interpreted text is enclosed in single backquotes (`).

1. Initially, it was proposed that an explicit role could be indicated
   as a word or phrase within the enclosing backquotes:

   - As a prefix, separated by a colon and whitespace::

         `role: interpreted text`

   - As a suffix, separated by whitespace and a colon::

         `interpreted text :role`

   There are problems with the initial approach:

   - There could be ambiguity with interpreted text containing colons.
     For example, an index entry of "Mission: Impossible" would
     require a backslash-escaped colon.

   - The explicit role is descriptive markup, not content, and will
     not be visible in the processed output.  Putting it inside the
     backquotes doesn't feel right; the *role* isn't being quoted.

2. Tony Ibbs suggested that the role be placed outside the
   backquotes::

       role:`prefix` or `suffix`:role

   This removes the embedded-colons ambiguity, but limits the role
   identifier to be a single word (whitespace would be illegal).
   Since roles are not meant to be visible after processing, the lack
   of whitespace support is not important.

   The suggested syntax remains ambiguous with respect to ratios and
   some writing styles.  For example, suppose there is a "signal"
   identifier, and we write::

       ...calculate the `signal`:noise ratio.

   "noise" looks like a role.

3. As an improvement on #2, we can bracket the role with colons::

       :role:`prefix` or `suffix`:role:

   This syntax is similar to that of field lists, which is fine since
   both are doing similar things: describing.

   This is the syntax chosen for reStructuredText.

4. Another alternative is two colons instead of one::

       role::`prefix` or `suffix`::role

   But this is used for analogies ("A:B::C:D": "A is to B as C is to
   D").

   Both alternative #2 and #4 lack delimiters on both sides of the
   role, making it difficult to parse (by the reader).

5. Some kind of bracketing could be used:

   - Parentheses::

         (role)`prefix` or `suffix`(role)

   - Braces::

         {role}`prefix` or `suffix`{role}

   - Square brackets::

         [role]`prefix` or `suffix`[role]

   - Angle brackets::

         <role>`prefix` or `suffix`<role>

     (The overlap of \*ML tags with angle brackets would be too
     confusing and precludes their use.)

Syntax #3 was chosen for reStructuredText.


``term`` Role
=============

Add a "term" role for unfamiliar or specialized terminology?
Probably not as a standard role; there is no real use case, and emphasis
is enough for most cases.
For semantic markup, authors may define a `custom role`_ or include the
"html-roles.txt" `standard definition file`_ that defines (`amongst
others`__) the "dfn" role (the "html5" writer selects the corresponding
`HTML <dfn> element`_).

.. _custom role: ../../ref/rst/directives.html#role
.. _standard definition file: ../../ref/rst/definitions.html
__ ../../ref/rst/definitions.html#additional-roles-for-html
.. _HTML <dfn> element:
    https://html.spec.whatwg.org/multipage/text-level-semantics.html
    #the-dfn-element


Comments
========

A problem with comments (actually, with all indented constructs) is
that they cannot be followed by an indented block -- a block quote --
without swallowing it up.

I thought that perhaps comments should be one-liners only.  But would
this mean that footnotes, hyperlink targets, and directives must then
also be one-liners?  Not a good solution.

Tony Ibbs suggested a "comment" directive.  I added that we could
limit a comment to a single text block, and that a "multi-block
comment" could use "comment-start" and "comment-end" directives.  This
would remove the indentation incompatibility.  A "comment" directive
automatically suggests "footnote" and (hyperlink) "target" directives
as well.  This could go on forever!  Bad choice.

Garth Kidd suggested that an "empty comment", a ".." explicit markup
start with nothing on the first line (except possibly whitespace) and
a blank line immediately following, could serve as an "unindent".  An
empty comment does **not** swallow up indented blocks following it,
so block quotes are safe.  "A tiny but practical wart."  Accepted.


Anonymous Hyperlinks
====================

Alan Jaffray came up with this idea, along with the following syntax::

    Search the `Python DOC-SIG mailing list archives`{}_.

    .. _: https://mail.python.org/pipermail/doc-sig/

The idea is sound and useful.  I suggested a "double underscore"
syntax::

    Search the `Python DOC-SIG mailing list archives`__.

    .. __: https://mail.python.org/pipermail/doc-sig/

But perhaps single underscores are okay?  The syntax looks better, but
the hyperlink itself doesn't explicitly say "anonymous"::

    Search the `Python DOC-SIG mailing list archives`_.

    .. _: https://mail.python.org/pipermail/doc-sig/

Mixing anonymous and named hyperlinks becomes confusing.  The order of
targets is not significant for named hyperlinks, but it is for
anonymous hyperlinks::

    Hyperlinks: anonymous_, named_, and another anonymous_.

    .. _named: named
    .. _: anonymous1
    .. _: anonymous2

Without the extra syntax of double underscores, determining which
hyperlink references are anonymous may be difficult.  We'd have to
check which references don't have corresponding targets, and match
those up with anonymous targets.  Keeping to a simple consistent
ordering (as with auto-numbered footnotes) seems simplest.

reStructuredText will use the explicit double-underscore syntax for
anonymous hyperlinks.  An alternative (see `Reworking Explicit Markup
(Round 1)`_ below) for the somewhat awkward ".. __:" syntax is "__"::

    An anonymous__ reference.

    __ http://anonymous


Reworking Explicit Markup (Round 1)
===================================

Alan Jaffray came up with the idea of `anonymous hyperlinks`_, added
to reStructuredText.  Subsequently it was asserted that hyperlinks
(especially anonymous hyperlinks) would play an increasingly important
role in reStructuredText documents, and therefore they require a
simpler and more concise syntax.  This prompted a review of the
current and proposed explicit markup syntaxes with regards to
improving usability.

1. Original syntax::

       .. _blah:                     internal hyperlink target
       .. _blah: http://somewhere    external hyperlink target
       .. _blah: blahblah_           indirect hyperlink target
       .. __:                        anonymous internal target
       .. __: http://somewhere       anonymous external target
       .. __: blahblah_              anonymous indirect target
       .. [blah] http://somewhere    footnote
       .. blah:: http://somewhere    directive
       .. blah: http://somewhere     comment

   .. Note::

      The comment text was intentionally made to look like a hyperlink
      target.

   Origins:

   * Except for the colon (a delimiter necessary to allow for
     phrase-links), hyperlink target ``.. _blah:`` comes from Setext.
   * Comment syntax from Setext.
   * Footnote syntax from StructuredText ("named links").
   * Directives and anonymous hyperlinks original to reStructuredText.

   Advantages:

   + Consistent explicit markup indicator: "..".
   + Consistent hyperlink syntax: ".. _" & ":".

   Disadvantages:

   - Anonymous target markup is awkward: ".. __:".
   - The explicit markup indicator ("..") is excessively overloaded?
   - Comment text is limited (can't look like a footnote, hyperlink,
     or directive).  But this is probably not important.

2. Alan Jaffray's proposed syntax #1::

       __ _blah                      internal hyperlink target
       __ blah: http://somewhere     external hyperlink target
       __ blah: blahblah_            indirect hyperlink target
       __                            anonymous internal target
       __ http://somewhere           anonymous external target
       __ blahblah_                  anonymous indirect target
       __ [blah] http://somewhere    footnote
       .. blah:: http://somewhere    directive
       .. blah: http://somewhere     comment

   The hyperlink-connoted underscores have become first-level syntax.

   Advantages:

   + Anonymous targets are simpler.
   + All hyperlink targets are one character shorter.

   Disadvantages:

   - Inconsistent internal hyperlink targets.  Unlike all other named
     hyperlink targets, there's no colon.  There's an extra leading
     underscore, but we can't drop it because without it, "blah" looks
     like a relative URI.  Unless we restore the colon::

         __ blah:                      internal hyperlink target

   - Obtrusive markup?

3. Alan Jaffray's proposed syntax #2::

       .. _blah                      internal hyperlink target
       .. blah: http://somewhere     external hyperlink target
       .. blah: blahblah_            indirect hyperlink target
       ..                            anonymous internal target
       .. http://somewhere           anonymous external target
       .. blahblah_                  anonymous indirect target
       .. [blah] http://somewhere    footnote
       !! blah: http://somewhere     directive
       ## blah: http://somewhere     comment

   Leading underscores have been (almost) replaced by "..", while
   comments and directives have gained their own syntax.

   Advantages:

   + Anonymous hyperlinks are simpler.
   + Unique syntax for comments.  Connotation of "comment" from
     some programming languages (including our favorite).
   + Unique syntax for directives.  Connotation of "action!".

   Disadvantages:

   - Inconsistent internal hyperlink targets.  Again, unlike all other
     named hyperlink targets, there's no colon.  There's a leading
     underscore, matching the trailing underscores of references,
     which no other hyperlink targets have.  We can't drop that one
     leading underscore though: without it, "blah" looks like a
     relative URI.  Again, unless we restore the colon::

         .. blah:                      internal hyperlink target

   - All (except for internal) hyperlink targets lack their leading
     underscores, losing the "hyperlink" connotation.

   - Obtrusive syntax for comments.  Alternatives::

         ;; blah: http://somewhere
            (also comment syntax in Lisp & others)
         ,, blah: http://somewhere
            ("comma comma": sounds like "comment"!)

   - Iffy syntax for directives.  Alternatives?

4. Tony Ibbs' proposed syntax::

       .. _blah:                     internal hyperlink target
       .. _blah: http://somewhere    external hyperlink target
       .. _blah: blahblah_           indirect hyperlink target
       ..                            anonymous internal target
       .. http://somewhere           anonymous external target
       .. blahblah_                  anonymous indirect target
       .. [blah] http://somewhere    footnote
       .. blah:: http://somewhere    directive
       .. blah: http://somewhere     comment

   This is the same as the current syntax, except for anonymous
   targets which drop their "__: ".

   Advantage:

   + Anonymous targets are simpler.

   Disadvantages:

   - Anonymous targets lack their leading underscores, losing the
     "hyperlink" connotation.
   - Anonymous targets are almost indistinguishable from comments.
     (Better to know "up front".)

5. David Goodger's proposed syntax: Perhaps going back to one of
   Alan's earlier suggestions might be the best solution.  How about
   simply adding "__ " as a synonym for ".. __: " in the original
   syntax?  These would become equivalent::

       .. __:                        anonymous internal target
       .. __: http://somewhere       anonymous external target
       .. __: blahblah_              anonymous indirect target

       __                            anonymous internal target
       __ http://somewhere           anonymous external target
       __ blahblah_                  anonymous indirect target

Alternative 5 has been adopted.


Backquotes in Phrase-Links
==========================

[From a 2001-06-05 Doc-SIG post in reply to questions from Doug
Hellmann.]

The first draft of the spec, posted to the Doc-SIG in November 2000,
used square brackets for phrase-links.  I changed my mind because:

1. In the first draft, I had already decided on single-backquotes for
   inline literal text.

2. However, I wanted to minimize the necessity for backslash escapes,
   for example when quoting Python repr-equivalent syntax that uses
   backquotes.

3. The processing of identifiers (function/method/attribute/module
   etc. names) into hyperlinks is a useful feature.  PyDoc recognizes
   identifiers heuristically, but it doesn't take much imagination to
   come up with counter-examples where PyDoc's heuristics would result
   in embarrassing failure.  I wanted to do it deterministically, and
   that called for syntax.  I called this construct "interpreted
   text".

4. Leveraging off the ``*emphasis*/**strong**`` syntax, lead to the
   idea of using double-backquotes as syntax.

5. I worked out some rules for inline markup recognition.

6. In combination with #5, double backquotes lent themselves to inline
   literals, neatly satisfying #2, minimizing backslash escapes.  In
   fact, the spec says that no interpretation of any kind is done
   within double-backquote inline literal text; backslashes do *no*
   escaping within literal text.

7. Single backquotes are then freed up for interpreted text.

8. I already had square brackets required for footnote references.

9. Since interpreted text will typically turn into hyperlinks, it was
   a natural fit to use backquotes as the phrase-quoting syntax for
   trailing-underscore hyperlinks.

The original inspiration for the trailing underscore hyperlink syntax
was Setext.  But for phrases Setext used a very cumbersome
``underscores_between_words_like_this_`` syntax.

The underscores can be viewed as if they were right-pointing arrows:
``-->``.  So ``hyperlink_`` points away from the reference, and
``.. _hyperlink:`` points toward the target.


Substitution Mechanism
======================

Substitutions arose out of a Doc-SIG thread begun on 2001-10-28 by
Alan Jaffray, "reStructuredText inline markup".  It reminded me of a
missing piece of the reStructuredText puzzle, first referred to in my
contribution to "Documentation markup & processing / PEPs" (Doc-SIG
2001-06-21).

Substitutions allow the power and flexibility of directives to be
shared by inline text.  They are a way to allow arbitrarily complex
inline objects, while keeping the details out of the flow of text.
They are the equivalent of SGML/XML's named entities.  For example, an
inline image (using reference syntax alternative 4d (vertical bars)
and definition alternative 3, the alternatives chosen for inclusion in
the spec)::

    The |biohazard| symbol must be used on containers used to dispose
    of medical waste.

    .. |biohazard| image:: biohazard.png
       [height=20 width=20]

The ``|biohazard|`` substitution reference will be replaced in-line by
whatever the ``.. |biohazard|`` substitution definition generates (in
this case, an image).  A substitution definition contains the
substitution text bracketed with vertical bars, followed by a an
embedded inline-compatible directive, such as "image".  A transform is
required to complete the substitution.

Syntax alternatives for the reference:

1. Use the existing interpreted text syntax, with a predefined role
   such as "sub"::

       The `biohazard`:sub: symbol...

   Advantages: existing syntax, explicit.  Disadvantages: verbose,
   obtrusive.

2. Use a variant of the interpreted text syntax, with a new suffix
   akin to the underscore in phrase-link references::

       (a) `name`@
       (b) `name`#
       (c) `name`&
       (d) `name`/
       (e) `name`<
       (f) `name`::
       (g) `name`:


   Due to incompatibility with other constructs and ordinary text
   usage, (f) and (g) are not possible.

3. Use interpreted text syntax with a fixed internal format::

       (a) `:name:`
       (b) `name:`
       (c) `name::`
       (d) `::name::`
       (e) `%name%`
       (f) `#name#`
       (g) `/name/`
       (h) `&name&`
       (i) `|name|`
       (j) `[name]`
       (k) `<name>`
       (l) `&name;`
       (m) `'name'`

   To avoid ML confusion (k) and (l) are definitely out.  Square
   brackets (j) won't work in the target (the substitution definition
   would be indistinguishable from a footnote).

   The ```/name/``` syntax (g) is reminiscent of "s/find/sub"
   substitution syntax in ed-like languages.  However, it may have a
   misleading association with regexps, and looks like an absolute
   POSIX path.  (i) is visually equivalent and lacking the
   connotations.

   A disadvantage of all of these is that they limit interpreted text,
   albeit only slightly.

4. Use specialized syntax, something new::

       (a) #name#
       (b) @name@
       (c) /name/
       (d) |name|
       (e) <<name>>
       (f) //name//
       (g) ||name||
       (h) ^name^
       (i) [[name]]
       (j) ~name~
       (k) !name!
       (l) =name=
       (m) ?name?
       (n) >name<

   "#" (a) and "@" (b) are obtrusive.  "/" (c) without backquotes
   looks just like a POSIX path; it is likely for such usage to appear
   in text.

   "|" (d) and "^" (h) are feasible.

5. Redefine the trailing underscore syntax.  See definition syntax
   alternative 4, below.

Syntax alternatives for the definition:

1. Use the existing directive syntax, with a predefined directive such
   as "sub".  It contains a further embedded directive resolving to an
   inline-compatible object::

       .. sub:: biohazard
          .. image:: biohazard.png
             [height=20 width=20]

       .. sub:: parrot
          That bird wouldn't *voom* if you put 10,000,000 volts
          through it!

   The advantages and disadvantages are the same as in inline
   alternative 1.

2. Use syntax as in #1, but with an embedded directivecompressed::

       .. sub:: biohazard image:: biohazard.png
          [height=20 width=20]

   This is a bit better than alternative 1, but still too much.

3. Use a variant of directive syntax, incorporating the substitution
   text, obviating the need for a special "sub" directive name.  If we
   assume reference alternative 4d (vertical bars), the matching
   definition would look like this::

       .. |biohazard| image:: biohazard.png
          [height=20 width=20]

4. (Suggested by Alan Jaffray on Doc-SIG from 2001-11-06.)

   Instead of adding new syntax, redefine the trailing underscore
   syntax to mean "substitution reference" instead of "hyperlink
   reference".  Alan's example::

       I had lunch with Jonathan_ today.  We talked about Zope_.

       .. _Jonathan: lj [user=jhl]
       .. _Zope: https://www.zope.dev/

   A problem with the proposed syntax is that URIs which look like
   simple reference names (alphanum plus ".", "-", "_") would be
   indistinguishable from substitution directive names.  A more
   consistent syntax would be::

       I had lunch with Jonathan_ today.  We talked about Zope_.

       .. _Jonathan: lj:: user=jhl
       .. _Zope: https://www.zope.dev/

   (``::`` after ``.. _Jonathan: lj``.)

   The "Zope" target is a simple external hyperlink, but the
   "Jonathan" target contains a directive.  Alan proposed is that the
   reference text be replaced by whatever the referenced directive
   (the "directive target") produces.  A directive reference becomes a
   hyperlink reference if the contents of the directive target resolve
   to a hyperlink.  If the directive target resolves to an icon, the
   reference is replaced by an inline icon.  If the directive target
   resolves to a hyperlink, the directive reference becomes a
   hyperlink reference.

   This seems too indirect and complicated for easy comprehension.

   The reference in the text will sometimes become a link, sometimes
   not.  Sometimes the reference text will remain, sometimes not.  We
   don't know *at the reference*::

       This is a `hyperlink reference`_; its text will remain.
       This is an `inline icon`_; its text will disappear.

   That's a problem.

The syntax that has been incorporated into the spec and parser is
reference alternative 4d with definition alternative 3::

    The |biohazard| symbol...

    .. |biohazard| image:: biohazard.png
       [height=20 width=20]

We can also combine substitution references with hyperlink references,
by appending a "_" (named hyperlink reference) or "__" (anonymous
hyperlink reference) suffix to the substitution reference.  This
allows us to click on an image-link::

    The |biohazard|_ symbol...

    .. |biohazard| image:: biohazard.png
       [height=20 width=20]
    .. _biohazard: https://www.cdc.gov/

There have been several suggestions for the naming of these
constructs, originally called "substitution references" and
"substitutions".

1. Candidate names for the reference construct:

   (a) substitution reference
   (b) tagging reference
   (c) inline directive reference
   (d) directive reference
   (e) indirect inline directive reference
   (f) inline directive placeholder
   (g) inline directive insertion reference
   (h) directive insertion reference
   (i) insertion reference
   (j) directive macro reference
   (k) macro reference
   (l) substitution directive reference

2. Candidate names for the definition construct:

   (a) substitution
   (b) substitution directive
   (c) tag
   (d) tagged directive
   (e) directive target
   (f) inline directive
   (g) inline directive definition
   (h) referenced directive
   (i) indirect directive
   (j) indirect directive definition
   (k) directive definition
   (l) indirect inline directive
   (m) named directive definition
   (n) inline directive insertion definition
   (o) directive insertion definition
   (p) insertion definition
   (q) insertion directive
   (r) substitution definition
   (s) directive macro definition
   (t) macro definition
   (u) substitution directive definition
   (v) substitution definition

"Inline directive reference" (1c) seems to be an appropriate term at
first, but the term "inline" is redundant in the case of the
reference.  Its counterpart "inline directive definition" (2g) is
awkward, because the directive definition itself is not inline.

"Directive reference" (1d) and "directive definition" (2k) are too
vague.  "Directive definition" could be used to refer to any
directive, not just those used for inline substitutions.

One meaning of the term "macro" (1k, 2s, 2t) is too
programming-language-specific.  Also, macros are typically simple text
substitution mechanisms: the text is substituted first and evaluated
later.  reStructuredText substitution definitions are evaluated in
place at parse time and substituted afterwards.

"Insertion" (1h, 1i, 2n-2q) is almost right, but it implies that
something new is getting added rather than one construct being
replaced by another.

Which brings us back to "substitution".  The overall best names are
"substitution reference" (1a) and "substitution definition" (2v).  A
long way to go to add one word!


Inline External Targets
=======================

Currently reStructuredText has two hyperlink syntax variations:

* Named hyperlinks::

      This is a named reference_ of one word ("reference").  Here is
      a `phrase reference`_.  Phrase references may even cross `line
      boundaries`_.

      .. _reference: https://www.example.org/reference/
      .. _phrase reference: https://www.example.org/phrase_reference/
      .. _line boundaries: https://www.example.org/line_boundaries/

  + Advantages:

    - The plaintext is readable.
    - Each target may be reused multiple times (e.g., just write
      ``"reference_"`` again).
    - No synchronized ordering of references and targets is necessary.

  + Disadvantages:

    - The reference text must be repeated as target names; could lead
      to mistakes.
    - The target URLs may be located far from the references, and hard
      to find in the plaintext.

* Anonymous hyperlinks (in current reStructuredText)::

      This is an anonymous reference__.  Here is an anonymous
      `phrase reference`__.  Phrase references may even cross `line
      boundaries`__.

      __ https://www.example.org/reference/
      __ https://www.example.org/phrase_reference/
      __ https://www.example.org/line_boundaries/

  + Advantages:

    - The plaintext is readable.
    - The reference text does not have to be repeated.

  + Disadvantages:

    - References and targets must be kept in sync.
    - Targets cannot be reused.
    - The target URLs may be located far from the references.

For comparison and historical background, StructuredText also has two
syntaxes for hyperlinks:

* First, ``"reference text":URL``::

      This is a "reference":https://www.example.org/reference/
      of one word ("reference").  Here is a "phrase
      reference":https://www.example.org/phrase_reference/.

* Second, ``"reference text", https://example.org/absolute_URL``::

      This is a "reference", https://www.example.org/reference/
      of one word ("reference").  Here is a "phrase reference",
      https://www.example.org/phrase_reference/.

Both syntaxes share advantages and disadvantages:

+ Advantages:

  - The target is specified immediately adjacent to the reference.

+ Disadvantages:

  - Poor plaintext readability.
  - Targets cannot be reused.
  - Both syntaxes use double quotes, common in ordinary text.
  - In the first syntax, the URL and the last word are stuck
    together, exacerbating the line wrap problem.
  - The second syntax is too magical; text could easily be written
    that way by accident (although only absolute URLs are recognized
    here, perhaps because of the potential for ambiguity).

A new type of "inline external hyperlink" has been proposed.

1. On 2002-06-28, Simon Budig proposed__ a new syntax for
   reStructuredText hyperlinks::

       This is a reference_(https://www.example.org/reference/) of one
       word ("reference").  Here is a `phrase
       reference`_(https://www.example.org/phrase_reference/).  Are
       these examples, (single-underscore), named?  If so, `anonymous
       references`__(https://www.example.org/anonymous/) using two
       underscores would probably be preferable.

   __ https://mail.python.org/pipermail/doc-sig/2002-June/002648.html

   The syntax, advantages, and disadvantages are similar to those of
   StructuredText.

   + Advantages:

     - The target is specified immediately adjacent to the reference.

   + Disadvantages:

     - Poor plaintext readability.
     - Targets cannot be reused (unless named, but the semantics are
       unclear).

   + Problems:

     - The ``"`ref`_(URL)"`` syntax forces the last word of the
       reference text to be joined to the URL, making a potentially
       very long word that can't be wrapped (URLs can be very long).
       The reference and the URL should be separate.  This is a
       symptom of the following point:

     - The syntax produces a single compound construct made up of two
       equally important parts, *with syntax in the middle*, *between*
       the reference and the target.  This is unprecedented in
       reStructuredText.

     - The "inline hyperlink" text is *not* a named reference (there's
       no lookup by name), so it shouldn't look like one.

     - According to the IETF standards RFC 2396 and RFC 2732,
       parentheses are legal URI characters and curly braces are legal
       email characters, making their use prohibitively difficult.

     - The named/anonymous semantics are unclear.

2. After an analysis__ of the syntax of (1) above, we came up with the
   following compromise syntax::

       This is an anonymous reference__
       __<https://www.example.org/reference/> of one word
       ("reference").  Here is a `phrase reference`__
       __<https://www.example.org/phrase_reference/>.  `Named
       references`_ _<https://www.example.org/anonymous/> use single
       underscores.

   __ https://mail.python.org/pipermail/doc-sig/2002-July/002670.html

   The syntax builds on that of the existing "inline internal
   targets": ``an _`inline internal target`.``

   + Advantages:

     - The target is specified immediately adjacent to the reference,
       improving maintainability:

       - References and targets are easily kept in sync.
       - The reference text does not have to be repeated.

     - The construct is executed in two parts: references identical to
       existing references, and targets that are new but not too big a
       stretch from current syntax.

     - There's overwhelming precedent for quoting URLs with angle
       brackets [#]_.

   + Disadvantages:

     - Poor plaintext readability.
     - Lots of "line noise".
     - Targets cannot be reused (unless named; see below).

   To alleviate the readability issue slightly, we could allow the
   target to appear later, such as after the end of the sentence::

       This is a named reference__ of one word ("reference").
       __<https://www.example.org/reference/>  Here is a `phrase
       reference`__.  __<https://www.example.org/phrase_reference/>

   Problem: this could only work for one reference at a time
   (reference/target pairs must be proximate [refA trgA refB trgB],
   not interleaved [refA refB trgA trgB] or nested [refA refB trgB
   trgA]).  This variation is too problematic; references and inline
   external targets will have to be kept immediately adjacent (see (3)
   below).

   The ``"reference__ __<target>"`` syntax is actually for "anonymous
   inline external targets", emphasized by the double underscores.  It
   follows that single trailing and leading underscores would lead to
   *implicitly named* inline external targets.  This would allow the
   reuse of targets by name.  So after ``"reference_ _<target>"``,
   another ``"reference_"`` would point to the same target.

   .. [#]
      From RFC 2396 (URI syntax):

          The angle-bracket "<" and ">" and double-quote (")
          characters are excluded [from URIs] because they are often
          used as the delimiters around URI in text documents and
          protocol fields.

          Using <> angle brackets around each URI is especially
          recommended as a delimiting style for URI that contain
          whitespace.

      From RFC 822 (email headers):

          Angle brackets ("<" and ">") are generally used to indicate
          the presence of a one machine-usable reference (e.g.,
          delimiting mailboxes), possibly including source-routing to
          the machine.

3. If it is best for references and inline external targets to be
   immediately adjacent, then they might as well be integrated.
   Here's an alternative syntax embedding the target URL in the
   reference::

       This is an anonymous `reference <https://www.example.org
       /reference/>`__ of one word ("reference").  Here is a `phrase
       reference <https://www.example.org/phrase_reference/>`__.

   Advantages and disadvantages are similar to those in (2).
   Readability is still an issue, but the syntax is a bit less
   heavyweight (reduced line noise).  Backquotes are required, even
   for one-word references; the target URL is included within the
   reference text, forcing a phrase context.

   We'll call this variant "embedded URIs".

   Problem: how to refer to a title like "HTML Anchors: <a>" (which
   ends with an HTML/SGML/XML tag)?  We could either require more
   syntax on the target (like ``"`reference text
   __<https://example.org/>`__"``), or require the odd conflicting
   title to be escaped (like ``"`HTML Anchors: \<a>`__"``).  The
   latter seems preferable, and not too onerous.

   Similarly to (2) above, a single trailing underscore would convert
   the reference & inline external target from anonymous to implicitly
   named, allowing reuse of targets by name.

   I think this is the least objectionable of the syntax alternatives.

Other syntax variations have been proposed (by Brett Cannon and Benja
Fallenstein)::

    `phrase reference`->https://www.example.org

    `phrase reference`@https://www.example.org

    `phrase reference`__ ->https://www.example.org

    `phrase reference` [-> https://www.example.org]

    `phrase reference`__ [-> https://www.example.org]

    `phrase reference` <https://www.example.org>_

None of these variations are clearly superior to #3 above.  Some have
problems that exclude their use.

With any kind of inline external target syntax it comes down to the
conflict between maintainability and plaintext readability.  I don't
see a major problem with reStructuredText's maintainability, and I
don't want to sacrifice plaintext readability to "improve" it.

The proponents of inline external targets want them for easily
maintainable web pages.  The arguments go something like this:

- Named hyperlinks are difficult to maintain because the reference
  text is duplicated as the target name.

  To which I said, "So use anonymous hyperlinks."

- Anonymous hyperlinks are difficult to maintain because the
  references and targets have to be kept in sync.

  "So keep the targets close to the references, grouped after each
  paragraph.  Maintenance is trivial."

- But targets grouped after paragraphs break the flow of text.

  "Surely less than URLs embedded in the text!  And if the intent is
  to produce web pages, not readable plaintext, then who cares about
  the flow of text?"

Many participants have voiced their objections to the proposed syntax:

    Garth Kidd: "I strongly prefer the current way of doing it.
    Inline is spectactularly messy, IMHO."

    Tony Ibbs: "I vehemently agree... that the inline alternatives
    being suggested look messy - there are/were good reasons they've
    been taken out...  I don't believe I would gain from the new
    syntaxes."

    Paul Moore: "I agree as well.  The proposed syntax is far too
    punctuation-heavy, and any of the alternatives discussed are
    ambiguous or too subtle."

Others have voiced their support:

    fantasai: "I agree with Simon.  In many cases, though certainly
    not in all, I find parenthesizing the url in plain text flows
    better than relegating it to a footnote."

    Ken Manheimer: "I'd like to weigh in requesting some kind of easy,
    direct inline reference link."

(Interesting that those *against* the proposal have been using
reStructuredText for a while, and those *for* the proposal are either
new to the list ["fantasai", background unknown] or longtime
StructuredText users [Ken Manheimer].)

I was initially ambivalent/against the proposed "inline external
targets".  I value reStructuredText's readability very highly, and
although the proposed syntax offers convenience, I don't know if the
convenience is worth the cost in ugliness.  Does the proposed syntax
compromise readability too much, or should the choice be left up to
the author?  Perhaps if the syntax is *allowed* but its use strongly
*discouraged*, for aesthetic/readability reasons?

After a great deal of thought and much input from users, I've decided
that there are reasonable use cases for this construct.  The
documentation should strongly caution against its use in most
situations, recommending independent block-level targets instead.
Syntax #3 above ("embedded URIs") will be used.


Doctree Representation of Transitions
=====================================

(Although not reStructuredText-specific, this section fits best in
this document.)

Having added the "horizontal rule" construct to the `reStructuredText
Markup Specification`_, a decision had to be made as to how to reflect
the construct in the implementation of the document tree.  Given this
source::

    Document
    ========

    Paragraph 1

    --------

    Paragraph 2

The horizontal rule indicates a "transition" (in prose terms) or the
start of a new "division".  Before implementation, the parsed document
tree would be::

    <document>
        <section names="document">
            <title>
                Document
            <paragraph>
                Paragraph 1
            --------               <--- error here
            <paragraph>
                Paragraph 2

There are several possibilities for the implementation:

1. Implement horizontal rules as "divisions" or segments.  A
   "division" is a title-less, non-hierarchical section.  The first
   try at an implementation looked like this::

       <document>
           <section names="document">
               <title>
                   Document
               <paragraph>
                   Paragraph 1
               <division>
                   <paragraph>
                       Paragraph 2

   But the two paragraphs are really at the same level; they shouldn't
   appear to be at different levels.  There's really an invisible
   "first division".  The horizontal rule splits the document body
   into two segments, which should be treated uniformly.

2. Treating "divisions" uniformly brings us to the second
   possibility::

       <document>
           <section names="document">
               <title>
                   Document
               <division>
                   <paragraph>
                       Paragraph 1
               <division>
                   <paragraph>
                       Paragraph 2

   With this change, documents and sections will directly contain
   divisions and sections, but not body elements.  Only divisions will
   directly contain body elements.  Even without a horizontal rule
   anywhere, the body elements of a document or section would be
   contained within a division element.  This makes the document tree
   deeper.  This is similar to the way HTML_ treats document contents:
   grouped within a ``<body>`` element.

3. Implement them as "transitions", empty elements::

       <document>
           <section names="document">
               <title>
                   Document
               <paragraph>
                   Paragraph 1
               <transition>
               <paragraph>
                   Paragraph 2

   A transition would be a "point element", not containing anything,
   only identifying a point within the document structure.  This keeps
   the document tree flatter, but the idea of a "point element" like
   "transition" smells bad.  A transition isn't a thing itself, it's
   the space between two divisions.  However, transitions are a
   practical solution.

Solution 3 was chosen for incorporation into the document tree model.

.. _HTML: https://www.w3.org/MarkUp/


Syntax for Line Blocks
======================

* An early idea: How about a literal-block-like prefix, perhaps
  "``;;``"?  (It is, after all, a *semi-literal* literal block, no?)
  Example::

      Take it away, Eric the Orchestra Leader!  ;;

          A one, two, a one two three four

          Half a bee, philosophically,
          must, *ipso facto*, half not be.
          But half the bee has got to be,
          *vis a vis* its entity.  D'you see?

          But can a bee be said to be
          or not to be an entire bee,
          when half the bee is not a bee,
          due to some ancient injury?

          Singing...

  Kinda lame.

* Another idea: in an ordinary paragraph, if the first line ends with
  a backslash (escaping the newline), interpret the entire paragraph
  as a verse block?  For example::

      Add just one backslash\
      And this paragraph becomes
      An awful haiku

  (Awful, and arguably invalid, since in Japanese the word "haiku"
  contains three syllables not two.)

  This idea was superseded by the rules for escaped whitespace, useful
  for `character-level inline markup`_.

* In a `2004-02-22 docutils-develop message`__, Jarno Elonen proposed
  a "plain list" syntax (and also provided a patch)::

       | John Doe
       | President, SuperDuper Corp.
       | jdoe@example.org

  __ https://thread.gmane.org/gmane.text.docutils.devel/1187

  This syntax is very natural.  However, these "plain lists" seem very
  similar to line blocks, and I see so little intrinsic "list-ness"
  that I'm loathe to add a new object.  I used the term "blurbs" to
  remove the "list" connotation from the originally proposed name.
  Perhaps line blocks could be refined to add the two properties they
  currently lack:

  A) long lines wrap nicely
  B) HTML output doesn't look like program code in non-CSS web
     browsers

  (A) is an issue of all 3 aspects of Docutils: syntax (construct
  behaviour), internal representation, and output.  (B) is partly an
  issue of internal representation but mostly of output.

ReStructuredText will redefine line blocks with the "|"-quoting
syntax.  The following is my current thinking.


Syntax
------

Perhaps line block syntax like this would do::

     | M6: James Bond
     | MIB: Mr. J.
     | IMF: not decided yet, but probably one of the following:
     |   Ethan Hunt
     |   Jim Phelps
     |   Claire Phelps
     | CIA: Lea Leiter

Note that the "nested" list does not have nested syntax (the "|" are
not further indented); the leading whitespace would still be
significant somehow (more below).  As for long lines in the input,
this could suffice::

     | John Doe
     | Founder, President, Chief Executive Officer, Cook, Bottle
       Washer, and All-Round Great Guy
     | SuperDuper Corp.
     | jdoe@example.org

The lack of "|" on the third line indicates that it's a continuation
of the second line, wrapped.

I don't see much point in allowing arbitrary nested content.  Multiple
paragraphs or bullet lists inside a "blurb" doesn't make sense to me.
Simple nested line blocks should suffice.


Internal Representation
-----------------------

Line blocks are currently represented as text blobs as follows::

     <!ELEMENT line_block %text.model;>
     <!ATTLIST line_block
         %basic.atts;
         %fixedspace.att;>

Instead, we could represent each line by a separate element::

     <!ELEMENT line_block (line+)>
     <!ATTLIST line_block %basic.atts;>

     <!ELEMENT line %text.model;>
     <!ATTLIST line %basic.atts;>

We'd keep the significance of the leading whitespace of each line
either by converting it to non-breaking spaces at output, or with a
per-line margin.  Non-breaking spaces are simpler (for HTML, anyway)
but kludgey, and wouldn't support indented long lines that wrap.  But
should inter-word whitespace (i.e., not leading whitespace) be
preserved?  Currently it is preserved in line blocks.

Representing a more complex line block may be tricky::

     | But can a bee be said to be
     |     or not to be an entire bee,
     |         when half the bee is not a bee,
     |             due to some ancient injury?

Perhaps the representation could allow for nested line blocks::

     <!ELEMENT line_block (line | line_block)+>

With this model, leading whitespace would no longer be significant.
Instead, left margins are implied by the nesting.  The example above
could be represented as follows::

     <line_block>
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

I wasn't sure what to do about even more complex line blocks::

     |     Indented
     | Not indented
     |   Indented a bit
     |     A bit more
     |  Only one space

How should that be parsed and nested?  Should the first line have
the same nesting level (== indentation in the output) as the fourth
line, or the same as the last line?  Mark Nodine suggested that such
line blocks be parsed similarly to complexly-nested block quotes,
which seems reasonable.  In the example above, this would result in
the nesting of first line matching the last line's nesting.  In
other words, the nesting would be relative to neighboring lines
only.


Output
------

In HTML, line blocks are currently output as "<pre>" blocks, which
gives us significant whitespace and line breaks, but doesn't allow
long lines to wrap and causes monospaced output without stylesheets.
Instead, we could output "<div>" elements parallelling the
representation above, where each nested <div class="line_block"> would
have an increased left margin (specified in the stylesheet).

Jarno suggested the following HTML output::

    <div class="line_block">
       <span class="line">First, top level line</span><br class="hidden"/>
       <div class="line_block"><span class="hidden">&nbsp;</span>
          <span class="line">Second, once nested</span><br class="hidden"/>
          <span class="line">Third, once nested</span><br class="hidden"/>
          ...
       </div>
       ...
    </div>

The ``<br class="hidden" />`` and ``<span
class="hidden">&nbsp;</span>`` are meant to support non-CSS and
non-graphical browsers.  I understand the case for "br", but I'm not
so sure about hidden "&nbsp;".  I question how much effort should be
put toward supporting non-graphical and especially non-CSS browsers,
at least for html4css1.py output.

Should the lines themselves be ``<span>`` or ``<div>``?  I don't like
mixing inline and block-level elements.


Implementation Plan
-------------------

We'll leave the old implementation in place (via the "line-block"
directive only) until all Writers have been updated to support the new
syntax & implementation.  The "line-block" directive can then be
updated to use the new internal representation, and its documentation
will be updated to recommend the new syntax.


List-Driven Tables
==================

The original idea came from Dylan Jay:

    ... to use a two level bulleted list with something to
    indicate it should be rendered as a table ...

It's an interesting idea.  It could be implemented in as a directive
which transforms a uniform two-level list into a table.  Using a
directive would allow the author to explicitly set the table's
orientation (by column or by row), the presence of row headers, etc.

Alternatives:

1. (Implemented in Docutils 0.3.8).

   Bullet-list-tables might look like this::

       .. list-table::

          * - Treat
            - Quantity
            - Description
          * - Albatross!
            - 299
            - On a stick!
          * - Crunchy Frog!
            - 1499
            - If we took the bones out, it wouldn't be crunchy,
              now would it?
          * - Gannet Ripple!
            - 199
            - On a stick!

   This list must be written in two levels.  This wouldn't work::

       .. list-table::

          * Treat
          * Albatross!
          * Gannet!
          * Crunchy Frog!

          * Quantity
          * 299
          * 199
          * 1499

          * Description
          * On a stick!
          * On a stick!
          * If we took the bones out...

   The above is a single list of 12 items.  The blank lines are not
   significant to the markup.  We'd have to explicitly specify how
   many columns or rows to use, which isn't a good idea.

2. Beni Cherniavsky suggested a field list alternative.  It could look
   like this::

       .. field-list-table::
          :headrows: 1

          - :treat: Treat
            :quantity: Quantity
            :descr: Description

          - :treat: Albatross!
            :quantity: 299
            :descr: On a stick!

          - :treat: Crunchy Frog!
            :quantity: 1499
            :descr: If we took the bones out, it wouldn't be
                    crunchy, now would it?

   Column order is determined from the order of fields in the first
   row.  Field order in all other rows is ignored.  As a side-effect,
   this allows trivial re-arrangement of columns.  By using named
   fields, it becomes possible to omit fields in some rows without
   losing track of things, which is important for spans.

3. An alternative to two-level bullet lists would be to use enumerated
   lists for the table cells::

       .. list-table::

           * 1. Treat
             2. Quantity
             3. Description
           * 1. Albatross!
             2. 299
             3. On a stick!
           * 1. Crunchy Frog!
             2. 1499
             3. If we took the bones out, it wouldn't be crunchy,
                now would it?

   That provides better correspondence between cells in the same
   column than does bullet-list syntax, but not as good as field list
   syntax.  I think that were only field-list-tables available, a lot
   of users would use the equivalent degenerate case::

       .. field-list-table::
           - :1: Treat
             :2: Quantity
             :3: Description
           ...

4. Another natural variant is to allow a description list with field
   lists as descriptions::

       .. list-table::
           :headrows: 1

           Treat
               :quantity: Quantity
               :descr: Description
           Albatross!
               :quantity: 299
               :descr: On a stick!
           Crunchy Frog!
               :quantity: 1499
               :descr: If we took the bones out, it wouldn't be
                       crunchy, now would it?

   This would make the whole first column a header column ("stub").
   It's limited to a single column and a single paragraph fitting on
   one source line.  Also it wouldn't allow for empty cells or row
   spans in the first column.  But these are limitations that we could
   live with, like those of simple tables.

The List-driven table feature could be done in many ways.  Each user
will have their preferred usage.  Perhaps a single "list-table"
directive could handle them all, depending on which options and
content are present.

Issues:

* How to indicate that there's 1 header row?  Perhaps two lists?  ::

      .. list-table::

         + - Treat
           - Quantity
           - Description

         * - Albatross!
           - 299
           - On a stick!

  This is probably too subtle though.  Better would be a directive
  option, like ``:headrows: 1``.  An early suggestion for the header
  row(s) was to use a directive option::

      .. field-list-table::
         :header:
             - :treat: Treat
               :quantity: Quantity
               :descr: Description
         - :treat: Albatross!
           :quantity: 299
           :descr: On a stick!

  But the table data is at two levels and looks inconsistent.

  In general, we cannot extract the header row from field lists' field
  names because field names cannot contain everything one might put in
  a table cell.  A separate header row also allows shorter field names
  and doesn't force one to rewrite the whole table when the header
  text changes.  But for simpler cases, we can offer a ":header:
  fields" option, which does extract header cells from field names::

      .. field-list-table::
          :header: fields

          - :Treat: Albatross!
            :Quantity: 299
            :Description: On a stick!

* How to indicate the column widths?  A directive option? ::

      .. list-table::
         :widths: 15 10 35

  Automatic defaults from the text used?

* How to handle row and/or column spans?

  In a field list, column-spans can be indicated by specifying the
  first and last fields, separated by space-dash-space or ellipsis::

      - :foo - baz: quuux
      - :foo ... baz: quuux

  Commas were proposed for column spans::

      - :foo, bar: quux

  But non-adjacent columns become problematic.  Should we report an
  error, or duplicate the value into each span of adjacent columns (as
  was suggested)?  The latter suggestion is appealing but may be too
  clever.  Best perhaps to simply specify the two ends.

  It was suggested that comma syntax should be allowed, too, in order
  to allow the user to avoid trouble when changing the column order.
  But changing the column order of a table with spans is not trivial;
  we shouldn't make it easier to mess up.

  One possible syntax for row-spans is to simply treat any row where a
  field is missing as a row-span from the last row where it appeared.
  Leaving a field empty would still be possible by writing a field
  with empty content.  But this is too implicit.

  Another way would be to require an explicit continuation marker
  (``...``/``-"-``/``"``?) in all but the first row of a spanned
  field.  Empty comments could work ("..").  If implemented, the same
  marker could also be supported in simple tables, which lack
  row-spanning abilities.

  Explicit markup like ":rowspan:" and ":colspan:" was also suggested.

  Sometimes in a table, the first header row contains spans.  It may
  be necessary to provide a way to specify the column field names
  independently of data rows.  A directive option would do it.

* We could specify "column-wise" or "row-wise" ordering, with the same
  markup structure.  For example, with definition data::

      .. list-table::
         :column-wise:

         Treat
             - Albatross!
             - Crunchy Frog!
         Quantity
             - 299
             - 1499
         Description
             - On a stick!
             - If we took the bones out, it wouldn't be
               crunchy, now would it?

* A syntax for _`stubs in grid tables` is easy to imagine::

      +------------------------++------------+----------+
      | Header row, column 1   || Header 2   | Header 3 |
      +========================++============+==========+
      | body row 1, column 1   || column 2   | column 3 |
      +------------------------++------------+----------+

  Or this idea from Nick Moffitt::

      +-----+---+---+
      | XOR # T | F |
      +=====+===+===+
      |   T # F | T |
      +-----+---+---+
      |   F # T | F |
      +-----+---+---+


Auto-Enumerated Lists
=====================

Implemented 2005-03-24: combination of variation 1 & 2.

The advantage of auto-numbered enumerated lists would be similar to
that of auto-numbered footnotes: lists could be written and rearranged
without having to manually renumber them.  The disadvantages are also
the same: input and output wouldn't match exactly; the markup may be
ugly or confusing (depending on which alternative is chosen).

1. Use the "#" symbol.  Example::

       #. Item 1.
       #. Item 2.
       #. Item 3.

   Advantages: simple, explicit.  Disadvantage: enumeration sequence
   cannot be specified (limited to arabic numerals); ugly.

2. As a variation on #1, first initialize the enumeration sequence?
   For example::

       a) Item a.
       #) Item b.
       #) Item c.

   Advantages: simple, explicit, any enumeration sequence possible.
   Disadvantages: ugly; perhaps confusing with mixed concrete/abstract
   enumerators.

3. Alternative suggested by Fred Bremmer, from experience with MoinMoin::

       1. Item 1.
       1. Item 2.
       1. Item 3.

   Advantages: enumeration sequence is explicit (could be multiple
   "a." or "(I)" tokens).  Disadvantages: perhaps confusing; otherwise
   erroneous input (e.g., a duplicate item "1.") would pass silently,
   either causing a problem later in the list (if no blank lines
   between items) or creating two lists (with blanks).

   Take this input for example::

       1. Item 1.

       1. Unintentional duplicate of item 1.

       2. Item 2.

   Currently the parser will produce two list, "1" and "1,2" (no
   warnings, because of the presence of blank lines).  Using Fred's
   notation, the current behavior is "1,1,2 -> 1 1,2" (without blank
   lines between items, it would be "1,1,2 -> 1 [WARNING] 1,2").  What
   should the behavior be with auto-numbering?

   Fred has produced a patch__, whose initial behavior is as follows::

       1,1,1   -> 1,2,3
       1,2,2   -> 1,2,3
       3,3,3   -> 3,4,5
       1,2,2,3 -> 1,2,3 [WARNING] 3
       1,1,2   -> 1,2 [WARNING] 2

   (After the "[WARNING]", the "3" would begin a new list.)

   I have mixed feelings about adding this functionality to the spec &
   parser.  It would certainly be useful to some users (myself
   included; I often have to renumber lists).  Perhaps it's too
   clever, asking the parser to guess too much.  What if you *do* want
   three one-item lists in a row, each beginning with "1."?  You'd
   have to use empty comments to force breaks.  Also, I question
   whether "1,2,2 -> 1,2,3" is optimal behavior.

   In response, Fred came up with "a stricter and more explicit rule
   [which] would be to only auto-number silently if *all* the
   enumerators of a list were identical".  In that case::

       1,1,1   -> 1,2,3
       1,2,2   -> 1,2 [WARNING] 2
       3,3,3   -> 3,4,5
       1,2,2,3 -> 1,2 [WARNING] 2,3
       1,1,2   -> 1,2 [WARNING] 2

   Should any start-value be allowed ("3,3,3"), or should
   auto-numbered lists be limited to begin with ordinal-1 ("1", "A",
   "a", "I", or "i")?

   __ https://sourceforge.net/tracker/index.php?func=detail&aid=548802
      &group_id=38414&atid=422032

4. Alternative proposed by Tony Ibbs::

       #1. First item.
       #3. Aha - I edited this in later.
       #2. Second item.

   The initial proposal required unique enumerators within a list, but
   this limits the convenience of a feature of already limited
   applicability and convenience.  Not a useful requirement; dropped.

   Instead, simply prepend a "#" to a standard list enumerator to
   indicate auto-enumeration.  The numbers (or letters) of the
   enumerators themselves are not significant, except:

   - as a sequence indicator (arabic, roman, alphabetic; upper/lower),

   - and perhaps as a start value (first list item).

   Advantages: explicit, any enumeration sequence possible.
   Disadvantages: a bit ugly.


Adjacent citation references
============================

A special case for inline markup was proposed and implemented:
multiple citation references could be joined into one::

   [cite1]_[cite2]_ instead of requiring [cite1]_ [cite2]_

However, this was rejected as an unwarranted exception to the rules
for inline markup.
(The main motivation for the proposal, grouping citations in the latex writer,
was implemented by recognising the second group in the example above and
transforming it into ``\cite{cite1,cite2}``.)


Inline markup recognition
=========================

Implemented 2011-12-05 (version 0.9):
Extended `inline markup recognition rules`_.

Non-ASCII whitespace, punctuation characters and "international" quotes are
allowed around inline markup (based on `Unicode categories`_). The rules for
ASCII characters were not changed.

Rejected alternatives:

a) Use `Unicode categories`_ for all chars (ASCII or not)

   +1  comprehensible, standards based,
   -1  many "false positives" need escaping,
   -1  not backwards compatible.

b) full backwards compatibility

   :Pi: only before start-string
   :Pf: only behind end-string
   :Po: "conservative" sorting of other punctuation:

        :``.,;!?\\``: Close
        :``¡¿``:   Open

   +1  backwards compatible,
   +1  logical extension of the existing rules,
   -1  exception list for "other" punctuation needed,
   -1  rules even more complicated,
   -1  not clear how to sort "other" punctuation that is currently not
       recognized,
   -2  international quoting convention like
       »German ›angular‹ quotes« not recognized.

.. _Inline markup recognition rules:
   ../../ref/rst/restructuredtext.html#inline-markup-recognition-rules
.. _Unicode categories:
   https://www.unicode.org/Public/5.1.0/ucd/UCD.html#General_Category_Values


-----------------
 Not Implemented
-----------------

Reworking Footnotes
===================

As a further wrinkle (see `Reworking Explicit Markup (Round 1)`_
above), in the wee hours of 2002-02-28 I posted several ideas for
changes to footnote syntax:

    - Change footnote syntax from ``.. [1]`` to ``_[1]``? ...
    - Differentiate (with new DTD elements) author-date "citations"
      (``[GVR2002]``) from numbered footnotes? ...
    - Render footnote references as superscripts without "[]"? ...

These ideas are all related, and suggest changes in the
reStructuredText syntax as well as the docutils tree model.

The footnote has been used for both true footnotes (asides expanding
on points or defining terms) and for citations (references to external
works).  Rather than dealing with one amalgam construct, we could
separate the current footnote concept into strict footnotes and
citations.  Citations could be interpreted and treated differently
from footnotes.  Footnotes would be limited to numerical labels:
manual ("1") and auto-numbered (anonymous "#", named "#label").

The footnote is the only explicit markup construct (starts with ".. ")
that directly translates to a visible body element.  I've always been
a little bit uncomfortable with the ".. " marker for footnotes because
of this; ".. " has a connotation of "special", but footnotes aren't
especially "special".  Printed texts often put footnotes at the bottom
of the page where the reference occurs (thus "foot note").  Some HTML
designs would leave footnotes to be rendered the same positions where
they're defined.  Other online and printed designs will gather
footnotes into a section near the end of the document, converting them
to "endnotes" (perhaps using a directive in our case); but this
"special processing" is not an intrinsic property of the footnote
itself, but a decision made by the document author or processing
system.

Citations are almost invariably collected in a section at the end of a
document or section.  Citations "disappear" from where they are
defined and are magically reinserted at some well-defined point.
There's more of a connection to the "special" connotation of the ".. "
syntax.  The point at which the list of citations is inserted could be
defined manually by a directive (e.g., ".. citations::"), and/or have
default behavior (e.g., a section automatically inserted at the end of
the document) that might be influenced by options to the Writer.

Syntax proposals:

+ Footnotes:

  - Current syntax::

        .. [1] Footnote 1
        .. [#] Auto-numbered footnote.
        .. [#label] Auto-labeled footnote.

  - The syntax proposed in the original 2002-02-28 Doc-SIG post:
    remove the ".. ", prefix a "_"::

        _[1] Footnote 1
        _[#] Auto-numbered footnote.
        _[#label] Auto-labeled footnote.

    The leading underscore syntax (earlier dropped because
    ``.. _[1]:`` was too verbose) is a useful reminder that footnotes
    are hyperlink targets.

  - Minimal syntax: remove the ".. [" and "]", prefix a "_", and
    suffix a "."::

        _1. Footnote 1.
        _#. Auto-numbered footnote.
        _#label. Auto-labeled footnote.

                 ``_1.``, ``_#.``, and ``_#label.`` are markers,
                 like list markers.

    Footnotes could be rendered something like this in HTML

        | 1. This is a footnote.  The brackets could be dropped
        |    from the label, and a vertical bar could set them
        |    off from the rest of the document in the HTML.

    Two-way hyperlinks on the footnote marker ("1." above) would also
    help to differentiate footnotes from enumerated lists.

    If converted to endnotes (by a directive/transform), a horizontal
    half-line might be used instead.  Page-oriented output formats
    would typically use the horizontal line for true footnotes.

+ Footnote references:

  - Current syntax::

        [1]_, [#]_, [#label]_

  - Minimal syntax to match the minimal footnote syntax above::

        1_, #_, #label_

    As a consequence, pure-numeric hyperlink references would not be
    possible; they'd be interpreted as footnote references.

+ Citation references: no change is proposed from the current footnote
  reference syntax::

      [GVR2001]_

+ Citations:

  - Current syntax (footnote syntax)::

        .. [GVR2001] Python Documentation; van Rossum, Drake, et al.;
           https://www.python.org/doc/

  - Possible new syntax::

        _[GVR2001] Python Documentation; van Rossum, Drake, et al.;
                   https://www.python.org/doc/

        _[DJG2002]
            Docutils: Python Documentation Utilities project; Goodger
            et al.; https://docutils.sourceforge.io/

    Without the ".. " marker, subsequent lines would either have to
    align as in one of the above, or we'd have to allow loose
    alignment (I'd rather not)::

        _[GVR2001] Python Documentation; van Rossum, Drake, et al.;
            https://www.python.org/doc/

I proposed adopting the "minimal" syntax for footnotes and footnote
references, and adding citations and citation references to
reStructuredText's repertoire.  The current footnote syntax for
citations is better than the alternatives given.

From a reply by Tony Ibbs on 2002-03-01:

    However, I think easier with examples, so let's create one::

        Fans of Terry Pratchett are perhaps more likely to use
        footnotes [1]_ in their own writings than other people
        [2]_.  Of course, in *general*, one only sees footnotes
        in academic or technical writing - it's use in fiction
        and letter writing is not normally considered good
        style [4]_, particularly in emails (not a medium that
        lends itself to footnotes).

        .. [1] That is, little bits of referenced text at the
           bottom of the page.
        .. [2] Because Terry himself does, of course [3]_.
        .. [3] Although he has the distinction of being
           *funny* when he does it, and his fans don't always
           achieve that aim.
        .. [4] Presumably because it detracts from linear
           reading of the text - this is, of course, the point.

    and look at it with the second syntax proposal::

        Fans of Terry Pratchett are perhaps more likely to use
        footnotes [1]_ in their own writings than other people
        [2]_.  Of course, in *general*, one only sees footnotes
        in academic or technical writing - it's use in fiction
        and letter writing is not normally considered good
        style [4]_, particularly in emails (not a medium that
        lends itself to footnotes).

        _[1] That is, little bits of referenced text at the
             bottom of the page.
        _[2] Because Terry himself does, of course [3]_.
        _[3] Although he has the distinction of being
             *funny* when he does it, and his fans don't always
             achieve that aim.
        _[4] Presumably because it detracts from linear
             reading of the text - this is, of course, the point.

    (I note here that if I have gotten the indentation of the
    footnotes themselves correct, this is clearly not as nice.  And if
    the indentation should be to the left margin instead, I like that
    even less).

    and the third (new) proposal::

        Fans of Terry Pratchett are perhaps more likely to use
        footnotes 1_ in their own writings than other people
        2_.  Of course, in *general*, one only sees footnotes
        in academic or technical writing - it's use in fiction
        and letter writing is not normally considered good
        style 4_, particularly in emails (not a medium that
        lends itself to footnotes).

        _1. That is, little bits of referenced text at the
            bottom of the page.
        _2. Because Terry himself does, of course 3_.
        _3. Although he has the distinction of being
            *funny* when he does it, and his fans don't always
            achieve that aim.
        _4. Presumably because it detracts from linear
            reading of the text - this is, of course, the point.

    I think I don't, in practice, mind the targets too much (the use
    of a dot after the number helps a lot here), but I do have a
    problem with the body text, in that I don't naturally separate out
    the footnotes as different than the rest of the text - instead I
    keep wondering why there are numbers interspered in the text.  The
    use of brackets around the numbers ([ and ]) made me somehow parse
    the footnote references as "odd" - i.e., not part of the body text
    - and thus both easier to skip, and also (paradoxically) easier to
    pick out so that I could follow them.

    Thus, for the moment (and as always susceptable to argument), I'd
    say -1 on the new form of footnote reference (i.e., I much prefer
    the existing ``[1]_`` over the proposed ``1_``), and ambivalent
    over the proposed target change.

    That leaves David's problem of wanting to distinguish footnotes
    and citations - and the only thing I can propose there is that
    footnotes are numeric or # and citations are not (which, as a
    human being, I can probably cope with!).

From a reply by Paul Moore on 2002-03-01:

    I think the current footnote syntax ``[1]_`` is *exactly* the
    right balance of distinctness vs unobtrusiveness.  I very
    definitely don't think this should change.

    On the target change, it doesn't matter much to me.

From a further reply by Tony Ibbs on 2002-03-01, referring to the
"[1]" form and actual usage in email:

    Clearly this is a form people are used to, and thus we should
    consider it strongly (in the same way that the usage of ``*..*``
    to mean emphasis was taken partly from email practise).

    Equally clearly, there is something "magical" for people in the
    use of a similar form (i.e., ``[1]``) for both footnote reference
    and footnote target - it seems natural to keep them similar.

    ...

    I think that this established plaintext usage leads me to strongly
    believe we should retain square brackets at both ends of a
    footnote.  The markup of the reference end (a single trailing
    underscore) seems about as minimal as we can get away with.  The
    markup of the target end depends on how one envisages the thing -
    if ".." means "I am a target" (as I tend to see it), then that's
    good, but one can also argue that the "_[1]" syntax has a neat
    symmetry with the footnote reference itself, if one wishes (in
    which case ".." presumably means "hidden/special" as David seems
    to think, which is why one needs a ".." *and* a leading underline
    for hyperlink targets.

Given the persuading arguments voiced, we'll leave footnote & footnote
reference syntax alone.  Except that these discussions gave rise to
the "auto-symbol footnote" concept, which has been added.  Citations
and citation references have also been added.


Syntax for Questions & Answers
==============================

Implement as a generic two-column marked list?  As a standalone
(non-directive) construct?  (Is the markup ambiguous?)  Add support to
parts.contents?

New elements would be required.  Perhaps::

    <!ELEMENT question_list (question_list_item+)>
    <!ATTLIST question_list
        numbering  (none | local | global)
                            #IMPLIED
        start     NUMBER    #IMPLIED>
    <!ELEMENT question_list_item (question, answer*)>
    <!ELEMENT question %text.model;>
    <!ELEMENT answer (%body.elements;)+>

Originally I thought of implementing a Q&A list with special syntax::

    Q: What am I?

    A: You are a question-and-answer
       list.

    Q: What are you?

    A: I am the omniscient "we".

Where each "Q" and "A" could also be numbered (e.g., "Q1").  However,
a simple enumerated or bulleted list will do just fine for syntax.  A
directive could treat the list specially; e.g. the first paragraph
could be treated as a question, the remainder as the answer (multiple
answers could be represented by nested lists).  Without special
syntax, this directive becomes low priority.

As described in the FAQ__, no special syntax or directive is needed
for this application.

__ https://docutils.sourceforge.io/FAQ.html
   #how-can-i-mark-up-a-faq-or-other-list-of-questions-answers


--------
 Tabled
--------

Reworking Explicit Markup (Round 2)
===================================

See `Reworking Explicit Markup (Round 1)`_ for an earlier discussion.

In April 2004, a new thread becan on docutils-develop: `Inconsistency
in RST markup`__.  Several arguments were made; the first argument
begat later arguments.  Below, the arguments are paraphrased "in
quotes", with responses.

__ https://thread.gmane.org/gmane.text.docutils.devel/1386

1. References and targets take this form::

       targetname_

       .. _targetname: stuff

   But footnotes, "which generate links just like targets do", are
   written as::

       [1]_

       .. [1] stuff

   "Footnotes should be written as"::

       [1]_

       .. _[1]: stuff

   But they're not the same type of animal.  That's not a "footnote
   target", it's a *footnote*.  Being a target is not a footnote's
   primary purpose (an arguable point).  It just happens to grow a
   target automatically, for convenience.  Just as a section title::

       Title
       =====

   isn't a "title target", it's a *title*, which happens to grow a
   target automatically.  The consistency is there, it's just deeper
   than at first glance.

   Also, ".. [1]" was chosen for footnote syntax because it closely
   resembles one form of actual footnote rendering.  ".. _[1]:" is too
   verbose; excessive punctuation is required to get the job done.

   For more of the reasoning behind the syntax, see `Problems With
   StructuredText (Hyperlinks) <problems.html#hyperlinks>`__ and
   `Reworking Footnotes`_.

2. "I expect directives to also look like ``.. this:`` [one colon]
   because that also closely parallels the link and footnote target
   markup."

   There are good reasons for the two-colon syntax:

       Two colons are used after the directive type for these reasons:

       - Two colons are distinctive, and unlikely to be used in common
         text.

       - Two colons avoids clashes with common comment text like::

             .. Danger: modify at your own risk!

       - If an implementation of reStructuredText does not recognize a
         directive (i.e., the directive-handler is not installed), a
         level-3 (error) system message is generated, and the entire
         directive block (including the directive itself) will be
         included as a literal block.  Thus "::" is a natural choice.

       -- `restructuredtext.html#directives
       <../../ref/rst/restructuredtext.html#directives>`__

   The last reason is not particularly compelling; it's more of a
   convenient coincidence or mnemonic.

3. "Comments always seemed too easy.  I almost never write comments.
   I'd have no problem writing '.. comment:' in front of my comments.
   In fact, it would probably be more readable, as comments *should*
   be set off strongly, because they are very different from normal
   text."

   Many people do use comments though, and some applications of
   reStructuredText require it.  For example, all reStructuredText
   PEPs (and this document!) have an Emacs stanza at the bottom, in a
   comment.  Having to write ".. comment::" would be very obtrusive.

   Comments *should* be dirt-easy to do.  It should be easy to
   "comment out" a block of text.  Comments in programming languages
   and other markup languages are invariably easy.

   Any author is welcome to preface their comments with "Comment:" or
   "Do Not Print" or "Note to Editor" or anything they like.  A
   "comment" directive could easily be implemented.  It might be
   confused with admonition directives, like "note" and "caution"
   though.  In unrelated (and unpublished and unfinished) work, adding
   a "comment" directive as a true document element was considered::

       If structure is necessary, we could use a "comment" directive
       (to avoid nonsensical DTD changes, the "comment" directive
       could produce an untitled topic element).

4. "One of the goals of reStructuredText is to be *readable* by people
   who don't know it.  This construction violates that: it is not at
   all obvious to the uninitiated that text marked by '..' is a
   comment.  On the other hand, '.. comment:' would be totally
   transparent."

   Totally transparent, perhaps, but also very obtrusive.  Another of
   `reStructuredText's goals`_ is to be unobtrusive, and
   ".. comment::" would violate that.  The goals of reStructuredText
   are many, and they conflict.  Determining the right set of goals
   and finding solutions that best fit is done on a case-by-case
   basis.

   Even readability is has two aspects.  Being readable without any
   prior knowledge is one.  Being as easily read in raw form as in
   processed form is the other.  ".." may not contribute to the former
   aspect, but ".. comment::" would certainly detract from the latter.

   .. _author's note:
   .. _reStructuredText's goals: ../../ref/rst/introduction.html#goals

5. "Recently I sent someone an rst document, and they got confused; I
   had to explain to them that '..' marks comments, *unless* it's a
   directive, etc..."

   The explanation of directives *is* roundabout, defining comments in
   terms of not being other things.  That's definitely a wart.

6. "Under the current system, a mistyped directive (with ':' instead
   of '::') will be silently ignored.  This is an error that could
   easily go unnoticed."

   A parser option/setting like "--comments-on-stderr" would help.

7. "I'd prefer to see double-dot-space / command / double-colon as the
   standard Docutils markup-marker.  It's unusual enough to avoid
   being accidentally used.  Everything that starts with a double-dot
   should end with a double-colon."

   That would increase the punctuation verbosity of some constructs
   considerably.

8. Edward Loper proposed the following plan for backwards
   compatibility:

       1. ".. foo" will generate a deprecation warning to stderr, and
          nothing in the output (no system messages).
       2. ".. foo: bar" will be treated as a directive foo.  If there
          is no foo directive, then do the normal error output.
       3. ".. foo:: bar" will generate a deprecation warning to
          stderr, and be treated as a directive.  Or leave it valid?

       So some existing documents might start printing deprecation
       warnings, but the only existing documents that would *break*
       would be ones that say something like::

           .. warning: this should be a comment

       instead of::

           .. warning:: this should be a comment

       Here, we're trading fairly common a silent error (directive
       falsely treated as a comment) for a fairly uncommon explicitly
       flagged error (comment falsely treated as directive).  To make
       things even easier, we could add a sentence to the
       unknown-directive error.  Something like "If you intended to
       create a comment, please use '.. comment:' instead".

On one hand, I understand and sympathize with the points raised.  On
the other hand, I think the current syntax strikes the right balance
(but I acknowledge a possible lack of objectivity).  On the gripping
hand, the comment and directive syntax has become well established, so
even if it's a wart, it may be a wart we have to live with.

Making any of these changes would cause a lot of breakage or at least
deprecation warnings.  I'm not sure the benefit is worth the cost.

For now, we'll treat this as an unresolved legacy issue.


-------
 To Do
-------

Nested Inline Markup
====================

These are collected notes on a long-discussed issue.  The original
mailing list messages should be referred to for details.

* In a 2001-10-31 discussion I wrote:

      Try, for example, `Ed Loper's 2001-03-21 post`_, which details
      some rules for nested inline markup. I think the complexity is
      prohibitive for the marginal benefit. (And if you can understand
      that tree without going mad, you're a better man than I. ;-)

      Inline markup is already fragile. Allowing nested inline markup
      would only be asking for trouble IMHO. If it proves absolutely
      necessary, it can be added later. The rules for what can appear
      inside what must be well thought out first though.

      .. _Ed Loper's 2001-03-21 post:
         https://mail.python.org/pipermail/doc-sig/2001-March/001487.html

      -- https://mail.python.org/pipermail/doc-sig/2001-October/002354.html

* In a 2001-11-09 Doc-SIG post, I wrote:

      The problem is that in the
      what-you-see-is-more-or-less-what-you-get markup language that
      is reStructuredText, the symbols used for inline markup ("*",
      "**", "`", "``", etc.) may preclude nesting.

  I've rethought this position.  Nested markup is not precluded, just
  tricky.  People and software parse "double and 'single' quotes" all
  the time.  Continuing,

      I've thought over how we might implement nested inline
      markup. The first algorithm ("first identify the outer inline
      markup as we do now, then recursively scan for nested inline
      markup") won't work; counterexamples were given in my `last post
      <https://mail.python.org/pipermail/doc-sig/2001-November/002363.html>`__.

      The second algorithm makes my head hurt::

          while 1:
              scan for start-string
              if found:
                  push on stack
                  scan for start or end string
                  if new start string found:
                      recurse
                  elif matching end string found:
                      pop stack
                  elif non-matching end string found:
                      if its a markup error:
                          generate warning
                      elif the initial start-string was misinterpreted:
                          # e.g. in this case: ***strong** in emphasis*
                          restart with the other interpretation
                          # but it might be several layers back ...
              ...

      This is similar to how the parser does section title
      recognition, but sections are much more regular and
      deterministic.

      Bottom line is, I don't think the benefits are worth the effort,
      even if it is possible. I'm not going to try to write the code,
      at least not now. If somebody codes up a consistent, working,
      general solution, I'll be happy to consider it.

      -- https://mail.python.org/pipermail/doc-sig/2001-November/002388.html

* In a `2003-05-06 Docutils-Users post`__ Paul Tremblay proposed a new
  syntax to allow for easier nesting.  It eventually evolved into
  this::

      :role:[inline text]

  The duplication with the existing interpreted text syntax is
  problematic though.

  __ https://article.gmane.org/gmane.text.docutils.user/317

* Could the parser be extended to parse nested interpreted text? ::

      :emphasis:`Some emphasized text with :strong:`some more
      emphasized text` in it and **perhaps** :reference:`a link``

* In a `2003-06-18 Docutils-Develop post`__, Mark Nodine reported on
  his implementation of a form of nested inline markup in his
  Perl-based parser (unpublished).  He brought up some interesting
  ideas.  The implementation was flawed, however, by the change in
  semantics required for backslash escapes.

  __ https://article.gmane.org/gmane.text.docutils.devel/795

* Docutils-develop threads between David Abrahams, David Goodger, and
  Mark Nodine (beginning 2004-01-16__ and 2004-01-19__) hashed out
  many of the details of a potentially successful implementation, as
  described below.  David Abrahams checked in code to the "nesting"
  branch of CVS, awaiting thorough review.

  __ https://thread.gmane.org/gmane.text.docutils.devel/1102
  __ https://thread.gmane.org/gmane.text.docutils.devel/1125

It may be possible to accomplish nested inline markup in general with
a more powerful inline markup parser.  There may be some issues, but
I'm not averse to the idea of nested inline markup in general.  I just
don't have the time or inclination to write a new parser now.  Of
course, a good patch would be welcome!

I envisage something like this.  Explicit-role interpreted text must
be nestable.  Prefix-based is probably preferred, since suffix-based
will look like inline literals::

    ``text`:role1:`:role2:

But it can be disambiguated, so it ought to be left up to the author::

    `\ `text`:role1:`:role2:

In addition, other forms of inline markup may be nested if
unambiguous::

    *emphasized ``literal`` and |substitution ref| and link_*

IOW, the parser ought to be as permissive as possible.


Index Entries & Indexes
=======================

Were I writing a book with an index, I guess I'd need two
different kinds of index targets: inline/implicit and
out-of-line/explicit.  For example::

    In this `paragraph`:index:, several words are being
    `marked`:index: inline as implicit `index`:index:
    entries.

    .. index:: markup
    .. index:: syntax

    The explicit index directives above would refer to
    this paragraph.  It might also make sense to allow multiple
    entries in an ``index`` directive:

    .. index::
        markup
        syntax

The words "paragraph", "marked", and "index" would become index
entries pointing at the words in the first paragraph.  The index
entry words appear verbatim in the text.  (Don't worry about the
ugly ":index:" part; if indexing is the only/main application of
interpreted text in your documents, it can be implicit and
omitted.)  The two directives provide manual indexing, where the
index entry words ("markup" and "syntax") do not appear in the
main text.  We could combine the two directives into one::

    .. index:: markup; syntax

Semicolons instead of commas because commas could *be* part of the
index target, like::

    .. index:: van Rossum, Guido

Another reason for index directives is because other inline markup
wouldn't be possible within inline index targets.

Sometimes index entries have multiple levels.  Given::

    .. index:: statement syntax: expression statements

In a hypothetical index, combined with other entries, it might
look like this::

    statement syntax
        expression statements ..... 56
        assignment ................ 57
        simple statements ......... 58
        compound statements ....... 60

Inline multi-level index targets could be done too.  Perhaps
something like::

    When dealing with `expression statements <statement syntax:>`,
    we must remember ...

The opposite sense could also be possible::

    When dealing with `index entries <:multi-level>`, there are
    many permutations to consider.

Also "see / see also" index entries.

Given::

    Here's a paragraph.

    .. index:: paragraph

(The "index" directive above actually targets the *preceding*
object.)  The directive should produce something like this XML::

    <paragraph>
    <index_entry text="paragraph"/>
    Here's a paragraph.
    </paragraph>

This kind of content model would also allow true inline
index-entries::

    Here's a `paragraph`:index:.

If the "index" role were the default for the application, it could be
dropped::

    Here's a `paragraph`.

Both of these would result in this XML::

    <paragraph>
    Here's a <index_entry>paragraph</index_entry>.
    </paragraph>


from 2002-06-24 docutils-develop posts
--------------------------------------

    If all of your index entries will appear verbatim in the text,
    this should be sufficient.  If not (e.g., if you want "Van Rossum,
    Guido" in the index but "Guido van Rossum" in the text), we'll
    have to figure out a supplemental mechanism, perhaps using
    substitutions.

I've thought a bit more on this, and I came up with two possibilities:

1. Using interpreted text, embed the index entry text within the
   interpreted text::

       ... by `Guido van Rossum [Van Rossum, Guido]` ...

   The problem with this is obvious: the text becomes cluttered and
   hard to read.  The processed output would drop the text in
   brackets, which goes against the spirit of interpreted text.

2. Use substitutions::

       ... by |Guido van Rossum| ...

       .. |Guido van Rossum| index:: Van Rossum, Guido

   A problem with this is that each substitution definition must have
   a unique name.  A subsequent ``.. |Guido van Rossum| index:: BDFL``
   would be illegal.  Some kind of anonymous substitution definition
   mechanism would be required, but I think that's going too far.

Both of these alternatives are flawed.  Any other ideas?


-------------------
 ... Or Not To Do?
-------------------

This is the realm of the possible but questionably probable.  These
ideas are kept here as a record of what has been proposed, for
posterity and in case any of them prove to be useful.


Compound Enumerated Lists
=========================

Allow for compound enumerators, such as "1.1." or "1.a." or "1(a)", to
allow for nested enumerated lists without indentation?


Indented Lists
==============

Allow for variant styles by interpreting indented lists as if they
weren't indented?  For example, currently the list below will be
parsed as a list within a block quote::

    paragraph

      * list item 1
      * list item 2

But a lot of people seem to write that way, and HTML browsers make it
look as if that's the way it should be.  The parser could check the
contents of block quotes, and if they contain only a single list,
remove the block quote wrapper.  There would be two problems:

1. What if we actually *do* want a list inside a block quote?

2. What if such a list comes immediately after an indented construct,
   such as a literal block?

Both could be solved using empty comments (problem 2 already exists
for a block quote after a literal block).  But that's a hack.

Perhaps a runtime setting, allowing or disabling this convenience,
would be appropriate.  But that raises issues too:

    User A, who writes lists indented (and their config file is set up
    to allow it), sends a file to user B, who doesn't (and their
    config file disables indented lists).  The result of processing by
    the two users will be different.

It may seem minor, but it adds ambiguity to the parser, which is bad.

See the `Doc-SIG discussion starting 2001-04-18`__ with Ed Loper's
"Structuring: a summary; and an attempt at EBNF", item 4 (and
follow-ups, here__ and here__).  Also `docutils-users, 2003-02-17`__
and `beginning 2003-08-04`__.

__ https://mail.python.org/pipermail/doc-sig/2001-April/001776.html
__ https://mail.python.org/pipermail/doc-sig/2001-April/001789.html
__ https://mail.python.org/pipermail/doc-sig/2001-April/001793.html
__ https://sourceforge.net/mailarchive/message.php?msg_id=3838913
__ https://sf.net/mailarchive/forum.php?thread_id=2957175&forum_id=11444


Sloppy Indentation of List Items
================================

Perhaps the indentation shouldn't be so strict.  Currently, this is
required::

    1. First line,
       second line.

Anything wrong with this? ::

    1. First line,
     second line.

Problem? ::

    1. First para.

       Block quote.  (no good: requires some indent relative to first
       para)

     Second Para.

    2. Have to carefully define where the literal block ends::

         Literal block

       Literal block?

Hmm...  Non-strict indentation isn't such a good idea.
Except for `field lists`_.

.. _field lists: ../../ref/rst/restructuredtext.html#field-lists


Lazy Indentation of List Items
==============================

Another approach: Going back to the first draft of reStructuredText
(2000-11-27 post to Doc-SIG)::

    - This is the fourth item of the main list (no blank line above).
    The second line of this item is not indented relative to the
    bullet, which precludes it from having a second paragraph.

Change that to *require* a blank line above and below, to reduce
ambiguity.  This "loosening" may be added later, once the parser's
been nailed down.  However, a serious drawback of this approach is to
limit the content of each list item to a single paragraph.


David's Idea for Lazy Indentation
---------------------------------

Consider a paragraph in a word processor.  It is a single logical line
of text which ends with a newline, soft-wrapped arbitrarily at the
right edge of the page or screen.  We can think of a plaintext
paragraph in the same way, as a single logical line of text, ending
with two newlines (a blank line) instead of one, and which may contain
arbitrary line breaks (newlines) where it was accidentally
hard-wrapped by an application.  We can compensate for the accidental
hard-wrapping by "unwrapping" every unindented second and subsequent
line.  The indentation of the first line of a paragraph or list item
would determine the indentation for the entire element.  Blank lines
would be required between list items when using lazy indentation.

The following example shows the lazy indentation of multiple body
elements::

    - This is the first paragraph
    of the first list item.

      Here is the second paragraph
    of the first list item.

    - This is the first paragraph
    of the second list item.

      Here is the second paragraph
    of the second list item.

A more complex example shows the limitations of lazy indentation::

    - This is the first paragraph
    of the first list item.

      Next is a definition list item:

      Term
          Definition.  The indentation of the term is
    required, as is the indentation of the definition's
    first line.

          When the definition extends to more than
    one line, lazy indentation may occur.  (This is the second
    paragraph of the definition.)

    - This is the first paragraph
    of the second list item.

      - Here is the first paragraph of
    the first item of a nested list.

      So this paragraph would be outside of the nested list,
    but inside the second list item of the outer list.

    But this paragraph is not part of the list at all.

And the ambiguity remains::

    - Look at the hyphen at the beginning of the next line
    - is it a second list item marker, or a dash in the text?

    Similarly, we may want to refer to numbers inside enumerated
    lists:

    1. How many socks in a pair? There are
    2. How many pants in a pair? Exactly
    1. Go figure.

Literal blocks and block quotes would still require consistent
indentation for all their lines.  For block quotes, we might be able
to get away with only requiring that the first line of each contained
element be indented.  For example::

    Here's a paragraph.

        This is a paragraph inside a block quote.
    Second and subsequent lines need not be indented at all.

        - A bullet list inside
    the block quote.

          Second paragraph of the
    bullet list inside the block quote.

Although feasible, this form of lazy indentation has problems.  The
document structure and hierarchy is not obvious from the indentation,
making the source plaintext difficult to read.  This will also make
keeping track of the indentation while writing difficult and
error-prone.  However, these problems may be acceptable for Wikis and
email mode, where we may be able to rely on less complex structure
(few nested lists, for example).


Multiple Roles in Interpreted Text
==================================

In reStructuredText, inline markup cannot be nested (yet; `see
above`__).  This also applies to interpreted text.  In order to
simultaneously combine multiple roles for a single piece of text, a
syntax extension would be necessary.  Ideas:

1. Initial idea::

       `interpreted text`:role1,role2:

2. Suggested by Jason Diamond::

       `interpreted text`:role1:role2:

If a document is so complex as to require nested inline markup,
perhaps another markup system should be considered.  By design,
reStructuredText does not have the flexibility of XML.

__ `Nested Inline Markup`_


Parameterized Interpreted Text
==============================

In some cases it may be expedient to pass parameters to interpreted
text, analogous to function calls.  Ideas:

1. Parameterize the interpreted text role itself (suggested by Jason
   Diamond)::

       `interpreted text`:role1(foo=bar):

   Positional parameters could also be supported::

       `CSS`:acronym(Cascading Style Sheets): is used for HTML, and
       `CSS`:acronym(Content Scrambling System): is used for DVDs.

   Technical problem: current interpreted text syntax does not
   recognize roles containing whitespace.  Design problem: this smells
   like programming language syntax, but reStructuredText is not a
   programming language.

2. Put the parameters inside the interpreted text::

       `CSS (Cascading Style Sheets)`:acronym: is used for HTML, and
       `CSS (Content Scrambling System)`:acronym: is used for DVDs.

   Although this could be defined on an individual basis (per role),
   we ought to have a standard.  Hyperlinks with embedded URIs already
   use angle brackets; perhaps they could be used here too::

       `CSS <Cascading Style Sheets>`:acronym: is used for HTML, and
       `CSS <Content Scrambling System>`:acronym: is used for DVDs.

   Do angle brackets connote URLs too much for this to be acceptable?
   How about the "tag" connotation -- does it save them or doom them?

3. `Nested inline markup`_ could prove useful here::

       `CSS :def:`Cascading Style Sheets``:acronym: is used for HTML,
       and `CSS :def:`Content Scrambling System``:acronym: is used for
       DVDs.

   Inline markup roles could even define the default roles of nested
   inline markup, allowing this cleaner syntax::

       `CSS `Cascading Style Sheets``:acronym: is used for HTML, and
       `CSS `Content Scrambling System``:acronym: is used for DVDs.

Does this push inline markup too far?  Readability becomes a serious
issue.  Substitutions may provide a better alternative (at the expense
of verbosity and duplication) by pulling the details out of the text
flow::

    |CSS| is used for HTML, and |CSS-DVD| is used for DVDs.

    .. |CSS| acronym:: Cascading Style Sheets
    .. |CSS-DVD| acronym:: Content Scrambling System
       :text: CSS

----------------------------------------------------------------------

This whole idea may be going beyond the scope of reStructuredText.
Documents requiring this functionality may be better off using XML or
another markup system.

This argument comes up regularly when pushing the envelope of
reStructuredText syntax.  I think it's a useful argument in that it
provides a check on creeping featurism.  In many cases, the resulting
verbosity produces such unreadable plaintext that there's a natural
desire *not* to use it unless absolutely necessary.  It's a matter of
finding the right balance.


Syntax for Interpreted Text Role Bindings
=========================================

The following syntax (idea from Jeffrey C. Jacobs) could be used to
associate directives with roles::

    .. :rewrite: class:: rewrite

    `She wore ribbons in her hair and it lay with streaks of
    grey`:rewrite:

The syntax is similar to that of substitution declarations, and the
directive/role association may resolve implementation issues.  The
semantics, ramifications, and implementation details would need to be
worked out.

The example above would implement the "rewrite" role as adding a
``class="rewrite"`` attribute to the interpreted text ("inline"
element).  The stylesheet would then pick up on the "class" attribute
to do the actual formatting.

The advantage of the new syntax would be flexibility.  Uses other than
"class" may present themselves.  The disadvantage is complexity:
having to implement new syntax for a relatively specialized operation,
and having new semantics in existing directives ("class::" would do
something different).

The `"role" directive`__ has been implemented.

__ ../../ref/rst/directives.html#role


Character Processing
====================

Several people have suggested adding some form of character processing
to reStructuredText:

* Some sort of automated replacement of ASCII sequences:

  - ``--`` to em-dash (or ``--`` to en-dash, and ``---`` to em-dash).
  - Convert quotes to curly quote entities.  (Essentially impossible
    for HTML?  Unnecessary for TeX.)
  - Various forms of ``:-)`` to smiley icons.
  - ``"\ "`` to &nbsp;.  Problem with line-wrapping though: it could
    end up escaping the newline.
  - Escaped newlines to <BR>.
  - Escaped period or quote or dash as a disappearing catalyst to
    allow character-level inline markup?

* XML-style character entities, such as "&copy;" for the copyright
  symbol.

Docutils has no need of a character entity subsystem.  Supporting
Unicode and text encodings, character entities should be directly
represented in the text: a copyright symbol should be represented by
the copyright symbol character.  If this is not possible in an
authoring environment, a pre-processing stage can be added, or a table
of substitution definitions can be devised.

A "unicode" directive has been implemented to allow direct
specification of esoteric characters.  In combination with the
substitution construct, `standard definition files`_ for common
sets of character entities are provided for inclusion.

To allow for `character-level inline markup`_, a limited form of
character processing has been added to the spec and parser: escaped
whitespace characters are removed from the processed document.  Any
further character processing will be of this functional type, rather
than of the character-encoding type.

.. _standard definition files: ../../ref/rst/definitions.html
.. _character-level inline markup:
   ../../ref/rst/restructuredtext.html#character-level-inline-markup

* Directive idea::

      .. text-replace:: "pattern" "replacement"

  - Support Unicode "U+XXXX" codes.
  - Support regexps, perhaps with alternative "regexp-replace"
    directive.
  - Flags for regexps; ":flags:" option, or individuals.
  - Specifically, should the default be case-sensistive or
    -insensitive?


Page Or Line Breaks
===================

* Should ^L (or something else in reST) be defined to mean
  force/suggest page breaks in whatever output we have?

  A "break" or "page-break" directive would be easy to add.  A new
  doctree element would be required though (perhaps "break").  The
  final behavior would be up to the Writer.  The directive argument
  could be one of page/column/recto/verso for added flexibility.

  Currently ^L (Python's ``\f``) characters are treated as whitespace.
  They're converted to single spaces, actually, as are vertical tabs
  (^K, Python's ``\v``).  It would be possible to recognize form feeds
  as markup, but it requires some thought and discussion first.  Are
  there any downsides?  Many editing environments do not allow the
  insertion of control characters.  Will it cause any harm?  It would
  be useful as a shorthand for the directive.

  It's common practice to use ^L before Emacs "Local Variables"
  lists (to prevent misinterpretation of unrelated text)::

      ^L
      ..
         Local Variables:
         mode: indented-text
         indent-tabs-mode: nil
         sentence-end-double-space: t
         fill-column: 70
         End:

  These are already present in many PEPs and Docutils project
  documents.  From the Emacs manual (info):

      A "local variables list" goes near the end of the file, in the
      last page.  (It is often best to put it on a page by itself.)

  It would be unfortunate if this construct caused a final blank page
  to be generated (for those Writers that recognize the page breaks).
  We'll have to add a transform that looks for a "break" plus zero or
  more comments at the end of a document, and removes them.

  Probably a bad idea because there is no such thing as a page in a
  generic document format.

* Could the "break" concept above be extended to inline forms?
  E.g. "^L" in the middle of a sentence could cause a line break.
  Only recognize it at the end of a line (i.e., ``\f\n``)?

  Or is formfeed inappropriate?  Perhaps vertical tab (``\v``), but
  even that's a stretch.  Can't use carriage returns, since they're
  commonly used for line endings.

  Probably a bad idea as well because we do not want to use control
  characters for well-readable and well-writable markup, and after all
  we have the line block syntax for line breaks.


Superscript Markup
==================

Add ``^superscript^`` inline markup?  The only common non-markup uses
of "^" I can think of are as short hand for "superscript" itself and
for describing control characters ("^C to cancel").  The former
supports the proposed syntax, and it could be argued that the latter
ought to be literal text anyhow (e.g. "``^C`` to cancel").

However, superscripts are seldom needed, and new syntax would break
existing documents.  When it's needed, the ``:superscript:``
(``:sup:``) role can be used as well.


Code Execution
==============

Add the following directives?

- "exec": Execute Python code & insert the results.  Call it
  "python" to allow for other languages?

- "system": Execute an ``os.system()`` call, and insert the results
  (possibly as a literal block).  Definitely dangerous!  How to make
  it safe?  Perhaps such processing should be left outside of the
  document, in the user's production system (a makefile or a script or
  whatever).  Or, the directive could be disabled by default and only
  enabled with an explicit command-line option or config file setting.
  Even then, an interactive prompt may be useful, such as:

      The file.rst document you are processing contains a "system"
      directive requesting that the ``sudo rm -rf /`` command be
      executed.  Allow it to execute?  (y/N)

- "eval": Evaluate an expression & insert the text.  At parse
  time or at substitution time?  Dangerous?  Perhaps limit to canned
  macros; see text.date_.

  .. _text.date: ../todo.html#text-date

It's too dangerous (or too complicated in the case of "eval").  We do
not want to have such things in the core.


``encoding`` Directive
======================

Add an "encoding" directive to specify the character encoding of the
input data?  Not a good idea for the following reasons:

- When it sees the directive, the parser will already have read the
  input data, and encoding determination will already have been done.

- If a file with an "encoding" directive is edited and saved with
  a different encoding, the directive may cause data corruption.


Support for Annotations
=======================

Add an "annotation" role, as the equivalent of the HTML "title"
attribute?  This is secondary information that may "pop up" when the
pointer hovers over the main text.  A corresponding directive would be
required to associate annotations with the original text (by name, or
positionally as in anonymous targets?).

There have not been many requests for such feature, though. [#]_  Also,
cluttering WYSIWYG plaintext with annotations may not seem like a good
idea, and there is no "tool tip" in formats other than HTML. [#]_

.. [#] But see the `feature-request ticket #108`__.

.. [#] As of 2025, there are also annotations in the output formats
   OpenDocument and PDF/LaTeX (the LaTeX package "pdfcomment" provides a
   \pdftooltip macro that creates pop-ups in PDF output).

   __ https://sourceforge.net/p/docutils/feature-requests/108/



Object references
=================

We need syntax for `object references`_.

  - Parameterized substitutions?  For example::

        See |figure (figure name)| on |page (figure name)|.

        .. |figure (name)| figure-ref:: (name)
        .. |page (name)| page-ref:: (name)

    The result would be::

        See figure 3.11 on page 157.

    But this would require substitution directives to be processed at
    reference-time, not at definition-time as they are now.  Or,
    perhaps the directives could just leave ``pending`` elements
    behind, and the transforms do the work?  How to pass the data
    through? Too complicated. Use interpreted text roles.

.. _object references:
   ../todo.html#object-numbering-and-object-references

.. Emacs settings

   Local Variables:
   mode: indented-text
   mode: rst
   indent-tabs-mode: nil
   sentence-end-double-space: t
   fill-column: 70
   End:
