#! /usr/bin/env python3
# $Id$
# Author: Günter Milde <milde@users.sourceforge.net>
# Copyright: This module has been placed in the public domain.

"""
Test `EnvironmentError` reporting.

In some locales, the `errstr` argument of IOError and OSError contains
non-ASCII chars.

In Python 2, converting an exception instance to `str` or `unicode`
might fail, with non-ASCII chars in arguments and the default encoding
and errors ('ascii', 'strict').

Therefore, Docutils must not use string interpolation with exception
instances like, e.g., ::

  try:
    something
  except IOError as error:
    print('Found %s' % error)

unless the minimal required Python version has this problem fixed.
"""

import sys
import unittest
from io import StringIO, BytesIO

import DocutilsTestSupport              # must be imported before docutils
from docutils import parsers, frontend, utils
from docutils.parsers import rst
from docutils.utils.error_reporting import ErrorString, ErrorOutput


class ErrorStringTests(unittest.TestCase):
    def test_str(self):
        bs = "ü".encode("utf-8")
        self.assertEqual("Exception: spam",
                         ErrorString(Exception("spam")))
        self.assertEqual(f"IndexError: {str('ü'.encode('utf-8'))}",
                         ErrorString(IndexError("ü".encode("utf-8"))))

    def test_unicode(self):
        self.assertEqual("Exception: spam",
                         ErrorString(Exception("spam")))
        self.assertEqual(f"IndexError: ü",
                         ErrorString(IndexError("ü")))


# ErrorOutput tests
# -----------------
class ErrorOutputTests(unittest.TestCase):
    def test_defaults(self):
        e = ErrorOutput()
        self.assertEqual(e.stream, sys.stderr)

    def test_bbuf(self):
        buf = BytesIO() # buffer storing byte string
        e = ErrorOutput(buf, encoding="ascii")
        # write byte-string as-is
        e.write(b'b\xfc')
        self.assertEqual(buf.getvalue(), b'b\xfc')
        # encode unicode data with backslashescape fallback replacement:
        e.write(u' u\xfc')
        self.assertEqual(buf.getvalue(), b'b\xfc u\\xfc')
        # handle Exceptions with Unicode string args
        # unicode(Exception(u'e\xfc')) # fails in Python < 2.6
        e.write(AttributeError(u' e\xfc'))
        self.assertEqual(buf.getvalue(), b'b\xfc u\\xfc e\\xfc')
        # encode with `encoding` attribute
        e.encoding = "utf8"
        e.write(u' u\xfc')
        self.assertEqual(buf.getvalue(), b'b\xfc u\\xfc e\\xfc u\xc3\xbc')

    def test_ubuf(self):
        buf = StringIO() # buffer only accepting unicode string
        # decode of binary strings
        e = ErrorOutput(buf, encoding='ascii')
        e.write(b'b\xfc')
        self.assertEqual(buf.getvalue(), u'b\ufffd') # use REPLACEMENT CHARACTER
        # write Unicode string and Exceptions with Unicode args
        e.write(u' u\xfc')
        self.assertEqual(buf.getvalue(), u'b\ufffd u\xfc')
        e.write(AttributeError(u' e\xfc'))
        self.assertEqual(buf.getvalue(), u'b\ufffd u\xfc e\xfc')
        # decode with `encoding` attribute
        e.encoding = 'latin1'
        e.write(b' b\xfc')
        self.assertEqual(buf.getvalue(), u'b\ufffd u\xfc e\xfc b\xfc')


class ErrorReportingTests(unittest.TestCase):
    """
    Test cases where error reporting can go wrong.

    Do not test the exact output (as this varies with the locale), just
    ensure that the correct exception is thrown.
    """

    parser = parsers.rst.Parser()
    """Parser shared by all ParserTestCases."""

    option_parser = frontend.OptionParser(components=(parsers.rst.Parser,))
    settings = option_parser.get_default_values()
    settings.report_level = 1
    settings.halt_level = 1
    settings.warning_stream = ''
    document = utils.new_document('test data', settings)

    def test_include(self):
        source = ('.. include:: bogus.txt')
        self.assertRaises(utils.SystemMessage,
                          self.parser.parse, source, self.document)

    def test_raw_file(self):
        source = ('.. raw:: html\n'
                  '   :file: bogus.html\n')
        self.assertRaises(utils.SystemMessage,
                          self.parser.parse, source, self.document)

    def test_csv_table(self):
        source = ('.. csv-table:: external file\n'
                  '   :file: bogus.csv\n')
        self.assertRaises(utils.SystemMessage,
                          self.parser.parse, source, self.document)

if __name__ == '__main__':
    unittest.main()
