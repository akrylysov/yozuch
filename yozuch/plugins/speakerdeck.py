import docutils.nodes
from docutils.parsers.rst import Directive, directives


class Speakerdeck(Directive):

    DEFAULT_ALIGN = 'left'

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    option_spec = {
        'align': lambda argument: directives.choice(argument, ('left', 'center', 'right')),
    }

    html_code = '<div class="align-{align} media">' \
                '<script async class="speakerdeck-embed" data-id="{id}" data-ratio="1.77777777777778" ' \
                'src="//speakerdeck.com/assets/embed.js"></script></div>'

    def run(self):
        self.options['id'] = directives.uri(self.arguments[0])
        if 'align' not in self.options:
            self.options['align'] = self.DEFAULT_ALIGN
        return [docutils.nodes.raw('', self.html_code.format(**self.options), format='html')]


def register(context):
    directives.register_directive('speakerdeck', Speakerdeck)
