.. include:: ../header.rst

===================
 Docutils Web Site
===================

:Author: David Goodger; open to all Docutils developers
:Contact: docutils-develop@lists.sourceforge.net
:Date: $Date$
:Revision: $Revision$
:Copyright: This document has been placed in the public domain.

The Docutils web site, <https://docutils.sourceforge.io/>, is
maintained by the ``docutils-update.local`` script, run by project
maintainers on their local machines.  The script
will process any .rst/.txt file which is newer than the corresponding .html
file in the local copy of the project's web directory and upload the changes
to the web site at SourceForge.

Please **do not** add any generated .html files to the Docutils
repository.  They will be generated automatically after a one-time
setup (`described below`__).

__ `Adding .rst/.txt Files`_

The docutils-update.local__ script is located at
``sandbox/infrastructure/docutils-update.local``.

__ https://docutils.sourceforge.io/sandbox/infrastructure/docutils-update.local


Setting Up
==========

(TBA)

.. hint::
  Anyone with checkin privileges can be a web-site maintainer. You need to
  set up the directories for a local website build.

  The procedure for that was on the docutils-devel list a while ago.


Adding .rst/.txt Files
======================

User/Contributor
----------------

When adding a new .rst/.txt file that should be converted to HTML:

#. Edit sandbox/infrastructure/htmlfiles.lst, and add the .html file
   corresponding to the new .rst/.txt file (please keep the sorted order).

#. Commit the edited version to the SVN repository.

Maintainer
----------

#. If there are new directories in the SVN, allow the update script to run
   once to create the directories in the filesystem before preparing for
   HTML processing.

#. Any .html document with a corresponding .rst/.txt file is regenerated
   if the .rst/.txt has changed, but no new .html files will be generated.

   Therefore *touch* the .html-file and then the .rst/.txt.

#. ``docutils-update.local -u``    Regenerate .html unconditionally.


Removing Files & Directories
============================

#. Remove from SVN

#. Remove to-be-generated HTML files from
   ``sandbox/infrastructure/htmlfiles.lst``.

#. Removing files and directories from SVN will not trigger their removal
   from the web site.  Files and directories must be manually removed from
   sourceforge.net (under ``/home/project-web/docutils/htdocs/``).

.. Emacs settings

   Local Variables:
   mode: indented-text
   mode: rst
   indent-tabs-mode: nil
   sentence-end-double-space: t
   fill-column: 70
   End:
