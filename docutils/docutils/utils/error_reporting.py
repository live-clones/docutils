#!/usr/bin/env python3
# :Id: $Id$
# :Copyright: © 2011 Günter Milde.
# :License: Released under the terms of the `2-Clause BSD license`_, in short:
#
#    Copying and distribution of this file, with or without modification,
#    are permitted in any medium without royalty provided the copyright
#    notice and this notice are preserved.
#    This file is offered as-is, without any warranty.
#
# .. _2-Clause BSD license: https://opensource.org/licenses/BSD-2-Clause

"""
Provisional module to handle Exceptions across Python versions.

This module is deprecated in Docutils 0.19.1 and will be removed in
Docutils 1.2.

Error reporting should be safe from encoding/decoding errors.
However, implicit conversions of strings and exceptions like

>>> u'%s world: %s' % ('H\xe4llo', Exception(u'H\xe4llo'))

"""

import codecs
import sys
import warnings

# Guess the locale's encoding.
# If no valid guess can be made, locale_encoding is set to `None`:
try:
    import locale # module missing in Jython
except ImportError:
    locale_encoding = None
else:
    try:
        locale_encoding = locale.getlocale()[1] or locale.getdefaultlocale()[1]
        # locale.getpreferredencoding([do_setlocale=True|False])
        # has side-effects | might return a wrong guess.
        # (cf. Update 1 in http://stackoverflow.com/questions/4082645/using-python-2-xs-locale-module-to-format-numbers-and-currency)
    except ValueError as error: # OS X may set UTF-8 without language code
        # see http://bugs.python.org/issue18378
        # and https://sourceforge.net/p/docutils/bugs/298/
        if "unknown locale: UTF-8" in error.args:
            locale_encoding = "UTF-8"
        else:
            locale_encoding = None
    except: # any other problems determining the locale -> use None
        locale_encoding = None
    try:
        codecs.lookup(locale_encoding or '') # None -> ''
    except LookupError:
        locale_encoding = None


def SafeString(data, encoding=None, encoding_errors="", decoding_errors=""):
    """
    A wrapper providing robust conversion to `str`.
    """
    warnings.warn("error_reporting.SafeString() is not required with Python 3"
                  " and will be removed in Docutils 1.2.",
                  DeprecationWarning, stacklevel=2)
    return str(data)


def ErrorString(data):
    """
    Safely report exception type and message.
    """
    warnings.warn("error_reporting.ErrorString() is not required with Python 3"
                  " and will be removed in Docutils 1.2.",
                  DeprecationWarning, stacklevel=2)
    return f"{data.__class__.__name__}: {data}"


class ErrorOutput(object):
    """
    Wrapper class for file-like error streams with
    failsafe de- and encoding of `str`, `bytes`, and
    `Exception` instances.
    """

    def __init__(self, stream=None, encoding=None,
                 encoding_errors='backslashreplace',
                 decoding_errors='replace'):
        """
        :Parameters:
            - `stream`: a file-like object,
                        a string (path to a file),
                        `None` (write to `sys.stderr`, default), or
                        evaluating to `False` (write() requests are ignored).
            - `encoding`: `stream` text encoding. Guessed if None.
            - `encoding_errors`: how to treat encoding errors.
        """
        if stream is None:
            stream = sys.stderr
        elif not stream:
            stream = False
        # if `stream` is a file name, open it
        elif isinstance(stream, str):
            stream = open(stream, "w")

        self.stream = stream
        """Where warning output is sent."""

        self.encoding = (encoding or getattr(stream, 'encoding', None) or
                         locale_encoding or 'ascii')
        """The output character encoding."""

        self.encoding_errors = encoding_errors
        """Encoding error handler."""

        self.decoding_errors = decoding_errors
        """Decoding error handler."""

    def write(self, data):
        """
        Write `data` to self.stream. Ignore, if self.stream is False.

        `data` can be a `string` or `Exception` instance.
        """
        if self.stream is False:
            return
        if isinstance(data, Exception):
            data = str(data)
        try:
            self.stream.write(data)
        except UnicodeEncodeError:
            self.stream.write(data.encode(self.encoding, self.encoding_errors))
        except TypeError:
            if isinstance(data, str): # passed stream may expect bytes
                self.stream.write(data.encode(self.encoding,
                                              self.encoding_errors))
                return
            if self.stream in (sys.stderr, sys.stdout):
                self.stream.buffer.write(data) # write bytes to raw stream
            else:
                self.stream.write(str(data, self.encoding,
                                          self.decoding_errors))

    def close(self):
        """
        Close the error-output stream.

        Ignored if the stream is` sys.stderr` or `sys.stdout` or has no
        close() method.
        """
        if self.stream in (sys.stdout, sys.stderr):
            return
        try:
            self.stream.close()
        except AttributeError:
            pass
