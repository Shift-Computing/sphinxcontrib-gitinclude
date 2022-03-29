# -*- coding: utf-8 -*-
# Copyright (c) 2022, Oz Tiram <oz.tirm@gmail.com>
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
    sphinxcontrib.gitinclude
    ========================

    This extension provides a directive to include code snippets
    directly from git repositories.

    .. moduleauthor::  Oz Tiram <oz.tiramgmail.com>
"""

from typing import Any, Dict, Tuple, List


import sys
import os
import shlex
from subprocess import Popen, PIPE, STDOUT
from collections import defaultdict, namedtuple

from docutils.nodes import Element, Node
from docutils import nodes
from docutils.parsers import rst
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives import flag, unchanged, nonnegative_int, unchanged_required
from sphinx.directives import optional_int
from docutils.statemachine import StringList
from sphinx.locale import __
from sphinx.config import Config
from sphinx.util import logging as sphinx_logging
from sphinx.util.typing import OptionSpec
from sphinx.directives.code import CodeBlock, LiteralInclude, LiteralIncludeReader

__version__ = '0.18.dev0'

logger = sphinx_logging.getLogger('contrib.programoutput')

class gitincluded(nodes.General, nodes.Element):
    pass


class GitIncludeDirective(CodeBlock):
    has_content = False
    final_argument_whitespace = True
    # .. gitinclude:: ~/Software/pwman3/  pwman/ui/cli.py v0.9.11
    required_arguments = 3

    option_spec = {'language': unchanged_required}

    def run(self):
        code_block = super().run()[0]
        env = self.state.document.settings.env
        import pdb; pdb.set_trace()
        node = gitincluded()
        node.line = self.lineno

        node['git_repo'] = self.arguments[0]
        node['path'] = self.arguments[1]
        node['hash_or_tag'] = self.arguments[2]
        node['language'] = self.options['language']
        self.add_name(node)
        node.append(code_block)
        return [node]


_GitReader = namedtuple(
    'GitReader', 'git_repo path hash_or_tag')


class GitReader(_GitReader):
    """
    Reads file from a git repository
    """

    def __new__(cls, git_repo, path, hash_or_tag):
        return _GitReader.__new__(cls, git_repo, path, hash_or_tag)

    @classmethod
    def from_hash_or_tag(cls, node):
        """
        Create a command from a :class:`gitinclude` node.
        """
        return cls(node['git_repo'], node['path'], node['hash_or_tag'])
    
    def get_current_branch(self):
        """
        keep a record of the current branch
        """
        command = "git branch --show-current"
        p = Popen(command,
                  shell=True,
                  stdout=PIPE,
                  stderr=PIPE,
                  cwd=self.git_repo)
        out, err = p.communicate()
        if err:
            raise RuntimeError(err)

        return out

    def read_path(self):
        """
        Read the file.
    
        store current branch
        checkout hash_or_tag
        read path
        restore previous branch

        Return the :class:`~subprocess.Popen` object representing the running
        command.
        """
        command = f'git checkout {self.hash_or_tag}'

        return """for item in container:
    if search_something(item):
        # Found it!
        process(item)
        break
else:
    # Didn't find anything..
    not_found_in_container()"""

    def restore_branch(self, hash_or_tag):
        pass
    
    def get_output(self):
        """
        Get the output of this command.

        Return a tuple ``(returncode, output)``.  ``returncode`` is the
        integral return code of the process, ``output`` is the output as
        unicode string, with final trailing spaces and new lines stripped.
        """
        branch = self.get_current_branch()
        content = self.read_path()
        self.restore_branch(branch)

        return content

    def __str__(self):
        return self.get_output()
fuckputin = """
for item in container:
    if search_something(item):
        # Found it!
        process(item)
        break
else:
    # Didn't find anything..
    not_found_in_container()
"""


class GitIncludeReader(LiteralIncludeReader):
    
    def __init__(self,
                 filename: str,
                 git_repo: str,
                 hash_or_tag: str,
                 options: Dict,
                 config: Config) -> None:

        self.filename = filename
        self.git_repo = git_repo
        self.hash_or_tag = hash_or_tag
        self.options = options
        self.encoding = options.get('encoding', config.source_encoding)
        self.lineno_start = self.options.get('lineno-start', 1)

        self.parse_options()

    def _read_file(self, cmd: str) -> List[str]:
        try:
            with Popen(cmd, cwd=self.git_repo, shell=True, stdout=PIPE, stderr=PIPE) as p:
                out, err = p.communicate()
                if err:
                    logger.warning(__(f'failed to run: {cmd}'))
                    return []

                text = out.decode()
                if 'tab-width' in self.options:
                    text = text.expandtabs(self.options['tab-width'])

                return text.splitlines(True)
        except OSError as exc:
            raise OSError(__('Include file %r not found or reading it failed') %
                          filename) from exc
        except UnicodeError as exc:
            raise UnicodeError(__('Encoding %r used for reading included file %r seems to '
                                  'be wrong, try giving an :encoding: option') %
                               (self.encoding, filename)) from exc

    def show_diff(self):
        diff = self.options.get('diff').split("/")[-1]
        cmd = f"git --no-pager  diff --no-color {self.hash_or_tag}..{diff} -- {self.filename}"
        return self._read_file(cmd)

    def read_file(self, filename: str, location: Tuple[str, int] = None) -> List[str]:
        cmd = f"git --no-pager show {self.hash_or_tag}:{filename}"
        return self._read_file(cmd)

    def read(self,
            location: Tuple[str, int] = None,
            
            ) -> Tuple[str, int]:
        
        if 'diff' in self.options:
            lines = self.show_diff()
        else:
            filters = [self.pyobject_filter,
                       self.start_filter,
                       self.end_filter,
                       self.lines_filter,
                       self.prepend_filter,
                       self.append_filter,
                       self.dedent_filter]
            
            lines = self.read_file(self.filename,
                                   location=location)
            for func in filters:
                lines = func(lines, location=location)

        return ''.join(lines), len(lines)


class GitInclude(LiteralInclude):
    
    has_content = False
    required_arguments = 3
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec: OptionSpec = {
        'dedent': optional_int,
        'linenos': directives.flag,
        'lineno-start': int,
        'lineno-match': directives.flag,
        'tab-width': int,
        'language': directives.unchanged_required,
        'force': directives.flag,
        'encoding': directives.encoding,
        'pyobject': directives.unchanged_required,
        'lines': directives.unchanged_required,
        'start-after': directives.unchanged_required,
        'end-before': directives.unchanged_required,
        'start-at': directives.unchanged_required,
        'end-at': directives.unchanged_required,
        'prepend': directives.unchanged_required,
        'append': directives.unchanged_required,
        'emphasize-lines': directives.unchanged_required,
        'caption': directives.unchanged,
        'class': directives.class_option,
        'name': directives.unchanged,
        'diff': directives.unchanged_required,
    }

    def run(self) -> List[Node]:
        document = self.state.document

        if not document.settings.file_insertion_enabled:
            return [document.reporter.warning('File insertion disabled',
                                              line=self.lineno)]
        # convert options['diff'] to absolute path
        if 'diff' in self.options:
            _, path = self.env.relfn2path(self.options['diff'])
            self.options['diff'] = path

        try:
            location = self.state_machine.get_source_and_line(self.lineno)
            rel_filename, filename = self.env.relfn2path(self.arguments[0])
            self.env.note_dependency(rel_filename)

            reader = GitIncludeReader(self.arguments[0],
                                            self.arguments[1],
                                            self.arguments[2],
                                            self.options,
                                            self.config)

            text, lines = reader.read(location=location)

            retnode: Element = nodes.literal_block(text, text, source=filename)

            retnode['force'] = 'force' in self.options
            self.set_source_info(retnode)
            if self.options.get('diff'):  # if diff is set, set udiff
                retnode['language'] = 'udiff'
            elif 'language' in self.options:
                retnode['language'] = self.options['language']
            if ('linenos' in self.options or 'lineno-start' in self.options or
                    'lineno-match' in self.options):
                retnode['linenos'] = True
            retnode['classes'] += self.options.get('class', [])
            extra_args = retnode['highlight_args'] = {}
            if 'emphasize-lines' in self.options:
                hl_lines = parselinenos(self.options['emphasize-lines'], lines)
                if any(i >= lines for i in hl_lines):
                    logger.warning(__('line number spec is out of range(1-%d): %r') %
                                   (lines, self.options['emphasize-lines']),
                                   location=location)
                extra_args['hl_lines'] = [x + 1 for x in hl_lines if x < lines]
            extra_args['linenostart'] = reader.lineno_start

            if 'caption' in self.options:
                caption = self.options['caption'] or self.arguments[0]
                retnode = container_wrapper(self, retnode, caption)

            # retnode will be note_implicit_target that is linked from caption and numref.
            # when options['name'] is provided, it should be primary ID.
            self.add_name(retnode)

            return [retnode]
        except Exception as exc:
            return [document.reporter.warning(exc, line=self.lineno)]


def setup(app: "Sphinx") -> Dict[str, Any]:
    app.add_config_value('git_repo', '', "")
    app.add_directive('gitinclude', GitInclude)
    return {
        'parallel_read_safe': False,
    }
