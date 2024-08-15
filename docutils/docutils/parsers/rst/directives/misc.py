# $Id$
# Authors: David Goodger <goodger@python.org>; Dethe Elza
# Copyright: This module has been placed in the public domain.

"""Miscellaneous directives."""

from __future__ import annotations

__docformat__ = 'reStructuredText'

import re
import sys
import time
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.request import urlopen
from urllib.error import URLError

from docutils import io, nodes, statemachine, utils
from docutils.parsers.rst import Directive, convert_directive_function
from docutils.parsers.rst import directives, roles, states
from docutils.parsers.rst.directives.body import CodeBlock, NumberLines
from docutils.transforms import misc

if TYPE_CHECKING:
    import os
    if sys.version_info[:2] >= (3, 12):
        from typing import TypeAlias
    else:
        from typing_extensions import TypeAlias

    from docutils.nodes import Node

    PathString: TypeAlias = str | os.PathLike[str]
    """File system path."""

    SourceString: TypeAlias = str | os.PathLike[str]
    """Path to or informal description of a Docutils input source."""


def adapt_path(path: str, source='', root_prefix='/') -> str:
    # Adapt path to files to include or embed.
    # `root_prefix` is prepended to absolute paths (cf. root_prefix setting),
    # `source` is the `current_source` of the including directive (which may
    # be a file included by the main document).
    if path.startswith('/'):
        base = Path(root_prefix)
        path = path[1:]
    else:
        base = Path(source).parent
    # pepend "base" and convert to relative path for shorter system messages
    return utils.relative_path(None, base/path)


class Include(Directive):

    """
    Include content read from a separate source file.

    Content may be parsed by the parser, or included as a literal
    block.  The encoding of the included file can be specified.  Only
    a part of the given file argument may be included by specifying
    start and end line or text to match before and/or after the text
    to be used.

    https://docutils.sourceforge.io/docs/ref/rst/directives.html#include
    """

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {'literal': directives.flag,
                   'code': directives.unchanged,
                   'encoding': directives.encoding,
                   'parser': directives.parser_name,
                   'tab-width': int,
                   'start-line': int,
                   'end-line': int,
                   'start-after': directives.unchanged_required,
                   'end-before': directives.unchanged_required,
                   # ignored except for 'literal' or 'code':
                   'number-lines': directives.value_or((None,), int),
                   'class': directives.class_option,
                   'name': directives.unchanged}

    standard_include_path = Path(states.__file__).parent / 'include'

    def run(self) -> list[Node]:
        """Include a file as part of the content of this reST file.

        Depending on the options, the file content (or a clipping) is
        converted to nodes and returned or inserted into the input stream.
        """
        self.settings = settings = self.state.document.settings
        if not settings.file_insertion_enabled:
            raise self.warning('"%s" directive disabled.' % self.name)
        self.tab_width = self.options.get('tab-width', settings.tab_width)
        self.clip_options = (self.options.get('start-line', None),
                             self.options.get('end-line', None),
                             self.options.get('start-after', ''),
                             self.options.get('end-before', ''))
        path = directives.path(self.arguments[0])
        if path.startswith('<') and path.endswith('>'):
            path = '/' + path[1:-1]
            root_prefix = self.standard_include_path
        else:
            root_prefix = settings.root_prefix
        path = adapt_path(path,
                          self.state.document.current_source,
                          root_prefix)
        self.options['source'] = path

        inputstring = self.read_file(path)

        if 'literal' in self.options:
            return self.as_literal_block(inputstring)
        if 'code' in self.options:
            return self.as_code_block(inputstring)
        if 'parser' in self.options:
            return self.custom_parse(inputstring)
        self.insert_into_input_lines(inputstring)
        return []

    def read_file(self, path: PathString) -> str:
        """Read text file at `path`. Clip and return content.

        Provisional.
        """
        encoding = self.options.get('encoding', self.settings.input_encoding)
        error_handler = self.settings.input_encoding_error_handler
        try:
            include_file = io.FileInput(source_path=path,
                                        encoding=encoding,
                                        error_handler=error_handler)
        except UnicodeEncodeError:
            raise self.severe(f'Problems with "{self.name}" directive path:\n'
                              f'Cannot encode input file path "{path}" '
                              '(wrong locale?).')
        except OSError as error:
            raise self.severe(f'Problems with "{self.name}" directive path:\n'
                              f'{io.error_string(error)}.')
        else:
            self.settings.record_dependencies.add(path)
        try:
            text = include_file.read()
        except UnicodeError as error:
            raise self.severe(f'Problem with "{self.name}" directive:\n'
                              + io.error_string(error))
        # Clip to-be-included content
        startline, endline, starttext, endtext = self.clip_options
        if startline or (endline is not None):
            lines = text.splitlines()
            text = '\n'.join(lines[startline:endline])
        # start-after/end-before: no restrictions on newlines in match-text,
        # and no restrictions on matching inside lines vs. line boundaries
        if starttext:
            # skip content in text before *and incl.* a matching text
            after_index = text.find(starttext)
            if after_index < 0:
                raise self.severe('Problem with "start-after" option of '
                                  f'"{self.name}" directive:\nText not found.')
            text = text[after_index + len(starttext):]
        if endtext:
            # skip content in text after *and incl.* a matching text
            before_index = text.find(endtext)
            if before_index < 0:
                raise self.severe('Problem with "end-before" option of '
                                  f'"{self.name}" directive:\nText not found.')
            text = text[:before_index]
        return text

    def as_literal_block(self, text: str) -> list[nodes.literal_block]:
        """Return list with literal_block containing `text`.

        Provisional
        """
        source = self.options['source']
        # Convert tabs to spaces unless `tab_width` is negative.
        if self.tab_width >= 0:
            text = text.expandtabs(self.tab_width)
        literal_block = nodes.literal_block(
            '', source=source, classes=self.options.get('class', []))
        literal_block.source = source
        literal_block.line = self.options.get('start-line', 0) + 1
        self.add_name(literal_block)
        if 'number-lines' in self.options:
            firstline = self.options['number-lines'] or 1
            text = text.removesuffix('\n')
            lastline = firstline + len(text.splitlines())
            tokens = NumberLines([([], text)], firstline, lastline)
            for classes, value in tokens:
                if classes:
                    literal_block += nodes.inline('', value, classes=classes)
                else:
                    literal_block += nodes.Text(value)
        else:
            literal_block += nodes.Text(text)
        return [literal_block]

    def as_code_block(self, text: str) -> list[nodes.literal_block]:
        """Pass `text` to the `CodeBlock` directive class.

        Provisional.
        """
        # convert tabs to spaces unless `tab_width` is negative:
        if self.tab_width >= 0:
            text = text.expandtabs(self.tab_width)
        codeblock = CodeBlock(self.name,
                              [self.options.pop('code')],  # pass as argument
                              self.options,
                              [text.removesuffix('\n')],   # content
                              self.lineno,
                              self.content_offset,
                              self.block_text,
                              self.state,
                              self.state_machine,
                              )
        return codeblock.run()

    def custom_parse(self, text: str) -> list[Node]:
        """Parse with custom parser.

        Parse with ``self.options['parser']`` into a new (dummy) document,
        apply the parser's default transforms,
        return child elements.

        Provisional.
        """
        settings = self.settings.copy()
        settings._source = self.options['source']
        document = utils.new_document(settings._source, settings)
        document.include_log = self.state.document.include_log
        parser = self.options['parser']()
        parser.parse(text, document)
        self.state.document.parse_messages.extend(document.parse_messages)
        # clean up doctree and complete parsing
        document.transformer.populate_from_components((parser,))
        document.transformer.apply_transforms()
        self.state.document.transform_messages.extend(
            document.transform_messages)
        return document.children

    def insert_into_input_lines(self, text: str) -> None:
        """Insert file content into the rST input of the calling parser.

        Returns an empty list to comply with the API of `Directive.run()`.

        Provisional.
        """
        source = self.options['source']
        textlines = statemachine.string2lines(text, self.tab_width,
                                              convert_whitespace=True)
        # Sanity checks:
        # excessively long lines
        for i, line in enumerate(textlines):
            if len(line) > self.settings.line_length_limit:
                line_no = i + 1 + self.options.get('start-line', 0)
                raise self.warning(f'"{source}": line {line_no} exceeds the'
                                   ' line-length-limit.')
        # circular inclusion
        include_log = self.state.document.include_log
        if not include_log:  # new document, initialize with document source
            current_source = utils.relative_path(
                                None, self.state.document.current_source)
            include_log.append((current_source, (None, None, '', '')))
        if (source, self.clip_options) in include_log:
            source_chain = (pth for (pth, opt) in reversed(include_log))
            inclusion_chain = '\n> '.join((source, *source_chain))
            raise self.warning(f'circular inclusion in "{self.name}"'
                               f' directive:\n{inclusion_chain}')
        include_log.append((source, self.clip_options))
        # marker for removing log entry (cf. parsers.rst.states.Body.comment())
        textlines += ['', f'.. end of inclusion from "{source}"']

        self.state_machine.insert_input(textlines, source)
        # TODO: if startline != 0, line numbers are wrong.


class Raw(Directive):

    """
    Pass through content unchanged

    Content is included in output based on type argument

    Content may be included inline (content section of directive) or
    imported from a file or url.
    """

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {'file': directives.path,
                   'url': directives.uri,
                   'encoding': directives.encoding,
                   'class': directives.class_option}
    has_content = True

    def run(self):
        settings = self.state.document.settings
        if (not settings.raw_enabled
            or (not settings.file_insertion_enabled
                and ('file' in self.options or 'url' in self.options))):
            raise self.warning('"%s" directive disabled.' % self.name)
        attributes = {'format': ' '.join(self.arguments[0].lower().split())}
        encoding = self.options.get('encoding', settings.input_encoding)
        error_handler = settings.input_encoding_error_handler
        if self.content:
            if 'file' in self.options or 'url' in self.options:
                raise self.error(
                    '"%s" directive may not both specify an external file '
                    'and have content.' % self.name)
            text = '\n'.join(self.content)
        elif 'file' in self.options:
            if 'url' in self.options:
                raise self.error(
                    'The "file" and "url" options may not be simultaneously '
                    'specified for the "%s" directive.' % self.name)
            path = adapt_path(self.options['file'],
                              self.state.document.current_source,
                              settings.root_prefix)
            try:
                raw_file = io.FileInput(source_path=path,
                                        encoding=encoding,
                                        error_handler=error_handler)
            except OSError as error:
                raise self.severe(f'Problems with "{self.name}" directive '
                                  f'path:\n{io.error_string(error)}.')
            else:
                # TODO: currently, raw input files are recorded as
                # dependencies even if not used for the chosen output format.
                settings.record_dependencies.add(path)
            try:
                text = raw_file.read()
            except UnicodeError as error:
                raise self.severe(f'Problem with "{self.name}" directive:\n'
                                  + io.error_string(error))
            attributes['source'] = path
        elif 'url' in self.options:
            source = self.options['url']
            try:
                raw_text = urlopen(source).read()
            except (URLError, OSError) as error:
                raise self.severe(f'Problems with "{self.name}" directive URL '
                                  f'"{self.options["url"]}":\n'
                                  f'{io.error_string(error)}.')
            raw_file = io.StringInput(source=raw_text, source_path=source,
                                      encoding=encoding,
                                      error_handler=error_handler)
            try:
                text = raw_file.read()
            except UnicodeError as error:
                raise self.severe(f'Problem with "{self.name}" directive:\n'
                                  + io.error_string(error))
            attributes['source'] = source
        else:
            # This will always fail because there is no content.
            self.assert_has_content()
        raw_node = nodes.raw('', text, classes=self.options.get('class', []),
                             **attributes)
        (raw_node.source,
         raw_node.line) = self.state_machine.get_source_and_line(self.lineno)
        return [raw_node]


class Replace(Directive):

    has_content = True

    def run(self):
        if not isinstance(self.state, states.SubstitutionDef):
            raise self.error(
                'Invalid context: the "%s" directive can only be used within '
                'a substitution definition.' % self.name)
        self.assert_has_content()
        text = '\n'.join(self.content)
        element = nodes.Element(text)
        self.state.nested_parse(self.content, self.content_offset,
                                element)
        # element might contain [paragraph] + system_message(s)
        node = None
        messages = []
        for elem in element:
            if not node and isinstance(elem, nodes.paragraph):
                node = elem
            elif isinstance(elem, nodes.system_message):
                elem['backrefs'] = []
                messages.append(elem)
            else:
                return [
                    self.reporter.error(
                        f'Error in "{self.name}" directive: may contain '
                        'a single paragraph only.', line=self.lineno)]
        if node:
            return messages + node.children
        return messages


class Unicode(Directive):

    r"""
    Convert Unicode character codes (numbers) to characters.  Codes may be
    decimal numbers, hexadecimal numbers (prefixed by ``0x``, ``x``, ``\x``,
    ``U+``, ``u``, or ``\u``; e.g. ``U+262E``), or XML-style numeric character
    entities (e.g. ``&#x262E;``).  Text following ".." is a comment and is
    ignored.  Spaces are ignored, and any other text remains as-is.
    """

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {'trim': directives.flag,
                   'ltrim': directives.flag,
                   'rtrim': directives.flag}

    comment_pattern = re.compile(r'( |\n|^)\.\. ')

    def run(self):
        if not isinstance(self.state, states.SubstitutionDef):
            raise self.error(
                'Invalid context: the "%s" directive can only be used within '
                'a substitution definition.' % self.name)
        substitution_definition = self.state_machine.node
        if 'trim' in self.options:
            substitution_definition.attributes['ltrim'] = 1
            substitution_definition.attributes['rtrim'] = 1
        if 'ltrim' in self.options:
            substitution_definition.attributes['ltrim'] = 1
        if 'rtrim' in self.options:
            substitution_definition.attributes['rtrim'] = 1
        codes = self.comment_pattern.split(self.arguments[0])[0].split()
        element = nodes.Element()
        for code in codes:
            try:
                decoded = directives.unicode_code(code)
            except ValueError as error:
                raise self.error('Invalid character code: %s\n%s'
                                 % (code, io.error_string(error)))
            element += nodes.Text(decoded)
        return element.children


class Class(Directive):

    """
    Set a "class" attribute on the directive content or the next element.
    When applied to the next element, a "pending" element is inserted, and a
    transform does the work later.
    """

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    has_content = True

    def run(self):
        try:
            class_value = directives.class_option(self.arguments[0])
        except ValueError:
            raise self.error(
                'Invalid class attribute value for "%s" directive: "%s".'
                % (self.name, self.arguments[0]))
        node_list = []
        if self.content:
            container = nodes.Element()
            self.state.nested_parse(self.content, self.content_offset,
                                    container)
            for node in container:
                node['classes'].extend(class_value)
            node_list.extend(container.children)
        else:
            pending = nodes.pending(
                misc.ClassAttribute,
                {'class': class_value, 'directive': self.name},
                self.block_text)
            self.state_machine.document.note_pending(pending)
            node_list.append(pending)
        return node_list


class Role(Directive):

    has_content = True

    argument_pattern = re.compile(r'(%s)\s*(\(\s*(%s)\s*\)\s*)?$'
                                  % ((states.Inliner.simplename,) * 2))

    def run(self):
        """Dynamically create and register a custom interpreted text role."""
        if self.content_offset > self.lineno or not self.content:
            raise self.error('"%s" directive requires arguments on the first '
                             'line.' % self.name)
        args = self.content[0]
        match = self.argument_pattern.match(args)
        if not match:
            raise self.error('"%s" directive arguments not valid role names: '
                             '"%s".' % (self.name, args))
        new_role_name = match.group(1)
        base_role_name = match.group(3)
        messages = []
        if base_role_name:
            base_role, messages = roles.role(
                base_role_name, self.state_machine.language, self.lineno,
                self.state.reporter)
            if base_role is None:
                error = self.state.reporter.error(
                    'Unknown interpreted text role "%s".' % base_role_name,
                    nodes.literal_block(self.block_text, self.block_text),
                    line=self.lineno)
                return messages + [error]
        else:
            base_role = roles.generic_custom_role
        assert not hasattr(base_role, 'arguments'), (
            'Supplemental directive arguments for "%s" directive not '
            'supported (specified by "%r" role).' % (self.name, base_role))
        try:
            converted_role = convert_directive_function(base_role)
            (arguments, options, content, content_offset
             ) = self.state.parse_directive_block(
                    self.content[1:], self.content_offset,
                    converted_role, option_presets={})
        except states.MarkupError as detail:
            error = self.reporter.error(
                'Error in "%s" directive:\n%s.' % (self.name, detail),
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno)
            return messages + [error]
        if 'class' not in options:
            try:
                options['class'] = directives.class_option(new_role_name)
            except ValueError as detail:
                error = self.reporter.error(
                    'Invalid argument for "%s" directive:\n%s.'
                    % (self.name, detail),
                    nodes.literal_block(self.block_text, self.block_text),
                    line=self.lineno)
                return messages + [error]
        role = roles.CustomRole(new_role_name, base_role, options, content)
        roles.register_local_role(new_role_name, role)
        return messages


class DefaultRole(Directive):

    """Set the default interpreted text role."""

    optional_arguments = 1
    final_argument_whitespace = False

    def run(self):
        if not self.arguments:
            if '' in roles._roles:
                # restore the "default" default role
                del roles._roles['']
            return []
        role_name = self.arguments[0]
        role, messages = roles.role(role_name, self.state_machine.language,
                                    self.lineno, self.state.reporter)
        if role is None:
            error = self.state.reporter.error(
                'Unknown interpreted text role "%s".' % role_name,
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno)
            return messages + [error]
        roles._roles[''] = role
        return messages


class Title(Directive):

    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True

    def run(self):
        self.state_machine.document['title'] = self.arguments[0]
        return []


class MetaBody(states.SpecializedBody):

    def field_marker(self, match, context, next_state):
        """Meta element."""
        node, blank_finish = self.parsemeta(match)
        self.parent += node
        return [], next_state, []

    def parsemeta(self, match):
        name = self.parse_field_marker(match)
        name = nodes.unescape(utils.escape2null(name))
        (indented, indent, line_offset, blank_finish
         ) = self.state_machine.get_first_known_indented(match.end())
        node = nodes.meta()
        node['content'] = nodes.unescape(utils.escape2null(
                                            ' '.join(indented)))
        if not indented:
            line = self.state_machine.line
            msg = self.reporter.info(
                  'No content for meta tag "%s".' % name,
                  nodes.literal_block(line, line))
            return msg, blank_finish
        tokens = name.split()
        try:
            attname, val = utils.extract_name_value(tokens[0])[0]
            node[attname.lower()] = val
        except utils.NameValueError:
            node['name'] = tokens[0]
        for token in tokens[1:]:
            try:
                attname, val = utils.extract_name_value(token)[0]
                node[attname.lower()] = val
            except utils.NameValueError as detail:
                line = self.state_machine.line
                msg = self.reporter.error(
                      'Error parsing meta tag attribute "%s": %s.'
                      % (token, detail), nodes.literal_block(line, line))
                return msg, blank_finish
        return node, blank_finish


class Meta(Directive):

    has_content = True

    SMkwargs = {'state_classes': (MetaBody,)}

    def run(self):
        self.assert_has_content()
        node = nodes.Element()
        new_line_offset, blank_finish = self.state.nested_list_parse(
            self.content, self.content_offset, node,
            initial_state='MetaBody', blank_finish=True,
            state_machine_kwargs=self.SMkwargs)
        if (new_line_offset - self.content_offset) != len(self.content):
            # incomplete parse of block?
            error = self.reporter.error(
                'Invalid meta directive.',
                nodes.literal_block(self.block_text, self.block_text),
                line=self.lineno)
            node += error
        # insert at begin of document
        index = self.state.document.first_child_not_matching_class(
                                        (nodes.Titular, nodes.meta)) or 0
        self.state.document[index:index] = node.children
        return []


class Date(Directive):

    has_content = True

    def run(self):
        if not isinstance(self.state, states.SubstitutionDef):
            raise self.error(
                'Invalid context: the "%s" directive can only be used within '
                'a substitution definition.' % self.name)
        format_str = '\n'.join(self.content) or '%Y-%m-%d'
        # @@@
        # Use timestamp from the `SOURCE_DATE_EPOCH`_ environment variable?
        # Pro: Docutils-generated documentation
        #      can easily be part of `reproducible software builds`__
        #
        #      __ https://reproducible-builds.org/
        #
        # Con: Changes the specs, hard to predict behaviour,
        #
        # See also the discussion about \date \time \year in TeX
        # http://tug.org/pipermail/tex-k/2016-May/002704.html
        # source_date_epoch = os.environ.get('SOURCE_DATE_EPOCH')
        # if (source_date_epoch):
        #     text = time.strftime(format_str,
        #                          time.gmtime(int(source_date_epoch)))
        # else:
        text = time.strftime(format_str)
        return [nodes.Text(text)]


class TestDirective(Directive):

    """This directive is useful only for testing purposes."""

    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {'option': directives.unchanged_required}
    has_content = True

    def run(self):
        if self.content:
            text = '\n'.join(self.content)
            info = self.reporter.info(
                'Directive processed. Type="%s", arguments=%r, options=%r, '
                'content:' % (self.name, self.arguments, self.options),
                nodes.literal_block(text, text), line=self.lineno)
        else:
            info = self.reporter.info(
                'Directive processed. Type="%s", arguments=%r, options=%r, '
                'content: None' % (self.name, self.arguments, self.options),
                line=self.lineno)
        return [info]
