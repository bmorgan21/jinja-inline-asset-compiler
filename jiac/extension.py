import os
import tempfile

from bs4 import BeautifulSoup
from jinja2 import nodes
from jinja2.ext import Extension

from . import compile


class CompilerExtension(Extension):
    tags = set(['compile'])

    def parse(self, parser):
        lineno = parser.stream.next().lineno
        args = [parser.parse_expression()]
        body = parser.parse_statements(['name:endcompile'], drop_needle=True)

        if len(body) > 1:
            raise RuntimeError('One tag supported for now.')

        return nodes.CallBlock(self.call_method('_compile', args), [], [], body).set_lineno(lineno)

    def _render_block(self, filename, type):
        """Returns an html element pointing to filename as a string.
        """
        filename = '%s/%s' % (self.environment.compressor_static_prefix, os.path.basename(filename))

        if type.lower() == 'css':
            return '<link type="text/css" rel="stylesheet" href="%s" />' % filename
        elif type.lower() == 'js':
            return '<script type="text/javascript" src="%s"></script>' % filename
        else:
            raise RuntimeError('Unsupported type of compiler %s' % type)

    def _compile(self, compiler_type, caller):
        html = caller()

        enabled = (not hasattr(self.environment, 'compiler_enabled') or
                   self.environment.compiler_enabled is not False)
        if not enabled:
            return html

        debug = (hasattr(self.environment, 'compiler_debug') and
                 self.environment.compiler_debug is True)
        compiler_type = compiler_type.lower()
        soup = BeautifulSoup(html)
        compilables = self._find_compilable_tags(soup)

        for c in compilables:
            if c.get('type') is None:
                raise RuntimeError('Tags to be compressed must have a compiler_type.')

            text = compile(c.string, c['type'], debug=debug)

            print '!!', text

        return ''
