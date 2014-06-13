from bs4 import BeautifulSoup
from jinja2 import nodes, Markup
from jinja2.exceptions import TemplateAssertionError
from jinja2.ext import Extension

from . import compile


class CompilerExtension(Extension):
    tags = set(['compile'])

    def parse(self, parser):
        lineno = parser.stream.next().lineno
        body = parser.parse_statements(['name:endcompile'], drop_needle=True)

        if len(body) > 1:
            raise TemplateAssertionError('One tag supported for now.', lineno, parser.name, parser.filename)

        if len(body[0].nodes) > 1:
            raise TemplateAssertionError('Tag disallowed.', body[0].nodes[1].lineno, parser.name, parser.filename)

        data = body[0].nodes[0].data
        html = self._compile(data)
        return nodes.Output([nodes.Const(Markup(html))]).set_lineno(lineno)

    def _find_compilable_tags(self, soup):
        tags = ['style', 'script']
        for tag in soup.find_all(tags):
            if tag.get('type') is None:
                if tag.name == 'script':
                    tag['type'] = 'text/javascript'
                if tag.name == 'style':
                    tag['type'] = 'text/css'
            else:
                tag['type'] == tag['type'].lower()
            yield tag

    def _tag_type(self, name):
        if name.lower() == 'script':
            return 'text/javascript'
        elif name.lower() == 'style':
            return 'text/css'

        raise RuntimeError('Unsupported tag name {}'.format(name))

    def _compile(self, html):
        enabled = (not hasattr(self.environment, 'compiler_enabled') or
                   self.environment.compiler_enabled is not False)
        if not enabled:
            return html

        debug = (hasattr(self.environment, 'compiler_debug') and
                 self.environment.compiler_debug is True)

        include_path = (hasattr(self.environment, 'compiler_include_path') and
                        self.environment.compiler_include_path)

        if include_path and not isinstance(include_path, (list, tuple)):
            include_path = [include_path]

        soup = BeautifulSoup(html)
        compilables = self._find_compilable_tags(soup)

        result = []
        for c in compilables:
            if c.get('type') is None:
                raise RuntimeError('Tags to be compressed must have a compiler_type.')

            text = compile(c.string, c['type'], include_path=include_path, debug=debug)

            result.append('<{} type="{}">\n{}\n</{}>'.format(c.name, self._tag_type(c.name), text.strip(), c.name))

        return '\n'.join(result)
