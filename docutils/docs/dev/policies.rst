.. include:: ../header.rst

===========================
 Docutils Project Policies
===========================

:Author: David Goodger; open to all Docutils developers
:Contact: docutils-develop@lists.sourceforge.net
:Date: $Date$
:Revision: $Revision$
:Copyright: This document has been placed in the public domain.

.. contents::

The Docutils project group is a meritocracy based on code contribution
and lots of discussion [#bcs]_.  A few quotes sum up the policies of
the Docutils project.  The IETF's classic credo (by MIT professor Dave
Clark) is an ideal we can aspire to:

    We reject: kings, presidents, and voting.  We believe in: rough
    consensus and running code.

As architect, chief cook and bottle-washer, David Goodger currently
functions as BDFN (Benevolent Dictator For Now).  (But he would
happily abdicate the throne given a suitable candidate.  Any takers?)

Eric S. Raymond, anthropologist of the hacker subculture, writes in
his essay `The Magic Cauldron`_:

    The number of contributors [to] projects is strongly and inversely
    correlated with the number of hoops each project makes a user go
    through to contribute.

We will endeavour to keep the barrier to entry as low as possible.
The policies below should not be thought of as barriers, but merely as
a codification of experience to date.  These are "best practices";
guidelines, not absolutes.  Exceptions are expected, tolerated, and
used as a source of improvement.  Feedback and criticism is welcome.

As for control issues, Emmett Plant (CEO of the Xiph.org Foundation,
originators of Ogg Vorbis) put it well when he said:

    Open source dictates that you lose a certain amount of control
    over your codebase, and that's okay with us.

.. [#bcs] Phrase borrowed from `Ben Collins-Sussman of the Subversion
   project <http://www.red-bean.com/sussman/svn-anti-fud.html>`__.

.. _The Magic Cauldron:
   http://www.catb.org/~esr/writings/magic-cauldron/


Python Coding Conventions
=========================

Contributed code will not be refused merely because it does not
strictly adhere to these conditions; as long as it's internally
consistent, clean, and correct, it probably will be accepted.  But
don't be surprised if the "offending" code gets fiddled over time to
conform to these conventions.

The Docutils project shall follow the generic coding conventions as
specified in the `Style Guide for Python Code` (:PEP:`8`) and `Docstring
Conventions` (:PEP:`257`), summarized, clarified, and extended as follows:

* 4 spaces per indentation level.  No hard tabs.

* Use UTF-8 encoding (no encoding declaration).
  Identifiers must use ASCII only.

* No one-liner compound statements (i.e., no ``if x: return``: use two
  lines & indentation), except for degenerate class or method
  definitions (i.e., ``class X: pass`` is OK.).

* Lines should be no more than 78 characters long.

* Use "StudlyCaps" for class names (except for element classes in
  docutils.nodes).

* Use "lowercase" or "lowercase_with_underscores" for function,
  method, and variable names.  For short names, maximum two words,
  joined lowercase may be used (e.g. "tagname").  For long names with
  three or more words, or where it's hard to parse the split between
  two words, use lowercase_with_underscores (e.g.,
  "note_explicit_target", "explicit_target").  If in doubt, use
  underscores.

* Avoid lambda expressions, which are inherently difficult to
  understand.  Named functions are preferable and superior: they're
  faster (no run-time compilation), and well-chosen names serve to
  document and aid understanding.

* Avoid functional constructs (filter, map, etc.).  Use list
  comprehensions instead.

* Avoid ``from __future__ import`` constructs.  They are inappropriate
  for production code.

* Use 'single quotes' for string literals, and """triple double
  quotes""" for docstrings.

.. _Docutils Internationalization: ../howto/i18n.html#python-code


Documentation Conventions
=========================

* Docutils documentation is written using reStructuredText, of course.

* The encoding of the documentation files is UTF-8.

* Use the following section title adornment styles::

      ================
       Document Title
      ================

      --------------------------------------------
       Document Subtitle, or Major Division Title
      --------------------------------------------

      Section
      =======

      Subsection
      ----------

      Sub-Subsection
      ``````````````

      Sub-Sub-Subsection
      ..................

* Use two blank lines before each section/subsection/etc. title.  One
  blank line is sufficient between immediately adjacent titles.

* Add a bibliographic field list immediately after the document
  title/subtitle.  See the beginning of this document for an example.

* Add an Emacs "local variables" block in a comment at the end of the
  document.  See the end of this document for an example.


Copyrights and Licensing
========================

The majority of the Docutils project code and documentation has been
placed in the public domain (see `Copying Docutils`_).

Unless clearly and explicitly indicated
otherwise, any patches (modifications to existing files) submitted to
the project for inclusion (via Subversion, SourceForge trackers,
mailing lists, or private email) are assumed to be in the public
domain as well.

Any new files contributed to the project should clearly state their
intentions regarding copyright, in one of the following ways:

* Public domain (preferred): include the statement "This
  module/document has been placed in the public domain."

* Copyright & open source license: include a copyright notice, along
  with either an embedded license statement, a reference to an
  accompanying license file, or a license URL.

  The license should be well known, simple and compatible with other
  open source software licenses. To keep the number of different
  licenses at a minimum, using the `2-Clause BSD license`_
  (`local copy`__) is recommended.

  .. Rationale:
     + clear wording, structured text
     + license used by the closely related Sphinx project

.. _Copying Docutils: ../../COPYING.html
.. _2-Clause BSD license: http://opensource.org/licenses/BSD-2-Clause
__ ../../licenses/BSD-2-Clause.rst


.. _Subversion Repository:

Repository
==========

Please see the `repository documentation`_ for details on how to
access Docutils' Subversion repository.  Anyone can access the
repository anonymously.  Only project developers can make changes.
(If you would like to become a project developer, just ask!)  Also see
`Setting Up For Docutils Development`_ below for some useful info.

Unless you really *really* know what you're doing, please do *not* use
``svn import``.  It's quite easy to mess up the repository with an
import.

.. _repository documentation: repository.html


Branches
--------

(These branch policies go into effect with Docutils 0.4.)

The "docutils" directory of the **trunk** (a.k.a. the **Docutils
core**) is used for active -- but stable, fully tested, and reviewed
-- development.

If we need to cut a bugfix release, we'll create a **maintenance branch**
based on the latest feature release.  For example, when Docutils 0.5 is
released, this would be ``branches/docutils-0.5``, and any existing 0.4.x
maintenance branches may be retired.  Maintenance branches will receive bug
fixes only; no new features will be allowed here.

Obvious and uncontroversial bug fixes *with tests* can be checked in
directly to the core and to the maintenance branches.  Don't forget to
add test cases!  Many (but not all) bug fixes will be applicable both
to the core and to the maintenance branches; these should be applied
to both.  No patches or dedicated branches are required for bug fixes,
but they may be used.  It is up to the discretion of project
developers to decide which mechanism to use for each case.

.. _feature branches:
.. _feature branch:

Feature additions and API changes will be done in **feature
branches**.  Feature branches will not be managed in any way.
Frequent small check-ins are encouraged here.  Feature branches must be
discussed on the `docutils-develop mailing list`_ and reviewed before
being merged into the core.

.. _docutils-develop mailing list:
   https://lists.sourceforge.net/lists/listinfo/docutils-develop


Review Criteria
```````````````

Before a new feature, an API change, or a complex, disruptive, or
controversial bug fix can be checked in to the core or into a
maintenance branch, it must undergo review.  These are the criteria:

* The branch must be complete, and include full documentation and
  tests.

* There should ideally be one branch merge commit per feature or
  change.  In other words, each branch merge should represent a
  coherent change set.

* The code must be stable and uncontroversial.  Moving targets and
  features under debate are not ready to be merged.

* The code must work.  The test suite must complete with no failures.
  See `Docutils Testing`_.

The review process will ensure that at least one other set of eyeballs
& brains sees the code before it enters the core.  In addition to the
above, the general `Check-ins`_ policy (below) also applies.

.. _Docutils testing: testing.html


Check-ins
---------

Changes or additions to the Docutils core and maintenance branches
carry a commitment to the Docutils user community.  Developers must be
prepared to fix and maintain any code they have committed.

The Docutils core (``trunk/docutils`` directory) and maintenance
branches should always be kept in a stable state (usable and as
problem-free as possible).  All changes to the Docutils core or
maintenance branches must be in `good shape`_, usable_, documented_,
tested_, and `reasonably complete`_. Starting with version 1.0, they must
also comply with the `backwards compatibility policy`_.

* _`Good shape` means that the code is clean, readable, and free of
  junk code (unused legacy code; by analogy to "junk DNA").

* _`Usable` means that the code does what it claims to do.  An "XYZ
  Writer" should produce reasonable XYZ output.

* _`Documented`: The more complete the documentation the better.
  Modules & files must be at least minimally documented internally.
  `Docutils Front-End Tools`_ should have a new section for any
  front-end tool that is added.  `Docutils Configuration Files`_
  should be modified with any settings/options defined.  For any
  non-trivial change, the HISTORY.rst_ file should be updated.

* _`Tested` means that unit and/or functional tests, that catch all
  bugs fixed and/or cover all new functionality, have been added to
  the test suite.  These tests must be checked by running the test
  suite under all supported Python versions, and the entire test suite
  must pass.  See `Docutils Testing`_.

* _`Reasonably complete` means that the code must handle all input.
  Here "handle" means that no input can cause the code to fail (cause
  an exception, or silently and incorrectly produce nothing).
  "Reasonably complete" does not mean "finished" (no work left to be
  done).  For example, a writer must handle every standard element
  from the Docutils document model; for unimplemented elements, it
  must *at the very least* warn that "Output for element X is not yet
  implemented in writer Y".

If you really want to check code directly into the Docutils core,
you can, but you must ensure that it fulfills the above criteria
first.  People will start to use it and they will expect it to work!
If there are any issues with your code, or if you only have time for
gradual development, you should put it on a branch or in the sandbox
first.  It's easy to move code over to the Docutils core once it's
complete.

It is the responsibility and obligation of all developers to keep the
Docutils core and maintenance branches stable.  If a commit is made to
the core or maintenance branch which breaks any test, the solution is
simply to revert the change.  This is not vindictive; it's practical.
We revert first, and discuss later.

Docutils will pursue an open and trusting policy for as long as
possible, and deal with any aberrations if (and hopefully not when)
they happen.  We'd rather see a torrent of loose contributions than
just a trickle of perfect-as-they-stand changes.  The occasional
mistake is easy to fix.  That's what version control is for!

.. _Docutils Front-End Tools: ../user/tools.html
.. _Docutils Configuration Files: ../user/config.html
.. _HISTORY.rst: ../../HISTORY.rst


.. _`Version Numbering`:

Version Identification
======================

The state of development of the current Docutils codebase is stored in
two forms: the sequence `docutils.__version_info__`_ and the
`PEP 440`_ conformant text string `docutils.__version__`_.
See also the `Docutils Release Procedure`_

.. _Docutils Release Procedure: release.html#version-numbers


``docutils.__version_info__``
-----------------------------

``docutils.__version_info__`` is an instance of ``docutils.VersionInfo``
based on collections.namedtuple_. It is modelled on `sys.version_info`_
and has the following attributes:

major : non-negative integer
    **Major releases** (x.0, e.g. 1.0) will be rare, and will
    represent major changes in API, functionality, or commitment.  The
    major number will be bumped to 1 when the project is
    feature-complete, and may be incremented later if there is a major
    change in the design or API.  When Docutils reaches version 1.0,
    the major APIs will be considered frozen.
    For details, see the `backwards compatibility policy`_.

minor : non-negative integer
    Releases that change the minor number (x.y, e.g. 0.5) will be
    **feature releases**; new features from the `Docutils core`_ will
    be included.

micro : non-negative integer
    Releases that change the micro number (x.y.z, e.g. 0.4.1) will be
    **bug-fix releases**.  No new features will be introduced in these
    releases; only bug fixes will be included.

    The micro number is omitted from `docutils.__version__`_ when it
    equals zero.

_`releaselevel` : text string
    The release level indicates the `development status`_ (or phase)
    of the project's codebase:

    =============  ==========  ===============================================
    Release Level  Label [#]_  Description
    =============  ==========  ===============================================
    alpha          ``a``       Reserved for use after major experimental
                               changes, to indicate an unstable codebase.

    beta           ``b``       Indicates active development, between releases.

    candidate      ``rc``      Release candidate: indicates that the
                               codebase is ready to release unless
                               significant bugs emerge.

    final                      Indicates an official project release.
    =============  ==========  ===============================================

    .. [#] The labels are used in the `docutils.__version__`_ pre-release
       segment.

    .. _development status:
       https://en.wikipedia.org/wiki/Software_release_life_cycle

_`serial` : non-negative integer
    The serial number is zero for final releases and incremented
    whenever a new pre-release is begun.

_`release` : boolean
    True for official releases and pre-releases, False during
    development.

* One of *{major, minor, micro, serial}* is incremented after each
  release, and the lower-order numbers are reset to 0.

* The default state of the repository during active development is
  release level = "beta", serial = 0, release = False.

``docutils.__version_info__`` can be used to test for a minimally
required version, e.g. ::

    docutils.__version_info__ >= (0, 13)

is True for all versions after ``"0.13"``.

.. _collections.namedtuple:
   https://docs.python.org/3/library/collections.html#collections.namedtuple
.. _sys.version_info:
   https://docs.python.org/3/library/sys.html#sys.version_info

``docutils.__version__``
------------------------

The text string ``docutils.__version__`` is a human readable,
`PEP 440`_-conforming version specifier.  For version comparison
operations, use `docutils.__version_info__`_.

``docutils.__version__`` takes the following form::

    "<major>.<minor>[.<micro>][<releaselevel>[<serial>]][.dev]"
     <--- release segment ---><-- pre-release segment -><- development ->

* The *pre-release segment* contains a label representing the
  releaselevel_ ("a", "b", or "rc") and eventually a serial_ number
  (omitted, if zero).

* The *development segment* is ``".dev"`` during active development
  (release_ == False) and omitted for official releases and pre-releases.

Examples of ``docutils.__version__`` identifiers, over the course of
normal development (without branches), in ascending order:

==============================  =============================
Release Level                   Version Identifier
==============================  =============================
final (release)                 0.14
beta (development) [#dev]_      0.15b.dev
beta (release)  [#skip]_        0.15b
candidate 1 (dev.)              0.15rc1.dev
candidate 1 (release)           0.15rc1
candidate 2 (dev.) [#skip]_     0.15rc2.dev
candidate 2 (release) [#skip]_  0.15rc2
...
final (release)                 0.15
beta (development) [#dev]_      0.16b.dev
==============================  =============================

.. [#dev] Default active development state between releases.
.. [#skip] These steps may be skipped.

.. _PEP 440: https://peps.python.org/pep-0440/

Policy History
--------------

* Prior to version 0.4, Docutils didn't have an official version
  numbering policy, and micro releases contained both bug fixes and
  new features.

* An earlier version of this policy was adopted in October 2005, and
  took effect with Docutils version 0.4.

* This policy was updated in June 2017 for Docutils version 0.14. See
  `Feature Request #50`_ and the `discussion on docutils-devel`__ from
  May 28 to June 20 2017.

  .. _Feature Request #50:
     https://sourceforge.net/p/docutils/feature-requests/50/
  __ https://sourceforge.net/p/docutils/mailman/message/35903816/


Backwards Compatibility Policy
==============================

.. note:: The backwards compatibility policy outlined below is a stub.

Docutils' backwards compatibility policy follows the rules for Python in
:PEP:`387`.

* The scope of the public API is laid out at the start of the `backwards
  compatibility rules`_.

* The rules for `making incompatible changes`_ apply.

A majority of projects depends on Docutils indirectly, via the Sphinx_
document processor.

* Sphinx developers should be given the chance to fix or work around a
  DeprecationWarning_ in the Sphinx development version before a new
  Docutils version is released. Otherwise, use a PendingDeprecationWarning_.

Changes that may affect end-users (e.g. by requiring changes to the
configuration file or potentially breaking custom style sheets) should be
announced with a FutureWarning_.

.. _backwards compatibility rules:
   https://peps.python.org/pep-0387/#backwards-compatibility-rules
.. _making incompatible changes:
   https://peps.python.org/pep-0387/#making-incompatible-changes
.. _Sphinx: https://www.sphinx-doc.org/
.. _DeprecationWarning:
   https://docs.python.org/3/library/exceptions.html#DeprecationWarning
.. _PendingDeprecationWarning:
   https://docs.python.org/3/library/exceptions.html#PendingDeprecationWarning
.. _FutureWarning:
   https://docs.python.org/3/library/exceptions.html#FutureWarning


Snapshots
=========

Snapshot tarballs can be downloaded from the repository (see the "download
snapshot" button in the head of the code listing table).

* the `Docutils core`_, representing the current cutting-edge state of
  development;

* the `sandbox directory`_ with contributed projects and extensions from
  `the Sandbox`_;

.. * maintenance branches, for bug fixes;

   TODO: do we have active maintenance branches?
   (the only branch looking like a maintenance branch is
   https://sourceforge.net/p/docutils/code/HEAD/tree/branches/docutils-0.4)

* `development branches`_, representing ongoing development efforts to bring
  new features into Docutils.

.. _Docutils core:
   https://sourceforge.net/p/docutils/code/HEAD/tree/trunk/docutils
.. _development branches:
   https://sourceforge.net/p/docutils/code/HEAD/tree/branches/


Setting Up For Docutils Development
===================================

When making changes to the code, testing_ is a must.  The code should
be run to verify that it produces the expected results, and the entire
test suite should be run too.  The modified Docutils code has to be
accessible to Python for the tests to have any meaning.
See `editable installs`_ for ways to keep the Docutils code
accessible during development.

.. _testing: tested_
.. _editable installs: repository.html#editable-installs


Mailing Lists
=============

Developers are recommended to subscribe to all `Docutils mailing
lists`_.

.. _Docutils mailing lists: ../user/mailing-lists.html


.. The Wiki
   ========

   The development wiki at http://docutils.python-hosting.com/
   is no longer active.


Extensions and Related Projects
===============================

The Sandbox
-----------

The `sandbox directory`_ is a place to play around, to try out and
share ideas.  It's a part of the Subversion repository but it isn't
distributed as part of Docutils releases.  Feel free to check in code
to the sandbox; that way people can try it out but you won't have to
worry about it working 100% error-free, as is the goal of the Docutils
core.  A project-specific subdirectory should be created for each new
project.  Any developer who wants to play in the sandbox may do so,
but project directories are recommended over personal directories,
which discourage collaboration.  It's OK to make a mess in the
sandbox!  But please, play nice.

Please update the `sandbox README`_ file with links and a brief
description of your work.

In order to minimize the work necessary for others to install and try
out new, experimental components, the following sandbox directory
structure is recommended::

    sandbox/
        project_name/ # For a collaborative project.
            README.rst  # Describe the requirements, purpose/goals, usage,
                        # and list the maintainers.
            docs/
                ...
            component.py    # The component is a single module.
                            # *OR* (but *not* both)
            component/      # The component is a package.
                __init__.py  # Contains the Reader/Writer class.
                other1.py    # Other modules and data files used
                data.rst     # by this component.
                ...
            test/       # Test suite.
                ...
            tools/      # For front ends etc.
                ...
            pyproject.toml   # Project metadata
        userid/       # For *temporary* personal space.

Some sandbox projects are destined to move to the Docutils core once
completed.  Others, such as add-ons to Docutils or applications of
Docutils, may graduate to become `parallel projects`_.

.. _sandbox README: https://docutils.sourceforge.io/sandbox/README.html
.. _sandbox directory:
   https://sourceforge.net/p/docutils/code/HEAD/tree/trunk/sandbox/


.. _parallel project:

Parallel Projects
-----------------

Parallel projects contain useful code that is not central to the
functioning of Docutils.  Examples are specialized add-ons or
plug-ins, and applications of Docutils.  They use Docutils, but
Docutils does not require their presence to function.

An official parallel project will have its own directory beside (or
parallel to) the main ``docutils`` directory in the Subversion
repository.  It can have its own web page in the
docutils.sourceforge.io domain, its own file releases and
downloadable snapshots, and even a mailing list if that proves useful.
However, an official parallel project has implications: it is expected
to be maintained and continue to work with changes to the core
Docutils.

A parallel project requires a project leader, who must commit to
coordinate and maintain the implementation:

* Answer questions from users and developers.
* Review suggestions, bug reports, and patches.
* Monitor changes and ensure the quality of the code and
  documentation.
* Coordinate with Docutils to ensure interoperability.
* Put together official project releases.

Of course, related projects may be created independently of Docutils.
The advantage of a parallel project is that the SourceForge
environment and the developer and user communities are already
established.  Core Docutils developers are available for consultation
and may contribute to the parallel project.  It's easier to keep the
projects in sync when there are changes made to the core Docutils
code.

Other related projects
----------------------

Many related but independent projects are listed in the Docutils
`link list`_. If you want your project to appear there, drop a note at
the Docutils-develop_ mailing list.

.. _link list: https://docutils.sourceforge.io/docs/user/links.html
.. _docutils-develop: docs/user/mailing-lists.html#docutils-develop

.. Emacs settings

   Local Variables:
   mode: indented-text
   mode: rst
   indent-tabs-mode: nil
   sentence-end-double-space: t
   fill-column: 70
   End:
