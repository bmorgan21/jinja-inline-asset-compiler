import os
import tempfile

from bs4 import BeautifulSoup
from jinja2 import nodes
from jinja2.ext import Extension

from . import compile


class CompilerExtension(Extension):
    tags = set(['compress'])

    def parse(self, parser):
        lineno = parser.stream.next().lineno
        args = [parser.parse_expression()]
        body = parser.parse_statements(['name:endcompress'], drop_needle=True)

        if len(body) > 1:
            raise RuntimeError('One tag supported for now.')

        return nodes.CallBlock(self.call_method('_compile', args), [], [], body).set_lineno(lineno)

    def _find_compilable_tags(self, soup):
        tags = ['link', 'style', 'script']
        for tag in soup.find_all(tags):
            if tag.get('type') is None:
                if tag.name == 'script':
                    tag['type'] = 'text/javascript'
                if tag.name == 'style':
                    tag['type'] = 'text/css'
            else:
                tag['type'] == tag['type'].lower()
            yield tag

    def _render_block(self, filename, type):
        """Returns an html element pointing to filename as a string.
        """
        filename = '%s/%s' % (self.environment.compressor_static_prefix, os.path.basename(filename))

        if type.lower() == 'css':
            return '<link type="text/css" rel="stylesheet" href="%s" />' % filename
        elif type.lower() == 'js':
            return '<script type="text/javascript" src="%s"></script>' % filename
        else:
            raise RuntimeError('Unsupported type of compression %s' % type)

    def _compile(self, compression_type, caller):
        html = caller()

        enabled = (not hasattr(self.environment, 'compressor_enabled') or
                   self.environment.compressor_enabled is not False)
        if not enabled:
            return html

        debug = (hasattr(self.environment, 'compressor_debug') and
                 self.environment.compressor_debug is True)
        compression_type = compression_type.lower()
        soup = BeautifulSoup(html)
        compilables = self._find_compilable_tags(soup)

        for c in compilables:
            if c.get('type') is None:
                raise RuntimeError('Tags to be compressed must have a compression_type.')

            c.string

            needs_compile = c['type'] != 'text/javascript'
            if not debug or needs_compile:
                text = compile(self._get_contents(src), c['type'], cwd=cwd,
                               uri_cwd=uri_cwd, debug=debug)
            else:
                text = self._get_contents(src)

            print '!!', text

        return ''
