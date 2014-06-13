import subprocess

from . import CompilerMeta


class JavaScriptCompiler(object):
    __metaclass__ = CompilerMeta
    supported_mimetypes = ['application/javascript', 'text/javascript', 'text/coffeescript']

    @classmethod
    def compile(cls, what, mimetype='text/javascript', include_path=None, debug=None):

        output = what

        if mimetype == 'text/coffeescript':
            args = ['coffee', '-c', '-p', '-s']

            handler = subprocess.Popen(args, stdout=subprocess.PIPE,
                                       stdin=subprocess.PIPE,
                                       stderr=subprocess.PIPE, cwd=None)

            (stdout, stderr) = handler.communicate(input=output)
            if handler.returncode == 0:
                output = stdout
            else:
                raise RuntimeError('Test this :S %s' % stderr)

        if not debug:
            args = ['uglifyjs', '-', '-c', '-m']

            handler = subprocess.Popen(args, stdout=subprocess.PIPE,
                                       stdin=subprocess.PIPE,
                                       stderr=subprocess.PIPE, cwd=None)

            (stdout, stderr) = handler.communicate(input=output)
            if handler.returncode == 0:
                output = stdout
            else:
                raise RuntimeError('Test this :S %s' % stderr)

        return output
